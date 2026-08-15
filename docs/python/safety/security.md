# Python Security Rules

**Forbidden:**

- Hardcoded secrets
- `eval()` / `exec()` with user input
- Unsanitized SQL (use parameterized queries)
- `pickle` from untrusted sources
- Shell‑injection vectors in `subprocess` calls

**Required:**

- Environment variables for secrets
- Parameterized SQL queries
- Input validation
- bcrypt / Argon2 for passwords
- `secrets` module for cryptographic operations
- `subprocess.run([...], shell=False)`

## Additional Scans

```bash
uv run bandit -r src/         # Static security analysis
uv run safety check           # Dependency vulnerabilities
uv run uv-secure scan         # Project dependency security
```

---

## Examples

### Secrets — never hardcode, use env vars

**Before:**

```python
API_KEY = "sk_live_3f9a2b..."  # committed to source control — leaked
requests.get("/api", headers={"Authorization": f"Bearer {API_KEY}"})
```

**After:**

```python
import os

API_KEY = os.environ["API_KEY"]  # injected at runtime; never in VCS
requests.get("/api", headers={"Authorization": f"Bearer {API_KEY}"})
```

### SQL — parameterized queries

**Before** (string interpolation → injection vector):

```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

**After** (parameters bound by the driver):

```python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### `subprocess` — no shell, list args

**Before** (shell injection + quoting bugs):

```python
os.system(f"git log -1 {file_path}")
subprocess.run(f"ls {dir}", shell=True)
```

**After:**

```python
import subprocess

result = subprocess.run(
    ["git", "log", "-1", file_path],
    capture_output=True,
    text=True,
    check=True,
)
listing = subprocess.run(["ls", dir], shell=False, capture_output=True, check=True)
```

### Password hashing — bcrypt/argon2, never plaintext

**Before:**

```python
def store_user(password: str) -> None:
    db.save({"password": password})  # plaintext — catastrophic if leaked
```

**After:**

```python
import bcrypt

def store_user(password: str) -> None:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    db.save({"password_hash": hashed})

def verify_user(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)
```
