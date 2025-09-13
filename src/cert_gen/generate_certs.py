import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

# Paths
CSV_FILE = "src/cert_gen/participants.csv"
TEMPLATE_FILE = "src/cert_gen/template.jpeg"   # rename your template accordingly
OUTPUT_DIR = "src/cert_gen/output/"

# Make sure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load font (use a .ttf font file from your system)
FONT_NAME = ImageFont.truetype("arial.ttf", 25)   # For Name
FONT_EVENT = ImageFont.truetype("arial.ttf", 20)  # For Event/Date
FONT_ACH = ImageFont.truetype("arial.ttf", 20)    # For Achievement

def generate_certificate(name, event, date, achievement):
    # Open template
    img = Image.open(TEMPLATE_FILE).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Text positions (adjust these x,y values for correct placement)
    draw.text((294, 245), name, font=FONT_NAME, fill="black")
    draw.text((279, 297), f"for {achievement}", font=FONT_ACH, fill="black")
    draw.text((282, 332), f"Event: {event}", font=FONT_EVENT, fill="black")
    draw.text((280, 386), f"Date: {date}", font=FONT_EVENT, fill="black")

    # Save as PDF
    output_path = os.path.join(OUTPUT_DIR, f"{name.replace(' ', '_')}.pdf")
    img.save(output_path, "PDF")
    print(f"Generated: {output_path}")

def main():
    df = pd.read_csv(CSV_FILE)
    for _, row in df.iterrows():
        generate_certificate(row["Name"], row["Event"], row["Date"], row["Achievement"])

if __name__ == "__main__":
    main()
