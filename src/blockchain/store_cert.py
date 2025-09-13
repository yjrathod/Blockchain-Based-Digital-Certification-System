import hashlib
import json
import os
import logging
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound

# ----------------------------
# Setup
# ----------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

load_dotenv()

RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:7545")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
ACCOUNT = os.getenv("ACCOUNT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not all([CONTRACT_ADDRESS, ACCOUNT, PRIVATE_KEY]):
    raise EnvironmentError("Missing CONTRACT_ADDRESS, ACCOUNT_ADDRESS or PRIVATE_KEY in .env")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise ConnectionError(f"Failed to connect to blockchain at {RPC_URL}")

# Load contract ABI
with open("build/contracts/CertificateStorage.json", encoding="utf-8") as f:
    contract_data = json.load(f)

contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS),
                           abi=contract_data["abi"])


# ----------------------------
# Helpers
# ----------------------------
def generate_hash(file_path: Path) -> str:
    """Generate SHA-256 hash for a file."""
    sha256 = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):  # read in chunks
            sha256.update(chunk)
    return sha256.hexdigest()


def store_certificate(cert_id: str, file_path: Path, name: str, event: str, date: str) -> str:
    """Store a certificate hash on the blockchain and return the hash."""
    try:
        cert_hash = generate_hash(file_path)
        tx = contract.functions.storeCertificate(
            cert_id,
            f"0x{cert_hash}",
            name,
            event,
            date
        ).build_transaction({
            "from": ACCOUNT,
            "nonce": w3.eth.get_transaction_count(ACCOUNT),
            "gas": 2_000_000,
            "gasPrice": w3.to_wei("20", "gwei"),
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        logging.info(f"✅ Stored {cert_id} | TxHash: {tx_hash.hex()} | Hash: 0x{cert_hash}")
        return cert_hash

    except (ContractLogicError, TransactionNotFound) as e:
        logging.error(f"Blockchain error for {cert_id}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error storing {cert_id}: {e}")

    return ""


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    certificate_folder = Path("E:/Programming/Blockchain/Blockchain based Certification generation/Blockchain-Based-Digital-Certification-System/certificates")

    participants: list[Dict[str, str]] = [
        {"cert_id": "CERT001", "file": "John_Doe_certificate.pdf",
         "name": "John Doe", "event": "Tech Event", "date": "2025-09-12"},
        # add more here...
    ]

    for p in participants:
        file_path = certificate_folder / p["file"]
        if file_path.exists():
            store_certificate(p["cert_id"], file_path, p["name"], p["event"], p["date"])
        else:
            logging.warning(f"⚠️ Certificate file {file_path} not found")
