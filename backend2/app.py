import os
import subprocess
import time
from flask import Flask, render_template, request, jsonify

# Base path to your project
BASE_DIR = r"E:\Programming\Blockchain\Blockchain based Certification generation\Backend"

app = Flask(__name__)

ganache_proc = None  # keep reference to Ganache process

def start_ganache():
    """Start Ganache CLI automatically"""
    global ganache_proc
    try:
        ganache_proc = subprocess.Popen(
            ["ganache", "--port", "8545", "--deterministic"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("🚀 Ganache started on http://127.0.0.1:8545")
        time.sleep(10)  
    except FileNotFoundError:
        print("❌ Ganache CLI not found. Install with: npm install -g ganache")


# Home page (choose dashboard or validation)
@app.route("/")
def index():
    return render_template("index.html")

# Dashboard page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Validation portal page
@app.route("/validation")
def validation():
    return render_template("validation.html")

# Run backend scripts via API
@app.route("/action", methods=["POST"])
def action():
    data = request.get_json(force=True)
    action = data.get("action")

    try:
        if action == "dashboard":
            subprocess.Popen(["python", os.path.join(BASE_DIR, "src/dashboard/app.py")])
            return jsonify({"message": "✅ Admin Dashboard started"})
        elif action == "validation":
            subprocess.Popen(["python", os.path.join(BASE_DIR, "src/validation_portal/app.py")])
            return jsonify({"message": "✅ Validation Portal started"})
        elif action == "generate":
            subprocess.Popen(["python", os.path.join(BASE_DIR, "src/cert_gen/generate_certs.py")])
            return jsonify({"message": "✅ Certificates generated"})
        elif action == "send":
            subprocess.Popen(["python", os.path.join(BASE_DIR, "src/email_dist/main.py")])
            return jsonify({"message": "✅ Certificates sent"})
        else:
            return jsonify({"message": "❌ Invalid action"}), 400
    except Exception as e:
        return jsonify({"message": f"❌ Error: {str(e)}"}), 500


if __name__ == "__main__":
    try:
        # Start Ganache before running Flask
        start_ganache()
        app.run(debug=True)
    finally:
        # Stop Ganache when Flask stops
        if ganache_proc:
            ganache_proc.terminate()
            print("🛑 Ganache stopped.")
