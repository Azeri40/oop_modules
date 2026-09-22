"""Abstract base template for all document types.

Each concrete template declares the crucial fields for its document type
and the regex patterns used to locate their values in OCR-extracted text.
Subclasses only supply data (fields/keywords); the extraction algorithm
lives here (inheritance + polymorphism).
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..models import DocumentType, ExtractedText, FilledTemplate


@dataclass(frozen=True)
class TemplateField:
    """A single field a template wants to capture.

    ``pattern`` is a regex with one capture group; the first match in the
    document text becomes the field value.
    """

    name: str
    pattern: Optional[str] = None
    default: Any = None


class BaseTemplate(ABC):
    """Contract for document templates."""

    @property
    @abstractmethod
    def document_type(self) -> DocumentType:
        """The document category this template targets."""

    @property
    @abstractmethod
    def fields(self) -> List[TemplateField]:
        """The crucial fields to capture for this document type."""

    @property
    @abstractmethod
    def keywords(self) -> List[str]:
        """Keywords whose presence in a document suggests this type."""

    def generate(self) -> Dict[str, Any]:
        """Generate the empty JSON template (all fields with defaults)."""
        return {f.name: f.default for f in self.fields}

    def fill(self, extracted: ExtractedText) -> FilledTemplate:
        """Fill the template with values found in *extracted* text."""
        values = self.generate()
        for f in self.fields:
            if not f.pattern:
                continue
            match = re.search(f.pattern, extracted.text, re.IGNORECASE | re.MULTILINE)
            if match:
                values[f.name] = match.group(1).strip()
        return FilledTemplate(document_type=self.document_type, fields=values)

    def match_score(self, extracted: ExtractedText) -> int:
        """How many of this template's keywords appear in the text."""
        text = extracted.text.lower()
        return sum(1 for kw in self.keywords if kw.lower() in text)
