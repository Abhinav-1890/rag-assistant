import os
import tempfile

os.environ["UPLOAD_DIR"] = tempfile.mkdtemp()
os.environ["CHROMA_DIR"] = tempfile.mkdtemp()