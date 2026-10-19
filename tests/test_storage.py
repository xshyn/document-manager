from pathlib import Path
import pytest
from app.storage import LocalFileStorage
from uuid import uuid4

def test_save_and_read_file(tmp_path: Path) -> None:
    source_file = tmp_path / "article.txt"
    text = "Hello Python"
    source_file.write_text(text , encoding='utf-8')

    storage = LocalFileStorage(tmp_path / "documents")

    document_id = storage.save(source_file)
    content = storage.read(document_id)

    assert storage.exists(document_id)
    assert content == b"Hello Python"

def test_delete_file(tmp_path: Path) -> None:
    source_file = tmp_path / 'article.txt'
    text = "Hello Python"
    source_file.write_text(text, encoding="utf-8")

    storage = LocalFileStorage(tmp_path / "documents")
    document_id = storage.save(source_file)

    storage.delete(document_id)
    assert not storage.exists(document_id)

def test_read_nonexistent_file_raises_error(tmp_path: Path) -> None:
    storage = LocalFileStorage(tmp_path / "documents")

    with pytest.raises(FileNotFoundError):
        storage.read(uuid4())

def test_save_nonexistent_source_raises_error(tmp_path: Path) -> None:
    storage = LocalFileStorage(tmp_path / "documents")

    with pytest.raises(FileNotFoundError):
        storage.save(tmp_path / "article.txt")