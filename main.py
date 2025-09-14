
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os


app = Flask(__name__)
CORS(app)  # allow frontend to call the API


# Mock database of certificates
certificates = {
    "CERT123": {"name": "Yash Rathod", "course": "Blockchain 101"}
}


@app.route("/api/verify", methods=["POST"])
def verify_certificate():
    data = request.json
    cert_id = data.get("certId")
    cert = certificates.get(cert_id)
    if cert:
        return jsonify({"valid": True, "certificate": cert})
    return jsonify({"valid": False, "message": "Certificate not found"}), 404


# Helper to run a script and return output
def run_script(script_path):
    try:
        # Use sys.executable to ensure correct Python
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "output": e.stdout + e.stderr}


# API endpoint to run Admin Dashboard
@app.route("/api/run_dashboard", methods=["POST"])
def run_dashboard():
    script_path = os.path.join("src", "dashboard", "app.py")
    result = run_script(script_path)
    return jsonify(result)

# API endpoint to run Validation Portal
@app.route("/api/run_validation_portal", methods=["POST"])
def run_validation_portal():
    script_path = os.path.join("src", "validation_portal", "app.py")
    result = run_script(script_path)
    return jsonify(result)

# API endpoint to generate certificates
@app.route("/api/generate_certificates", methods=["POST"])
def generate_certificates():
    script_path = os.path.join("src", "cert_gen", "generate_certs.py")
    result = run_script(script_path)
    return jsonify(result)

# API endpoint to send certificates via email
@app.route("/api/send_certificates", methods=["POST"])
def send_certificates():
    script_path = os.path.join("src", "email_dist", "main.py")
    result = run_script(script_path)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
