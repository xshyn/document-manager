from pathlib import Path
from uuid import UUID
from app.manifest_repository import ManifestRepository
from app.models import Manifest
from app.storage import LocalFileStorage
from datetime import datetime, timezone
import logging
from app.config import get_config

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(
        self,
        manifest_repository: ManifestRepository | None = None,
        storage: LocalFileStorage | None = None,
    ):
        self.manifest_repository = (
            manifest_repository
            if manifest_repository is not None
            else ManifestRepository(get_config().manifest_path)
        )

        self.storage = (
            storage
            if storage is not None
            else LocalFileStorage(get_config().documents_dir)
        )

    def create_document(self, source_path: Path) -> UUID:
        logger.info("Processing document: %s", source_path)
        if not source_path.is_file():
            logger.warning("Source file does not exist: %s", source_path)
            raise FileNotFoundError(f"Source file not found: {source_path}")

        content = source_path.read_text(encoding='utf-8')
        document_id = self.storage.save(source_path)
        
        manifest: Manifest = {
            'id': str(document_id),
            'created_at': datetime.now(timezone.utc).isoformat(),
            'filename': source_path.name,
            'size': source_path.stat().st_size,
            'word_count': len(content.split()),
            'status': 'processed',
        }

        self.manifest_repository.add(manifest)
        return document_id

    def get_document(self, document_id: UUID):
        return self.manifest_repository.get_by_id(str(document_id))
    def list_documents(self) -> list[Manifest]:
        return self.manifest_repository.get_all()

    def delete_document(self, document_id: UUID) -> None:
        self.manifest_repository.get_by_id(str(document_id))

        content = self.storage.read(document_id)

        self.storage.delete(document_id)

        try:
            self.manifest_repository.delete_by_id(str(document_id))
        except Exception:
            backup_path = self.storage.base_path / str(document_id)
            backup_path.write_bytes(content)
            raise
