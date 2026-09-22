"""Abstract OCR client interface.

Any OCR backend (HTTP API, local engine, mock) must implement this
interface so the rest of the pipeline stays decoupled from OCR details
(encapsulation + abstraction).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Document, ExtractedText


class OcrClient(ABC):
    """Contract for OCR services: send a file, receive its textual content."""

    @abstractmethod
    def extract(self, document: Document) -> ExtractedText:
        """Send *document* to the OCR backend and return the extracted text.

        Implementations should populate ``ExtractedText.raw_response`` with
        the backend's original txt/json payload when available.
        """
        raise NotImplementedError
