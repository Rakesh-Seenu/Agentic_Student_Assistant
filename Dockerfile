# ==========================================
# Single-Stage Build (Corrected)
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy all files at once
COPY . .

# Install dependencies into .venv
# Note: uv sync automatically creates .venv in the project root
# We clean up caches to save space
RUN uv sync --frozen && \
    rm -rf /root/.cache && \
    rm -rf /root/.local

# Set path to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

# Run FastAPI
CMD uvicorn app.backend.main:app --host 0.0.0.0 --port ${PORT}
