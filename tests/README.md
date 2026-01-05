# Test Scenarios for Agentic Student Assistant

## Router Accuracy Tests

### Curriculum Queries
- ✅ "What courses cover machine learning?" → curriculum
- ✅ "Tell me about the data science program" → curriculum  
- ✅ "What are prerequisites for AI courses?" → curriculum

### Job Market Queries
- ✅ "Find Python jobs in Berlin" → job_market
- ✅ "Show me data science careers" → job_market
- ✅ "Hiring trends in AI?" → job_market

### Skill Mapping Queries
- ✅ "What skills do I need for data science?" → skill_mapping
- ✅ "Analyze gap between curriculum and jobs" → skill_mapping
- ✅ "How does education match industry?" → skill_mapping

### Books Queries
- ✅ "Recommend Python books" → books
- ✅ "Learning resources for deep learning?" → books
- ✅ "ML textbooks?" → books

### Complex Queries (Orchestrator)
- ✅ "What courses to get AI job in Germany?" → orchestrator
- ✅ "Want to work in data science, what to learn?" → orchestrator
- ✅ "Compare curriculum with ML jobs and suggest books" → orchestrator

### Fallback Queries
- ✅ "What's the weather?" → fallback
- ✅ "Hello, how are you?" → fallback

## Manual Testing Checklist

### Basic Functionality
- [ ] Run Streamlit app: `streamlit run streamlit_app.py`
- [ ] Ask simple curriculum question
- [ ] Ask job search question
- [ ] Verify responses are relevant

### Caching
- [ ] Ask same question twice
- [ ] Verify second response is faster
- [ ] Check "Retrieved from cache" indicator
- [ ] View cache hit rate in sidebar
- [ ] Clear cache and verify it resets

### Routing Metadata
- [ ] Expand "Routing Details" section
- [ ] Verify agent name is shown
- [ ] Verify confidence score is displayed
- [ ] Verify reasoning is shown
- [ ] Check latency metric

### Complex Scenarios
- [ ] Ask multi-domain question
- [ ] Verify orchestrator is used
- [ ] Check that multiple agents are called
- [ ] Verify comprehensive answer

### Logging
- [ ] Check `logs/workflow_logs.txt` exists
- [ ] Verify logs include confidence and reasoning
- [ ] Check timestamp format
- [ ] Verify all queries are logged

### Configuration
- [ ] Upload custom curriculum PDF
- [ ] Switch between SRH and uploaded curriculum
- [ ] Verify queries use correct curriculum source

### Error Handling
- [ ] Test with invalid query
- [ ] Verify graceful error handling
- [ ] Check fallback agent works

## Performance Metrics

### Target Metrics
- Router Accuracy: >90%
- Cache Hit Rate: >60% (after warmup)
- Average Latency: <3 seconds
- Complex Query Handling: ✅

### Actual Results
- Router Accuracy: ___ % (run tests/test_router_accuracy.py)
- Cache Hit Rate: ___ % (check Streamlit sidebar)
- Average Latency: ___ s
- Complex Queries: ✅ / ❌

## Integration Tests

### End-to-End
1. Start Streamlit app
2. Ask: "What courses should I take to get an AI job?"
3. Verify:
   - Routes to orchestrator
   - Calls multiple agents
   - Returns comprehensive answer
   - Logs interaction
   - Shows routing metadata

### Configuration Changes
1. Edit `config/models/gpt4.yaml` - change temperature
2. Restart app
3. Verify new temperature is used

### Prompt Changes
1. Edit `config/prompts/prompts.yaml` - modify router prompt
2. Restart app
3. Ask routing question
4. Verify behavior matches new prompt
