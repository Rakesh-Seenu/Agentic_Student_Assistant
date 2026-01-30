"""
Integration tests for core.orchestration.orchestrator_agent module.
No mocks - tests real orchestrator functionality.
"""
import pytest
from agentic_student_assistant.core.orchestration.orchestrator_agent import OrchestratorAgent


class TestOrchestratorAgent:
    """Integration tests for OrchestratorAgent."""
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initializes correctly."""
        agent = OrchestratorAgent()
        
        assert agent is not None
        assert agent.llm is not None
        assert agent.config is not None
    
    @pytest.mark.integration
    def test_create_plan(self):
        """Test creating a plan from query."""
        agent = OrchestratorAgent()
        
        plan = agent.create_plan("Find AI jobs and machine learning books")
        
        assert isinstance(plan, list)
        # Plan may be empty or have steps depending on LLM response
    
    @pytest.mark.integration
    def test_create_plan_simple_query(self):
        """Test creating plan for simple query."""
        agent = OrchestratorAgent()
        
        plan = agent.create_plan("Find books")
        
        assert isinstance(plan, list)
    
    @pytest.mark.integration
    def test_synthesize_response(self):
        """Test synthesizing response from results."""
        agent = OrchestratorAgent()
        
        results = {
            "job_market": "Found 5 AI jobs in Berlin",
            "books": "Found 3 books on machine learning"
        }
        
        response = agent.synthesize_response("Find jobs and books", results)
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    @pytest.mark.integration
    def test_synthesize_empty_results(self):
        """Test synthesizing with empty results."""
        agent = OrchestratorAgent()
        
        response = agent.synthesize_response("test query", {})
        
        assert isinstance(response, str)
