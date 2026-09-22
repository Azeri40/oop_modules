"""Template for letters."""

from __future__ import annotations

from typing import List

from ..models import DocumentType
from .base_template import BaseTemplate, TemplateField


class LetterTemplate(BaseTemplate):
    """Captures crucial details of letters."""

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.LETTER

    @property
    def fields(self) -> List[TemplateField]:
        return [
            TemplateField("sender", r"(?:from|sender)[:\s]+(.+)"),
            TemplateField("recipient", r"(?:to|dear|recipient)[:\s]+(.+?)[,\n]"),
            TemplateField("date", r"date[:\s]+([\d./-]+|\w+\s+\d{1,2},?\s+\d{4})"),
            TemplateField("subject", r"(?:subject|re)[:\s]+(.+)"),
            TemplateField("signature", r"(?:sincerely|regards|respectfully),?\s*\n\s*(.+)"),
        ]

    @property
    def keywords(self) -> List[str]:
        return ["dear", "sincerely", "regards", "subject", "respectfully"]
