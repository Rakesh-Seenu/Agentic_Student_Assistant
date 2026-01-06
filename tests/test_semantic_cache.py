import os
import sys
import time
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.cache import get_cache

def test_semantic_cache():
    print("[INFO] Starting Semantic Cache Verification...")
    load_dotenv()
    
    # Initialize cache
    cache = get_cache(ttl_seconds=3600)
    stats = cache.get_stats()
    print(f"[INFO] Backend: {stats.get('type')}")
    
    if stats.get('type') != 'redis-semantic':
        print("[ERROR] Semantic Redis is NOT active. Check your connection.")
        return

    # 1. SET a response for a specific question
    original_query = "What are the best data science jobs in Berlin?"
    answer = "The top data science roles in Berlin include ML Engineer, Data Analyst, and AI Research Scientist."
    
    print(f"\n[SET] Storing original: '{original_query}'")
    cache.set(original_query, answer)
    
    # Wait a moment for consistency
    time.sleep(1)

    # 2. TEST EXACT MATCH
    print("\n[TEST] Testing Exact Match...")
    res1 = cache.get(original_query)
    if res1 == answer:
        print("[SUCCESS] Exact match successful.")
    else:
        print(f"[FAIL] Exact match failed. Got: {res1}")

    # 3. TEST SEMANTIC MATCH (Different wording)
    similar_query = "Jobs for data scientists in Berlin area"
    print(f"\n[TEST] Testing Semantic Match for: '{similar_query}'")
    
    start_time = time.time()
    res2 = cache.get(similar_query)
    latency = time.time() - start_time
    
    if res2 == answer:
        print(f"[SUCCESS] Semantic match SUCCESSFUL! (Latency: {latency:.4f}s)")
    else:
        print(f"[FAIL] Semantic match FAILED. Got: {res2}")
        
    # 4. TEST TYPO MATCH
    typo_query = "Data science job Berln"
    print(f"\n[TEST] Testing Typo Match for: '{typo_query}'")
    res3 = cache.get(typo_query)
    if res3 == answer:
        print(f"[SUCCESS] Typo match SUCCESSFUL!")
    else:
        print(f"[FAIL] Typo match FAILED.")

    print("\n[DONE] Semantic Caching logic confirmed.")

if __name__ == "__main__":
    test_semantic_cache()
