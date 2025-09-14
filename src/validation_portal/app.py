
from flask import Flask, render_template, request
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3

app = Flask(__name__)

# Blockchain setup (copied from verify_cert.py)
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
assert w3.is_connected(), "Failed to connect to blockchain"
with open("build/contracts/CertificateStorage.json", encoding="utf-8") as f:
    contract_data = json.load(f)
contract = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=contract_data["abi"]
)

def check_certificate(cert_id):
    """Check certificate against blockchain."""
    try:
        details = contract.functions.getCertificateDetails(cert_id).call()
        # details: [name, event, date, hash]
        if details[0]:
            return {
                "valid": True,
                "participant": details[0],
                "event": details[1],
                "date": details[2],
                "hash": details[3]
            }
    except Exception as e:
        print(f"Blockchain error: {e}")
    return {"valid": False}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cert_id = request.form["cert_id"].strip()
        result = check_certificate(cert_id)
        return render_template("result.html", cert_id=cert_id, result=result)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
