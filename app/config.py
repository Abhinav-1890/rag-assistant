import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Folders (can be overridden with environment variables, useful for tests)
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "uploads"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", BASE_DIR / "chroma_db"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Chunking settings
CHUNK_SIZE = 800      # characters per chunk
CHUNK_OVERLAP = 150   # characters shared between neighbouring chunks

# Models
EMBED_MODEL = "all-MiniLM-L6-v2"
CLAUDE_MODEL = "claude-sonnet-5-5"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Search settings
TOP_K = 4
MIN_SCORE = 0.15  # ignore chunks less similar than this