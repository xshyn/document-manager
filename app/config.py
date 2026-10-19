from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Config:
    manifest_path: Path
    documents_dir: Path

def get_config() -> Config:
    return Config(
        manifest_path=Path(os.getenv("MANIFEST_PATH" , 'data/manifest.json')),
        documents_dir=Path(os.getenv("DOCUMENTS_DIR" , 'data/documents')),)