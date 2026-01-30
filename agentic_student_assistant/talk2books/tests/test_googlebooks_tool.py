"""
Integration tests for talk2books.tools.googlebooks_tool module.
No mocks - tests real Google Books API.
"""
import pytest
from agentic_student_assistant.talk2books.tools.googlebooks_tool import GoogleBooksSearch


class TestGoogleBooksSearch:
    """Integration tests for Google Books search."""
    
    def test_initialization(self):
        """Test Google Books search initialization."""
        search = GoogleBooksSearch()
        
        assert search is not None
    
    @pytest.mark.integration
    def test_search_basic(self):
        """Test basic book search."""
        search = GoogleBooksSearch()
        
        results = search.search("Python programming", limit=3)
        
        assert isinstance(results, list)
        assert len(results) <= 3
    
    @pytest.mark.integration
    def test_search_with_limit(self):
        """Test search with different limits."""
        search = GoogleBooksSearch()
        
        results = search.search("machine learning", limit=1)
        
        assert isinstance(results, list)
        assert len(results) <= 1
    
    @pytest.mark.integration
    def test_search_specific_topic(self):
        """Test searching for specific topic."""
        search = GoogleBooksSearch()
        
        results = search.search("artificial intelligence", limit=5)
        
        assert isinstance(results, list)
        assert len(results) <= 5
    
    @pytest.mark.integration
    def test_search_empty_query(self):
        """Test search with empty query."""
        search = GoogleBooksSearch()
        
        results = search.search("", limit=1)
        
        assert isinstance(results, list)
