# Python Type Hints

## Strict Type Hint Rules

**Forbidden:** Missing type hints, `Any` (unless justified), bare `list`/`dict`, mixing `Union[A, B]` and `A | B`.

**Required:** Full signatures, `T | None` for nullable (3.10+, prefer `|`), variable annotations, generic types, `Protocol`, `TypeVar`, `Literal`, `TypedDict`, `Final`, `NoReturn`, `Self` (3.11+), `NotRequired`/`Required` for `TypedDict` (3.11+).

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

`pyright-lsp` (editor) and `mypy` (CI) may disagree. `mypy` output is authoritative for CI and pre-merge verification.
