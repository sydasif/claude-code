---
name: python-style
description: Python toolchain, style, and code review rules (single canonical source)
---

# Python Style & Toolchain

> Single canonical source — for all Python style and toolchain rules

---

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
| Pyright LSP | In-editor type hints (`pyright-lsp` in `settings.json`) |

When **pyright-lsp** is enabled, use IDE diagnostics while editing; still run `uv run mypy` (or the project’s configured checker) before marking work verified — LSP and CI checks can differ.

## Type Checker Selection

| Situation                                                             | Use                                                          |
| --------------------------------------------------------------------- | ------------------------------------------------------------ |
| New project, no existing type config                                  | `mypy --strict`                                              |
| Existing project already configured with `mypy`                       | Keep `mypy` — do not migrate mid-project                     |
| `mypy.ini` or `[tool.mypy]` in `pyproject.toml` present               | `mypy`                                                       |
| Using Pydantic v1, Django, SQLAlchemy legacy, Netmiko, NAPALM, NORNIR | Prefer `mypy`                                                |
| Using Pydantic v2, FastAPI, modern stdlib only                        | Either works; `mypy` preferred                               |
| Both configs present                                                  | Follow `pyproject.toml` — do not introduce the other checker |

Never add a second type checker to a project that already has one configured.

## Standard Workflow

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

```bash
uv run safety scan            # Check for vulnerable dependencies
uv run bandit -r src/         # Static security analysis
uv run uv-secure scan         # Project dependency scanning
```

- **safety scan**: Medium+ severity = blocking. Halt until user confirms.
- **bandit**: HIGH severity or HIGH confidence = blocking. Everything else = report, do not auto-fix.
- **uv-secure**: Any vulnerability = blocking. Halt until user confirms.
- Never suppress or ignore security scan output. If a known false positive, document why.

---

## Code Style Rules

### 1. Google-Style Docstrings (PEP 257)

All public modules, classes, and functions must have Google-style docstrings.

**Forbidden:** Missing docstrings on public entities. Sphinx/reST or NumPy style (unless reconfigured).

**Required:** Triple quotes, `Args:` section, `Returns:` section, `Raises:` section for known exceptions, module-level and class docstrings.

```python
def fetch_user(user_id: int) -> dict:
    """Fetches a user profile from the database.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        A dictionary containing the user's profile data.

    Raises:
        ValueError: If user_id is negative.
    """
    ...
```

### 2. Strict Type Hints (PEP 484, 526, 544)

**Forbidden:** Missing type hints, `Any` (unless justified), bare `list`/`dict`, mixing `Union[A, B]` and `A | B`.

**Required:** Full signatures, `T | None` for nullable (3.10+, prefer `|`), variable annotations, generic types, `Protocol`, `TypeVar`, `Literal`, `TypedDict`, `Final`, `NoReturn`.

### 3. No Print in Production

Use `logging` module.

**Forbidden:** `print()`, `pprint()`, `sys.stdout.write()`, `sys.stderr.write()` for app messages.

**Required:** `import logging; logger = logging.getLogger(__name__)`, use `logger.info()`, `.warning()`, `.error()`, `.debug()`.

### 4. Explicit Error Handling

**Forbidden:** Bare `except:`, `except Exception:` without re-raise or logging, `pass` in except without comment.

**Required:** Catch specific exceptions, `try/finally` or `with` for resources, `raise ... from original_exc`, log with context.

### 5. PEP 8 Naming

| Element                       | Convention            |
| ----------------------------- | --------------------- |
| Functions, variables, modules | `snake_case`          |
| Classes, exceptions           | `PascalCase`          |
| Constants                     | `UPPER_CASE`          |
| Private attributes            | `_leading_underscore` |

### 6. Import Organization

1. Standard library
2. Third-party
3. Local application

Blank lines between groups. Absolute imports preferred. `from module import name` over `import module.name`.

### 7. Modern Python

- f-strings over `%`/`.format()`
- `pathlib` over `os.path`
- `@dataclass` for simple data containers
- `@dataclass(frozen=True)` for immutable data containers
- `match`/`case` for long `if/elif` chains over a single variable (3.10+)
- Walrus operator `:=` where it clarifies
- Context managers for all resources
- `typing.Self` for method chaining (3.11+)
- `typing.Protocol` for structural typing
- `typing.NotRequired`/`typing.Required` for TypedDict (3.11+)

### 8. Async Patterns

`async`/`await`, `asyncio.gather()` for concurrency, `asyncio.create_task()`, `asyncio.timeout()` (3.11+), `async with` for cleanup. Never `asyncio.run()` in libraries.

### 9. Security

**Forbidden:** Hardcoded secrets, `eval()`/`exec()` with user input, unsanitized SQL, pickle from untrusted sources.

**Required:** Env vars for secrets, parameterized queries, input validation, bcrypt/Argon2 for passwords.
Use `secrets` module for cryptographic operations.
Use `subprocess.run([...], shell=False)` for shell commands.

### 10. Performance

Generators for large data, `itertools`, `functools.lru_cache`, `collections.defaultdict`.
Use `str.join()` for string concatenation in loops.
Use `set` for membership testing when appropriate.
Leverage `heapq` for priority queues.
Use `Counter` for counting hashable objects.

### 11. Dependency Management

Use `uv`. No direct `pip install`. Use `pyproject.toml`. Pin in `uv.lock`.
Regularly update dependencies with `uv lock --upgrade`.
Remove unused dependencies.

---

## Framework-Specific Guidelines

### FastAPI / Pydantic v2

- Use `async def` for all route handlers to leverage concurrency
- Leverage Pydantic v2 models for request/response validation (`BaseModel`)
- Use `Depends()` for dependency injection (DB sessions, auth, config)
- Structure projects: `app/routers/`, `app/schemas/`, `app/services/`, `app/models/`
- Use `APIRouter` prefix with versioning (`/api/v1/...`)
- Prefer `SQLModel` or `SQLAlchemy 2.0` async for database access
- Configure CORS explicitly in production

### Django

- Keep business logic out of views — use services or model methods
- Use `select_related()` / `prefetch_related()` to avoid N+1 queries
- Write model `Meta` classes with `indexes`, `ordering`, `constraints`
- Use Django REST Framework (DRF) or `ninja` for API endpoints
- Configure `DATABASES` with connection pooling (e.g., `psycopg2` pool or `asyncpg`)
- Set `DEBUG=False`, configure `ALLOWED_HOSTS`, use HTTPS in production

### Flask

- Use `flask-smorest` or `flask-apispec` for OpenAPI docs and validation
- Prefer application factory pattern: `create_app()` function
- Keep config in `instance/` folder or env vars via `python-dotenv`
- Use `SQLAlchemy` with Flask-Migrate (Alembic) for database changes

---

## Python Version Requirements

- **Minimum**: Python 3.10+ (enforce via `requires-python = ">=3.10"` in pyproject.toml)
- **Target**: Python 3.12+ for new projects (faster, better error messages, improved typing)
- **CI matrix**: Test against >=3.10, <=3.13 to ensure compatibility
- **Version pin**: Use `.python-version` file at project root with a single version
- **EOL policy**: Drop support when upstream reaches end-of-life

### Version-Specific Features to Use

| Python | Key features to leverage                                          |
| ------ | ----------------------------------------------------------------- |
| 3.10   | `match`/`case`, `X \| Y` union syntax, `TypeGuard`, `kw_only` dataclasses |
| 3.11   | `Self` type, `Never`, `@dataclass(slots=True)`, `asyncio.TaskGroup` |
| 3.12   | `@override`, `type` statement, `typing.Unpack`, perf improvements |
| 3.13   | Free-threaded mode (experimental), JIT compiler, improved `locals()` |

---

## CI/CD Integration

### Standard Workflow (GitHub Actions)

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
