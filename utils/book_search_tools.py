import requests
import os
import streamlit as st
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


def normalize_books(openlib_results: List[Dict], google_results: List[Dict]) -> List[Dict]:
    """
    Merge and deduplicate book results based on title.
    """
    seen_titles = set()
    merged = []

    # Prioritize OpenLibrary (Academic) then Google Books
    for book in openlib_results + google_results:
        title = book.get("title", "")
        if not title:
            continue
            
        # Create a normalized component for deduping
        title_key = title.lower().strip()
        
        # Simple fuzzy check (exact match on normalized title)
        if title_key in seen_titles:
            continue
            
        seen_titles.add(title_key)
        merged.append(book)

    return merged
