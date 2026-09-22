"""Data models used across the json_template_generator pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class DocumentType(str, Enum):
    """Supported document categories."""

    COURT_FILE = "court_file"
    INVOICE = "invoice"
    LETTER = "letter"
    OTHER = "other"


@dataclass
class Document:
    """An input document to be processed (PDF, scanned image, text, ...)."""

    path: Path
    mime_type: Optional[str] = None

    def __post_init__(self) -> None:
        self.path = Path(self.path)

    @property
    def name(self) -> str:
        return self.path.name

    def read_bytes(self) -> bytes:
        return self.path.read_bytes()


@dataclass
class ExtractedText:
    """The OCR service response for a document."""

    text: str
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @property
    def lines(self) -> List[str]:
        return [line.strip() for line in self.text.splitlines() if line.strip()]


@dataclass
class FilledTemplate:
    """A generated JSON template populated with extracted document details."""

    document_type: DocumentType
    fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"document_type": self.document_type.value, **self.fields}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
