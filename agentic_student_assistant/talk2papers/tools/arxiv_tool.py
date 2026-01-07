"""
ArXiv API search tool for CS and AI research papers.
"""
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any


class ArXivSearch:
    """
    Search client for ArXiv API (CS and AI focused).
    """
    BASE_URL = "http://export.arxiv.org/api/query"

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search ArXiv for papers.
        """
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }

        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
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
