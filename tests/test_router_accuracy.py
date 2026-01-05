"""
Test queries for router accuracy and agent functionality.
Used for Phase 8 testing and validation.
"""

# Test queries with expected routing
TEST_QUERIES = [
    # Curriculum queries
    {
        "query": "What courses cover machine learning?",
        "expected_agent": "curriculum",
        "description": "Simple curriculum query about ML courses"
    },
    {
        "query": "Tell me about the data science program",
        "expected_agent": "curriculum",
        "description": "Program information query"
    },
    {
        "query": "What are the prerequisites for advanced AI courses?",
        "expected_agent": "curriculum",
        "description": "Prerequisites query"
    },
    
    # Job market queries
    {
        "query": "Find Python developer jobs in Berlin",
        "expected_agent": "job_market",
        "description": "Job search with location"
    },
    {
        "query": "Show me data science career opportunities",
        "expected_agent": "job_market",
        "description": "Career opportunities query"
    },
    {
        "query": "What are the hiring trends in AI?",
        "expected_agent": "job_market",
        "description": "Job market trends query"
    },
    
    # Skill mapping queries
    {
        "query": "What skills do I need for data science jobs?",
        "expected_agent": "skill_mapping",
        "description": "Skill requirements query"
    },
    {
        "query": "Analyze the gap between my curriculum and job requirements",
        "expected_agent": "skill_mapping",
        "description": "Gap analysis query"
    },
    {
        "query": "How does my education match industry needs?",
        "expected_agent": "skill_mapping",
        "description": "Education-industry matching"
    },
    
    # Books queries
    {
        "query": "Recommend books on Python programming",
        "expected_agent": "books",
        "description": "Book recommendation query"
    },
    {
        "query": "What are good learning resources for deep learning?",
        "expected_agent": "books",
        "description": "Learning resources query"
    },
    {
        "query": "Suggest textbooks for machine learning",
        "expected_agent": "books",
        "description": "Textbook recommendation"
    },
    
    # Complex queries (orchestrator)
    {
        "query": "What courses should I take to get an AI job in Germany?",
        "expected_agent": "orchestrator",
        "description": "Multi-step query: curriculum + job market"
    },
    {
        "query": "I want to work in data science, what should I learn and where can I find jobs?",
        "expected_agent": "orchestrator",
        "description": "Complex query: education + career path"
    },
    {
        "query": "Compare my curriculum with ML job requirements and suggest books",
        "expected_agent": "orchestrator",
        "description": "Multi-domain: curriculum + jobs + books"
    },
    
    # Fallback queries
    {
        "query": "What's the weather today?",
        "expected_agent": "fallback",
        "description": "Out-of-scope query"
    },
    {
        "query": "Hello, how are you?",
        "expected_agent": "fallback",
        "description": "General greeting"
    },
]


if __name__ == "__main__":
    from agents.router_agent import route_query
    
    print("🧪 Router Accuracy Test\n")
    print("=" * 70)
    
    correct = 0
    total = len(TEST_QUERIES)
    
    for i, test in enumerate(TEST_QUERIES, 1):
        query = test["query"]
        expected = test["expected_agent"]
        description = test["description"]
        
        # Route query
        decision = route_query(query, enable_orchestration=True)
        actual = decision.agent
        
        # Check if correct
        is_correct = actual == expected
        if is_correct:
            correct += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"\n{status} Test {i}/{total}: {description}")
        print(f"   Query: {query}")
        print(f"   Expected: {expected} | Actual: {actual} | Confidence: {decision.confidence:.2f}")
        if not is_correct:
            print(f"   Reasoning: {decision.reasoning}")
        print("-" * 70)
    
    accuracy = correct / total
    print(f"\n\n📊 Final Results:")
    print(f"   Correct: {correct}/{total}")
    print(f"   Accuracy: {accuracy:.1%}")
    
    if accuracy >= 0.90:
        print("   ✅ EXCELLENT - Router performing very well!")
    elif accuracy >= 0.75:
        print("   ✅ GOOD - Router performing adequately")
    else:
        print("   ⚠️ NEEDS IMPROVEMENT - Consider adjusting router prompts")
