"""
Integration tests for talk2papers.tools.core_tool module.
No mocks - tests real CORE API.
"""
import pytest
from agentic_student_assistant.talk2papers.tools.core_tool import CORESearch


class TestCORESearch:
    """Integration tests for CORE search."""
    
    def test_initialization(self):
        """Test CORE search initialization."""
        search = CORESearch()
        
        assert search is not None
    
    @pytest.mark.integration
    def test_search_basic(self):
        """Test basic paper search."""
        search = CORESearch()
        
        results = search.search("machine learning", limit=3)
        
        assert isinstance(results, list)
        assert len(results) <= 3
    
    @pytest.mark.integration
    def test_search_with_limit(self):
        """Test search with limit."""
        search = CORESearch()
        
        results = search.search("artificial intelligence", limit=2)
        
        assert isinstance(results, list)
