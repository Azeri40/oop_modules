"""Template filling engine."""

from __future__ import annotations

from .models import ExtractedText, FilledTemplate
from .templates import BaseTemplate


class TemplateFiller:
    """Populates a document template with values from extracted text.

    Thin orchestration layer over ``BaseTemplate.fill`` — kept separate so
    filling strategies (regex, NER, LLM, ...) can be swapped independently
    of the template definitions.
    """

    def fill(self, template: BaseTemplate, extracted: ExtractedText) -> FilledTemplate:
        return template.fill(extracted)
