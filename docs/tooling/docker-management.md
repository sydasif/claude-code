# Multistage Dockerfile with UV for Python

## Basic Structure

```dockerfile
# Stage 1: Build dependencies
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as builder

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies to a virtual environment
RUN uv sync --frozen --no-cache

# Stage 2: Runtime
FROM debian:bookworm-slim

# Install uv for runtime
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Ensure we use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uv", "run", "python", "main.py"]
```

## Key Benefits

- **Smaller final image**: Build dependencies aren't included in the final image
- **Faster builds**: UV's speed advantage for dependency resolution
- **Better caching**: Dependency installation is cached separately from code changes
- **Security**: No build tools in production image

## Essential Commands

### UV Installation

```dockerfile
# Use UV's Python images directly
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Or install UV on minimal base
FROM debian:bookworm-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
```

### Dependency Management

```dockerfile
# Sync dependencies (equivalent to pip install)
RUN uv sync --frozen --no-cache

# For production-only dependencies
RUN uv sync --frozen --no-cache --no-dev
```

### Environment Variables

```dockerfile
# Use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Optional: Set UV cache directory
ENV UV_CACHE_DIR=/tmp/uv-cache
```

## Advanced Example

```dockerfile
# Build stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-dev

# Production stage (similar to basic structure, plus non‑root user)
# ... (full example in original file)
```
