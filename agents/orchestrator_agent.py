"""
Orchestrator agent using ReAct pattern for complex multi-step queries.
Coordinates multiple specialist agents to answer comprehensive questions.
"""
import os
import sys
from typing import List
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.base_agent import BaseAgent
from utils.config_loader import get_config, get_prompt
from utils.llm_factory import LLMFactory


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator agent that uses ReAct to coordinate multiple specialist agents.
    Handles complex queries requiring multiple steps or multiple domain expertise.
    """
    
    def __init__(self):
        """Initialize orchestrator with ReAct agent and tools."""
        config = get_config()
        super().__init__(config, agent_name="orchestrator")
        
        # Create tools for each specialist agent
        self.tools = self._create_tools()
        
        # Create ReAct agent
        self.agent = self._create_react_agent()
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    
    def _create_tools(self) -> List[Tool]:
        """
        Create tools for each specialist agent.
        
        Returns:
            List of LangChain tools
        """
        from agents.curriculum_agent import CurriculumAgent
        from agents.job_market_agent import JobMarketAgent
        from agents.skill_mapping_agent import SkillMappingAgent
        from agents.curriculum_agent import CurriculumAgent
        from agents.job_market_agent import JobMarketAgent
        from agents.skill_mapping_agent import SkillMappingAgent
        from agents.books_recommend_agent import BooksRecommendAgent
        from agents.paper_recommend_agent import PaperRecommendAgent
        
        # Initialize agents (lazy loading to avoid circular imports)
        curriculum_agent = None
        job_agent = None
        skill_agent = None
        books_agent = None
        papers_agent = None
        
        def get_curriculum_agent():
            nonlocal curriculum_agent
            if curriculum_agent is None:
                curriculum_agent = CurriculumAgent()
            return curriculum_agent
        
        def get_job_agent():
            nonlocal job_agent
            if job_agent is None:
                job_agent = JobMarketAgent()
            return job_agent
        
        def get_skill_agent():
            nonlocal skill_agent
            if skill_agent is None:
                skill_agent = SkillMappingAgent()
            return skill_agent
        
        def get_books_agent():
            nonlocal books_agent
        def get_books_agent():
            nonlocal books_agent
            if books_agent is None:
                books_agent = BooksRecommendAgent()
            return books_agent
        
        def get_papers_agent():
            nonlocal papers_agent
            if papers_agent is None:
                papers_agent = PaperRecommendAgent()
            return papers_agent
        
        tools = [
            Tool(
                name="CurriculumSearch",
                func=lambda q: get_curriculum_agent().process(q),
                description="Search curriculum content, course information, modules, and academic programs. Use this for questions about what courses cover specific topics, course requirements, or curriculum structure."
            ),
            Tool(
                name="JobMarketSearch",
                func=lambda q: get_job_agent().process(q),
                description="Search job listings and career opportunities. Use this to find current job openings, understand job market demand, or get information about specific roles and their requirements."
            ),
            Tool(
                name="SkillAnalysis",
                func=lambda q: get_skill_agent().process(q),
                description="Analyze skill gaps between curriculum and job market requirements. Use this to identify what skills students need, compare curriculum coverage with job demands, or recommend learning paths."
            ),
            Tool(
                name="BookRecommendations",
                func=lambda q: get_books_agent().process(q),
                description="Find academic book recommendations and learning resources. Use this to suggest textbooks, monographs, or other high-quality learning materials for specific topics."
            ),
            Tool(
                name="PaperRecommendations",
                func=lambda q: get_papers_agent().process(q),
                description="Find scientific research papers and academic articles. Use this to find primary sources, latest research, citations, and technical details from Semantic Scholar and CORE."
            )
        ]
        
        return tools
    
    def _create_react_agent(self):
        """
        Create ReAct agent with appropriate prompts.
        
        Returns:
            ReAct agent
        """
        # Get prompts from config
        system_prompt = get_prompt("orchestrator_system")
        react_template = get_prompt("react_template")
        
        # Format the template with system prompt
        formatted_template = react_template.format(system_prompt=system_prompt)
        
        prompt = PromptTemplate.from_template(formatted_template)
        
        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
    
    def process(self, query: str, **kwargs) -> str:
        """
        Process complex query using ReAct orchestration.
        
        Args:
            query: Complex user query
            **kwargs: Additional parameters
            
        Returns:
            Comprehensive answer from orchestration
        """
        try:
            result = self.agent_executor.invoke({"input": query})
            return result.get("output", "Unable to process query")
        except Exception as e:
            print(f"❌ Orchestration error: {e}")
            return f"I encountered an error while processing your complex query: {str(e)}. Please try breaking it down into simpler questions."


if __name__ == "__main__":
    print("🎭 Orchestrator Agent Test\n")
    
    agent = OrchestratorAgent()
    
    # Test complex query
    test_query = "What courses should I take to get an AI job in Berlin?"
    print(f"Query: {test_query}\n")
    
    result = agent.process(test_query)
    print(f"\n✅ Final Answer:\n{result}")
