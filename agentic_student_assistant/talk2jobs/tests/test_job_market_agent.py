"""
Integration tests for talk2jobs.agents.job_market_agent module.
"""
import pytest
from agentic_student_assistant.talk2jobs.agents.job_market_agent import JobMarketAgent


class TestJobMarketAgent:
    def test_agent_initialization(self):
        """Test job market agent initializes correctly."""
        agent = JobMarketAgent()
        
        assert agent.agent_name == "job_market"
        assert agent.llm is not None
    
    def test_extract_location(self):
        """Test location extraction from queries."""
        agent = JobMarketAgent()
        
        query, location = agent._extract_location("Find jobs in Berlin")
        
        assert location == "Berlin"
        assert "Berlin" not in query or query == "Find jobs in Berlin"
    
    def test_extract_field(self):
        """Test field extraction from queries."""
        agent = JobMarketAgent()
        
        field = agent._extract_field_from_query("Find AI engineer jobs")
        
        assert isinstance(field, str)
    
    @pytest.mark.integration
    def test_process_job_query(self):
        """Test processing a job search query."""
        agent = JobMarketAgent()
        
        result = agent.process("Find AI jobs in Berlin")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.integration
    def test_process_with_location(self):
        """Test job search with specific location."""
        agent = JobMarketAgent()
        
        result = agent.process("Software engineer jobs in London")
        
        assert isinstance(result, str)
