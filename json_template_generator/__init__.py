"""json_template_generator.

A module that turns raw document files into structured, filled-in JSON
templates:

1. Extracts document text via an OCR service.
2. Detects the document type (court file, invoice, letter, other).
3. Generates a JSON template capturing the crucial fields for that type.
4. Fills the template with values found in the extracted text.
"""

__version__ = "0.1.0"

from .generator import JsonTemplateGenerator

__all__ = ["JsonTemplateGenerator"]
