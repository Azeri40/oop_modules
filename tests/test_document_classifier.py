"""Tests for keyword-based document classification."""

from json_template_generator.document_classifier import DocumentClassifier
from json_template_generator.models import DocumentType, ExtractedText


def classify(text: str) -> DocumentType:
    return DocumentClassifier().classify(ExtractedText(text=text)).document_type


def test_classifies_invoice():
    assert classify("Invoice No: 1\nBill To: X\nTotal: 5") == DocumentType.INVOICE


def test_classifies_court_file():
    assert classify("Case No: 1\nPlaintiff: A\nDefendant: B") == DocumentType.COURT_FILE


def test_classifies_letter():
    assert classify("Dear Bob,\nSincerely,\nAlice") == DocumentType.LETTER


def test_falls_back_to_generic():
    assert classify("completely unrelated content") == DocumentType.OTHER
