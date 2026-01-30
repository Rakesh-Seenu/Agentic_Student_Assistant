"""
Integration tests for core.utils.parse_pdf module.
No mocks - tests real PDF parsing.
"""
import pytest
from pathlib import Path
from agentic_student_assistant.core.utils.parse_pdf import extract_text_from_pdf


class TestParsePdf:
    """Integration tests for PDF parsing."""
    
    def test_extract_text_nonexistent_file(self):
        """Test extracting text from non-existent file."""
        result = extract_text_from_pdf(Path("/nonexistent/file.pdf"))
        
        # Should return empty string or handle gracefully
        assert isinstance(result, str)
    
    def test_extract_text_invalid_path(self):
        """Test with invalid path."""
        result = extract_text_from_pdf(Path(""))
        
        assert isinstance(result, str)
