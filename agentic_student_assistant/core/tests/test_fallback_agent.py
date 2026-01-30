"""
Integration tests for core.base.fallback_agent module.
"""
import pytest
from agentic_student_assistant.core.base.fallback_agent import FallbackAgent


class TestFallbackAgent:
    def test_fallback_agent_initialization(self):
        """Test fallback agent initializes correctly."""
        agent = FallbackAgent()
        
        assert agent.agent_name == "fallback"
        assert agent.llm is not None
    
    def test_fallback_agent_process(self):
        """Test fallback agent processes queries."""
        agent = FallbackAgent()
        
        result = agent.process("What is the weather?")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_fallback_agent_empty_query(self):
        """Test fallback agent handles empty queries."""
        agent = FallbackAgent()
        
        result = agent.process("")
        
        assert isinstance(result, str)
    
    def test_fallback_agent_with_kwargs(self):
        """Test fallback agent accepts kwargs."""
        agent = FallbackAgent()
        
        result = agent.process("test", extra="param")
        
        assert isinstance(result, str)
