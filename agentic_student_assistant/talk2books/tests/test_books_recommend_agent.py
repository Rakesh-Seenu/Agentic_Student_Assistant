"""
Integration tests for talk2books.agents.books_recommend_agent module.
"""
import pytest
from agentic_student_assistant.talk2books.agents.books_recommend_agent import BooksRecommendAgent


class TestBooksRecommendAgent:
    def test_agent_initialization(self):
        """Test books agent initializes correctly."""
        agent = BooksRecommendAgent()
        
        assert agent.agent_name == "books"
        assert agent.llm is not None
        assert agent.ol_search is not None
        assert agent.gb_search is not None
    
    @pytest.mark.integration
    def test_process_book_query(self):
        """Test processing a book recommendation query."""
        agent = BooksRecommendAgent()
        
        result = agent.process("Recommend books on machine learning")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.integration
    def test_process_specific_topic(self):
        """Test processing query for specific topic."""
        agent = BooksRecommendAgent()
        
        result = agent.process("Find books on Python programming")
        
        assert isinstance(result, str)
        # Should contain book-related content
        assert len(result) > 50
    
    @pytest.mark.integration
    def test_process_empty_results(self):
        """Test handling when no books are found."""
        agent = BooksRecommendAgent()
        
        result = agent.process("xyzabc123nonexistent")
        
        assert isinstance(result, str)
