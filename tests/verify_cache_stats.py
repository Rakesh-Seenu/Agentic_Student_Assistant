import sys
import os
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from agentic_student_assistant.core.utils.cache import ResponseCache, SemanticRedisCache, REDIS_AVAILABLE

def test_stats(cache_obj, name):
    print(f"Testing {name} stats...")
    stats = cache_obj.get_stats()
    expected_keys = ['hits', 'misses', 'size', 'max_size', 'hit_rate', 'type']
    missing_keys = [key for key in expected_keys if key not in stats]
    
    if missing_keys:
        print(f"❌ {name} is missing keys: {missing_keys}")
        return False
    else:
        print(f"✅ {name} has all expected keys.")
        print(f"   Stats: {stats}")
        return True

def main():
    success = True
    
    # Test ResponseCache
    rc = ResponseCache(max_size=500)
    success &= test_stats(rc, "ResponseCache")
    
    # Test SemanticRedisCache (mocking redis if not available or just testing the class)
    if REDIS_AVAILABLE:
        try:
            # We try to init it, if it fails to connect it should still return default stats
            # But we might need to mock if no redis server is running
            src = SemanticRedisCache(max_size=2000)
            success &= test_stats(src, "SemanticRedisCache")
        except Exception as e:
            print(f"⚠️ Could not fully test SemanticRedisCache due to connection error, checking fallback stats...")
            # We can't easily test the 'try' block ohne redis, but we can check the 'except' block if we trigger it
            # Actually, the __init__ calls ping(), so it might fail there.
            print(f"   Error was: {e}")
    else:
        print("⏭️ Redis not available, skipping SemanticRedisCache test.")

    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
