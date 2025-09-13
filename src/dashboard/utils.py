import qrcode
from io import BytesIO
import hashlib

def generate_certificate_hash(file_path):
    """
    Generate SHA-256 hash of a certificate file (PDF/PNG).
    """
    with open(file_path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()

def generate_qr_code(data, size=150):
    """
    Generate a QR code image from the given data.
    Returns a PIL Image object.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size))
    return img

def save_qr_to_file(img, file_path):
    """
    Save a PIL Image (QR code) to a file.
    """
    img.save(file_path)
