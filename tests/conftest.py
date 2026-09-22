"""Shared fixtures for the test suite."""

from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


@pytest.fixture
def invoice_path() -> Path:
    return EXAMPLES_DIR / "sample_invoice.txt"


@pytest.fixture
def court_file_path() -> Path:
    return EXAMPLES_DIR / "sample_court_file.txt"


@pytest.fixture
def letter_path() -> Path:
    return EXAMPLES_DIR / "sample_letter.txt"
