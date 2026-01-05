"""
Books agent for searching and recommending learning resources.
Refactored to inherit from BaseAgent and use config-based architecture.
"""
import os
import sys
from dotenv import load_dotenv
import streamlit as st

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.base_agent import BaseAgent
from utils.config_loader import get_config, get_prompt
from utils.google_search import GoogleSearch

load_dotenv()


class BooksAgent(BaseAgent):
    """
    Agent for searching and recommending books and learning resources.
    Uses web search (Goodreads) and GPT for recommendations.
    """
    
    def __init__(self):
        """Initialize books agent."""
        config = get_config()
        super().__init__(config, agent_name="books")
        self.recommendation_prompt = get_prompt("books_recommendation")
    
    def search_books(self, query: str) -> list:
        """
        Search for books using SerpAPI (Goodreads).
        
        Args:
            query: Book search query
            
        Returns:
            List of book suggestions
        """
        params = {
            "engine": "google",
            "q": f"{query} site:goodreads.com",
            "api_key": os.getenv("SERPAPI_API_KEY") or st.secrets.get("SERPAPI_API_KEY")
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        books = results.get("organic_results", [])
        if not books:
            return []
        
        suggestions = []
        for book in books[:5]:
            title = book.get("title", "No title")
            snippet = book.get("snippet", "")
            link = book.get("link", "")
            suggestions.append(f"{title}\n{snippet}\n{link}")
        
        return suggestions
    
    def summarize_books(self, book_list: list) -> str:
        """
        Summarize and recommend books using GPT.
        
        Args:
            book_list: List of book data
            
        Returns:
            Formatted recommendations
        """
        if not book_list:
            return "❌ No relevant books found."
        
        prompt = f"{self.recommendation_prompt}\n\n{book_list}"
        response = self.llm.invoke(prompt)
        return response.content
    
    def process(self, query: str, **kwargs) -> str:
        """
        Process book recommendation query.
        
        Args:
            query: Book search query
            **kwargs: Additional parameters
            
        Returns:
            Book recommendations
        """
        results = self.search_books(query)
        return self.summarize_books(results)


# Legacy function for backward compatibility
def run_books_agent(query: str) -> str:
    """Legacy entry point."""
    agent = BooksAgent()
    return agent.process(query)


if __name__ == "__main__":
    agent = BooksAgent()
    
    serp_key = os.getenv("SERPAPI_API_KEY") or st.secrets.get("SERPAPI_API_KEY")
    if not serp_key:
        print("❌ SERPAPI_API_KEY not found in environment.")
    else:
        print("📚 Books Agent — type your query.")
        
        while True:
            try:
                query = input("\n🔎 Query: ").strip()
                if query.lower() == "exit" or query == "":
                    print("👋 Bye!")
                    break
                
                answer = agent.process(query)
                print("\n✅ Suggestions:\n")
                print(answer)
                print("\n" + "-" * 60)
            except KeyboardInterrupt:
                print("\n👋 Bye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")
