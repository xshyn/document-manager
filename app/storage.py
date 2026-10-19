from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID, uuid4

class FileStorage(ABC):
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def save(self, source_path: Path) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def read(self, document_id: UUID) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def delete(self, document_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, document_id: UUID) -> bool:
        raise NotImplementedError

class LocalFileStorage(FileStorage):
    def __init__(
        self,
        base_path: Path = Path("data/documents")
    ):
        super().__init__(base_path)

    def _get_file_path(self, document_id: UUID) -> Path:
        return self.base_path / str(document_id)

    def save(self, source_path: Path) -> UUID:
        if not source_path.is_file():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        document_id = uuid4()
        destination = self._get_file_path(document_id)

        content = source_path.read_bytes()
        destination.write_bytes(content)

        return document_id

    def read(self, document_id: UUID) -> bytes:
        path = self._get_file_path(document_id)

        if not path.is_file():
            raise FileNotFoundError(f"Document not found: {document_id}")
        return path.read_bytes()

    def delete(self, document_id: UUID) -> None:
        path = self._get_file_path(document_id)

        if not path.is_file():
            raise FileNotFoundError(f"Document not found: {document_id}")
        path.unlink()

    def exists(self, document_id: UUID) -> bool:
        return self._get_file_path(document_id).is_file()
