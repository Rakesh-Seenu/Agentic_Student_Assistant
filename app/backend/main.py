"""
FastAPI backend for Agentic Student Assistant.
Production-ready API with health checks, chat endpoints, and cache management.
"""
import time
from typing import Optional, List, Tuple
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from dotenv import load_dotenv
load_dotenv()

# --- Pydantic Models ---

class ChatRequest(BaseModel):
    """Request model for the chat endpoint."""
    query: str = Field(..., description="The user's question or query")
    use_cache: bool = Field(default=True, description="Whether to use caching")
    chat_history: Optional[List[Tuple[str, str]]] = Field(
        default=[], description="List of (role, message) tuples"
    )

class ChatResponse(BaseModel):
    """Response model for the chat endpoint."""
    answer: str
    agent: str
    confidence: Optional[float] = None
    latency: float
    reasoning: Optional[str] = None

class HealthResponse(BaseModel):
    """Response model for the health check."""
    status: str = "healthy"
    version: str
    timestamp: float

class CacheStatsResponse(BaseModel):
    """Response model for cache statistics."""
    hits: int = 0
    misses: int = 0
    hit_rate: float = 0.0
    size: int = 0

class PaperRequest(BaseModel):
    """Request model for paper recommendations."""
    query: str = Field(..., description="Research topic or paper query")
    use_cache: bool = Field(default=True, description="Whether to use caching")

class JobRequest(BaseModel):
    """Request model for job search."""
    query: str = Field(..., description="Job search query (role, location, etc.)")
    use_cache: bool = Field(default=True, description="Whether to use caching")

class BookRequest(BaseModel):
    """Request model for book recommendations."""
    query: str = Field(..., description="Book topic or genre query")
    use_cache: bool = Field(default=True, description="Whether to use caching")


# --- Lifespan ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown events."""
    # Startup: Import heavy modules
    from agentic_student_assistant.core.orchestration.main_graph import app as agent_app
    from agentic_student_assistant.core.utils.cache import get_cache
    app.state.agent_app = agent_app
    app.state.cache = get_cache()
    yield
    # Shutdown: cleanup if needed


# --- FastAPI App ---

app = FastAPI(
    title="Agentic Student Assistant API",
    description="Intelligent AI agents for academic career support",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Endpoints ---

@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=time.time()
    )


@app.post("/api/v1/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Routes the query to the appropriate agent and returns the response.
    """
    cache = app.state.cache
    agent_app = app.state.agent_app

    # Check cache first
    if request.use_cache:
        cached_result = cache.get(request.query)
        if cached_result:
            return ChatResponse(
                answer=cached_result,
                agent="cached",
                confidence=1.0,
                latency=0.01,
                reasoning="Retrieved from semantic cache"
            )

    start_time = time.time()
    try:
        result = agent_app.invoke({
            "query": request.query,
            "chat_history": request.chat_history or []
        })

        agent_used = result.get("agent", "unknown")
        answer = result.get("result", "I couldn't find a specific answer.")
        confidence = result.get("confidence")
        reasoning = result.get("reasoning", "")
        latency = time.time() - start_time

        # Store in cache
        if request.use_cache and agent_used != "error":
            cache.set(request.query, answer, agent=agent_used)

        return ChatResponse(
            answer=answer,
            agent=agent_used,
            confidence=confidence,
            latency=latency,
            reasoning=reasoning
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/v1/cache/stats", response_model=CacheStatsResponse, tags=["Cache"])
async def get_cache_stats():
    """Get cache statistics."""
    stats = app.state.cache.get_stats()
    return CacheStatsResponse(**stats)


@app.delete("/api/v1/cache", tags=["Cache"])
async def clear_cache():
    """Clear the entire cache."""
    app.state.cache.clear()
    return {"message": "Cache cleared successfully"}


# --- Agent-Specific Endpoints ---

@app.post("/api/recommend-papers", response_model=ChatResponse, tags=["Agents"])
async def recommend_papers(request: PaperRequest):
    """
    Direct endpoint for paper recommendations.
    Routes directly to the Talk2Papers agent.
    """
    cache = app.state.cache
    agent_app = app.state.agent_app

    # Check cache first
    if request.use_cache:
        cached_result = cache.get(request.query)
        if cached_result:
            return ChatResponse(
                answer=cached_result,
                agent="cached",
                confidence=1.0,
                latency=0.01,
                reasoning="Retrieved from semantic cache"
            )

    start_time = time.time()
    try:
        result = agent_app.invoke({
            "query": request.query,
            "chat_history": []
        })

        agent_used = result.get("agent", "unknown")
        answer = result.get("result", "I couldn't find relevant papers.")
        confidence = result.get("confidence")
        reasoning = result.get("reasoning", "")
        latency = time.time() - start_time

        # Store in cache
        if request.use_cache and agent_used != "error":
            cache.set(request.query, answer, agent=agent_used)

        return ChatResponse(
            answer=answer,
            agent=agent_used,
            confidence=confidence,
            latency=latency,
            reasoning=reasoning
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/find-jobs", response_model=ChatResponse, tags=["Agents"])
async def find_jobs(request: JobRequest):
    """
    Direct endpoint for job search.
    Routes directly to the Talk2Jobs agent.
    """
    cache = app.state.cache
    agent_app = app.state.agent_app

    # Check cache first
    if request.use_cache:
        cached_result = cache.get(request.query)
        if cached_result:
            return ChatResponse(
                answer=cached_result,
                agent="cached",
                confidence=1.0,
                latency=0.01,
                reasoning="Retrieved from semantic cache"
            )

    start_time = time.time()
    try:
        result = agent_app.invoke({
            "query": request.query,
            "chat_history": []
        })

        agent_used = result.get("agent", "unknown")
        answer = result.get("result", "I couldn't find relevant jobs.")
        confidence = result.get("confidence")
        reasoning = result.get("reasoning", "")
        latency = time.time() - start_time

        # Store in cache
        if request.use_cache and agent_used != "error":
            cache.set(request.query, answer, agent=agent_used)

        return ChatResponse(
            answer=answer,
            agent=agent_used,
            confidence=confidence,
            latency=latency,
            reasoning=reasoning
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/recommend-books", response_model=ChatResponse, tags=["Agents"])
async def recommend_books(request: BookRequest):
    """
    Direct endpoint for book recommendations.
    Routes directly to the Talk2Books agent.
    """
    cache = app.state.cache
    agent_app = app.state.agent_app

    # Check cache first
    if request.use_cache:
        cached_result = cache.get(request.query)
        if cached_result:
            return ChatResponse(
                answer=cached_result,
                agent="cached",
                confidence=1.0,
                latency=0.01,
                reasoning="Retrieved from semantic cache"
            )

    start_time = time.time()
    try:
        result = agent_app.invoke({
            "query": request.query,
            "chat_history": []
        })

        agent_used = result.get("agent", "unknown")
        answer = result.get("result", "I couldn't find relevant books.")
        confidence = result.get("confidence")
        reasoning = result.get("reasoning", "")
        latency = time.time() - start_time

        # Store in cache
        if request.use_cache and agent_used != "error":
            cache.set(request.query, answer, agent=agent_used)

        return ChatResponse(
            answer=answer,
            agent=agent_used,
            confidence=confidence,
            latency=latency,
            reasoning=reasoning
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# --- Run with Uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
