<div align="center">

# e.WAI

### AI-Powered Water Quality Monitoring Platform

[![Release](https://img.shields.io/github/v/release/e-Ray-Europa-GmbH/e.WAI2?style=flat-square&label=Latest%20Release&color=0078D4)](https://github.com/e-Ray-Europa-GmbH/e.WAI2/releases)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](./LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](./docker-compose.yml)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](./server)
[![React](https://img.shields.io/badge/React-Vite-61DAFB?style=flat-square&logo=react&logoColor=black)](./myapp)

*Ingest complex environmental PDF reports and visualise water-quality data on an interactive geospatial dashboard — powered by [Groq / Llama 3.3](https://groq.com/).*

</div>

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Local Development](#local-development)
- [Usage](#usage)
- [Common Commands](#common-commands)
- [Contributing](#contributing)
- [Further Reading](#further-reading)

---

## Overview

**e.WAI** is an end-to-end environmental intelligence platform developed by **e.Ray Europa GmbH**. It automates the extraction of structured water-quality parameters from unstructured PDF reports and presents them as real-time markers on an interactive map — enabling environmental engineers to identify trends, compare sampling areas, and act on data faster.

Key capabilities:

- 📄 **PDF Ingestion** — Upload environmental reports; AI extracts measurement data automatically
- 🗺 **Geospatial Dashboard** — Visualise sampling points on an interactive map with per-parameter drill-downs
- 📊 **Area Comparison** — Side-by-side comparison of sampling stations
- 🔐 **Authentication** — Role-based access control via Flask sessions
- ⚙️ **Async Processing** — Long-running PDF jobs handled by Celery workers, keeping the API responsive

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Docker Compose                    │
│                                                     │
│  ┌──────────────┐   ┌──────────────┐  ┌──────────┐  │
│  │  Flask API   │   │Celery Worker │  │  React/  │  │
│  │  Port 8001   │──▶│ (Groq/Llama) │  │  Vite    │  │
│  │              │   │              │  │Port 5173 │  │
│  └──────┬───────┘   └──────┬───────┘  └──────────┘  │
│         │                  │                         │
│  ┌──────▼───────┐   ┌──────▼───────┐                 │
│  │  PostgreSQL  │   │    Redis     │                 │
│  │   Database   │   │   (Broker)   │                 │
│  └──────────────┘   └──────────────┘                 │
└─────────────────────────────────────────────────────┘
```

| Service | Responsibility | Port |
| :--- | :--- | :---: |
| **Flask API** | Auth · Chat · Ingestion orchestration | `8001` |
| **Celery Worker** | Async PDF processing via Groq / Llama 3.3 | — |
| **React / Vite** | Interactive map dashboard | `5173` |
| **PostgreSQL** | Persistent data store | `5432` |
| **Redis** | Celery task broker & result backend | `6379` |

---

## Getting Started

### Prerequisites

| Requirement | Version |
| :--- | :--- |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Latest |
| Git | ≥ 2.40 |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/e-Ray-Europa-GmbH/e.WAI2.git
cd e.WAI2

# 2. Start all services
docker compose up -d --build

# 3. Seed the database (first run only)
docker compose exec api python3 scripts/ingest_historic_v2.py
```

The application will be running at **[http://localhost](http://localhost)**.

### Configuration

Copy the environment template and populate the required values:

```bash
cp server/.env.example server/.env
```

| Variable | Description | Required |
| :--- | :--- | :---: |
| `GROQ_API_KEY` | Groq API key for Llama 3.3 PDF extraction | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `REDIS_URL` | Redis connection string | ✅ |
| `SECRET_KEY` | Flask session secret | ✅ |

> [!IMPORTANT]
> PDF extraction will not function without a valid `GROQ_API_KEY`.  
> Contact the team or refer to [DEPLOYMENT_TEAM.md](./DEPLOYMENT_TEAM.md) for the full secrets template.

---

## Local Development

For rapid backend iteration without a full Docker stack:

```bash
# Create and activate a virtual environment
py -3.14 -m venv myvenv          # Windows
myvenv\Scripts\activate

# Install backend dependencies
pip install -r server/requirements.txt

# Install frontend dependencies
cd myapp && npm install && cd ..
```

Run all services in four separate terminals:

| Terminal | Service | Command |
| :---: | :--- | :--- |
| 1 | Database + Redis | `docker compose up -d db redis` |
| 2 | Celery Worker | `celery -A ewai_api.celery_app worker --loglevel=info` |
| 3 | Flask API | `python3 server/app.py` |
| 4 | Vite Frontend | `cd myapp && npm run dev` |

> [!TIP]
> Run `bash start_local.sh` to launch all four processes automatically.

---

## Usage

1. Open [http://localhost](http://localhost) in your browser
2. Upload an environmental PDF report via the **Chat** panel
3. The Celery worker processes the file asynchronously — progress is shown in the UI
4. Once complete, sampling-point **markers appear on the Map** tab
5. Click any marker to inspect the full parameter breakdown
6. Use **Compare Areas** to run side-by-side analysis across stations

---

## Common Commands

```bash
# Start / stop the full stack
docker compose up -d
docker compose down

# Live service logs
docker logs ewai-api-1 -f
docker logs ewai-worker-1 -f

# Run a one-off server-side script
docker compose exec api python3 <script.py>

# Clean up stopped containers and dangling images
docker system prune -f
```

---

## Contributing

We welcome contributions from all team members. Please read the guidelines before opening a pull request.

> [!NOTE]
> **All changes must go through a reviewed Pull Request. Direct commits to `main` are not permitted.**

### Branch Workflow

```bash
git checkout main && git pull origin main
git checkout -b feat/<your-feature-name>
# ... make changes ...
git commit -m "feat(scope): short description"
git push -u origin feat/<your-feature-name>
# → Open a Pull Request on GitHub targeting main
```

### Versioning

Releases are fully automated via [semantic-release](https://semantic-release.gitbook.io/). Your **merge commit prefix** determines the version bump:

| Commit Prefix | Release Type | Example |
| :--- | :--- | :--- |
| `feat:` | Minor — new feature | `1.0.0 → 1.1.0` |
| `fix:` | Patch — bug fix | `1.0.0 → 1.0.1` |
| `chore:` / `docs:` | No release | — |
| `BREAKING CHANGE:` | Major | `1.0.0 → 2.0.0` |

📖 **[Read the full DevOps & PR Guide →](./docs/devops.md)**

---

## Further Reading

| Document | Description |
| :--- | :--- |
| [**DevOps & PR Guide**](./docs/devops.md) | Branch workflow, commit conventions, CI/CD, environment setup |
| [**Deployment Team Guide**](./DEPLOYMENT_TEAM.md) | SSL, database administration, production configuration |
| [**Changelog**](./CHANGELOG.md) | Full release history |

---

<div align="center">

**e.Ray Europa GmbH** · Smart Environmental Solutions  
© 2026 e.Ray Europa GmbH · All rights reserved

</div>
