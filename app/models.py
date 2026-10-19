from typing import TypedDict, Literal
from pathlib import Path
class Manifest(TypedDict):
    id: str
    filename: str
    size: int
    word_count: int
    created_at: str
    status: Literal["processed"]

class File(TypedDict):
    source: Path
    text: str