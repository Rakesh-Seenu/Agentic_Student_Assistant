# ==========================================
# Single-Stage Build (Optimized for Speed)
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy all files at once (Fastest)
COPY . .

# Install dependencies & Cleanup in ONE step to save space
# We use --system to install directly into the container python
# This avoids creating a huge .venv folder that needs management
RUN uv sync --frozen --system && \
    rm -rf /root/.cache && \
    rm -rf /root/.local && \
    rm -rf .venv

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

# Run FastAPI
CMD uvicorn app.backend.main:app --host 0.0.0.0 --port ${PORT}
