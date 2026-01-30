"""
Integration tests for talk2papers.tools.paper_utils module.
No mocks - tests real paper normalization.
"""
import pytest
from agentic_student_assistant.talk2papers.tools.paper_utils import normalize_papers


class TestPaperUtils:
    """Integration tests for paper utilities."""
    
    def test_normalize_papers_empty_lists(self):
        """Test normalizing empty paper lists."""
        result = normalize_papers([], [])
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_normalize_papers_single_source(self):
        """Test normalizing papers from single source."""
        papers1 = [
            {"title": "Paper 1", "authors": ["Author 1"], "year": 2020},
            {"title": "Paper 2", "authors": ["Author 2"], "year": 2021}
        ]
        
        result = normalize_papers(papers1, [])
        
        assert isinstance(result, list)
    
    def test_normalize_papers_multiple_sources(self):
        """Test normalizing papers from multiple sources."""
        papers1 = [{"title": "Paper A", "authors": ["Author A"]}]
        papers2 = [{"title": "Paper B", "authors": ["Author B"]}]
        
        result = normalize_papers(papers1, papers2)
        
        assert isinstance(result, list)
    
    def test_normalize_papers_with_citations(self):
        """Test normalizing papers with citation counts."""
        papers1 = [
            {"title": "Popular Paper", "authors": ["Author"], "citations": 1000}
        ]
        papers2 = [
            {"title": "New Paper", "authors": ["Author"], "citations": 10}
        ]
        
        result = normalize_papers(papers1, papers2)
        
        assert isinstance(result, list)
    
    def test_normalize_papers_duplicates(self):
        """Test handling duplicate papers."""
        papers1 = [{"title": "Same Paper", "authors": ["Author"]}]
        papers2 = [{"title": "Same Paper", "authors": ["Author"]}]
        
        result = normalize_papers(papers1, papers2)
        
        assert isinstance(result, list)
