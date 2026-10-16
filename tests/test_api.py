from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_upload_txt():
    files = {"file": ("t.txt", b"Hello world. " * 100, "text/plain")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    assert r.json()["chunks"] > 0


def test_upload_rejects_bad_type():
    files = {"file": ("virus.exe", b"abc", "application/octet-stream")}
    r = client.post("/upload", files=files)
    assert r.status_code == 400