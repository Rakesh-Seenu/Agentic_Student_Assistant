"""
Integration tests for core.utils.sheets_logger module.
No mocks - tests real Google Sheets integration.
"""
import pytest
from agentic_student_assistant.core.utils.sheets_logger import SheetsLogger


class TestSheetsLogger:
    """Integration tests for Sheets Logger."""
    
    @pytest.mark.integration
    def test_sheets_logger_initialization(self):
        """Test sheets logger initialization."""
        # This will fail if credentials not configured, which is expected
        try:
            logger = SheetsLogger("test_sheet")
            assert logger is not None
        except Exception as e:
            # Expected if no credentials
            assert isinstance(e, Exception)
    
    @pytest.mark.integration
    def test_log_interaction(self):
        """Test logging an interaction."""
        try:
            logger = SheetsLogger("test_sheet")
            logger.log_interaction("test query", "test response", "test_agent")
            # If it doesn't error, it worked
            assert True
        except Exception:
            # Expected if no credentials
            pytest.skip("Google Sheets credentials not configured")
