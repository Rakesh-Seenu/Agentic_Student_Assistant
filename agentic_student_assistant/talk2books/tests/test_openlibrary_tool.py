"""
Integration tests for talk2books.tools.openlibrary_tool module.
No mocks - tests real OpenLibrary API.
"""
import pytest
from agentic_student_assistant.talk2books.tools.openlibrary_tool import OpenLibrarySearch


class TestOpenLibrarySearch:
    """Integration tests for OpenLibrary search."""
    
    def test_initialization(self):
        """Test OpenLibrary search initialization."""
        search = OpenLibrarySearch()
        
        assert search is not None
    
    @pytest.mark.integration
    def test_search_basic(self):
        """Test basic book search."""
        search = OpenLibrarySearch()
        
        results = search.search("Python", limit=3)
        
        assert isinstance(results, list)
        assert len(results) <= 3
    
    @pytest.mark.integration
    def test_search_with_limit(self):
        """Test search with different limits."""
        search = OpenLibrarySearch()
        
        results = search.search("programming", limit=2)
        
        assert isinstance(results, list)
        assert len(results) <= 2
    
    @pytest.mark.integration
    def test_search_academic(self):
        """Test searching for academic books."""
        search = OpenLibrarySearch()
        
        results = search.search("computer science", limit=5)
        
        assert isinstance(results, list)
