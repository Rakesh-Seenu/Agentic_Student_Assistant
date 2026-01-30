"""
Integration tests for core.orchestration.router_agent module.
"""
import pytest
from agentic_student_assistant.core.orchestration.router_agent import (
    RouterAgent,
    RouteDecision,
    get_router,
    route_query
)


class TestRouteDecision:
    def test_valid_route_decision(self):
        """Test creating valid route decisions."""
        decision = RouteDecision(
            agent="job_market",
            confidence=0.95,
            reasoning="Job related query"
        )
        
        assert decision.agent == "job_market"
        assert decision.confidence == 0.95
        assert decision.reasoning == "Job related query"
    
    def test_all_agent_types(self):
        """Test all valid agent types."""
        agents = ["job_market", "books", "papers", "orchestrator", "fallback"]
        
        for agent in agents:
            decision = RouteDecision(agent=agent, confidence=0.8, reasoning="test")
            assert decision.agent == agent


class TestRouterAgent:
    def test_router_initialization(self):
        """Test router initializes correctly."""
        router = RouterAgent()
        
        assert router.llm is not None
        assert router.chain is not None
    
    @pytest.mark.integration
    def test_route_job_query(self):
        """Test routing a job-related query."""
        router = RouterAgent()
        
        decision = router.route("Find AI jobs in Berlin")
        
        assert isinstance(decision, RouteDecision)
        assert decision.agent in ["job_market", "orchestrator", "fallback"]
        assert 0 <= decision.confidence <= 1
    
    @pytest.mark.integration
    def test_route_books_query(self):
        """Test routing a books-related query."""
        router = RouterAgent()
        
        decision = router.route("Recommend books on machine learning")
        
        assert isinstance(decision, RouteDecision)
        assert decision.agent in ["books", "orchestrator", "fallback"]
    
    @pytest.mark.integration
    def test_route_papers_query(self):
        """Test routing a papers-related query."""
        router = RouterAgent()
        
        decision = router.route("Find papers on transformers")
        
        assert isinstance(decision, RouteDecision)
        assert decision.agent in ["papers", "orchestrator", "fallback"]
    
    @pytest.mark.integration
    def test_route_with_orchestration(self):
        """Test routing with orchestration detection."""
        router = RouterAgent()
        
        decision = router.route_with_orchestration(
            "Find papers and books on AI for my job search"
        )
        
        assert isinstance(decision, RouteDecision)
        # Multi-domain query should route to orchestrator
        assert decision.agent in ["orchestrator", "fallback"]


class TestGetRouter:
    def test_singleton_pattern(self):
        """Test that get_router returns singleton."""
        router1 = get_router()
        router2 = get_router()
        
        assert router1 is router2


class TestRouteQuery:
    @pytest.mark.integration
    def test_route_query_basic(self):
        """Test basic query routing."""
        decision = route_query("Find jobs in tech")
        
        assert isinstance(decision, RouteDecision)
        assert decision.agent in ["job_market", "orchestrator", "fallback"]
    
    @pytest.mark.integration
    def test_route_query_with_orchestration(self):
        """Test query routing with orchestration enabled."""
        decision = route_query(
            "Find books and papers on AI",
            enable_orchestration=True
        )
        
        assert isinstance(decision, RouteDecision)
