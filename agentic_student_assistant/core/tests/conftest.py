"""
Additional fixtures for core module tests.
"""
import pytest
from pathlib import Path
from unittest.mock import Mock


@pytest.fixture
def test_fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_pdf_path(test_fixtures_dir):
    """Return path to sample PDF file."""
    return test_fixtures_dir / "sample.pdf"
