from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append('../')
from ocr.ocr_service import process_document

app = FastAPI(
    title="SKMH API",
    description="Smart Knowledge Management Hub - API Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API SKMH", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload et traitement OCR d'un document"""
    contents = await file.read()
    result = process_document(contents, file.filename)
    return result