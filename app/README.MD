<div align="center">

# e.WAI

### AI-Powered Water Quality Monitoring Platform

[![Release](https://img.shields.io/github/v/release/e-Ray-Europa-GmbH/e.WAI2?style=flat-square&label=Latest%20Release&color=0078D4)](https://github.com/e-Ray-Europa-GmbH/e.WAI2/releases)
[![CI](https://img.shields.io/github/actions/workflow/status/e-Ray-Europa-GmbH/e.WAI2/release.yml?style=flat-square&label=CI)](https://github.com/e-Ray-Europa-GmbH/e.WAI2/actions)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](./LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](./docker-compose.yml)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](./server)
[![React](https://img.shields.io/badge/React-Vite-61DAFB?style=flat-square&logo=react&logoColor=black)](./myapp)

*Automate the extraction of water-quality parameters from environmental PDF reports and visualise them on a real-time geospatial dashboard — powered by [Groq / Llama 3.3](https://groq.com/).*

</div>

---

## Overview

**e.WAI** is an end-to-end environmental intelligence platform developed by **e.Ray Europa GmbH**. It eliminates manual data entry by using AI to parse unstructured environmental reports and surface structured insights on an interactive map — enabling engineers to identify trends, compare sampling stations, and act on data faster.

### Key Features

- 📄 **Automated PDF Ingestion** — Upload any environmental report; Llama 3.3 extracts measurements, units, and station metadata automatically
- 🗺 **Geospatial Dashboard** — Interactive map with per-parameter drill-downs at each sampling point
- 📊 **Area Comparison** — Side-by-side analysis across multiple sampling stations in a single view
- ⚡ **Async Processing** — Celery workers handle long-running AI jobs in the background; the UI stays responsive
- 🔐 **Role-Based Access** — Secure, session-based auth via Flask
- 🔄 **Automated Releases** — Every merge to `main` is automatically versioned, tagged, and released via semantic-release

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      Docker Compose                      │
│                                                          │
│  ┌─────────────────┐        ┌───────────────────────┐    │
│  │   Flask API      │        │    React / Vite        │    │
│  │   Port 8001      │        │    Port 5173           │    │
│  │ Auth·Chat·Ingest │        │  Map · Dashboard · UI  │    │
│  └────────┬─────────┘        └───────────────────────┘    │
│           │ enqueues                                       │
│  ┌────────▼─────────┐        ┌───────────────────────┐    │
│  │  Celery Worker    │        │      Nginx Proxy       │    │
│  │  Groq / Llama 3.3 │        │      Port 80 / 443     │    │
│  └────────┬──────────┘        └───────────────────────┘    │
│           │                                                │
│  ┌────────▼──────────┐  ┌───────────────────────────┐      │
│  │    PostgreSQL      │  │         Redis             │      │
│  │    Port 5432       │  │   Celery Broker · Port 6379│      │
│  └───────────────────┘  └───────────────────────────┘      │
└──────────────────────────────────────────────────────────┘
```

| Service | Responsibility | Port |
| :--- | :--- | :---: |
| **Flask API** | Auth · Chat · Ingestion orchestration | `8001` |
| **Celery Worker** | Async PDF extraction via Groq / Llama 3.3 | — |
| **React / Vite** | Interactive map dashboard | `5173` |
| **PostgreSQL** | Persistent data store | `5432` |
| **Redis** | Celery task broker & result backend | `6379` |
| **Nginx** | Reverse proxy · TLS termination | `80` / `443` |

---

## Compatibility

| Component | Requirement |
| :--- | :--- |
| OS | Windows 10/11 · macOS 13+ · Ubuntu 22.04+ |
| Docker Desktop | ≥ 4.25 |
| Python | 3.14+ |
| Node.js | ≥ 20 LTS |
| Browser | Chrome 120+· Firefox 121+ · Edge 120+ |

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — installed and running
- `GROQ_API_KEY` — obtain from [console.groq.com](https://console.groq.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/e-Ray-Europa-GmbH/e.WAI2.git
cd e.WAI2

# 2. Configure secrets
cp server/.env.example server/.env
# Edit server/.env and fill in all required values

# 3. Start the full stack
docker compose up -d --build

# 4. Seed initial data (first run only)
docker compose exec api python3 scripts/ingest_historic_v2.py
```

The application is now available at **[http://localhost](http://localhost)**.

### Configuration

| Variable | Description | Required |
| :--- | :--- | :---: |
| `GROQ_API_KEY` | Groq API key for Llama 3.3 inference | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `REDIS_URL` | Redis connection string | ✅ |
| `SECRET_KEY` | Flask session secret (min. 32 chars) | ✅ |

> [!IMPORTANT]
> PDF extraction will not function without a valid `GROQ_API_KEY`.  
> See [DEPLOYMENT_TEAM.md](./DEPLOYMENT_TEAM.md) for the complete secrets reference.

---

## Local Development

For rapid backend iteration without the full Docker stack:

```bash
# Python virtual environment
py -3.14 -m venv myvenv && myvenv\Scripts\activate     # Windows
# python3.14 -m venv myvenv && source myvenv/bin/activate  # macOS/Linux

pip install -r server/requirements.txt

# Frontend
cd myapp && npm install && cd ..
```

Start services in four terminals:

| Terminal | Service | Command |
| :---: | :--- | :--- |
| 1 | Database + Redis | `docker compose up -d db redis` |
| 2 | Celery Worker | `celery -A ewai_api.celery_app worker --loglevel=info` |
| 3 | Flask API | `python3 server/app.py` |
| 4 | Vite Frontend | `cd myapp && npm run dev` |

> [!TIP]
> Run `bash start_local.sh` to launch all four processes in one command.

---

## Usage

1. Navigate to [http://localhost](http://localhost)
2. Upload an environmental PDF via the **Chat** panel
3. The worker processes the file asynchronously — status is shown in real time
4. Sampling-point **markers appear on the Map** tab once extraction is complete
5. Click any marker to inspect the full parameter breakdown
6. Use **Compare Areas** to run side-by-side analyses across stations

---

## Common Commands

```bash
# Stack management
docker compose up -d          # Start all services
docker compose down           # Stop all services
docker compose down -v        # Stop and remove volumes

# Live log streaming
docker logs ewai-api-1 -f
docker logs ewai-worker-1 -f

# One-off server-side scripts
docker compose exec api python3 <script.py>

# Housekeeping
docker system prune -f        # Remove stopped containers and dangling images
```

---

## Contributing

All contributions are made through Pull Requests. **Direct commits to `main` are blocked.**

### Branch Workflow

```bash
git checkout main && git pull origin main
git checkout -b feat/<short-description>

# ... implement, test, iterate ...

git commit -m "feat(scope): concise description"
git push -u origin feat/<short-description>
# → Open a PR on GitHub targeting main
```

### Release Versioning

Releases are fully automated by [semantic-release](https://semantic-release.gitbook.io/). The merge commit prefix determines the version bump:

| Commit Prefix | Release Type | Example |
| :--- | :--- | :--- |
| `feat:` | Minor | `1.0.0 → 1.1.0` |
| `fix:` | Patch | `1.0.0 → 1.0.1` |
| `chore:` / `docs:` | No release | — |
| `BREAKING CHANGE:` (in body) | Major | `1.0.0 → 2.0.0` |

> [!NOTE]
> Use **Squash and merge** on GitHub and set the PR title to your commit prefix (e.g. `feat(map): add heatmap layer`).  
> This ensures semantic-release picks up the correct prefix.

📖 **[Read the full DevOps & PR Guide →](./docs/devops.md)**

---

## Further Reading

| Document | Description |
| :--- | :--- |
| [**DevOps & PR Guide**](./docs/devops.md) | Branch workflow, commit conventions, CI/CD, environment setup |
| [**Deployment Team Guide**](./DEPLOYMENT_TEAM.md) | SSL, database administration, production configuration |
| [**Changelog**](./CHANGELOG.md) | Full release history |

---

## License

This software is proprietary and confidential.  
© 2026 **e.Ray Europa GmbH** — All rights reserved.  
Unauthorised copying, distribution, or use is strictly prohibited.

---

<div align="center">

**e.Ray Europa GmbH** · Smart Environmental Solutions

</div>
