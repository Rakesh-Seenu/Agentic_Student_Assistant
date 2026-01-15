# Agentic Student Assistant

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Overview

**Agentic Student Assistant** is an intelligent academic companion built with **LangGraph**, **OpenAI**, and modern AI infrastructure. It empowers students and researchers with specialized AI agents for career intelligence, academic research, and curated reading recommendations.

Our toolkit consists of the following intelligent agents:

- **Talk2Jobs**: Real-time global job market intelligence with regional optimization for Germany, USA, Mexico, India, Japan, and more.
- **Talk2Papers**: Multi-tier academic search across ArXiv, Semantic Scholar, CORE, and OpenReview with deep-dive Q&A capabilities.
- **Talk2Books**: Curated reading recommendations from Open Library and Google Books with academic focus.
- **Talk2Events**: Real-time events recommentation agent using meetup and event bride Library.(Comming soon...)

---

## 🏗️ Architecture

The system leverages a sophisticated multi-agent orchestration pattern using **LangGraph**, featuring semantic caching with **Redis** and comprehensive monitoring via **Google Cloud Logging**.

![Architecture Diagram](assets/architecture.png)

---

## 🛠️ Tech Stack

- **Orchestration**: LangGraph (ReAct)
- **Intelligence**: OpenAI GPT-4
- **Infrastructure**: Redis (Semantic Cache), Google Cloud Logging
- **Interface**: Streamlit (Dashboard)
- **Language**: Python 3.10+

---

## 🌟 Key Features

### 1. Advanced Academic Research (Talk2Papers) 📑
A high-fidelity research tool that queries the world's leading academic databases in parallel:
- **Multi-Tier Search**: `ArXiv` + `Semantic Scholar` + `CORE` + `OpenReview.net`
- **Deep-Dive Q&A**: Ask follow-up questions about specific papers' methodology or findings
- **Robust Fallback**: Automatically switches sources if an API is rate-limited or forbidden
- **Semantic Similarity**: Local embedding-based semantic caching for instant similar query responses

### 2. Reading Recommendations (Talk2Books) 📚
Curated reading lists using **Open Library** and **Google Books**:
- **Academic Focus**: Filters for reputable publishers and academic sources
- **Detailed Summaries**: Provides insights into core contributions and target audience

### 3. Global Job Market Intelligence (Talk2Jobs) 💼
Precision search across international regions:
- **Regional Intelligence**: Specific optimizations for **Mexico**, **Germany**, **Japan**, **India**, **USA**, and more
- **Language Aware**: Automatically adjusts search parameters (`hl`, `gl`, `google_domain`) for local results

### 4. Smart Caching System 🧠
Redis-based persistent caching with local semantic similarity:
- **Exact Match**: Hash-based instant retrieval
- **Semantic Match**: SentenceTransformer-powered similarity search (threshold: 0.88)
- **Zero API Cost**: Completely local embedding generation
- **80-90% Latency Reduction**: Through intelligent response caching


# Clone and enter the repository
```bash
git clone https://github.com/yourusername/Agentic_Student_Assistant
cd Agentic_Student_Assistant
```

# Install dependencies
### Installation with uv
1. Install [uv](https://github.com/astral-sh/uv) if you haven't already.
2. Sync dependencies:
```bash
uv sync
```

# Set up .env with your API keys (OpenAI, SerpAPI, etc.)
## Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_openai_key
SERPAPI_API_KEY=your_serpapi_key
# Optional (for enhanced features)
CORE_API_KEY=your_core_key
SEMANTIC_SCHOLAR_API_KEY=your_ss_key
REDIS_HOST=your_redis_host
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_redis_password
GROQ_API_KEY=your_groq_key  # For free LLM alternative```
```

# Launch the dashboard
```streamlit run app/frontend/streamlit_app.py```

---

## 📖 Usage

### Example Queries

**Job Search:**
```
"Find data science jobs in Berlin"
"Show me machine learning positions in Tokyo"
```

**Paper Research:**
```
"Papers about transformer architecture"
"Explain the BioBridge paper"
```

**Book Recommendations:**
```
"Books on deep learning for beginners"
"Academic texts on quantum computing"
```

## 📊 Performance Metrics

- **Routing Accuracy**: ~98%
- **Cache Hit Rate**: 80-90% (with Redis + Semantic Matching)
- **Average Latency**: <2s (cached), 5-8s (fresh query)
- **Supported Databases**: 7 (ArXiv, Semantic Scholar, CORE, OpenReview, Open Library, Google Books, Google Jobs)


**Built with ❤️ for students and researchers worldwide** 🌍🎓

