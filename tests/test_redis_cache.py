import os
import sys
import time
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.cache import get_cache

def test_redis_cache():
    print("🧪 Starting Redis Cache Verification...")
    load_dotenv()
    
    # Initialize cache
    cache = get_cache(ttl_seconds=60)
    stats = cache.get_stats()
    cache_type = stats.get('type')
    
    print(f"📡 Cache Type: {cache_type}")
    
    if cache_type == 'redis':
        print("✅ Redis is ACTIVE.")
    else:
        print("⚠️ Redis is NOT ACTIVE. Using in-memory fallback.")
        print("   (Make sure a Redis server is running on localhost:6379)")
    
    # Test SET
    test_query = "Who won the FIFA World Cup 2022?"
    test_response = "Argentina won the FIFA World Cup 2022, defeating France in the final."
    
    print(f"📥 Setting cache for: '{test_query}'")
    cache.set(test_query, test_response, agent="sports_test")
    
    # Test GET
    print("📤 Retrieving from cache...")
    retrieved = cache.get(test_query, agent="sports_test")
    
    if retrieved == test_response:
        print("✅ Cache GET successful and accurate.")
    else:
        print(f"❌ Cache GET failed. Retrieved: {retrieved}")
        return
    
    # Verify Stats
    new_stats = cache.get_stats()
    print(f"📊 Stats: Hits={new_stats['hits']}, Misses={new_stats['misses']}, Size={new_stats['size']}")
    
    if cache_type == 'redis':
        print("\n🔄 To verify PERSISTENCE:")
        print("1. Run this script again.")
        print("2. It should show 'Cache hit' immediately without SET-ting again if you modify the code to skip SET.")
    
    print("\n✨ Verification Complete.")

if __name__ == "__main__":
    test_redis_cache()
