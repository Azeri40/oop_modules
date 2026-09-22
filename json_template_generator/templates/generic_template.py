"""Fallback template for uncategorized documents."""

from __future__ import annotations

from typing import List

from ..models import DocumentType, ExtractedText, FilledTemplate
from .base_template import BaseTemplate, TemplateField


class GenericTemplate(BaseTemplate):
    """Generic template used when no specific document type matches."""

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.OTHER

    @property
    def fields(self) -> List[TemplateField]:
        return [
            TemplateField("title"),
            TemplateField("date", r"date[:\s]+([\d./-]+|\w+\s+\d{1,2},?\s+\d{4})"),
            TemplateField("summary"),
        ]

    @property
    def keywords(self) -> List[str]:
        # Fallback template: never wins keyword matching on its own.
        return []

    def fill(self, extracted: ExtractedText) -> FilledTemplate:
        filled = super().fill(extracted)
        lines = extracted.lines
        if lines:
            filled.fields["title"] = lines[0]
            filled.fields["summary"] = " ".join(lines[:3])
        return filled
