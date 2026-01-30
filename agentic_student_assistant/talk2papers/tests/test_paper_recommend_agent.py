"""
Integration tests for talk2papers.agents.paper_recommend_agent module.
"""
import pytest
from agentic_student_assistant.talk2papers.agents.paper_recommend_agent import PaperRecommendAgent


class TestPaperRecommendAgent:
    def test_agent_initialization(self):
        """Test paper agent initializes correctly."""
        agent = PaperRecommendAgent()
        
        assert agent.agent_name == "papers"
        assert agent.llm is not None
    
    def test_refine_query(self):
        """Test query refinement."""
        agent = PaperRecommendAgent()
        
        refined = agent._refine_query("tell me about transformer papers")
        
        assert isinstance(refined, str)
        assert len(refined) > 0
    
    def test_is_selection_query(self):
        """Test selection query detection."""
        agent = PaperRecommendAgent()
        
        assert agent._is_selection_query("tell me more about paper 1")
        assert agent._is_selection_query("explain the first one")
        assert not agent._is_selection_query("find papers on AI")
    
    @pytest.mark.integration
    def test_process_paper_query(self):
        """Test processing a paper search query."""
        agent = PaperRecommendAgent()
        
        result = agent.process("Find papers on transformers")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.integration
    def test_process_specific_topic(self):
        """Test searching for specific research topic."""
        agent = PaperRecommendAgent()
        
        result = agent.process("Recent papers on large language models")
        
        assert isinstance(result, str)
