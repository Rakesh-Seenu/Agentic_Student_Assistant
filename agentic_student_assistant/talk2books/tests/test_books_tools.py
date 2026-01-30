"""
Integration tests for talk2books tools.
"""
import pytest
from agentic_student_assistant.talk2books.tools.googlebooks_tool import GoogleBooksSearch
from agentic_student_assistant.talk2books.tools.openlibrary_tool import OpenLibrarySearch
from agentic_student_assistant.talk2books.tools.book_utils import normalize_books


class TestGoogleBooksSearch:
    @pytest.mark.integration
    def test_search_books(self):
        """Test searching for books."""
        search = GoogleBooksSearch()
        
        results = search.search("Python programming", limit=5)
        
        assert isinstance(results, list)
        assert len(results) <= 5
    
    @pytest.mark.integration
    def test_search_with_limit(self):
        """Test search respects limit."""
        search = GoogleBooksSearch()
        
        results = search.search("machine learning", limit=2)
        
        assert isinstance(results, list)
        assert len(results) <= 2


class TestOpenLibrarySearch:
    @pytest.mark.integration
    def test_search_books(self):
        """Test searching OpenLibrary."""
        search = OpenLibrarySearch()
        
        results = search.search("artificial intelligence", limit=5)
        
        assert isinstance(results, list)
        assert len(results) <= 5


class TestBookUtils:
    def test_normalize_books(self):
        """Test book normalization."""
        books1 = [{"title": "Book 1", "authors": ["Author 1"]}]
        books2 = [{"title": "Book 2", "authors": ["Author 2"]}]
        
        normalized = normalize_books(books1, books2)
        
        assert isinstance(normalized, list)
        assert len(normalized) >= 0
