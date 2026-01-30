"""
Integration tests for core.utils.llm_factory module.
"""
import pytest
import os
from agentic_student_assistant.core.utils.llm_factory import LLMFactory
from agentic_student_assistant.core.utils.config_loader import get_config


class TestLLMFactory:
    def test_create_llm(self):
        """Test LLM creation."""
        config = get_config()
        llm = LLMFactory.create_llm(config.models)
        
        assert llm is not None
        assert hasattr(llm, 'invoke')
    
    def test_create_llm_with_temperature(self):
        """Test LLM creation with custom temperature."""
        config = get_config()
        llm = LLMFactory.create_llm(config.models, temperature=0.7)
        
        assert llm is not None
        assert llm.temperature == 0.7
    
    def test_create_chat_model(self):
        """Test chat model creation."""
        llm = LLMFactory.create_chat_model(
            model_name="gpt-3.5-turbo",
            temperature=0.5
        )
        
        assert llm is not None
        assert llm.temperature == 0.5
    
    def test_create_embeddings(self):
        """Test embeddings creation."""
        config = get_config()
        embeddings = LLMFactory.create_embeddings(config.models)
        
        assert embeddings is not None
        assert hasattr(embeddings, 'embed_query')
    
    @pytest.mark.integration
    def test_llm_invoke(self):
        """Test that created LLM can be invoked."""
        config = get_config()
        llm = LLMFactory.create_llm(config.models)
        
        response = llm.invoke("Say hello")
        
        assert response is not None
        assert hasattr(response, 'content')
        assert len(response.content) > 0
