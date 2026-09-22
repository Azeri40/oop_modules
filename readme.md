# JSON Template Generator

A basic implementation of the **`json_template_generator`** module — a document-understanding pipeline that turns raw document files into structured, filled-in JSON templates.

## Purpose

Organizations deal with many kinds of documents: **court files, invoices, letters, contracts, and more**. Each document type carries its own set of crucial details (case numbers, invoice totals, sender/recipient info, dates, etc.). This module demonstrates how to:

1. **Extract** the text content of a document using an OCR service.
2. **Generate** a JSON template that captures the important fields for that document type.
3. **Fill in** the template with the actual values extracted from the document.

The result is a clean, machine-readable JSON representation of any supported document.

## How It Works

```
 ┌──────────┐      ┌─────────────┐      ┌───────────────────┐      ┌─────────────────┐
 │  Input   │ ───► │ OCR Service │ ───► │ Template          │ ───► │ Filled JSON     │
 │  File    │      │ (txt/json)  │      │ Generation        │      │ Output          │
 └──────────┘      └─────────────┘      └───────────────────┘      └─────────────────┘
```

1. **Input** — A document file (PDF, scanned image, etc.) is provided to the module.
2. **OCR** — The file is sent to an OCR service, which returns the document's contents as text/JSON.
3. **Template generation** — Based on the document type (court file, invoice, letter, or other), a JSON template is generated that defines the fields worth capturing.
4. **Template filling** — The template is populated with the crucial details found in the extracted text.

### Example

Given an invoice as input, the module might produce:

```json
{
  "document_type": "invoice",
  "invoice_number": "INV-2025-0042",
  "issue_date": "2025-09-01",
  "seller": "Acme Corp.",
  "buyer": "Example LLC",
  "total_amount": "1250.00",
  "currency": "USD",
  "line_items": [
    { "description": "Consulting services", "quantity": 10, "unit_price": "125.00" }
  ]
}
```

## Supported Document Types

- ⚖️ Court files — case numbers, parties, hearing dates, rulings
- 🧾 Invoices — invoice numbers, dates, parties, line items, totals
- ✉️ Letters — sender, recipient, date, subject, body summary
- 📄 Others — a generic template for uncategorized documents

## OOP Principles Used

This module doubles as a showcase of core object-oriented design:

| Principle | Where |
|-----------|-------|
| **Abstraction** | [`OcrClient`](json_template_generator/ocr/ocr_client.py) and [`BaseTemplate`](json_template_generator/templates/base_template.py) are abstract base classes (ABCs) that define `@abstractmethod` contracts without committing to an implementation. |
| **Inheritance** | [`InvoiceTemplate`](json_template_generator/templates/invoice_template.py), [`CourtFileTemplate`](json_template_generator/templates/court_file_template.py), [`LetterTemplate`](json_template_generator/templates/letter_template.py), and [`GenericTemplate`](json_template_generator/templates/generic_template.py) inherit from `BaseTemplate`; [`HttpOcrService` and `LocalTextOcrService`](json_template_generator/ocr/ocr_service.py) inherit from `OcrClient`. Subclasses only supply data (fields/keywords) — the shared extraction algorithm lives in the base class. |
| **Polymorphism** | The [classifier](json_template_generator/document_classifier.py) and [generator](json_template_generator/generator.py) work with *any* `BaseTemplate` / `OcrClient` through the base interface; `GenericTemplate` even overrides `fill()` with its own behavior. |
| **Encapsulation** | OCR backend details are hidden behind private attributes (`self._endpoint`, `self._ocr`); templates keep their regex extraction logic internal and expose only `generate()` / `fill()`. |
| **Composition + Dependency Injection** | [`JsonTemplateGenerator`](json_template_generator/generator.py) *composes* an OCR client, a classifier, and a filler — all injectable via the constructor (e.g., swap `LocalTextOcrService` for `HttpOcrService` in production without touching the pipeline). |

### Importable module

```python
from json_template_generator import JsonTemplateGenerator

generator = JsonTemplateGenerator()
filled = generator.process("examples/sample_letter.txt")
print(filled.to_json())
```

## Roadmap

- [x] Core `json_template_generator` module
- [x] OCR service integration
- [x] Document-type detection
- [x] Template definitions per document type
- [x] Template filling engine
- [x] Examples and tests

## Getting Started

Clone the repository:

```bash
git clone https://github.com/Azeri40/oop_modules.git
```
