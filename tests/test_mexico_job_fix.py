
import os
import sys
import json
from dotenv import load_dotenv


from agentic_student_assistant.talk2jobs.agents.job_market_agent import JobMarketAgent

def test_mexico_search():
    agent = JobMarketAgent()
    query = "Give me jobs based on Data Analyst in Mexico"
    
    # We won't actually call the API if we don't have a key, 
    # but we can look at how search_jobs would build params if we mock GoogleSearch
    
    field = agent._extract_field_from_query(query)
    cleaned_query, location = agent._extract_location(query)
    
    print(f"Field: {field}")
    print(f"Location: {location}")
    
    # Manually mimic the param building logic to verify
    search_q = field if field else cleaned_query
    if search_q and "jobs" not in search_q.lower():
        search_q = f"{search_q} jobs"
        
    params = {
        "engine": "google_jobs",
        "q": search_q,
    }
    
    if location:
        location = location.title()
        params["location"] = location
        
        region_map = {
            "usa": {"gl": "us", "hl": "en", "google_domain": "google.com"},
            "mexico": {"gl": "mx", "hl": "es", "google_domain": "google.com.mx"},
        }
        
        loc_lower = location.lower()
        for key, region_params in region_map.items():
            if key in loc_lower:
                params.update(region_params)
                break
                
    print(f"Generated Params: {json.dumps(params, indent=2)}")
    
    if params.get("gl") == "mx" and params.get("hl") == "es" and params.get("location") == "Mexico":
        print("✅ SUCCESS: Mexico parameters correctly assigned.")
    else:
        print("❌ FAILURE: Parameters mismatch.")

if __name__ == "__main__":
    test_mexico_search()
