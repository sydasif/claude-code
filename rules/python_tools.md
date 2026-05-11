# Python Toolchain Rules

## Required Stack

| Tool      | Purpose                                                                 |
| --------- | ----------------------------------------------------------------------- |
| `uv`      | Environment management + dependencies                                   |
| `ruff`    | Linting + formatting                                                    |
| `pyright` | Static type checking — new projects                                     |
| `mypy`    | Static type checking — existing projects or legacy library dependencies |
| `pytest`  | Test runner                                                             |

## Type Checker Selection

Before running type checks, determine which checker the project uses:

| Situation                                                             | Use                                                          |
| --------------------------------------------------------------------- | ------------------------------------------------------------ |
| New project, no existing type config                                  | `pyright --strict`                                           |
| Existing project already configured with `mypy`                       | Keep `mypy` — do not migrate mid-project                     |
| `pyrightconfig.json` present                                          | `pyright`                                                    |
| `mypy.ini` or `[tool.mypy]` in `pyproject.toml` present               | `mypy`                                                       |
| Using Pydantic v1, Django, SQLAlchemy legacy, Netmiko, NAPALM, NORNIR | Prefer `mypy` — pyright stub coverage is thinner for these   |
| Using Pydantic v2, FastAPI, modern stdlib only                        | Either works; `pyright` preferred                            |
| Both configs present                                                  | Follow `pyproject.toml` — do not introduce the other checker |

**Rule:** Never add a second type checker to a project that already has one configured. Resolve the checker choice in Discovery and stick to it for the entire task.

## Standard Workflow

```bash
uv sync                        # Install dependencies
uv run ruff check --fix .      # Lint and auto-fix
uv run ruff format .           # Format code

# New projects
uv run pyright src/            # Type check (strict)

# Existing projects
uv run mypy src/               # Type check

uv run pytest                  # Run tests
```

## Security Scans

```bash
uv run safety check            # Check for vulnerable dependencies
uv run bandit -r src/          # Static security analysis
```

### Security Scan Output Handling

- **`safety check` findings:** Any vulnerability rated medium or above is a **blocking issue**. Report it in the Discovery Report under Assumptions & Risks and halt until the user confirms how to proceed. Low-severity findings are reported but do not block.
- **`bandit` findings:** Severity HIGH or confidence HIGH = blocking. Everything else = report in the output structure under Assumptions & Risks, do not auto-fix.
- Never suppress or ignore security scan output. If a finding is a known false positive, document why explicitly.

---

## See Also

- `rules/testing_rules.md` — Test patterns, coverage thresholds
