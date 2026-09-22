"""Template for court documents."""

from __future__ import annotations

from typing import List

from ..models import DocumentType
from .base_template import BaseTemplate, TemplateField


class CourtFileTemplate(BaseTemplate):
    """Captures crucial details of court files."""

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.COURT_FILE

    @property
    def fields(self) -> List[TemplateField]:
        return [
            TemplateField("case_number", r"case\s*(?:no\.?|number)[:\s]+([A-Z0-9./-]+)"),
            TemplateField("court_name", r"^((?:[A-Z][\w.]*\s)+court(?:\s+of\s+[\w\s]+)?)"),
            TemplateField("plaintiff", r"plaintiff[:\s]+(.+)"),
            TemplateField("defendant", r"defendant[:\s]+(.+)"),
            TemplateField("judge", r"(?:judge|presiding)[:\s]+(.+)"),
            TemplateField("hearing_date", r"hearing\s*date[:\s]+([\d./-]+)"),
            TemplateField("ruling", r"ruling[:\s]+(.+)"),
        ]

    @property
    def keywords(self) -> List[str]:
        return ["court", "plaintiff", "defendant", "case no", "hearing", "judge", "ruling"]
