
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


class CoreSearch:
    """
    Search client for CORE API (Open Access).
    """
    BASE_URL = "https://api.core.ac.uk/v3/search/works"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search CORE API.
        """
        api_key = os.getenv("CORE_API_KEY")
        if not api_key:
            # CORE usually requires an API key for search
            print("⚠️ CORE API key missing. Skipping CORE search.")
            return []

        headers = {"Authorization": f"Bearer {api_key}"}
        params = {
            "q": query,
            "limit": limit
        }

        try:
            resp = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            papers = []
            for item in data.get("results", []):
                authors = [a.get("name") for a in item.get("authors", [])]
                papers.append({
                    "title": item.get("title"),
                    "authors": authors,
                    "year": item.get("yearPublished"),
                    "abstract": item.get("abstract"),
                    "link": item.get("downloadUrl") or item.get("fullTextIdentifier"),
                    "source": "core",
                    "publisher": item.get("publisher")
                })
            return papers
        except requests.exceptions.Timeout:
            print("⚠️ CORE API: Search timed out.")
            return [{"error": "timeout", "message": "CORE search timed out."}]
        except Exception as e:
            print(f"⚠️ CORE API Error: {e}")
            return []


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


class ArXivSearch:
    """
    Search client for ArXiv API (CS and AI focused).
    """
    BASE_URL = "http://export.arxiv.org/api/query"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search ArXiv for papers.
        """
        import xml.etree.ElementTree as ET
        
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }

        try:
            resp = requests.get(self.V2_URL if hasattr(self, 'V2_URL') else self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            
            # ArXiv returns XML (Atom feed)
            root = ET.fromstring(resp.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            papers = []
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                year = entry.find('atom:published', ns).text[:4]
                link = entry.find('atom:id', ns).text
                
                authors_found = entry.findall('atom:author', ns)
                authors = [a.find('atom:name', ns).text for a in authors_found]
                
                papers.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "abstract": abstract,
                    "link": link,
                    "source": "arxiv"
                })
            return papers
        except Exception as e:
            print(f"⚠️ ArXiv Search Error: {e}")
            return []


def normalize_papers(*source_lists: List[Dict]) -> List[Dict]:
    """
    Merge and deduplicate paper results based on title from multiple sources.
    """
    seen_titles = set()
    merged = []

    for source_list in source_lists:
        if not source_list:
            continue
        for paper in source_list:
            if not isinstance(paper, dict) or "title" not in paper:
                continue
            
            title = paper.get("title", "")
            if not title:
                continue
                
            title_key = title.lower().strip()
            # Basic cleanup for matching
            title_key = "".join(e for e in title_key if e.isalnum())
            
            if title_key in seen_titles:
                continue
                
            seen_titles.add(title_key)
            merged.append(paper)

    return merged
