---
name: readme-structure
description: Standard README template with dev setup, testing sections for Python projects using uv
---

# Project Name

Brief project description.

## Features

- Feature 1
- Feature 2

## Requirements

- Python 3.10+
- uv

## Installation

```bash
uv sync
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras --dev

# Run linter
uv run ruff check .

# Run formatter
uv run ruff format .

# Run type checker
uv run mypy src/

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-branch
```

## Usage

```python
from my_project import main

main()
```

## Testing

Run all tests:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=src --cov-report=html
```

## License

MIT
