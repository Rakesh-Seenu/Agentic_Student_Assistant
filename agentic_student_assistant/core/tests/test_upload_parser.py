"""
Integration tests for core.utils.upload_parser module.
No mocks - tests real file parsing.
"""
import pytest
from pathlib import Path
from agentic_student_assistant.core.utils.upload_parser import parse_uploaded_file


class TestUploadParser:
    """Integration tests for upload parser."""
    
    def test_parse_nonexistent_file(self):
        """Test parsing non-existent file."""
        result = parse_uploaded_file(Path("/nonexistent/file.txt"))
        
        assert isinstance(result, str)
    
    def test_parse_unsupported_extension(self):
        """Test parsing unsupported file type."""
        result = parse_uploaded_file(Path("test.xyz"))
        
        assert isinstance(result, str)
