---
name: code-refactor
description: Modernize legacy Python code with best practices, type hints, and efficient patterns.
---

# Python Refactoring Specialist

> **Prerequisite**: Run the `code-cleanup` skill before this one if the codebase hasn't been pruned recently.
> This skill modernizes code that _should exist_ — not code that should be deleted.
> Cleanup first, refactor second.

This skill transforms legacy Python code into modern, maintainable, and efficient implementations following current best practices.

> If `guidelines`, are missing, treat those as informational placeholders and apply your team's conventions directly.

- For comprehensive Python best practices, see [Python Guidelines](../python-pro/reference/python.md)

---

## Refactoring Process

### 1. Assessment

1. Identify legacy patterns in the code
2. Prioritize refactoring based on impact and risk
3. Check for existing tests — ensure they exist and pass before refactoring anything

### 2. Safe Refactoring Steps

1. Run existing tests to establish a baseline
2. Apply one refactoring pattern at a time
3. Run tests after each change
4. Verify functionality remains identical

### 3. Modernization Checklist

**String and data handling**

- [ ] All string formatting uses f-strings (replace `%` and `.format()`)
- [ ] Path operations use `pathlib` (replace `os.path.*`)
- [ ] Config parsing uses `tomllib` (3.11+) or `tomli` where `configparser` is overkill

**Type system**

- [ ] Function signatures have type hints on inputs and return values
- [ ] Keyword-only arguments used where callers should not rely on positional order
- [ ] `TypedDict` or dataclasses used for structured dicts passed between functions

**Classes and data structures**

- [ ] Simple attribute-only classes replaced with `@dataclass`
- [ ] Boilerplate methods (`__init__`, `__repr__`, `__eq__`) removed where dataclass covers them
- [ ] `__slots__` added to hot-path dataclasses where memory efficiency matters

**Control flow**

- [ ] Long `if/elif` chains over a single variable replaced with `match` statements (Python 3.10+)
- [ ] Complex lambda functions moved to named functions
- [ ] Iterations use appropriate patterns: `enumerate`, list/dict/set comprehensions, `zip`

**Resource and error handling**

- [ ] Context managers handle all file, socket, and connection resources
- [ ] Exception handling is specific — no bare `except:` or `except Exception:` without re-raise
- [ ] `print` statements for diagnostics replaced with `logging` calls at appropriate levels

**Async (if applicable)**

- [ ] `asyncio` patterns are consistent — no mixing of sync blocking calls inside async functions
- [ ] `async with` and `async for` used where available on async-capable resources

**Imports**

- [ ] Imports organized in standard groups: stdlib → third-party → local
- [ ] No unused imports (should already be clear after `code-cleanup` pass)

---

## Quality Assurance

For detailed tool commands, see `CLAUDE.md`.

### Before Refactoring

Run type checking, linting, and tests to establish baseline:

```
mypy <target>
ruff check <target>   # or flake8
pytest --tb=short
pytest --cov=<target> --cov-report=term-missing
```

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

### Scenario 4: Migrate to match statements

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

---

Use this skill to modernize legacy Python code into clean, maintainable, and efficient implementations using contemporary Python features and best practices — after the codebase has been pruned with `code-cleanup`.
