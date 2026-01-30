"""
Integration tests for talk2papers.tools.openreview_tool module.
No mocks - tests real OpenReview API.
"""
import pytest
from agentic_student_assistant.talk2papers.tools.openreview_tool import OpenReviewSearch


class TestOpenReviewSearch:
    """Integration tests for OpenReview search."""
    
    def test_initialization(self):
        """Test OpenReview search initialization."""
        search = OpenReviewSearch()
        
        assert search is not None
    
    @pytest.mark.integration
    def test_search_basic(self):
        """Test basic paper search."""
        search = OpenReviewSearch()
        
        results = search.search("deep learning", limit=3)
        
        assert isinstance(results, list)
        assert len(results) <= 3
    
    @pytest.mark.integration
    def test_search_conference_papers(self):
        """Test searching for conference papers."""
        search = OpenReviewSearch()
        
        results = search.search("NeurIPS", limit=2)
        
        assert isinstance(results, list)
