"""Template for invoice documents."""

from __future__ import annotations

from typing import List

from ..models import DocumentType
from .base_template import BaseTemplate, TemplateField


class InvoiceTemplate(BaseTemplate):
    """Captures crucial details of invoices."""

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.INVOICE

    @property
    def fields(self) -> List[TemplateField]:
        return [
            TemplateField("invoice_number", r"invoice\s*(?:no\.?|number|#)[:\s]*([A-Z0-9-]+)"),
            TemplateField("issue_date", r"(?:issue\s*date|date\s*of\s*issue|invoice\s*date)[:\s]+([\d./-]+)"),
            TemplateField("due_date", r"due\s*date[:\s]+([\d./-]+)"),
            TemplateField("seller", r"(?:seller|from|vendor)[:\s]+(.+)"),
            TemplateField("buyer", r"(?:buyer|to|bill\s*to|customer)[:\s]+(.+)"),
            TemplateField("total_amount", r"total(?:\s*amount)?(?:\s*due)?[:\s]*(?:[A-Z]{3}|[$€£₼])?\s*([\d,]+\.?\d*)"),
            TemplateField("currency", r"\b(USD|EUR|GBP|AZN|TRY)\b"),
        ]

    @property
    def keywords(self) -> List[str]:
        return ["invoice", "bill to", "total", "due date", "amount due", "vendor"]
