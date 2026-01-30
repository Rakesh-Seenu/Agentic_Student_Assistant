"""Tests for core.utils.logging_manager module."""
import pytest
from unittest.mock import Mock, patch
from agentic_student_assistant.core.utils.logging_manager import setup_logger, get_logger


class TestLoggingManager:
    def test_setup_logger(self):
        logger = setup_logger("test_logger")
        assert logger.name == "test_logger"
        assert len(logger.handlers) > 0
    
    def test_get_logger(self):
        logger = get_logger("test")
        assert logger is not None
        assert logger.name == "test"
    
    def test_logger_singleton(self):
        logger1 = get_logger("same")
        logger2 = get_logger("same")
        assert logger1 == logger2
