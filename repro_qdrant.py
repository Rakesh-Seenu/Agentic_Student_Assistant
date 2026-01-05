
import os
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

def test_qdrant_init():
    print("🧪 Testing Qdrant Initialization")
    
    # Initialize embeddings (using HF as per current config)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Initialize Qdrant in memory
    client = QdrantClient(":memory:")
    
    from qdrant_client.models import VectorParams, Distance
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    
    try:
        vectorstore = Qdrant(
            client=client, 
            collection_name="test_collection", 
            embeddings=embeddings,
        )
        print("✅ Vectorstore initialized")
        
        # Add dummy data
        vectorstore.add_texts(["Hello world"], metadatas=[{"source": "test"}])
        print("✅ Added text")
        
        # Search
        results = vectorstore.similarity_search("Hello")
        print(f"✅ Search results: {len(results)}")
        
        # MMR Search (where the error was)
        print("Testing MMR Search...")
        mmr_results = vectorstore.max_marginal_relevance_search("Hello")
        print(f"✅ MMR Search results: {len(mmr_results)}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_qdrant_init()
