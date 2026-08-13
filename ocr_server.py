#!/usr/bin/env python3
"""
SKMH - OCR Demo Server (Standalone)
Lancer : python ocr_server.py
Puis ouvrir : http://localhost:8000
"""
import io
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# HTML servi directement depuis ce dossier
HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_ocr.html")
with open(HTML_FILE, encoding="utf-8") as f:
    HTML_CONTENT = f.read()

app = FastAPI(title="SKMH OCR Demo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_CONTENT

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    import pdfplumber
    import pytesseract
    import cv2
    import numpy as np
    from PIL import Image

    contents = await file.read()
    filename = file.filename
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        text = ""
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                text += (page_text or "[scanned page]") + "\n"

    elif ext in ["jpg", "jpeg", "png"]:
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        text = pytesseract.image_to_string(thresh, lang="fra+eng+tha")

    else:
        return {"error": "Format non supporté — utilisez PDF, JPG ou PNG"}

    return {
        "filename": filename,
        "word_count": len(text.split()),
        "text": text.strip(),
    }

if __name__ == "__main__":
    print("\n✅ SKMH OCR Demo lancé → http://localhost:8000\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
