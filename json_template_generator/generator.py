"""Pipeline orchestrator: file in -> filled JSON template out."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from .document_classifier import DocumentClassifier
from .models import Document, FilledTemplate
from .ocr import LocalTextOcrService, OcrClient
from .template_filler import TemplateFiller


class JsonTemplateGenerator:
    """End-to-end document processing pipeline.

    1. Sends the input file to the OCR service and receives its txt/json.
    2. Detects the document type (court file, invoice, letter, other).
    3. Generates the matching JSON template.
    4. Fills the template with the crucial details found in the text.
    """

    def __init__(
        self,
        ocr_client: Optional[OcrClient] = None,
        classifier: Optional[DocumentClassifier] = None,
        filler: Optional[TemplateFiller] = None,
    ) -> None:
        self._ocr = ocr_client or LocalTextOcrService()
        self._classifier = classifier or DocumentClassifier()
        self._filler = filler or TemplateFiller()

    def process(self, file_path: Union[str, Path]) -> FilledTemplate:
        """Run the full pipeline for *file_path* and return the filled template."""
        document = Document(path=Path(file_path))
        extracted = self._ocr.extract(document)
        template = self._classifier.classify(extracted)
        return self._filler.fill(template, extracted)
