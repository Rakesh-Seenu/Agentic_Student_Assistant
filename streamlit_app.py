"""
Streamlit application for Agentic Student Assistant.
Updated to use new architecture with caching, logging, and enhanced UI.
"""
import os
import json
import time
import datetime
import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document

# Utilities
from utils.parse_pdf import parse_single_pdf
from utils.chunker import chunk_text
from utils.logging_manager import LoggingManager
from utils.cache import get_cache
from langgraph_workflow.main_graph import app

load_dotenv()

# ---------------- UI Setup ----------------
st.set_page_config(page_title="SRH Assistant", layout="wide", page_icon="🎓")
st.title("🎓 AI-Powered University Assistant")
st.caption("Powered by GPT-4 with LLM-based routing and multi-agent orchestration")

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Configuration")

# Cache settings
st.sidebar.subheader("🚀 Performance")
use_cache = st.sidebar.checkbox("Enable Response Caching", value=True)

if use_cache:
    cache = get_cache()
    cache_stats = cache.get_stats()
    st.sidebar.metric("Cache Type", cache_stats.get('type', 'unknown').title())
    st.sidebar.metric("Cache Hit Rate", f"{cache_stats['hit_rate']:.1%}")
    st.sidebar.metric("Cached Responses", f"{cache_stats['size']}/{cache_stats['max_size']}")
    
    if st.sidebar.button("Clear Cache"):
        cache.clear()
        st.sidebar.success("Cache cleared!")
        st.rerun()

# ---------------- Initialize Logger ----------------
if "logger" not in st.session_state:
    st.session_state.logger = LoggingManager(
        enable_file=True,
        enable_gsheets=True,  # Enable if you have Google Sheets configured
        enable_console=False
    )

# ---------------- Chat Interface ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Chat input
st.sidebar.divider()
user_query = st.chat_input("Ask about jobs, research papers, or books...")

if user_query:
    # Add user message to chat
    st.session_state.chat_history.append(("user", user_query))
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Check cache first if enabled
    cached_result = None
    if use_cache:
        cache = get_cache()
        cached_result = cache.get(user_query)
        if cached_result:
            st.info("📦 Retrieved from cache")
    
    if cached_result:
        # Use cached result
        answer = cached_result
        agent_used = "cached"
        confidence = None
        reasoning = "Response retrieved from cache"
        latency = 0.0
    else:
        # Process query
        start_time = time.time()
        
        try:
            with st.spinner("🤖 Thinking..."):
                result = app.invoke({
                    "query": user_query,
                    "chat_history": st.session_state.chat_history
                })
            
            agent_used = result.get("agent", "unknown")
            confidence = result.get("confidence")
            reasoning = result.get("reasoning", "")
            answer = result.get("result", "")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            answer = f"I apologize, but I encountered an error while processing your request: {str(e)}"
            agent_used = "error"
            confidence = 0
            reasoning = str(e)
        
        end_time = time.time()
        latency = end_time - start_time
        
        # Cache the result if enabled and successful
        if use_cache and agent_used != "error":
            cache.set(user_query, answer, agent=agent_used)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)
        
        # Show routing metadata in professional expander
        if agent_used != "cached":
            with st.expander("🔍 Execution Details"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Agent:** {agent_used.title()}")
                    if confidence is not None:
                        st.write(f"**Confidence:** {confidence:.2%}")
                with col2:
                    st.write(f"**Latency:** {latency:.2f}s")
                    if reasoning:
                        st.caption(f"**Reasoning:** {reasoning}")
    
    # Add assistant response to chat history
    st.session_state.chat_history.append(("assistant", answer))
    
    # Log interaction
    is_fallback = agent_used == "fallback"
    st.session_state.logger.log_interaction(
        query=user_query,
        agent=agent_used,
        result=answer,
        latency=latency,
        is_fallback=is_fallback,
        confidence=confidence,
        reasoning=reasoning
    )



# ---------------- Sidebar Stats ----------------
st.sidebar.divider()
st.sidebar.subheader("📊 Session Stats")
st.sidebar.metric("Questions Asked", len([m for m in st.session_state.chat_history if m[0] == "user"]))

if use_cache:
    st.sidebar.metric("Cache Hits", cache_stats['hits'])
    st.sidebar.metric("Cache Misses", cache_stats['misses'])
