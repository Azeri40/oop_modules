"""Concrete OCR client implementations."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..models import Document, ExtractedText
from .ocr_client import OcrClient


class HttpOcrService(OcrClient):
    """OCR client backed by a remote HTTP OCR service.

    Sends the document file to the service endpoint and expects a JSON
    response of the form ``{"text": "..."}`` (extra keys are preserved in
    ``raw_response``).
    """

    def __init__(self, endpoint: str, api_key: Optional[str] = None, timeout: int = 60) -> None:
        self._endpoint = endpoint
        self._api_key = api_key
        self._timeout = timeout

    def extract(self, document: Document) -> ExtractedText:
        import requests

        headers: Dict[str, str] = {}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        with open(document.path, "rb") as fh:
            response = requests.post(
                self._endpoint,
                headers=headers,
                files={"file": (document.name, fh, document.mime_type or "application/octet-stream")},
                timeout=self._timeout,
            )
        response.raise_for_status()

        payload: Dict[str, Any] = response.json()
        return ExtractedText(text=payload.get("text", ""), raw_response=payload)


class LocalTextOcrService(OcrClient):
    """OCR client for local development and testing.

    Treats the input file as plain text (e.g. a pre-OCRed ``.txt`` file),
    which makes the full pipeline runnable without a real OCR backend.
    """

    def extract(self, document: Document) -> ExtractedText:
        text = document.path.read_text(encoding="utf-8")
        return ExtractedText(text=text, raw_response={"text": text, "source": "local"})
