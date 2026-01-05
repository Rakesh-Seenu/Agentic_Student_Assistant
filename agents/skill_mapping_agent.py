"""
Skill mapping agent for analyzing skill gaps between curriculum and job market.
Refactored to inherit from BaseAgent and use config-based architecture.
"""
import os
import sys
import json
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.base_agent import BaseAgent
from utils.config_loader import get_config, get_prompt

load_dotenv()


class SkillMappingAgent(BaseAgent):
    """
    Agent for analyzing skill gaps between curriculum and job requirements.
    Compares student curriculum with job market needs and recommends learning paths.
    """
    
    def __init__(self):
        """Initialize skill mapping agent."""
        config = get_config()
        super().__init__(config, agent_name="skill_mapping")
        self.analysis_prompt = get_prompt("skill_mapping_analysis")
    
    def fetch_curriculum_chunks(self):
        """
        Fetch curriculum chunks from curriculum agent or database.
        
        Returns:
            List of curriculum documents/chunks
        """
        # This is a simplified version - ideally would query the vectorstore
        # For now, return placeholder that agents can work with
        try:
            from agents.curriculum_agent import CurriculumAgent
            agent = CurriculumAgent()
            # Get sample curriculum info
            sample_query = "What topics are covered in the curriculum?"
            result = agent.process(sample_query)
            return [{"content": result, "source": "curriculum"}]
        except Exception as e:
            print(f"⚠️ Could not fetch curriculum: {e}")
            return [{"content": "Data Science, Machine Learning, Software Engineering topics covered", "source": "placeholder"}]
    
    def load_job_listings(self):
        """
        Load recent job listings from saved data.
        
        Returns:
            List of job listings
        """
        job_file = "data/job_listings.json"
        if os.path.exists(job_file):
            with open(job_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return []
    
    def analyze_skill_match(self, curriculum_data, job_data):
        """
        Analyze skill gaps between curriculum and jobs.
        
        Args:
            curriculum_data: Curriculum information
            job_data: Job listings data
            
        Returns:
            Analysis of skill gaps and recommendations
        """
        curriculum_summary = "\n".join([doc.get("content", str(doc)) for doc in curriculum_data[:3]])
        job_summary = json.dumps(job_data[:3], indent=2) if job_data else "No recent job data available"
        
        prompt = f"""{self.analysis_prompt}

**Curriculum Coverage:**
{curriculum_summary}

**Job Market Requirements:**
{job_summary}

Provide your analysis."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def process(self, query: str, **kwargs) -> str:
        """
        Process skill mapping query.
        
        Args:
            query: User query about skill gaps
            **kwargs: Can include 'curriculum_data' and 'job_data'
            
        Returns:
            Skill gap analysis
        """
        # Get data from kwargs or fetch it
        curriculum_data = kwargs.get('curriculum_data') or self.fetch_curriculum_chunks()
        job_data = kwargs.get('job_data') or self.load_job_listings()
        
        return self.analyze_skill_match(curriculum_data, job_data)


# Legacy functions for backward compatibility
def fetch_curriculum_chunks():
    """Legacy function."""
    agent = SkillMappingAgent()
    return agent.fetch_curriculum_chunks()


def load_job_listings():
    """Legacy function."""
    agent = SkillMappingAgent()
    return agent.load_job_listings()


def analyze_skill_match(curriculum_docs, job_listings):
    """Legacy function."""
    agent = SkillMappingAgent()
    return agent.analyze_skill_match(curriculum_docs, job_listings)


if __name__ == "__main__":
    agent = SkillMappingAgent()
    
    print("📊 Skill Mapping Agent")
    print("Analyzing curriculum vs job market...")
    
    result = agent.process("Analyze skill gaps")
    print("\n✅ Analysis:")
    print(result)
