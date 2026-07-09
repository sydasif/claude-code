# Modernization Checklist

## Section 1: Type System

- [ ] Add type hints to function signatures (inputs and return values)
- [ ] Use keyword-only arguments where callers should not rely on positional order
- [ ] Replace structured dicts passed between functions with `TypedDict` or dataclasses

## Section 2: Syntax Modernization

- [ ] Replace `%` and `.format()` string formatting with f-strings
- [ ] Replace `os.path.*` path operations with `pathlib`
- [ ] Replace `configparser` with `tomllib` (3.11+) or `tomli` where appropriate
- [ ] Replace long `if/elif` chains over a single variable with `match` statements (Python 3.10+ only)

## Section 3: Structural Improvements

- [ ] Replace simple attribute-only classes with `@dataclass`
- [ ] Remove boilerplate methods (`__init__`, `__repr__`, `__eq__`) where dataclass covers them
- [ ] Add `__slots__` to hot-path dataclasses where memory efficiency matters
- [ ] Move complex lambda functions to named functions
- [ ] Use appropriate iteration patterns: `enumerate`, list/dict/set comprehensions, `zip`
- [ ] Use context managers for all file, socket, and connection resources
- [ ] Replace bare `except:` or `except Exception:` without re-raise with specific exception types
- [ ] Replace diagnostic `print` statements with `logging` calls at appropriate levels

## Async (if applicable)

- [ ] Use consistent `asyncio` patterns - no sync blocking calls (e.g., `time.sleep`, `open()`) inside async functions
- [ ] Use `async with` and `async for` where available on async-capable resources
- [ ] Await all coroutines - unawaited coroutines do nothing
- [ ] Use `asyncio.gather()` for concurrent independent tasks instead of sequential `await` calls
- [ ] Replace `asyncio.sleep(0)` busy-loops with proper event-driven patterns

## Imports

- [ ] Organize imports in standard groups: stdlib -> third-party -> local
- [ ] Remove unused imports
