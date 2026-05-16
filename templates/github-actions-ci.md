---
name: github-actions-ci
description: GitHub Actions CI/CD workflow for Python projects with uv, ruff, mypy, pytest, and security scanning
---

# .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  UV_CACHE_DIR: /tmp/.uv-cache

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
          cache-dependency-glob: "uv.lock"
      - name: Set up Python
        run: uv python install
      - name: Install dependencies
        run: uv sync --locked --all-extras --dev
      - name: Lint with ruff
        run: uv run ruff check .
      - name: Check formatting
        run: uv run ruff format --check .
      - name: Type check with mypy
        run: uv run mypy src/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v6
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
          cache-dependency-glob: "uv.lock"
      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}
      - name: Install dependencies
        run: uv sync --locked --all-extras --dev
      - name: Run tests
        run: uv run pytest --cov=src --cov-branch --cov-report=xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install uv
        uses: astral-sh/setup-uv@v5
      - name: Run security scans
        run: |
          uv sync --locked --dev
          uv run bandit -r src/
          uv run safety check
```
