from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
assert w3.is_connected(), "Failed to connect to blockchain"

with open("build/contracts/CertificateStorage.json") as f:
    contract_data = json.load(f)
contract = w3.eth.contract(address=os.getenv("CONTRACT_ADDRESS"), abi=contract_data["abi"])

def verify_certificate(cert_id, cert_hash):
    is_valid = contract.functions.verifyCertificate(cert_id, cert_hash).call()
    if is_valid:
        details = contract.functions.getCertificateDetails(cert_id).call()
        print(f"Certificate {cert_id} is valid. Details: Name={details[0]}, Event={details[1]}, Date={details[2]}")
    else:
        print(f"Certificate {cert_id} is invalid")
    return is_valid

if __name__ == "__main__":
    # Update with real cert_id and hash from store_cert.py
    verify_certificate("CERT001", "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")