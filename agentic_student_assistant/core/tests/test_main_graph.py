"""
Integration tests for core.orchestration.main_graph module.
No mocks - tests real graph functionality.
"""
import pytest
from agentic_student_assistant.core.orchestration.main_graph import MainGraph


class TestMainGraph:
    """Integration tests for MainGraph."""
    
    def test_main_graph_initialization(self):
        """Test main graph initializes correctly."""
        graph = MainGraph()
        
        assert graph is not None
        assert graph.graph_builder is not None
        assert graph.graph is not None
    
    @pytest.mark.integration
    def test_run_simple_query(self):
        """Test running a simple query through the graph."""
        graph = MainGraph()
        
        result = graph.run("Find books on Python")
        
        assert isinstance(result, dict)
        assert 'response' in result or 'error' in result
    
    @pytest.mark.integration
    def test_run_job_query(self):
        """Test running a job query."""
        graph = MainGraph()
        
        result = graph.run("Find AI jobs")
        
        assert isinstance(result, dict)
    
    @pytest.mark.integration
    def test_run_paper_query(self):
        """Test running a paper query."""
        graph = MainGraph()
        
        result = graph.run("Find papers on transformers")
        
        assert isinstance(result, dict)
    
    @pytest.mark.integration
    def test_run_complex_query(self):
        """Test running a complex multi-domain query."""
        graph = MainGraph()
        
        result = graph.run("Find jobs and books on AI")
        
        assert isinstance(result, dict)
    
    @pytest.mark.integration
    def test_run_empty_query(self):
        """Test running an empty query."""
        graph = MainGraph()
        
        result = graph.run("")
        
        assert isinstance(result, dict)
