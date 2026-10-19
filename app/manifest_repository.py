from pathlib import Path
from app.models import Manifest
import json

class ManifestRepository:
    def __init__(self, manifest_path: Path):
        self.manifest_path = manifest_path
        self.manifest_path.parent.mkdir(parents=True,exist_ok=True)

        if not self.manifest_path.exists(): 
            self.manifest_path.write_text('[]', encoding='utf-8')

    def get_all(self) -> list[Manifest]:
        with self.manifest_path.open('r' , encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Manifest must contain a JSON list")

        return data

    def save_all(self, manifests: list[Manifest]) -> None:
        with self.manifest_path.open('w' , encoding='utf-8') as file:
            json.dump(manifests, file, indent=2, ensure_ascii=False)

    def add(self, manifest: Manifest) -> None:
        manifests = self.get_all()
        manifests.append(manifest)
        self.save_all(manifests)

    def get_by_id(self, document_id: str) -> Manifest:
        manifests = self.get_all()
        manifest = next((m for m in  manifests if m['id'] == document_id), None)
            
        if manifest is None: raise FileNotFoundError(f'Document metadata not found: {document_id}')
        return manifest

    def delete_by_id(self, document_id: str) -> None: 
        manifests = self.get_all()
        filtered_manifests = [m for m in manifests if m['id'] != document_id]

        if len(filtered_manifests) == len(manifests):
            raise FileNotFoundError(f"Docuent metadata not found: {document_id}")

        self.save_all(filtered_manifests)