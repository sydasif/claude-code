---
name: pre-commit-config
description: Pre-commit hooks for ruff, mypy, bandit, safety, pytest
---

# .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        args: [--strict, src/]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.10
    hooks:
      - id: bandit
        args: [-r, src/]

  - repo: https://github.com/pyupio/safety
    rev: 3.2.0
    hooks:
      - id: safety
```

## Install

```bash
pip install pre-commit
pre-commit install
```

## Usage

```bash
pre-commit run --all-files
pre-commit autoupdate
```
