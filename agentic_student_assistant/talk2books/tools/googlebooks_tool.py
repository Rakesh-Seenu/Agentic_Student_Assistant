"""
Google Books API search tool for book enrichment and fallback.
"""
import requests
import os
from typing import List, Dict, Any


class GoogleBooksSearch:
    """
    Search client for Google Books API (Enrichment & Fallback).
    """
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search Google Books API.
        """
        api_key = os.getenv("GOOGLE_BOOKS_API_KEY") # Optional, works without key for public data often
        
        params = {
            "q": query,
            "printType": "books",
            "langRestrict": "en",
            "maxResults": limit
        }
        if api_key:
            params["key"] = api_key

        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            books = []
            for item in data.get("items", []):
                info = item.get("volumeInfo", {})
                books.append({
                    "title": info.get("title"),
                    "authors": info.get("authors", []),
                    "publisher": info.get("publisher"),
                    "year": info.get("publishedDate")[:4] if info.get("publishedDate") else None,
                    "categories": info.get("categories", []),
                    "page_count": info.get("pageCount"),
                    "source": "google_books",
                    "link": info.get("infoLink", "")
                })
            return books
        except Exception as e:
            print(f"⚠️ Google Books Error: {e}")
            return []
