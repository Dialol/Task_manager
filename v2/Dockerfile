# Stage 1: Builder
FROM python:3.11-slim AS builder

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync

# Stage 2: Final image
FROM python:3.11-slim

RUN pip install uv

# Set working directory
WORKDIR /app

# Copy installed dependencies and application code from builder stage
COPY --from=builder /app/.venv /app/.venv
COPY . /app

# Set environment variable for uv to use the installed virtual environment
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
