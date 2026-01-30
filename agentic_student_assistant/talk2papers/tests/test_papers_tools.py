"""
Integration tests for talk2papers tools.
"""
import pytest
from agentic_student_assistant.talk2papers.tools.arxiv_tool import ArXivSearch
from agentic_student_assistant.talk2papers.tools.semantic_scholar_tool import SemanticScholarSearch
from agentic_student_assistant.talk2papers.tools.paper_utils import normalize_papers


class TestArXivSearch:
    @pytest.mark.integration
    def test_search_papers(self):
        """Test searching ArXiv for papers."""
        search = ArXivSearch()
        
        results = search.search("machine learning", limit=3)
        
        assert isinstance(results, list)
        assert len(results) <= 3


class TestSemanticScholarSearch:
    @pytest.mark.integration
    def test_search_papers(self):
        """Test searching Semantic Scholar."""
        search = SemanticScholarSearch()
        
        results = search.search("deep learning", limit=3)
        
        assert isinstance(results, list)
        assert len(results) <= 3


class TestPaperUtils:
    def test_normalize_papers(self):
        """Test paper normalization."""
        papers1 = [{"title": "Paper 1", "authors": ["Author 1"]}]
        papers2 = [{"title": "Paper 2", "authors": ["Author 2"]}]
        
        normalized = normalize_papers(papers1, papers2)
        
        assert isinstance(normalized, list)
