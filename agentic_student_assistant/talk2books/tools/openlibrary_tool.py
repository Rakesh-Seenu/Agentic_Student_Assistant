"""
Open Library API search tool for academic books.
"""
import requests
from typing import List, Dict, Any


class OpenLibrarySearch:
    """
    Search client for Open Library API (Academic focus).
    """
    BASE_URL = "https://openlibrary.org/search.json"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search Open Library for books.
        """
        params = {
            "q": query,
            "language": "eng",
            "has_fulltext": "true",  # String "true" often works better with some APIs
            "limit": limit
        }

        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            books = []
            for doc in data.get("docs", [])[:limit]:
                books.append({
                    "title": doc.get("title"),
                    "authors": doc.get("author_name", []),
                    "year": doc.get("first_publish_year"),
                    "subjects": doc.get("subject", [])[:6],
                    "publisher": doc.get("publisher", [])[:3] if doc.get("publisher") else [],
                    "edition_count": doc.get("edition_count", 0),
                    "source": "openlibrary",
                    "link": f"https://openlibrary.org{doc.get('key')}" if doc.get('key') else ""
                })
            return books
        except Exception as e:
            print(f"⚠️ OpenLibrary Error: {e}")
            return []
