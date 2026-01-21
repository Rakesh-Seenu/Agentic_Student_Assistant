# ==========================================
# Multi-Stage Build for Optimizing Size
# ==========================================

# --- Stage 1: Builder ---
FROM python:3.10-slim AS builder

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency definition
COPY pyproject.toml uv.lock ./

# Install dependencies (no project) to .venv
# --compile bytecode for faster startup
RUN uv sync --frozen --no-install-project --compile-bytecode

# --- Stage 2: Runner ---
FROM python:3.10-slim AS runner

WORKDIR /app

# Copy the virtual environment from builder
# This excludes all build tools and caches, making image smaller
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

# Railway-compatible entrypoint
CMD uvicorn app.backend.main:app --host 0.0.0.0 --port ${PORT}
