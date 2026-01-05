"""
Response caching layer with TTL support.
Reduces duplicate LLM calls and improves performance.
"""
import time
import hashlib
import pickle
from typing import Optional, Any, Dict
from collections import OrderedDict


class ResponseCache:
    """
    LRU cache with TTL for storing agent responses.
    """
    
    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000):
        """
        Initialize cache.
        
        Args:
            ttl_seconds: Time to live for cached entries (default 1 hour)
            max_size: Maximum number of entries to cache
        """
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, query: str, agent: str = "") -> str:
        """
        Generate cache key from query and agent.
        
        Args:
            query: User query
            agent: Agent name (optional)
            
        Returns:
            str: Cache key
        """
        # Normalize query (lowercase, strip whitespace)
        normalized = f"{agent}:{query.lower().strip()}"
        # Hash for consistent key length
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, query: str, agent: str = "") -> Optional[str]:
        """
        Get cached response if available and not expired.
        
        Args:
            query: User query
            agent: Agent name
            
        Returns:
            Cached response or None if not found/expired
        """
        key = self._generate_key(query, agent)
        
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        # Check if expired
        if time.time() - entry['timestamp'] > self.ttl_seconds:
            del self.cache[key]
            self.misses += 1
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        self.hits += 1
        
        return entry['response']
    
    def set(self, query: str, response: str, agent: str = ""):
        """
        Cache a response.
        
        Args:
            query: User query
            response: Agent response
            agent: Agent name
        """
        key = self._generate_key(query, agent)
        
        # Remove oldest entry if at max size
        if len(self.cache) >= self.max_size and key not in self.cache:
            self.cache.popitem(last=False)
        
        self.cache[key] = {
            'response': response,
            'timestamp': time.time(),
            'agent': agent
        }
    
    def clear(self):
        """Clear all cached entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict with cache hits, misses, size, and hit rate
        """
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'size': len(self.cache),
            'max_size': self.max_size,
            'hit_rate': hit_rate
        }
    
    def save_to_disk(self, filepath: str):
        """Save cache to disk."""
        with open(filepath, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def load_from_disk(self, filepath: str):
        """Load cache from disk."""
        try:
            with open(filepath, 'rb') as f:
                self.cache = pickle.load(f)
        except FileNotFoundError:
            pass


# Global cache instance
_global_cache: Optional[ResponseCache] = None


def get_cache(ttl_seconds: int = 3600, max_size: int = 1000) -> ResponseCache:
    """
    Get global cache instance (singleton).
    
    Args:
        ttl_seconds: TTL for cache entries
        max_size: Max cache size
        
    Returns:
        ResponseCache instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = ResponseCache(ttl_seconds=ttl_seconds, max_size=max_size)
    return _global_cache


if __name__ == "__main__":
    # Test cache
    cache = ResponseCache(ttl_seconds=10, max_size=3)
    
    # Test set and get
    print("🧪 Testing cache...")
    cache.set("What is ML?", "Machine learning explanation", agent="curriculum")
    result = cache.get("What is ML?", agent="curriculum")
    print(f"✅ Cache hit: {result[:30]}...")
    
    # Test cache miss
    result = cache.get("Different query", agent="curriculum")
    print(f"❌ Cache miss: {result}")
    
    # Test stats
    stats = cache.get_stats()
    print(f"\n📊 Cache Stats:")
    print(f"   Hits: {stats['hits']}")
    print(f"   Misses: {stats['misses']}")
    print(f"   Hit Rate: {stats['hit_rate']:.2%}")
    print(f"   Size: {stats['size']}/{stats['max_size']}")
    
    # Test TTL
    print(f"\n⏳ Testing TTL (waiting 11 seconds)...")
    time.sleep(11)
    result = cache.get("What is ML?", agent="curriculum")
    print(f"❌ Expired cache: {result}")
    
    stats = cache.get_stats()
    print(f"\n📊 Updated Stats:")
    print(f"   Hits: {stats['hits']}")
    print(f"   Misses: {stats['misses']}")
