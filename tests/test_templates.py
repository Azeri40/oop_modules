"""Tests for template generation and filling."""

from json_template_generator.models import ExtractedText
from json_template_generator.templates import GenericTemplate, InvoiceTemplate


def test_generate_returns_empty_template():
    template = InvoiceTemplate().generate()
    assert set(template) == {
        "invoice_number",
        "issue_date",
        "due_date",
        "seller",
        "buyer",
        "total_amount",
        "currency",
    }
    assert all(value is None for value in template.values())


def test_fill_captures_matching_fields():
    extracted = ExtractedText(text="Invoice Number: A-1\nTotal: USD 9.99")
    filled = InvoiceTemplate().fill(extracted)
    assert filled.fields["invoice_number"] == "A-1"
    assert filled.fields["total_amount"] == "9.99"
    assert filled.fields["due_date"] is None


def test_generic_template_uses_first_lines():
    extracted = ExtractedText(text="Some Title\nSecond line")
    filled = GenericTemplate().fill(extracted)
    assert filled.fields["title"] == "Some Title"
    assert "Second line" in filled.fields["summary"]
