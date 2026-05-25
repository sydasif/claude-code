# Python Core Style & Toolchain

## Required Toolchain

| Tool        | Purpose                               |
| ----------- | ------------------------------------- |
| `uv`        | Environment management + dependencies |
| `ruff`      | Linting + formatting                  |
| `mypy`      | Static type checking                  |
| `pytest`    | Test runner                           |
| `bandit`    | Security linting                      |
| `safety`    | Dependency vulnerability scanning     |
| `uv-secure` | Project dependency security scanning  |

## Standard Workflow

Ruff linting and formatting apply automatically to edited Python files via a `PostToolUse` hook.

```bash
uv sync                        # Install dependencies
uv run ruff check --fix .      # Lint and auto-fix
uv run ruff format .           # Format code
uv run mypy src/               # Type check (strict)
uv run pytest                  # Run tests
uv run bandit -r src/          # Security analysis
uv run safety check            # Dependency security
uv run uv-secure scan          # Project security scanning
```

## Security Scans

- `safety`: Medium+ severity = blocking. Halt until user confirms.
- `bandit`: HIGH severity or HIGH confidence = blocking. Report others.
- `uv-secure`: Any vulnerability = blocking. Halt until user confirms.

## Naming Conventions (PEP 8)

| Element                       | Convention            |
| ----------------------------- | --------------------- |
| Functions, variables, modules | `snake_case`          |
| Classes, exceptions           | `PascalCase`          |
| Constants                     | `UPPER_CASE`          |
| Private attributes            | `_leading_underscore` |

## Import Organization

1. Standard library
2. Third-party
3. Local application

Blank lines between groups. Absolute imports preferred. Prefer `from module import name` over `import module.name`.

## Modern Python Basics

- f-strings over `%`/`.format()`
- `pathlib` over `os.path`
- `@dataclass` for simple data containers
- `@dataclass(frozen=True)` for immutable data containers
- `match`/`case` for long `if/elif` chains (3.10+)
- Walrus operator `:=` where it clarifies
- Context managers for all resources

## Dependency Management

Use `uv`. No direct `pip install`. Use `pyproject.toml` and `uv.lock`. Update via `uv lock --upgrade`. Remove unused dependencies.

## CI/CD Integration

Canonical workflow file: `~/.claude/templates/ci-python.yml` — copy to `.github/workflows/ci.yml` in the project.

### Pre-commit

Install hooks once per clone:

```bash
uv run pre-commit install
```

Run hooks on all files:

```bash
uv run pre-commit run --all-files
```
