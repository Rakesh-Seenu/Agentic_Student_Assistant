"""
Integration tests for core.utils modules.
No mocks - tests real functionality.
"""
import pytest
from pathlib import Path
from agentic_student_assistant.core.utils.config_loader import get_config, get_prompt
from agentic_student_assistant.core.utils.chunker import chunk_text
from agentic_student_assistant.core.utils.prompt_loader import load_agent_prompts
from agentic_student_assistant.core.utils.logging_manager import setup_logger, get_logger


class TestConfigLoader:
    """Integration tests for config loader."""
    
    def test_get_config(self):
        """Test loading configuration."""
        config = get_config()
        
        assert config is not None
        assert hasattr(config, 'models')
        assert hasattr(config, 'routing')
        assert hasattr(config, 'cache')
    
    def test_get_prompt_existing(self):
        """Test loading existing prompt."""
        prompt = get_prompt("router_system")
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
    
    def test_get_prompt_nonexistent(self):
        """Test loading non-existent prompt."""
        prompt = get_prompt("nonexistent_xyz_123")
        
        assert prompt == ""


class TestChunker:
    """Integration tests for text chunker."""
    
    def test_chunk_text_normal(self):
        """Test normal text chunking."""
        text = "word " * 100
        chunks = chunk_text(text, chunk_size=50, overlap=10)
        
        assert isinstance(chunks, list)
        assert len(chunks) > 1
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_chunk_text_small(self):
        """Test chunking small text."""
        text = "small text here"
        chunks = chunk_text(text, chunk_size=100)
        
        assert len(chunks) == 1
        assert chunks[0] == text
    
    def test_chunk_text_empty(self):
        """Test chunking empty text."""
        chunks = chunk_text("", chunk_size=100)
        
        assert isinstance(chunks, list)
    
    def test_chunk_text_no_overlap(self):
        """Test chunking without overlap."""
        text = "word " * 50
        chunks = chunk_text(text, chunk_size=20, overlap=0)
        
        assert isinstance(chunks, list)
        assert len(chunks) >= 1
    
    def test_chunk_text_large_overlap(self):
        """Test chunking with large overlap."""
        text = "word " * 50
        chunks = chunk_text(text, chunk_size=30, overlap=20)
        
        assert isinstance(chunks, list)


class TestPromptLoader:
    """Integration tests for prompt loader."""
    
    def test_load_agent_prompts_valid_path(self):
        """Test loading prompts from valid agent path."""
        agent_path = Path(__file__).parent.parent.parent / "talk2books"
        prompts = load_agent_prompts(agent_path)
        
        assert isinstance(prompts, dict)
    
    def test_load_agent_prompts_invalid_path(self):
        """Test loading prompts from invalid path."""
        agent_path = Path("/nonexistent/path/xyz")
        prompts = load_agent_prompts(agent_path)
        
        assert prompts == {}


class TestLoggingManager:
    """Integration tests for logging manager."""
    
    def test_setup_logger(self):
        """Test setting up a logger."""
        logger = setup_logger("test_logger")
        
        assert logger is not None
        assert logger.name == "test_logger"
        assert len(logger.handlers) > 0
    
    def test_get_logger(self):
        """Test getting a logger."""
        logger = get_logger("test_app")
        
        assert logger is not None
        assert logger.name == "test_app"
    
    def test_logger_singleton(self):
        """Test logger returns same instance."""
        logger1 = get_logger("same_name")
        logger2 = get_logger("same_name")
        
        assert logger1 == logger2
    
    def test_logger_different_names(self):
        """Test loggers with different names."""
        logger1 = get_logger("name1")
        logger2 = get_logger("name2")
        
        assert logger1.name == "name1"
        assert logger2.name == "name2"
