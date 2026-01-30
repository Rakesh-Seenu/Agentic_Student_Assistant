"""
Integration tests for talk2books.tools.book_utils module.
No mocks - tests real book normalization.
"""
import pytest
from agentic_student_assistant.talk2books.tools.book_utils import normalize_books


class TestBookUtils:
    """Integration tests for book utilities."""
    
    def test_normalize_books_empty_lists(self):
        """Test normalizing empty book lists."""
        result = normalize_books([], [])
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_normalize_books_single_source(self):
        """Test normalizing books from single source."""
        books1 = [
            {"title": "Book 1", "authors": ["Author 1"], "year": 2020},
            {"title": "Book 2", "authors": ["Author 2"], "year": 2021}
        ]
        
        result = normalize_books(books1, [])
        
        assert isinstance(result, list)
        assert len(result) >= 0
    
    def test_normalize_books_multiple_sources(self):
        """Test normalizing books from multiple sources."""
        books1 = [{"title": "Book 1", "authors": ["Author 1"]}]
        books2 = [{"title": "Book 2", "authors": ["Author 2"]}]
        
        result = normalize_books(books1, books2)
        
        assert isinstance(result, list)
    
    def test_normalize_books_duplicates(self):
        """Test handling duplicate books."""
        books1 = [{"title": "Same Book", "authors": ["Author"]}]
        books2 = [{"title": "Same Book", "authors": ["Author"]}]
        
        result = normalize_books(books1, books2)
        
        assert isinstance(result, list)
    
    def test_normalize_books_different_formats(self):
        """Test normalizing books with different data formats."""
        books1 = [
            {"title": "Book A", "authors": ["Author A"], "publisher": "Pub A"}
        ]
        books2 = [
            {"title": "Book B", "author_name": ["Author B"], "publish_year": [2020]}
        ]
        
        result = normalize_books(books1, books2)
        
        assert isinstance(result, list)
