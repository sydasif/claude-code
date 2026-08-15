# Explicit Error Handling

**Forbidden:** Bare `except:`, `except Exception:` without re‑raise or logging, `pass` in except without comment.

**Required:** Catch specific exceptions, `try/finally` or `with` for resources, `raise ... from original_exc`, log with context.

## Logging (No `print` in Production)

Use `logging` module. `logger = logging.getLogger(__name__)`. Use `logger.info()`, `.warning()`, `.error()`, `.debug()`.

Use `%`-style positional args in logging calls (`logger.info("User %s logged in", username)`) for lazy formatting. Do not use f‑strings in logging.

---

## Examples

### Catch specific exceptions

**Before:**

```python
try:
    risky()
except:  # catches KeyboardInterrupt, SystemExit — bad
    log("Failed")
```

**After:**

```python
import logging

logger = logging.getLogger(__name__)

try:
    risky()
except Exception as e:
    logger.exception("Failed: %s", e)
```

For targeted recovery, catch the exact type:

```python
try:
    risky()
except ValueError as e:
    handle_value_error(e)
except OSError as e:
    handle_io_error(e)
```

### Preserve cause with `raise ... from`

**Before** (original cause is lost in the traceback):

```python
try:
    config = json.loads(raw)
except json.JSONDecodeError:
    raise ConfigError("bad config")
```

**After** (chain the original exception):

```python
try:
    config = json.loads(raw)
except json.JSONDecodeError as e:
    raise ConfigError("bad config") from e
```

### Resource cleanup with `try/finally` → use `with`

**Before:**

```python
f = open(path)
try:
    data = f.read()
finally:
    f.close()
```

**After** (context manager — always closes, even on error):

```python
with open(path) as f:
    data = f.read()
```

### Logging, not `print`

**Before** (library code printing to stdout):

```python
def import_data(file_path):
    print(f"Loading {file_path}...")
    data = parse(file_path)
    print(f"Loaded {len(data)} records")
    return data
```

**After:**

```python
import logging

logger = logging.getLogger(__name__)

def import_data(file_path: Path) -> list[Record]:
    logger.info("Loading %s", file_path)
    data = parse(file_path)
    logger.info("Loaded %d records", len(data))
    return data
```

