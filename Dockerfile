# syntax=docker/dockerfile:1.6

# Base image with Python 3.13 (slim for smaller footprint)
FROM python:3.13-slim

# Avoid interactive tzdata prompts and Python .pyc files in container
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install system dependencies commonly needed by deps:
# - curl/ca-certificates: install Poetry
# - build-essential: compile any wheels if needed
# - git: some libs may fetch extras
# - ffmpeg: used by yt-dlp at runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl ca-certificates \
        build-essential \
        git \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.1.4
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Workdir
WORKDIR /app

# Copy dependency manifests first for better build caching
COPY pyproject.toml poetry.lock README.md ./

# Install Python dependencies into the base env (no venv)
RUN poetry install --no-ansi --no-interaction --only main --no-root

# Now copy the rest of the application
COPY . .

# Default command is overridden by docker-compose; keep a sane default here
CMD ["uvicorn", "--reload", "application.main:app", "--host", "0.0.0.0", "--port", "8000"]
