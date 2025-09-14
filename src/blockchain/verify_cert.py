import hashlib
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3

# ----------------------------
# Setup
# ----------------------------
load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
assert w3.is_connected(), "Failed to connect to blockchain"

with open("build/contracts/CertificateStorage.json", encoding="utf-8") as f:
    contract_data = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=contract_data["abi"]
)

# ----------------------------
# Helpers
# ----------------------------
def generate_hash(file_path: Path) -> str:
    """Generate SHA-256 hash for a certificate file."""
    sha256 = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):  # read in chunks
            sha256.update(chunk)
    return "0x" + sha256.hexdigest()


def verify_certificate(cert_id: str, file_path: Path) -> bool:
    """Verify certificate by calculating its hash and checking on-chain."""
    cert_hash = generate_hash(file_path)
    is_valid = contract.functions.verifyCertificate(cert_id, cert_hash).call()

    if is_valid:
        details = contract.functions.getCertificateDetails(cert_id).call()
        print(
            f"✅ Certificate {cert_id} is valid.\n"
            f"   Name: {details[0]}\n"
            f"   Event: {details[1]}\n"
            f"   Date: {details[2]}"
        )
    else:
        print(f"❌ Certificate {cert_id} is invalid (hash mismatch).")

    return is_valid


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    certificate_folder = Path("../certificates")

    # Example: check one file
    cert_id = "CERT001"
    cert_file = certificate_folder / "John_Doe_certificate.pdf"

    if cert_file.exists():
        verify_certificate(cert_id, cert_file)
    else:
        print(f"⚠️ File not found: {cert_file}")
