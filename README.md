# Python Document Manager

A lightweight document management project built with Python to practice core Python concepts, file handling, JSON persistence, object-oriented design, and automated testing.

## Features

- Create documents from local text files.
- Store document files in a dedicated local directory.
- Maintain document metadata in a JSON manifest.
- Retrieve documents by their unique IDs.
- Delete documents and their associated metadata.
- Handle missing files and nonexistent document IDs.
- Test service behavior and failure scenarios using `pytest`.

## Project Structure

```text
my-project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── manifest_repository.py
│   ├── storage.py
│   └── services/
│       └── document_service.py
├── data/
│   └── documents/
├── tests/
│   ├── conftest.py
│   └── test_document_service.py
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.10 or newer
- `pytest` for running tests

## Installation

Clone the repository and navigate to the project directory.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

Install the project and its development dependencies according to the configuration in `pyproject.toml`.

If `pytest` is not included in the project dependencies, install it with:

```bash
python -m pip install pytest
```

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run only the document service tests:

```bash
python -m pytest -v tests/test_document_service.py
```

The test suite uses temporary directories and fixtures to isolate test data and avoid modifying persistent application data.

## Document Metadata

Each document manifest contains the following fields:

| Field | Description |
|---|---|
| `id` | Unique document identifier |
| `filename` | Original filename |
| `size` | Document size in bytes |
| `word_count` | Number of words in the document |
| `created_at` | Document creation timestamp |
| `status` | Processing status, currently `processed` |

## Architecture

The project separates responsibilities into three main components:

- **DocumentService:** Coordinates document creation, retrieval, deletion, and metadata operations.
- **LocalFileStorage:** Handles document file storage and file-related operations.
- **ManifestRepository:** Manages document metadata persisted in JSON.

The `models.py` module defines typed data structures using Python's `TypedDict` and `Literal`.

## Testing

The project uses `pytest` to verify expected behavior, including:

- Successful document creation and deletion.
- Correct metadata generation.
- Handling nonexistent source files and document IDs.
- Ensuring failed operations raise the expected exceptions.
- Verifying file and metadata state when manifest operations fail.

Tests use fixtures, `tmp_path`, and `monkeypatch` to isolate dependencies and simulate failures.

## Scope and Limitations

This is a local Python learning project, not yet a production-ready document management service.

- Documents and metadata are stored locally.
- The manifest uses JSON persistence rather than a database.
- No HTTP API or authentication layer is included yet.
- Concurrent writes, crash recovery, and full transactional guarantees require additional design and testing.

## Learning Objectives

This project provides practical experience with:

- Python modules and packages.
- Type hints and typed data structures.
- Object-oriented programming and separation of responsibilities.
- File handling with `pathlib`.
- JSON serialization and persistence.
- Exception handling.
- Automated testing with `pytest`.
- Dependency substitution and failure simulation in tests.

## Roadmap

- [ ] Improve consistency when file and manifest operations fail.
- [ ] Add structured logging.
- [ ] Expand unit and integration test coverage.
- [ ] Build a REST API using FastAPI.
- [ ] Introduce persistent database storage if required.
- [ ] Add configuration management and production-oriented error handling.

## License

No license has been specified yet.
