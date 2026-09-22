"""End-to-end tests for the JsonTemplateGenerator pipeline."""

import json

from json_template_generator import JsonTemplateGenerator


def test_invoice_pipeline(invoice_path):
    filled = JsonTemplateGenerator().process(invoice_path)
    data = filled.to_dict()
    assert data["document_type"] == "invoice"
    assert data["invoice_number"] == "INV-2025-0042"
    assert data["total_amount"] == "1250.00"
    assert data["currency"] == "USD"


def test_court_file_pipeline(court_file_path):
    filled = JsonTemplateGenerator().process(court_file_path)
    data = filled.to_dict()
    assert data["document_type"] == "court_file"
    assert data["case_number"] == "CV-2025-01187"
    assert data["plaintiff"] == "John Doe"
    assert data["defendant"] == "Acme Corp."


def test_letter_pipeline(letter_path):
    filled = JsonTemplateGenerator().process(letter_path)
    data = filled.to_dict()
    assert data["document_type"] == "letter"
    assert data["sender"] == "Alice Johnson"
    assert data["subject"] == "Meeting follow-up"


def test_output_is_valid_json(invoice_path):
    filled = JsonTemplateGenerator().process(invoice_path)
    parsed = json.loads(filled.to_json())
    assert parsed["document_type"] == "invoice"
