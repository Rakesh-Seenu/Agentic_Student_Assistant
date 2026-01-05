
import os
import sys

# Add parent to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.router_agent import RouterAgent

from unittest.mock import patch

def test_router_prompt_construction():
    print("🧪 Testing Router Prompt Construction")
    
    try:
        # Mock environment to pass LLMFactory check
        with patch.dict(os.environ, {"GROQ_API_KEY": "gsk-mock-key"}):
            agent = RouterAgent()
            print("✅ Router Agent initialized")
            
            # Test rendering
            prompt_val = agent.prompt.invoke({"query": "test"})
        messages = prompt_val.to_messages()
        
        system_msg = messages[0].content
        print(f"✅ Prompt rendered successfully.")
        print(f"   System prompt length: {len(system_msg)}")
        
        if "json" in system_msg.lower():
             print("✅ Format instructions present (JSON schema found)")
        else:
             print("❌ Format instructions might be missing")

    except Exception as e:
        print(f"❌ Failed to construct/render prompt: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_router_prompt_construction()
