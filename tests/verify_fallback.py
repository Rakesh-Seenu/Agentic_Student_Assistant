
import os
import sys
from unittest.mock import patch

# Add parent to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.llm_factory import LLMFactory

def test_fallback_logic():
    print("🧪 Testing LLM Factory Fallback Logic")
    
    # Case 1: OpenAI key is valid
    print("\n1️⃣ Test: Valid OpenAI Key")
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-valid-key-123", "GROQ_API_KEY": "gsk-groq-key"}):
        provider = LLMFactory._get_provider()
        print(f"   Provider: {provider}")
        if provider == "openai":
            print("   ✅ Passed")
        else:
            print("   ❌ Failed (Expected openai)")

    # Case 2: OpenAI key is placeholder
    print("\n2️⃣ Test: Placeholder OpenAI Key (sk-your-...)")
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-your-***************here", "GROQ_API_KEY": "gsk-groq-key"}):
        provider = LLMFactory._get_provider()
        print(f"   Provider: {provider}")
        if provider == "groq":
            print("   ✅ Passed")
        else:
            print("   ❌ Failed (Expected groq)")

    # Case 3: OpenAI key is missing
    print("\n3️⃣ Test: Missing OpenAI Key")
    with patch.dict(os.environ, {"OPENAI_API_KEY": "", "GROQ_API_KEY": "gsk-groq-key"}):
        provider = LLMFactory._get_provider()
        print(f"   Provider: {provider}")
        if provider == "groq":
            print("   ✅ Passed")
        else:
            print("   ❌ Failed (Expected groq)")

if __name__ == "__main__":
    test_fallback_logic()
