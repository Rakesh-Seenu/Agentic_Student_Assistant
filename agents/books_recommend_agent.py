
import os
import sys
import json
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.base_agent import BaseAgent
from utils.config_loader import get_config, get_prompt
from utils.book_search_tools import OpenLibrarySearch, GoogleBooksSearch, normalize_books


class BooksRecommendAgent(BaseAgent):
    """
    Agent for recommending academic books using multi-source search.
    """
    
    def __init__(self):
        """Initialize books recommendation agent."""
        config = get_config()
        super().__init__(config, agent_name="books") # Reusing 'books' config namespace for now
        self.recommendation_prompt = get_prompt("books_recommendation_academic")
        self.ol_search = OpenLibrarySearch()
        self.gb_search = GoogleBooksSearch()
    
    def process(self, query: str, **kwargs) -> str:
        """
        Process book recommendation query.
        
        Args:
            query: User query for books
            
        Returns:
            Academic book recommendations
        """
        # print(f"📚 Searching for books: {query}")
        
        # 1. Search Open Library (Primary - Academic)
        ol_results = self.ol_search.search(query, limit=3)
        
        # 2. Search Google Books (Secondary - Enrichment)
        gb_results = self.gb_search.search(query, limit=3)
        
        # 3. Merge and Normalize
        merged_books = normalize_books(ol_results, gb_results)
        
        if not merged_books:
            return f"⚠️ I couldn't find any academic books matching '{query}'. Try broader terms."
        
        # 4. LLM Ranking & Recommendation
        prompt = self.recommendation_prompt.format(
            query=query,
            books_data=json.dumps(merged_books, indent=2)
        )
        
        response = self.llm.invoke(prompt)
        return response.content

if __name__ == "__main__":
    load_dotenv()
    agent = BooksRecommendAgent()
    query = input(" Enter book topic: ")
    print(agent.process(query))
