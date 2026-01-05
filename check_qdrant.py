
import importlib.metadata
from qdrant_client import QdrantClient

try:
    version = importlib.metadata.version("qdrant-client")
    print(f"Qdrant Client Version: {version}")
except Exception as e:
    print(f"Could not get version: {e}")

print(f"Has 'search' method: {hasattr(QdrantClient, 'search')}")
print(f"Has 'search_points' method: {hasattr(QdrantClient, 'search_points')}")

try:
    from qdrant_client import AsyncQdrantClient
    print(f"Has AsyncQdrantClient: True")
    print(f"AsyncQdrantClient has 'search': {hasattr(AsyncQdrantClient, 'search')}")
except ImportError:
    print("AsyncQdrantClient not found")
