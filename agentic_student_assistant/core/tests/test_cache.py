"""
Integration tests for core.utils.cache module.
"""
import pytest
import time
from agentic_student_assistant.core.utils.cache import ResponseCache, get_cache


class TestResponseCache:
    def test_cache_initialization(self):
        """Test cache initializes correctly."""
        cache = ResponseCache(ttl_seconds=1800, max_size=500)
        
        assert cache.ttl_seconds == 1800
        assert cache.max_size == 500
        assert cache.hits == 0
        assert cache.misses == 0
    
    def test_cache_set_and_get(self):
        """Test setting and getting values."""
        cache = ResponseCache()
        
        cache.set("What is AI?", "AI is artificial intelligence")
        result = cache.get("What is AI?")
        
        assert result == "AI is artificial intelligence"
        assert cache.hits == 1
        assert cache.misses == 0
    
    def test_cache_miss(self):
        """Test cache miss."""
        cache = ResponseCache()
        
        result = cache.get("nonexistent")
        
        assert result is None
        assert cache.misses == 1
    
    def test_cache_ttl_expiration(self):
        """Test TTL expiration."""
        cache = ResponseCache(ttl_seconds=1)
        
        cache.set("test", "value")
        assert cache.get("test") == "value"
        
        time.sleep(1.1)
        assert cache.get("test") is None
    
    def test_cache_lru_eviction(self):
        """Test LRU eviction."""
        cache = ResponseCache(max_size=2)
        
        cache.set("q1", "r1")
        cache.set("q2", "r2")
        cache.set("q3", "r3")  # Should evict q1
        
        assert cache.get("q1") is None
        assert cache.get("q2") == "r2"
        assert cache.get("q3") == "r3"
    
    def test_cache_clear(self):
        """Test clearing cache."""
        cache = ResponseCache()
        
        cache.set("q1", "r1")
        cache.set("q2", "r2")
        cache.clear()
        
        assert cache.get("q1") is None
        assert cache.get("q2") is None
    
    def test_cache_stats(self):
        """Test cache statistics."""
        cache = ResponseCache()
        
        cache.set("q1", "r1")
        cache.get("q1")  # Hit
        cache.get("q2")  # Miss
        
        stats = cache.get_stats()
        
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['hit_rate'] == 0.5


class TestGetCache:
    def test_get_cache_singleton(self):
        """Test cache singleton pattern."""
        cache1 = get_cache()
        cache2 = get_cache()
        
        # Should return same instance
        assert cache1 is cache2
