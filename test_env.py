import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 ENVIRONMENT VARIABLES CHECK")
print("=" * 60)

required_vars = {
    "OPENAI_API_KEY": "OpenAI API (CRITICAL - All LLM operations)",
    "QDRANT_URL": "Qdrant Vector DB (Curriculum search)",
    "QDRANT_API_KEY": "Qdrant Authentication",
    "SERPAPI_API_KEY": "SerpAPI (Job search & Book recommendations)"
}

optional_vars = {
    "LANGSMITH_API_KEY": "LangSmith (Tracing - optional)",
    "LANGSMITH_TRACING": "LangSmith Tracing Flag",
    "LANGSMITH_PROJECT": "LangSmith Project Name"
}

print("\n✅ REQUIRED Variables:")
print("-" * 60)
all_set = True
for var, description in required_vars.items():
    value = os.getenv(var)
    if value:
        # Mask the key for security
        masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
        print(f"  ✅ {var:20} = {masked:20} | {description}")
    else:
        print(f"  ❌ {var:20} = NOT SET{' ' * 16} | {description}")
        all_set = False

print("\n🔧 OPTIONAL Variables:")
print("-" * 60)
for var, description in optional_vars.items():
    value = os.getenv(var)
    if value:
        print(f"  ✅ {var:20} = {value:20} | {description}")
    else:
        print(f"  ⚪ {var:20} = NOT SET{' ' * 16} | {description}")

print("\n" + "=" * 60)
if all_set:
    print("✅ ALL REQUIRED VARIABLES ARE SET!")
    print("   You're ready to run: streamlit run streamlit_app.py")
else:
    print("❌ MISSING REQUIRED VARIABLES!")
    print("   Please add the missing variables to your .env file")
    print("   See .env.example for the template")
print("=" * 60)
