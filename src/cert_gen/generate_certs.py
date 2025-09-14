import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

import qrcode
from io import BytesIO
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / 'blockchain'))
from store_cert import store_certificate

# Paths
CSV_FILE = "src/cert_gen/participants.csv"
TEMPLATE_FILE = "src/cert_gen/template.jpeg"   # your template
OUTPUT_DIR = "src/cert_gen/output/"

# Make sure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load font
FONT_NAME = ImageFont.truetype("arial.ttf", 25)
FONT_EVENT = ImageFont.truetype("arial.ttf", 20)
FONT_ACH = ImageFont.truetype("arial.ttf", 20)

# Verification portal URL (replace with your actual URL)
VERIFICATION_BASE_URL = "https://your-validation-portal.com/verify?hash="

def generate_certificate(cert_id, name, event, date, achievement):
    # Open template
    img = Image.open(TEMPLATE_FILE).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Draw text
    draw.text((294, 245), name, font=FONT_NAME, fill="black")
    draw.text((279, 297), f"for {achievement}", font=FONT_ACH, fill="black")
    draw.text((282, 332), f"Event: {event}", font=FONT_EVENT, fill="black")
    draw.text((280, 386), f"Date: {date}", font=FONT_EVENT, fill="black")

    # Save certificate as PDF first
    output_path = os.path.join(OUTPUT_DIR, f"{name.replace(' ', '_')}.pdf")
    img.save(output_path, "PDF")

    # Store hash on blockchain and get blockchain hash
    blockchain_hash = store_certificate(cert_id, Path(output_path), name, event, date)
    print(f"{name}'s blockchain hash: {blockchain_hash}")

    # Generate QR code with blockchain hash link
    verify_url = VERIFICATION_BASE_URL + blockchain_hash
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(verify_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Resize QR code if needed
    qr_img = qr_img.resize((150, 150))

    # Paste QR code onto certificate
    img.paste(qr_img, (img.width - 170, img.height - 170))  # bottom-right corner

    # Save final certificate with QR code as PDF (overwrite)
    img.save(output_path, "PDF")
    print(f"Generated with QR: {output_path}")

    # Save final certificate as PDF
    output_path = os.path.join(OUTPUT_DIR, f"{name.replace(' ', '_')}.pdf")
    img.save(output_path, "PDF")
    print(f"Generated with QR: {output_path}")


def main():
    df = pd.read_csv(CSV_FILE)
    for idx, row in df.iterrows():
        cert_id = f"CERT{idx+1:03d}"
        generate_certificate(cert_id, row["Name"], row["Event"], row["Date"], row["Achievement"])

if __name__ == "__main__":
    main()
