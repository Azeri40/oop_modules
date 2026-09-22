"""CLI entry point: generate a filled JSON template from a document file.

Usage:
    python main.py <file> [--ocr-endpoint URL] [--api-key KEY] [-o OUTPUT]

Without --ocr-endpoint the input is treated as plain text (local mode),
which is handy for development and demos.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from json_template_generator.generator import JsonTemplateGenerator
from json_template_generator.ocr import HttpOcrService, LocalTextOcrService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate and fill a JSON template from a document file."
    )
    parser.add_argument("file", help="Path to the input document")
    parser.add_argument("--ocr-endpoint", help="OCR service endpoint URL (omit for local text mode)")
    parser.add_argument("--api-key", help="API key for the OCR service")
    parser.add_argument("-o", "--output", help="Write the filled JSON to this file instead of stdout")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.ocr_endpoint:
        ocr = HttpOcrService(endpoint=args.ocr_endpoint, api_key=args.api_key)
    else:
        ocr = LocalTextOcrService()

    generator = JsonTemplateGenerator(ocr_client=ocr)
    filled = generator.process(args.file)
    output = filled.to_json()

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
