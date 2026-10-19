import pytest
from app.manifest_repository import ManifestRepository
from pathlib import Path
from app.storage import LocalFileStorage
from app.services.document_service import DocumentService
from app.models import File


@pytest.fixture
def manifest_repository(tmp_path: Path) -> ManifestRepository:
    return ManifestRepository(Path(tmp_path / 'manifest.json'))

@pytest.fixture
def storage(tmp_path: Path) -> LocalFileStorage:
    return LocalFileStorage(Path(tmp_path / "data/documents"))

@pytest.fixture
def service(manifest_repository: ManifestRepository, storage: LocalFileStorage) -> DocumentService:
    return DocumentService(manifest_repository, storage)

@pytest.fixture
def file(tmp_path: Path) -> File:
    source_file = tmp_path / 'article.txt'
    text = 'hello'
    source_file.write_text(text, encoding='utf-8')
    return {
        'source': source_file,
        'text': text
    }