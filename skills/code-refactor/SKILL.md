---
name: code-refactor
description: Modernize legacy Python code with best practices, type hints, and efficient patterns. Use when asked to refactor, modernize, or update Python code.
---

# Python Refactoring Specialist

> **Prerequisite**: Run the `code-cleanup` skill before this one if the codebase hasn't been pruned recently.
> This skill modernizes code that _should exist_ — not code that should be deleted.
> Cleanup first, refactor second.

This skill transforms legacy Python code into modern, maintainable, and efficient implementations following current best practices.

> **Style and toolchain:** `rules/python-style.md` (auto-loaded). Project `CLAUDE.md` or `AGENTS.md` overrides global rules.

---

## Refactoring Process

### 1. Assessment

1. **Check the project's minimum supported Python version** before applying any version-gated pattern. Look in `pyproject.toml`, `setup.cfg`, `.python-version`, or CI config (e.g., `python-version` matrix in `.github/workflows/`). Only apply features available at or below that floor — do not use `match` statements on a 3.9 codebase, `tomllib` below 3.11, etc.
2. **Inventory legacy patterns** using the Modernization Checklist below as your scanning tool. For each item, flag it as: _applies and safe_, _applies but needs version check_, or _not present_.
3. Prioritize refactoring based on impact and risk.
4. Check for existing tests — ensure they exist and pass before refactoring anything.

### 2. When to Skip a Modernization

Not every pattern needs updating. Skip a change if:

- The existing code is already clear, short, and readable — changing it adds ceremony without aiding comprehension or safety.
- The change is version-gated and the project's minimum Python version is too low.
- The file is generated, a one-off migration script, or otherwise unlikely to be maintained.
- The abstraction introduced (e.g., a dataclass for a two-field struct) is heavier than the code it replaces.

Apply modernization where it reduces noise, improves safety, or makes intent clearer — not as a mechanical sweep.

### 3. Safe Refactoring Steps

1. Run existing tests to establish a baseline.
2. For large codebases with many mechanical changes (f-strings, pathlib, import ordering), consider running automated tools first — `pyupgrade`, `ruff --fix`, or `python-modernize` — to handle bulk transformations safely. Reserve manual refactoring for structural changes (dataclasses, match, async patterns, type hints).
3. Apply one refactoring pattern at a time.
4. Run tests after each change.
5. Verify functionality remains identical.

### 4. Modernization Checklist

**String and data handling**

- [ ] Replace `%` and `.format()` string formatting with f-strings
- [ ] Replace `os.path.*` path operations with `pathlib`
- [ ] Replace `configparser` with `tomllib` (3.11+) or `tomli` where appropriate

**Type system**

- [ ] Add type hints to function signatures (inputs and return values)
- [ ] Use keyword-only arguments where callers should not rely on positional order
- [ ] Replace structured dicts passed between functions with `TypedDict` or dataclasses

**Classes and data structures**

- [ ] Replace simple attribute-only classes with `@dataclass`
- [ ] Remove boilerplate methods (`__init__`, `__repr__`, `__eq__`) where dataclass covers them
- [ ] Add `__slots__` to hot-path dataclasses where memory efficiency matters

**Control flow**

- [ ] Replace long `if/elif` chains over a single variable with `match` statements (Python 3.10+ only)
- [ ] Move complex lambda functions to named functions
- [ ] Use appropriate iteration patterns: `enumerate`, list/dict/set comprehensions, `zip`

**Resource and error handling**

- [ ] Use context managers for all file, socket, and connection resources
- [ ] Replace bare `except:` or `except Exception:` without re-raise with specific exception types
- [ ] Replace diagnostic `print` statements with `logging` calls at appropriate levels

**Async (if applicable)**

- [ ] Use consistent `asyncio` patterns — no sync blocking calls (e.g., `time.sleep`, `open()`) inside async functions
- [ ] Use `async with` and `async for` where available on async-capable resources
- [ ] Await all coroutines — unawaited coroutines silently do nothing
- [ ] Use `asyncio.gather()` for concurrent independent tasks instead of sequential `await` calls
- [ ] Replace `asyncio.sleep(0)` busy-loops with proper event-driven patterns

**Imports**

- [ ] Organize imports in standard groups: stdlib → third-party → local
- [ ] Remove unused imports (should already be clear after `code-cleanup` pass)

---

## Quality Assurance

For detailed tool commands, see `CLAUDE.md` if present in the project root; otherwise use the defaults below.

### Before Refactoring

Run type checking, linting, and tests to establish baseline (from project root; use `uv run` when `pyproject.toml` exists):

```sh
uv run mypy src/
uv run ruff check .
uv run pytest --tb=short
uv run pytest --cov=src --cov-report=term-missing
```

If the project has no `uv`/`pyproject.toml`, use commands from the project README instead.

Record the baseline pass/fail counts. Any test that was already failing before refactoring is not your regression to fix — flag it and leave it.

### After Refactoring

Verify refactored code passes all checks:

- Type checking (no new mypy errors)
- Linting (no new lint violations)
- Unit tests (same or better pass rate as baseline)
- Coverage (no meaningful drop from baseline)

---

## Common Refactoring Scenarios

### Scenario 1: Migrate to f-strings

```python
# Before
msg = "Host %s unreachable after %d retries" % (host, retries)
msg = "Host {} unreachable after {} retries".format(host, retries)

# After
msg = f"Host {host} unreachable after {retries} retries"

# Preserve alignment options where needed
msg = f"{'Interface':<20} {'Status':>10}"
```

### Scenario 2: Migrate to dataclasses

```python
# Before
class DeviceInfo:
    def __init__(self, hostname, ip, platform):
        self.hostname = hostname
        self.ip = ip
        self.platform = platform

    def __repr__(self):
        return f"DeviceInfo({self.hostname}, {self.ip}, {self.platform})"

# After
from dataclasses import dataclass

@dataclass
class DeviceInfo:
    hostname: str
    ip: str
    platform: str
```

### Scenario 3: Migrate to pathlib

```python
# Before
import os
config_path = os.path.join(base_dir, "config", "devices.yaml")
if os.path.exists(config_path):
    with open(config_path) as f:
        ...

# After
from pathlib import Path
config_path = Path(base_dir) / "config" / "devices.yaml"
if config_path.exists():
    with config_path.open() as f:
        ...
```

### Scenario 4: Migrate to match statements (Python 3.10+ only)

```python
# Before
if platform == "ios":
    driver = IOSDriver()
elif platform == "eos":
    driver = EOSDriver()
elif platform == "nxos":
    driver = NXOSDriver()
else:
    raise ValueError(f"Unknown platform: {platform}")

# After (Python 3.10+)
match platform:
    case "ios":
        driver = IOSDriver()
    case "eos":
        driver = EOSDriver()
    case "nxos":
        driver = NXOSDriver()
    case _:
        raise ValueError(f"Unknown platform: {platform}")
```

### Scenario 5: Replace print with logging

```python
# Before
print(f"Connecting to {host}...")
print(f"ERROR: timeout on {host}")

# After
import logging
logger = logging.getLogger(__name__)

logger.debug("Connecting to %s", host)
logger.error("Timeout on %s", host)
```

> **Why `%`-style args in logging, not f-strings?** The logging module uses lazy formatting — the string is only interpolated if the log level is actually active. With f-strings, the interpolation happens unconditionally at the call site, even if the message is never emitted. Use `%`-style positional args (`"msg %s", value`) in all `logger.*` calls.

---

Use this skill to modernize legacy Python code into clean, maintainable, and efficient implementations using contemporary Python features and best practices — after the codebase has been pruned with `code-cleanup`.

## See Also

- `rules/python-style.md` — Toolchain, typing, security scans
- `code-cleanup` skill — Run this first to prune dead code before refactoring
- `code-review` skill — For final gate review after refactoring
