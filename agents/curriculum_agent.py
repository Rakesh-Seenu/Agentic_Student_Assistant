"""
Curriculum agent for answering questions about course content.
Refactored to inherit from BaseAgent and use config-based architecture.
"""
import os
import sys
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from qdrant_client import QdrantClient
import streamlit as st

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.base_agent import BaseAgent
from utils.config_loader import get_config, get_prompt
from utils.llm_factory import LLMFactory

load_dotenv()


class CurriculumAgent(BaseAgent):
    """
    Agent for answering curriculum-related questions.
    Uses vector store (Qdrant) for retrieval-augmented generation.
    """
    
    def __init__(self):
        """Initialize curriculum agent with vectorstore and retrieval chain."""
        config = get_config()
        super().__init__(config, agent_name="curriculum")
        
        # Initialize Qdrant client
        self.qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL") or st.secrets.get("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY") or st.secrets.get("QDRANT_API_KEY"),
        )
        print(f"🐛 DEBUG: QdrantClient type: {type(self.qdrant)}")
        print(f"🐛 DEBUG: Has 'search': {hasattr(self.qdrant, 'search')}")
        print(f"🐛 DEBUG: Qdrant URL: {os.getenv('QDRANT_URL')}")
        
        # Create embeddings and vectorstore
        self.embeddings = LLMFactory.create_embeddings(config.models)
        
        self.vectorstore = Qdrant(
            client=self.qdrant,
            collection_name=config.vectorstore.qdrant.collection_name,
            embeddings=self.embeddings,
        )
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type=config.retrieval.search_type,
            search_kwargs={"k": config.retrieval.top_k}
        )
        
        # Create memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )
        
        # Create QA chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            output_key="answer",
        )
    
    def process(self, query: str, **kwargs) -> str:
        """
        Process curriculum query using retrieval chain.
        
        Args:
            query: User query about curriculum
            **kwargs: Additional parameters (unused)
            
        Returns:
            str: Answer from retrieval chain
        """
        result = self.qa_chain.invoke({"question": query})
        return result["answer"]


# Legacy global instance for backward compatibility
def create_curriculum_agent():
    """Create and return curriculum agent instance."""
    return CurriculumAgent()


# Legacy QA chain for backward compatibility
try:
    _legacy_agent = CurriculumAgent()
    qa_chain = _legacy_agent.qa_chain
except Exception as e:
    print(f"⚠️ Warning: Could not initialize legacy qa_chain: {e}")
    qa_chain = None


if __name__ == "__main__":
    agent = CurriculumAgent()
    
    query = input("\n🔎 Enter your query: ")
    result = agent.process(query)
    
    print("\n🤖 Answer:")
    print(result)
