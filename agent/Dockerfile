# Use official Python runtime as base image
FROM python:3.11-slim AS builder

# Install Poetry
RUN pip install poetry==2.1.1

# Set working directory
WORKDIR /app

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies into a virtual environment
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --only main

# Final stage: runtime image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy virtual environment and app code from builder
COPY --from=builder /app/.venv ./.venv
COPY . .

# Ensure virtual environment is in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port (default 8000, configurable via .env)
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "agent.demo:app", "--host", "0.0.0.0", "--port", "8000"]
