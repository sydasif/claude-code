# Python Development Best Practices

Python-specific patterns and standards. For API, database, and documentation details, use the other files in this `reference/` directory.

## Modern Python Standards (3.12+)

- Use **type hints** for all public function signatures and when clarity improves code understanding
- Prefer **f-strings** for string formatting
- Use **pathlib** for path manipulation
- Implement **async/await** patterns for I/O operations
- Use **dataclasses** for simple data structures
- Prefer **pydantic** for data validation

## Code Quality Requirements

### Type Hints - Pragmatic Approach

**REQUIRED:**

- Public API functions (in `__all__`)
- Functions with 2+ parameters
- Non-obvious return types
- Library/package code

**OPTIONAL:**

- Private functions with obvious signatures
- Lambda functions
- Simple property getters/setters
- `__init__` methods (use `@dataclass` instead)
- Script-level code

**Examples:**

```python
# ❌ Low value - obvious from name
def is_valid(email: str) -> bool:
    return "@" in email

# ✅ High value - complex signature
def transform_records(
    records: Iterable[Dict[str, Any]],
    filters: Optional[List[Callable[[Dict], bool]]] = None,
    limit: int = 100
) -> Iterator[ProcessedRecord]:
    ...
```

- **Documentation**: Use Google-style docstrings
- **Security**: No hardcoded secrets
- **Performance**: Avoid unnecessary memory usage

## Package Management Guidelines

### Dependency Management - Tool Selection

#### Primary Recommendation: `uv`

- Fastest package installer (10-100x faster than pip)
- Built-in Python version management
- Compatible with pip/PyPI
- Use for: New projects, speed-critical workflows

#### Alternative: Poetry (if team already uses it)

- Mature, stable, large ecosystem
- Use for: Existing Poetry projects, team familiarity

#### Alternative: PDM (PEP 582)

- Standards-compliant
- Use for: Strict PEP adherence requirements

**Never Use:**

- Bare `pip` for project management (only for Docker/CI)
- `requirements.txt` without lock files

### Decision Tree

```text

Starting new project? → uv
Team already uses Poetry? → Poetry
Must follow PEPs exactly? → PDM
Simple script/prototype? → uv
```

## Performance Best Practices

- Use generators for large datasets: `(x for x in items if condition)`
- Use `itertools` for efficient iteration patterns
- Consider `functools.lru_cache` for expensive pure functions
- Use `collections.defaultdict` to avoid repeated key checking

## Async Programming Patterns

- Use `async`/`await` syntax for asynchronous operations
- Use `asyncio.gather()` for concurrent operations with error handling:

```python
async def safe_gather(*coroutines):
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
    return results
```

- Use `asyncio.create_task()` to schedule concurrent tasks
- Use `asyncio.timeout()` (Python 3.11+) or `asyncio.wait_for()` for timeouts
- Implement proper cleanup with async context managers: `async with`
- Avoid `asyncio.run()` in libraries; reserve for main entry points
- Use `asyncio.sleep()` instead of `time.sleep()` in async functions

## Framework Selection Guidelines

### Decision Tree

```text

What are you building?
├── API-first / Microservices → FastAPI
├── Full-stack web / CMS / Admin → Django
├── Simple / Script / Learning → Flask
├── AI/ML API serving → FastAPI
└── Background workers → Celery + any framework
```

## Type Hint Complexity Guidelines

**Use TypeAlias for complex types:**

```python
from typing import TypeAlias

Matrix: TypeAlias = list[list[float]]
JsonData: TypeAlias = dict[str, str | int | float | list | dict]
```

**Use TypedDict for dictionary structures:**

```python
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    email: str
```

**Use Protocol for interface definitions:**

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...
```

**Avoid overly complex type annotations that reduce readability.**

## Async vs Sync Decision Matrix

**Use ASYNC when:**

- Handling **10+ concurrent** I/O operations
- Building web APIs/servers
- Response time < 100ms required
- Integrating with async libraries

**Use SYNC when:**

- Sequential processing (< 10 operations)
- Simple CLI scripts
- Batch jobs (not latency-sensitive)
- CPU-bound operations
- Blocking libraries only

## Key Principles

- Always use `uv run`, `poetry run`, or `pdm run` to execute Python scripts
- Use virtual environments for project isolation
- Pin dependencies in lock files
- Scan dependencies for security vulnerabilities
