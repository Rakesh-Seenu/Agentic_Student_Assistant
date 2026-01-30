"""Tests for core.utils.config_loader module."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from omegaconf import DictConfig
from agentic_student_assistant.core.utils.config_loader import get_config, get_prompt


class TestConfigLoader:
    @patch('agentic_student_assistant.core.utils.config_loader.compose')
    def test_get_config(self, mock_compose):
        mock_cfg = MagicMock(spec=DictConfig)
        mock_compose.return_value = mock_cfg
        config = get_config()
        assert config == mock_cfg
        mock_compose.assert_called_once()
    
    @patch('agentic_student_assistant.core.utils.config_loader.OmegaConf.load')
    def test_get_prompt(self, mock_load):
        mock_load.return_value = {"test_prompt": "Test content"}
        prompt = get_prompt("test_prompt")
        assert prompt == "Test content"
        
    @patch('agentic_student_assistant.core.utils.config_loader.OmegaConf.load')
    def test_get_prompt_not_found(self, mock_load):
        mock_load.return_value = {}
        prompt = get_prompt("nonexistent")
        assert prompt == ""
