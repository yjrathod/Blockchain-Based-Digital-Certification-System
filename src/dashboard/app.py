
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import os
import pandas as pd
from werkzeug.utils import secure_filename
from utils import generate_qr_code, save_qr_to_file


app = Flask(__name__)
app.secret_key = "your_secret_key"

# Config
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
QR_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'qr')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# In-memory storage for demo (replace with DB in prod)
certificates = []
cert_issued = 0
cert_validated = 0


# Organizer login/logout
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "password":  # Replace with secure auth in prod
            session['logged_in'] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# Dashboard page
@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("dashboard.html", certificates=certificates, cert_issued=cert_issued, cert_validated=cert_validated)

# CSV upload route
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    file = request.files.get('csvFile')
    if not file or not file.filename.endswith('.csv'):
        flash('Please upload a valid CSV file.')
        return redirect(url_for('dashboard'))
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    # Process CSV
    df = pd.read_csv(filepath)
    global cert_issued
    for idx, row in df.iterrows():
        cert_id = f"CERT{len(certificates)+1:03d}"
        name = row.get('Name')
        event = row.get('Event')
        date = row.get('Date')
        achievement = row.get('Achievement', '')
        # Generate QR code (simulate hash/URL)
        verify_url = f"https://your-validation-portal.com/verify?cert_id={cert_id}"
        qr_img = generate_qr_code(verify_url)
        qr_filename = f"{cert_id}.png"
        qr_path = os.path.join(QR_FOLDER, qr_filename)
        save_qr_to_file(qr_img, qr_path)
        certificates.append({
            'id': cert_id,
            'name': name,
            'event': event,
            'date': date,
            'qr_url': url_for('static', filename=f'qr/{qr_filename}')
        })
        cert_issued += 1
    flash('Participants uploaded and certificates generated!')
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
