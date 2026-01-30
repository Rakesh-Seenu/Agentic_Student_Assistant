"""
Comprehensive integration tests for core.base.base_agent module.
100% coverage target - no mocks.
"""
import pytest
from omegaconf import OmegaConf, DictConfig
from agentic_student_assistant.core.base.base_agent import BaseAgent
from agentic_student_assistant.core.utils.config_loader import get_config


class DummyLLM:
    """Dummy LLM for testing without API keys."""
    def __init__(self, model_name="dummy", temperature=0.0):
        self.model_name = model_name
        self.temperature = temperature
        
    def invoke(self, query):
        return type('obj', (object,), {'content': f"Dummy response to: {query}"})


class ConcreteTestAgent(BaseAgent):
    """Concrete implementation for testing."""
    def process(self, query: str, **kwargs) -> str:
        return f"Processed: {query}"


class TestBaseAgentComprehensive:
    """Comprehensive tests for BaseAgent - 100% coverage."""
    
    def test_init_with_config_and_name(self):
        """Test initialization with config and custom name."""
        config = get_config()
        # Inject dummy LLM to avoid API key requirements
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, agent_name="custom_agent", llm=dummy)
        
        assert agent.config == config
        assert agent.agent_name == "custom_agent"
        assert agent.llm is dummy
    
    def test_init_with_default_name(self):
        """Test initialization with default agent name."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        assert agent.agent_name == "base"
    
    def test_init_llm_creation_real(self):
        """Test that LLM is created during initialization (real path)."""
        # This might fail if no keys are present, so we handle expected error
        config = get_config()
        try:
            agent = ConcreteTestAgent(config, agent_name="test")
            assert agent.llm is not None
        except ValueError as e:
            # Expected if no keys
            assert "No valid API key found" in str(e)
    
    def test_process_basic_query(self):
        """Test process method with basic query."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        result = agent.process("test query")
        
        assert result == "Processed: test query"
    
    def test_process_empty_query(self):
        """Test process method with empty query."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        result = agent.process("")
        
        assert result == "Processed: "
    
    def test_process_with_kwargs(self):
        """Test process method with additional kwargs."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        result = agent.process("query", param1="value1", param2="value2")
        
        assert result == "Processed: query"
    
    def test_process_long_query(self):
        """Test process method with long query."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        long_query = "a" * 1000
        result = agent.process(long_query)
        
        assert result == f"Processed: {long_query}"
    
    def test_process_special_characters(self):
        """Test process method with special characters."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        special_query = "query with !@#$%^&*() special chars"
        result = agent.process(special_query)
        
        assert result == f"Processed: {special_query}"
    
    def test_get_metadata_complete(self):
        """Test get_metadata returns all required fields."""
        config = get_config()
        dummy = DummyLLM(model_name="test-model", temperature=0.5)
        agent = ConcreteTestAgent(config, agent_name="metadata_test", llm=dummy)
        
        metadata = agent.get_metadata()
        
        assert 'agent_name' in metadata
        assert 'model' in metadata
        assert 'temperature' in metadata
        assert metadata['agent_name'] == "metadata_test"
        assert metadata['model'] == "test-model"
        assert metadata['temperature'] == 0.5
    
    def test_repr_format(self):
        """Test __repr__ returns correct format."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, agent_name="repr_test", llm=dummy)
        
        repr_str = repr(agent)
        
        assert "ConcreteTestAgent" in repr_str
        assert "repr_test" in repr_str
        assert "name=" in repr_str
    
    def test_repr_different_names(self):
        """Test __repr__ with different agent names."""
        config = get_config()
        dummy = DummyLLM()
        
        agent1 = ConcreteTestAgent(config, agent_name="agent1", llm=dummy)
        agent2 = ConcreteTestAgent(config, agent_name="agent2", llm=dummy)
        
        assert "agent1" in repr(agent1)
        assert "agent2" in repr(agent2)
        assert repr(agent1) != repr(agent2)
    
    def test_abstract_class_cannot_instantiate(self):
        """Test that BaseAgent cannot be instantiated directly."""
        config = get_config()
        
        with pytest.raises(TypeError):
            BaseAgent(config)
    
    def test_config_attribute_accessible(self):
        """Test that config attribute is accessible."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        assert agent.config is not None
        assert hasattr(agent.config, 'models')
    
    def test_llm_attribute_accessible(self):
        """Test that llm attribute is accessible."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        assert agent.llm is not None
        assert agent.llm is dummy
    
    def test_agent_name_attribute(self):
        """Test agent_name attribute."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, agent_name="test_name", llm=dummy)
        
        assert agent.agent_name == "test_name"
        assert isinstance(agent.agent_name, str)
    
    def test_multiple_agents_independent(self):
        """Test that multiple agent instances are independent."""
        config = get_config()
        dummy = DummyLLM()
        
        agent1 = ConcreteTestAgent(config, agent_name="agent1", llm=dummy)
        agent2 = ConcreteTestAgent(config, agent_name="agent2", llm=dummy)
        
        assert agent1.agent_name != agent2.agent_name
        assert agent1 is not agent2
    
    def test_process_unicode_query(self):
        """Test process with unicode characters."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        unicode_query = "Hello 世界 🌍"
        result = agent.process(unicode_query)
        
        assert result == f"Processed: {unicode_query}"
    
    def test_process_multiline_query(self):
        """Test process with multiline query."""
        config = get_config()
        dummy = DummyLLM()
        agent = ConcreteTestAgent(config, llm=dummy)
        
        multiline_query = "line1\nline2\nline3"
        result = agent.process(multiline_query)
        
        assert result == f"Processed: {multiline_query}"
    
    def test_main_block(self):
        """Test the main block using runpy or similar mechanisms if possible, 
           or just rely on the fact that this test file imports the module."""
        # Testing if __name__ == "__main__" block usually requires invoking the script
        # via subprocess or runpy.
        import runpy
        # This will execute the main block
        try:
           runpy.run_module("agentic_student_assistant.core.base.base_agent", run_name="__main__")
        except ValueError:
            # Expected if keys are missing in the main block execution
            pass
