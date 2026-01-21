FROM python:3.10-slim

WORKDIR /app

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Railway uses PORT environment variable
ENV PORT=8000
EXPOSE ${PORT}

# Run FastAPI with dynamic port
CMD uvicorn app.backend.main:app --host 0.0.0.0 --port ${PORT}
