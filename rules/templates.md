---
name: templates
description: Project templates available for scaffolding new Python projects
---

# Templates

Ready-to-use project templates. Each file shows the complete content inside code fences — copy it into your project and customize.

These files are **not** auto-loaded (they'd bloat every session). Reference them on demand.

## Available Templates

| Template                | File                              | Purpose                                                             |
| ----------------------- | --------------------------------- | ------------------------------------------------------------------- |
| pyproject.toml          | `@templates/pyproject-toml.md`    | Project config with ruff, mypy, pytest, coverage, bandit, uv-secure |
| README.md               | `@templates/readme-structure.md`  | Standard project README with dev and testing sections               |
| .pre-commit-config.yaml | `@templates/pre-commit-config.md` | Pre-commit hooks for ruff, mypy, bandit, safety, pytest             |
| GitHub Actions CI       | `@templates/github-actions-ci.md` | CI/CD pipeline with lint, test, security, and build jobs            |

## Quick Start for a New Project

```bash
# 1. Initialize project
uv init my-project
cd my-project

# 2. Copy pyproject.toml template (from @templates/pyproject-toml.md)
# 3. Copy pre-commit config template (from @templates/pre-commit-config.md)
# 4. Copy CI workflow template to .github/workflows/ci.yml (from @templates/github-actions-ci.md)
# 5. Copy README template (from @templates/readme-structure.md)

# 6. Install dependencies
uv sync --all-extras --dev

# 7. Install pre-commit hooks
uv run pre-commit install

# 8. Run all checks
uv run pre-commit run --all-files
```

## See Also

- `@rules/python-style.md` — Python toolchain and style rules
- `@rules/python-testing.md` — Testing patterns and coverage thresholds
