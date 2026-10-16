import pytest
from app.ingest import chunk_text, build_chunks


def test_short_text_gives_one_chunk():
    assert len(chunk_text("hello world", 100, 20)) == 1


def test_long_text_is_split():
    chunks = chunk_text("word " * 1000, 200, 50)
    assert len(chunks) > 1
    assert all(len(c) <= 200 for c in chunks)


def test_chunks_overlap():
    chunks = chunk_text("abcdefghij" * 50, 100, 20)
    assert chunks[0][-20:] == chunks[1][:20]


def test_build_chunks_from_txt(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("Hello world. " * 100)
    chunks = build_chunks(f, "a.txt")
    assert len(chunks) > 0
    assert chunks[0]["source"] == "a.txt"
    assert chunks[0]["page"] == 1


def test_unsupported_type_raises(tmp_path):
    f = tmp_path / "a.exe"
    f.write_text("nope")
    with pytest.raises(ValueError):
        build_chunks(f, "a.exe")