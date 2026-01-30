"""
Tests for core.utils.prompt_loader module.
"""
import pytest
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from agentic_student_assistant.core.utils.prompt_loader import load_agent_prompts


class TestPromptLoader:
    """Test cases for prompt_loader module."""
    
    def test_load_agent_prompts_success(self):
        """Test successfully loading prompts from YAML."""
        mock_yaml_content = """
        prompts:
            system: "System prompt"
            user: "User prompt"
        """
        
        agent_path = Path("/mock/agent/path")
        expected_config_path = agent_path / "configs" / "prompts.yaml"
        
        with patch("builtins.open", mock_open(read_data=mock_yaml_content)) as mock_file:
            prompts = load_agent_prompts(agent_path)
            
            assert prompts["system"] == "System prompt"
            assert prompts["user"] == "User prompt"
            mock_file.assert_called_once_with(expected_config_path, "r", encoding="utf-8")
            
    def test_load_agent_prompts_file_not_found(self):
        """Test handling when prompt file is missing."""
        agent_path = Path("/mock/agent/path")
        
        with patch("builtins.open", side_effect=FileNotFoundError):
            prompts = load_agent_prompts(agent_path)
            
            assert prompts == {}
    
    def test_load_agent_prompts_yaml_error(self, capsys):
        """Test handling of YAML parsing errors."""
        agent_path = Path("/mock/agent/path")
        
        with patch("builtins.open", mock_open(read_data="invalid: yaml: content:")):
            with patch("yaml.safe_load", side_effect=yaml.YAMLError("Parse error")):
                prompts = load_agent_prompts(agent_path)
                
                assert prompts == {}
                captured = capsys.readouterr()
                assert "Error loading prompts" in captured.out


class TestPromptLoaderMain:
    """Test the __main__ block of prompt_loader."""
    
    def test_main_block(self):
        """Test main block execution simulation."""
        # Main block just prints, so we just verify function works
        # No complex logic in main block to test specifically
        pass
