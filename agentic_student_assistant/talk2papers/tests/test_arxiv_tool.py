"""
Integration tests for talk2papers.tools.arxiv_tool module.
No mocks - tests real ArXiv API.
"""
import pytest
from agentic_student_assistant.talk2papers.tools.arxiv_tool import ArXivSearch


class TestArXivSearch:
    """Integration tests for ArXiv search."""
    
    def test_initialization(self):
        """Test ArXiv search initialization."""
        search = ArXivSearch()
        
        assert search is not None
    
    @pytest.mark.integration
    def test_search_basic(self):
        """Test basic paper search."""
        search = ArXivSearch()
        
        results = search.search("machine learning", limit=3)
        
        assert isinstance(results, list)
        assert len(results) <= 3
    
    @pytest.mark.integration
    def test_search_specific_topic(self):
        """Test searching for specific research topic."""
        search = ArXivSearch()
        
        results = search.search("transformers", limit=2)
        
        assert isinstance(results, list)
        assert len(results) <= 2
    
    @pytest.mark.integration
    def test_search_with_limit(self):
        """Test search respects limit parameter."""
        search = ArXivSearch()
        
        results = search.search("deep learning", limit=1)
        
        assert isinstance(results, list)
        assert len(results) <= 1
