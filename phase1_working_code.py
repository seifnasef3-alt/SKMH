# SKMH Project - Phase 1 : Setup & Architecture
# Seïf NASEF - Week 1-3 - June 2026
# STATUS : Completed ✅

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append('../')

app = FastAPI(
    title="SKMH API",
    description="Smart Knowledge Management Hub - Backend API",
    version="1.0.0"
)

# Allow frontend (React) to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Route 1 : Health check ──
# Just to verify the server is running correctly
@app.get("/")
def read_root():
    return {
        "message": "SKMH API is running",
        "status": "ok",
        "version": "1.0.0"
    }


# ── Route 2 : Health check ──
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ── Route 3 : Upload a document ──
# Receives a file from the frontend and sends it to the OCR pipeline
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()

    # Pass file to OCR service (Phase 2)
    from ocr.ocr_service import process_document
    result = process_document(contents, file.filename)

    return result
