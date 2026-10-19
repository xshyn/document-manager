from pathlib import Path
from app.services.document_service import DocumentService
from app.manifest_repository import ManifestRepository
from app.storage import LocalFileStorage
import pytest
from uuid import uuid4
from app.models import File, Manifest

def test_create_document(
        manifest_repository: ManifestRepository, 
        service: DocumentService, 
        storage: LocalFileStorage,
        file: File, 
        ) -> None:
    document_id = service.create_document(file["source"])

    manifest = manifest_repository.get_by_id(str(document_id))

    assert manifest["id"] == str(document_id)
    assert manifest["filename"] == "article.txt"
    assert manifest["size"] == len(file['text'].encode("utf-8"))
    assert manifest["word_count"] == 1
    assert storage.exists(document_id)
    
def test_delete_document(
    manifest_repository: ManifestRepository,
    service: DocumentService,
    storage: LocalFileStorage,
    file: File
    ) -> None:

    document_id = service.create_document(file['source'])
    service.delete_document(document_id)
    assert manifest_repository.get_all() == []
    assert not storage.exists(document_id)

def test_create_document_nonexistent_file_raises_error(
    tmp_path: Path,
    manifest_repository: ManifestRepository,
    service: DocumentService
) -> None:

    source_file = tmp_path / 'article.txt'

    with pytest.raises(FileNotFoundError):
        service.create_document(source_file)

    assert manifest_repository.get_all() == []

def test_get_document_nonexistent_id_raises_error(
    service: DocumentService
) -> None:

    with pytest.raises(FileNotFoundError):
        service.get_document(uuid4())

def test_delete_document_nonexistent_id_raises_error(
    service: DocumentService,
    manifest_repository: ManifestRepository
) -> None:
    with pytest.raises(FileNotFoundError):
        service.delete_document(uuid4())

    assert manifest_repository.get_all() == []



def test_delete_document_when_manifest_delete_fails(
    monkeypatch: pytest.MonkeyPatch,
    service: DocumentService,
    manifest_repository: ManifestRepository,
    storage: LocalFileStorage,
    file: File,
) -> None:
    document_id = service.create_document(file["source"])

    def fail_delete(document_id: str) -> None:
        raise OSError("Simulated manifest write failure")

    monkeypatch.setattr(
        manifest_repository,
        "delete_by_id",
        fail_delete,
    )

    with pytest.raises(OSError, match="Simulated manifest write failure"):
        service.delete_document(document_id)

    assert storage.exists(document_id)
    assert storage.read(document_id) == b"hello"

    manifest = manifest_repository.get_by_id(str(document_id))
    assert manifest["id"] == str(document_id)

def test_create_document_when_manifest_add_fails(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        service: DocumentService,
        manifest_repository: ManifestRepository,
        storage: LocalFileStorage,
        file: File
) -> None:
    def fail_add(manifest: Manifest) -> None:
        raise OSError("Simulated manifest write failure")

    monkeypatch.setattr(manifest_repository, 'add' , fail_add)
    with pytest.raises(OSError):
        service.create_document(file["source"])

    files = list(Path(tmp_path / "data/documents").iterdir())

    

    assert manifest_repository.get_all() == []
    assert len(files) == 1