"""
Integration tests for talk2jobs.tools.google_search module.
No mocks - tests real Google Search functionality.
"""
import pytest
import os
from agentic_student_assistant.talk2jobs.tools.google_search import GoogleSearch


class TestGoogleSearch:
    """Integration tests for Google Search tool."""
    
    def test_google_search_initialization(self):
        """Test Google Search initializes correctly."""
        search = GoogleSearch()
        assert search is not None
    
    @pytest.mark.integration
    def test_search_jobs_basic(self):
        """Test basic job search."""
        search = GoogleSearch()
        results = search.search_jobs("software engineer", location="Berlin")
        
        assert isinstance(results, list)
        # Results may be empty if API key not configured, but should not error
    
    @pytest.mark.integration
    def test_search_jobs_with_field(self):
        """Test job search with specific field."""
        search = GoogleSearch()
        results = search.search_jobs("AI engineer", location="London")
        
        assert isinstance(results, list)
    
    @pytest.mark.integration
    def test_search_jobs_no_location(self):
        """Test job search without location."""
        search = GoogleSearch()
        results = search.search_jobs("data scientist")
        
        assert isinstance(results, list)
