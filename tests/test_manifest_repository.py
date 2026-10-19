from pathlib import Path
import pytest
from app.manifest_repository import ManifestRepository, Manifest
from uuid import uuid4

def test_add_and_get_by_id(tmp_path: Path) -> None:
    repo = ManifestRepository(tmp_path / 'manifest.json')
    manifest: Manifest = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "filename": "article.txt",
        "size": 100,
        "word_count": 20,
        "created_at": "2026-10-14T10:00:00+00:00",
        "status": "processed",
    }

    repo.add(manifest)

    recovered_manifest = repo.get_by_id(manifest['id'])
    assert recovered_manifest == manifest

def test_get_by_id_nonexistent_raises_error(tmp_path: Path) -> None:
    repo = ManifestRepository(tmp_path / 'manifest.json')

    with pytest.raises(FileNotFoundError): 
        repo.get_by_id(str(uuid4()))

def test_delete_by_id(tmp_path: Path) -> None:
    repo = ManifestRepository(tmp_path / 'manifest.json')
    manifest: Manifest = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "filename": "article.txt",
        "size": 100,
        "word_count": 20,
        "created_at": "2026-10-14T10:00:00+00:00",
        "status": "processed",
    }
    repo.add(manifest)

    repo.delete_by_id(str(manifest['id']))

    manifests = repo.get_all()

    assert manifests == []

def test_delete_nonexistent_id_raises_error(tmp_path: Path):
    repo = ManifestRepository(tmp_path / 'manifest.json')
    with pytest.raises(FileNotFoundError):
        repo.delete_by_id(str(uuid4()))