import pytesseract
import cv2
import numpy as np
from PIL import Image
import pdfplumber
import io

# Chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_bytes: bytes) -> str:
    """Extrait le texte d'une image"""
    image = Image.open(io.BytesIO(image_bytes))
    image_np = np.array(image)
    
    # Prétraitement pour améliorer l'OCR
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang='fra+eng')
    return text.strip()

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extrait le texte d'un PDF"""
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def process_document(file_bytes: bytes, filename: str) -> dict:
    """Traite un document et retourne le texte extrait"""
    extension = filename.lower().split('.')[-1]
    
    if extension == 'pdf':
        text = extract_text_from_pdf(file_bytes)
        doc_type = "PDF"
    elif extension in ['jpg', 'jpeg', 'png']:
        text = extract_text_from_image(file_bytes)
        doc_type = "Image"
    else:
        return {"error": "Format non supporté"}
    
    return {
        "filename": filename,
        "type": doc_type,
        "text": text,
        "word_count": len(text.split())
    }