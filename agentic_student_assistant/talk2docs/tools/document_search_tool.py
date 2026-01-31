"""
Tool for searching documents using semantic search.
"""
from typing import List, Dict, Optional
from qdrant_client.models import Filter, FieldCondition, MatchValue
from agentic_student_assistant.talk2docs.tools.base_vector_tool import BaseVectorTool

class DocumentSearchTool(BaseVectorTool):
    """
    Tool for searching within the document vector store.
    """
    
    def search_documents(
        self,
        query: str,
        document_id: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, any]]:
        """
        Search for relevant document chunks.
        """
        if not self.client:
            return []
            
        # Generate query embedding
        query_embedding = self.embedder.encode(query).tolist()
        
        # Build filter if document_id specified
        query_filter = None
        if document_id:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id)
                    )
                ]
            )
        
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=query_filter,
                limit=top_k
            )
            
            chunks = []
            for result in results:
                chunks.append({
                    "content": result.payload["content"],
                    "score": result.score,
                    "document_id": result.payload["document_id"],
                    "filename": result.payload.get("filename", "Unknown"),
                    "chunk_index": result.payload.get("chunk_index", 0),
                    "metadata": result.payload
                })
            return chunks
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
