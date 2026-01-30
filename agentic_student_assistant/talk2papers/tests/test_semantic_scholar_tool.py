"""
Integration tests for talk2papers.tools.semantic_scholar_tool module.
No mocks - tests real Semantic Scholar API.
"""
import pytest
from agentic_student_assistant.talk2papers.tools.semantic_scholar_tool import SemanticScholarSearch


class TestSemanticScholarSearch:
    """Integration tests for Semantic Scholar search."""
    
    def test_initialization(self):
        """Test Semantic Scholar search initialization."""
        search = SemanticScholarSearch()
        
        assert search is not None
    
    @pytest.mark.integration
    def test_search_basic(self):
        """Test basic paper search."""
        search = SemanticScholarSearch()
        
        results = search.search("neural networks", limit=3)
        
        assert isinstance(results, list)
        assert len(results) <= 3
    
    @pytest.mark.integration
    def test_search_with_limit(self):
        """Test search with limit."""
        search = SemanticScholarSearch()
        
        results = search.search("AI", limit=2)
        
        assert isinstance(results, list)
        assert len(results) <= 2
    
    @pytest.mark.integration
    def test_search_specific_field(self):
        """Test searching in specific field."""
        search = SemanticScholarSearch()
        
        results = search.search("computer vision", limit=5)
        
        assert isinstance(results, list)
