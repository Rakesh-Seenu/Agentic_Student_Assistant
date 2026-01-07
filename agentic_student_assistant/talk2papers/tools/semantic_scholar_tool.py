"""
Semantic Scholar API search tool for academic papers.
"""
import requests
import os
from typing import List, Dict, Any


class SemanticScholarSearch:
    """
    Search client for Semantic Scholar API.
    """
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search Semantic Scholar for papers.
        """
        api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        headers = {}
        if api_key:
            headers["x-api-key"] = api_key

        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,abstract,venue,url,citationCount,isOpenAccess"
        }

        try:
            resp = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            if resp.status_code == 429:
                print("⚠️ Semantic Scholar: Rate limit exceeded (429).")
                return [{"error": "rate_limit", "message": "Semantic Scholar API rate limit reached. Please wait a minute."}]
            
            if resp.status_code == 403:
                print("⚠️ Semantic Scholar: Access Forbidden (403). Possible IP block or invalid parameters.")
                return [{"error": "forbidden", "message": "Semantic Scholar access forbidden. Try using a different query or wait a few minutes."}]

            resp.raise_for_status()
            data = resp.json()

            papers = []
            for item in data.get("data", []):
                authors = [a.get("name") for a in item.get("authors", [])]
                papers.append({
                    "title": item.get("title"),
                    "authors": authors,
                    "year": item.get("year"),
                    "abstract": item.get("abstract"),
                    "venue": item.get("venue"),
                    "citation_count": item.get("citationCount"),
                    "is_open_access": item.get("isOpenAccess"),
                    "source": "semantic_scholar",
                    "link": item.get("url")
                })
            return papers
        except requests.exceptions.Timeout:
            print("⚠️ Semantic Scholar: Search timed out.")
            return [{"error": "timeout", "message": "Semantic Scholar search timed out."}]
        except Exception as e:
            print(f"⚠️ Semantic Scholar Error: {e}")
            return []
