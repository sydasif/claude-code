---
name: refactor-code
description: Use when asked to refactor, modernize, or update Python code with type hints, dataclasses, pathlib, f-strings, or other best practices. Run cleanup-code first to prune dead code.
allowed-tools:
  - "Bash(uv:*)"
  - "Bash(pyupgrade:*)"
  - "Bash(ruff:*)"
  - "Bash(pytest:*)"
  - "Bash(mypy:*)"
---

# Python Refactoring Specialist

> Prune with `cleanup-code` before refactoring. Refactor code that _should exist_ - not code that should be deleted.

## Refactoring Process

### 1. Assessment

1. **Check minimum Python version** - Look in `pyproject.toml`, `setup.cfg`, `.python-version`, or CI config. Only apply features available at or below that floor.
2. **Inventory legacy patterns** - For each checklist item, flag: _applies and safe_, _applies but needs version check_, or _not present_.
3. **Check existing tests** - Ensure they exist and pass before refactoring.

### 2. When to Skip

Skip if: code is already clear/short, change is version-gated, file is generated/one-off, or abstraction is heavier than what it replaces.

### 3. Safe Steps

1. Run tests to establish baseline.
2. For bulk mechanical changes, run `pyupgrade`/`ruff --fix` first. Reserve manual work for structural changes.
3. Apply one pattern at a time. Run tests after each.
4. Verify functionality remains identical.

### 4. Quality Assurance

Before: run `uv run mypy src/`, `uv run ruff check .`, `uv run pytest --tb=short`, `uv run pytest --cov=src --cov-report=term-missing`. Record baseline. Flag existing failures as non-regressions.

After: no new mypy errors, no new lint violations, same or better test pass rate, coverage matches baseline.

For modernization checklists, read `references/checklist.md`. For code examples, read `references/scenarios.md`.

## See Also

- `cleanup-code` agent - Run first to prune dead code
- `review-code` skill - Final gate review after refactoring
