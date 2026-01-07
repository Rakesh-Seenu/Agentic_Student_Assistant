"""
Streamlit application for Agentic Student Assistant.
Redesigned with a professional two-column layout.
"""
import os
import json
import time
import datetime
import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

# Utilities
from agentic_student_assistant.core.utils.parse_pdf import parse_single_pdf
from agentic_student_assistant.core.utils.chunker import chunk_text
from agentic_student_assistant.core.utils.logging_manager import LoggingManager
from agentic_student_assistant.core.utils.cache import get_cache
from agentic_student_assistant.core.orchestration.main_graph import app

# UI Utils
from app.frontend.utils import apply_custom_css

load_dotenv()

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Agentic Student Assistant", 
    layout="wide", 
    page_icon="🎓"
)
apply_custom_css()

# ---------------- Initialize Session State ----------------
if "logger" not in st.session_state:
    st.session_state.logger = LoggingManager(
        enable_file=True,
        enable_gsheets=True,
        enable_console=False
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- Top Heading ----------------
st.markdown(
    """
    <div style='text-align: center; padding: 0rem 0 1rem 0;'>
        <h1 style='margin: 0; font-weight: 800; color: #ffffff; font-size: 2.5rem; letter-spacing: -0.02em;'>
            🎓 Agentic Student Assistant
        </h1>
        <p style='margin: 5px 0 0 0; color: #808495; font-size: 1.1rem;'>
            Your Intelligent Partner for Academic Success
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Two-Column Layout ----------------
col1, col2 = st.columns([3, 7])

# ========== LEFT COLUMN: Control Panel ==========
with col1:
    # Performance Settings Container
    with st.container(border=True):
        st.markdown("#### ⚙️ Settings")
        use_cache = st.toggle(
            "⚡ Engine Caching", 
            value=True,
            help="Cache responses"
        )
        
        # Compact Cache Stats
        if use_cache:
            cache = get_cache()
            cache_stats = cache.get_stats()
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Hits", cache_stats.get('hits', 0), label_visibility="visible")
            with c2:
                hit_rate = cache_stats.get('hit_rate', 0)
                st.metric("Rate", f"{hit_rate:.0%}")
            with c3:
                st.metric("Miss", cache_stats.get('misses', 0))
            
            if st.button("Clear", use_container_width=True, key="clear_cache"):
                cache.clear()
                st.success("✓ Cleared!")
                time.sleep(0.3)
                st.rerun()
    
    # Compact Session Stats
    with st.container(border=True):
        st.markdown("#### 📊 Session")
        user_msgs = len([m for m in st.session_state.chat_history if m[0] == "user"])
        st.metric("Questions", user_msgs, label_visibility="visible")
    
    # Chat Input - Always at bottom
    user_query = st.chat_input("Type your question here...")


# ========== RIGHT COLUMN: Chat Area ==========
with col2:
    with st.container(border=True, height=800):
        st.markdown("#### 💬 Chat History")
        
        # Display chat history
        for role, message in st.session_state.chat_history:
            with st.chat_message(role, avatar="🤖" if role == "assistant" else "👤"):
                st.markdown(message)
        
        # Welcome message for new users
        if not st.session_state.chat_history:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown("""
                Hello! I'm your **SRH Smart Assistant**. I can help you with:
                
                1. **Job Market & Career Opportunities** - Find job trends, career paths, and improve employability
                2. **Research Papers & Academic Articles** - Discover, understand, and create research papers
                3. **Book Recommendations** - Get suggestions on books related to your field of study
                
                Feel free to ask me anything!
                """)
        
        # Process user input
        if user_query:
            # Add user message
            st.session_state.chat_history.append(("user", user_query))
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_query)
            
            # Check cache
            cached_result = None
            if use_cache:
                cache = get_cache()
                cached_result = cache.get(user_query)
            
            if cached_result:
                answer = cached_result
                agent_used = "cached"
                confidence = 1.0
                reasoning = "Retrieved from semantic cache"
                latency = 0.01
                st.toast("⚡ Retrieved from Cache", icon="📦")
            else:
                start_time = time.time()
                try:
                    with st.spinner("Analyzing your request..."):
                        result = app.invoke({
                            "query": user_query,
                            "chat_history": st.session_state.chat_history
                        })
                    
                    agent_used = result.get("agent", "unknown")
                    confidence = result.get("confidence")
                    reasoning = result.get("reasoning", "")
                    answer = result.get("result", "I couldn't find a specific answer.")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    answer = "I'm sorry, I encountered an error."
                    agent_used = "error"
                    confidence = 0
                    reasoning = str(e)
                
                latency = time.time() - start_time
                
                if use_cache and agent_used != "error":
                    cache.set(user_query, answer, agent=agent_used)
            
            # Display response
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(answer)
                
                # # Execution details
                # with st.expander("🔍 Execution Details"):
                #     st.markdown(f"**Engine:** `{agent_used.upper()}`")
                #     cols = st.columns(2)
                #     with cols[0]:
                #         if confidence is not None:
                #             color = "#10b981" if confidence > 0.8 else "#f59e0b" if confidence > 0.5 else "#ef4444"
                #             st.markdown(f"**Confidence:** <span style='color:{color}; font-weight:bold'>{confidence:.1%}</span>", unsafe_allow_html=True)
                #     with cols[1]:
                #         st.markdown(f"**Latency:** `{latency:.2f}s`")
                    
                #     if reasoning:
                #         st.info(reasoning)
            
            # Add to history
            st.session_state.chat_history.append(("assistant", answer))
            
            # Log interaction
            st.session_state.logger.log_interaction(
                query=user_query,
                agent=agent_used,
                result=answer,
                latency=latency,
                is_fallback=(agent_used == "fallback"),
                confidence=confidence,
                reasoning=reasoning
            )
            
            st.rerun()

