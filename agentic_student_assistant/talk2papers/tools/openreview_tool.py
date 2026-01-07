"""
OpenReview API search tool for conference papers (ICLR, NeurIPS, etc.).
"""
import requests
from typing import List, Dict, Any


class OpenReviewSearch:
    """
    Search client for OpenReview API (ICLR, NeurIPS, etc.).
    Uses API v2 primary and API v1 as fallback.
    """
    V2_URL = "https://api2.openreview.net/notes/search"
    V1_URL = "https://api.openreview.net/notes/search"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search OpenReview for papers.
        """
        papers = []
        
        # Try API v2 (Newer conferences like ICLR 2024+)
        try:
            resp = requests.get(self.V2_URL, params={"term": query, "limit": limit}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("notes", []):
                    content = item.get("content", {})
                    # API v2 has content values nested under 'value' metadata
                    title = content.get("title", {}).get("value")
                    authors = content.get("authors", {}).get("value", [])
                    abstract = content.get("abstract", {}).get("value")
                    pdf = content.get("pdf", {}).get("value")
                    
                    papers.append({
                        "title": title,
                        "authors": authors if isinstance(authors, list) else [authors],
                        "year": item.get("cdate") or item.get("tcdate"), # Use creation date
                        "abstract": abstract,
                        "venue": item.get("invitation", "").split("/")[0], # Rough venue
                        "link": f"https://openreview.net/forum?id={item.get('id')}",
                        "pdf_link": f"https://openreview.net{pdf}" if pdf else None,
                        "source": "openreview_v2"
                    })
        except Exception as e:
            print(f"⚠️ OpenReview V2 Search Error: {e}")

        # If we got results from V2, return them. Otherwise try V1.
        if papers:
            return papers

        # Try API v1 (Older conferences)
        try:
            resp = requests.get(self.V1_URL, params={"term": query, "limit": limit}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("notes", []):
                    content = item.get("content", {})
                    # API v1 has content values directly
                    papers.append({
                        "title": content.get("title"),
                        "authors": content.get("authors", []),
                        "year": item.get("cdate") or item.get("tcdate"),
                        "abstract": content.get("abstract"),
                        "venue": item.get("invitation", "").split("/")[0],
                        "link": f"https://openreview.net/forum?id={item.get('id')}",
                        "source": "openreview_v1"
                    })
        except Exception as e:
            print(f"⚠️ OpenReview V1 Search Error: {e}")

        return papers
