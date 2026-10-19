from pathlib import Path
from app.config import get_config

def test_get_config_from_environment(monkeypatch):
    monkeypatch.setenv("MANIFEST_PATH" , 'tmp/custom.json')
    monkeypatch.setenv("DOCUMENTS_DIR" , 'tmp/files')

    config = get_config()

    assert config.manifest_path == Path('tmp/custom.json')
    assert config.documents_dir == Path('tmp/files')