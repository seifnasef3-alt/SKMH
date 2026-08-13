# SKMH Project - OCR Pipeline
# Seïf NASEF - Week 4 - June 23, 2026

import pytesseract
import cv2
import numpy as np
from PIL import Image
import pdfplumber
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def preprocess_image(image_np):
    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Remove noise - still testing which parameters work best
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Black & white threshold
    thresh = cv2.adaptiveThreshold(blurred, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2)

    # TODO: handle rotated scans (deskewing) - not done yet

    return thresh


def extract_text_from_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image_np = np.array(image)

    cleaned = preprocess_image(image_np)

    # lang='fra+eng+tha' for KUIC documents (French, English and Thai)
    text = pytesseract.image_to_string(cleaned, lang='fra+eng+tha')

    return text.strip()


def extract_text_from_pdf(pdf_bytes):
    text = ""

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"
            else:
                # Scanned page - need OCR here
                # TODO: convert page to image then run Tesseract
                text += "[scanned page - OCR not implemented yet]\n"

    return text.strip()


def process_document(file_bytes, filename):
    ext = filename.lower().split('.')[-1]

    if ext == 'pdf':
        text = extract_text_from_pdf(file_bytes)
    elif ext in ['jpg', 'jpeg', 'png']:
        text = extract_text_from_image(file_bytes)
    else:
        return {"error": "Format not supported"}

    return {
        "filename": filename,
        "word_count": len(text.split()),
        "text": text
        # TODO: add category field once classifier is built (Phase 3)
        # TODO: save to database (Phase 4)
    }
