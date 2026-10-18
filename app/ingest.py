from pathlib import Path
from pypdf import PdfReader
from app.config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_pages(path: Path) -> list[dict]:
    """Return a list like [{"page": 1, "text": "..."}, ...]"""
    ext = path.suffix.lower()

    if ext == ".pdf":
        reader = PdfReader(str(path))
        return [
            {"page": i + 1, "text": (page.extract_text() or "")}
            for i, page in enumerate(reader.pages)
        ]

    if ext in (".txt", ".md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        return [{"page": 1, "text": text}]

    raise ValueError(f"Unsupported file type: {ext}")


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping pieces."""
    text = " ".join(text.split())  # collapse whitespace
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def build_chunks(path: Path, filename: str) -> list[dict]:
    """Full pipeline: file -> list of chunk dictionaries with metadata."""
    results = []
    for page in extract_text_pages(path):
        for i, piece in enumerate(chunk_text(page["text"])):
            if piece.strip():
                results.append({
                    "text": piece,
                    "source": filename,
                    "page": page["page"],
                    "chunk_index": i,
                })
    return results