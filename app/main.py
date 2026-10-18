import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.config import UPLOAD_DIR
from app.ingest import build_chunks

app = FastAPI(title="RAG Document Q&A Assistant")

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = Path(file.filename).name
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Only {sorted(ALLOWED_EXTENSIONS)} files are allowed")

    dest = UPLOAD_DIR / filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks = build_chunks(dest, filename)
    if not chunks:
        raise HTTPException(422, "No text could be extracted from this file")

    return {"filename": filename, "chunks": len(chunks)}