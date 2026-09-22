"""Keyword-based document type detection."""

from __future__ import annotations

from typing import List, Optional

from .models import ExtractedText
from .templates import (
    BaseTemplate,
    CourtFileTemplate,
    GenericTemplate,
    InvoiceTemplate,
    LetterTemplate,
)


class DocumentClassifier:
    """Picks the best-matching template for a document's extracted text.

    Each template exposes ``match_score`` (number of its keywords present
    in the text); the highest-scoring template wins. Falls back to the
    generic template when nothing matches.
    """

    def __init__(self, templates: Optional[List[BaseTemplate]] = None) -> None:
        self._templates = templates or [
            CourtFileTemplate(),
            InvoiceTemplate(),
            LetterTemplate(),
        ]
        self._fallback = GenericTemplate()

    def classify(self, extracted: ExtractedText) -> BaseTemplate:
        best = max(self._templates, key=lambda t: t.match_score(extracted))
        if best.match_score(extracted) == 0:
            return self._fallback
        return best
