# API Design Best Practices

API design guidance for Python services. Use `python.md` for framework selection and `documentation.md` for documenting OpenAPI/Swagger output.

## RESTful Principles

### HTTP Methods

| Method | Action            | Idempotent | Safe |
| ------ | ----------------- | ---------- | ---- |
| GET    | Retrieve resource | Yes        | Yes  |
| POST   | Create resource   | No         | No   |
| PUT    | Replace resource  | Yes        | No   |
| PATCH  | Partial update    | No         | No   |
| DELETE | Remove resource   | Yes        | No   |

### URL Design

```text
# Good - Resource-oriented
collection:       /api/v1/users
single resource:  /api/v1/users/123
nested resource:  /api/v1/users/123/orders
filter:           /api/v1/users?status=active&role=admin
sort:             /api/v1/users?sort=-created_at,name
pagination:       /api/v1/users?page=2&limit=20

# Avoid - Action-oriented
/api/v1/getUser
/api/v1/createOrder
/api/v1/deleteProduct
```

### Resource Naming

- Use nouns, not verbs
- Use plural form
- Use kebab-case for multi-word names
- Keep URLs short and meaningful

```python
# Good
GET /api/v1/order-items
POST /api/v1/shopping-carts

# Avoid
GET /api/v1/getOrderItems
POST /api/v1/createShoppingCart
GET /api/v1/orderItems
```

## Request/Response Format

### Standard Response Structure

```json
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### HTTP Status Codes

| Code | Meaning           | Use Case                   |
| ---- | ----------------- | -------------------------- |
| 200  | OK                | Successful GET, PUT, PATCH |
| 201  | Created           | Successful POST            |
| 204  | No Content        | Successful DELETE          |
| 400  | Bad Request       | Validation error           |
| 401  | Unauthorized      | Missing/invalid auth       |
| 403  | Forbidden         | No permission              |
| 404  | Not Found         | Resource doesn't exist     |
| 409  | Conflict          | Resource already exists    |
| 422  | Unprocessable     | Business logic error       |
| 429  | Too Many Requests | Rate limit exceeded        |
| 500  | Server Error      | Unexpected error           |

## API Versioning

### Versioning Strategies

1. **URL Path** (Recommended)

   ```text
   /api/v1/users
   /api/v2/users
   ```

2. **Header**

   ```text
   Accept: application/vnd.api+json;version=1
   X-API-Version: 2
   ```

3. **Query Parameter**

   ```text
   /api/users?version=2
   ```

### Versioning Best Practices

- Maintain at least 2 versions
- Deprecate gracefully with warnings
- Document breaking changes
- Use semantic versioning principles

```python
# FastAPI example with versioning
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI()

@app.get("/users")
@version(1)
async def get_users_v1():
    return {"users": [...], "version": 1}

@app.get("/users")
@version(2)
async def get_users_v2():
    return {"data": [...], "meta": {...}, "version": 2}

app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')
```

## Authentication & Authorization

### Authentication Methods

1. **API Keys** - Simple, good for service-to-service
2. **JWT Tokens** - Stateless, scalable
3. **OAuth 2.0** - Third-party integration
4. **Session Cookies** - Traditional web apps

### JWT Implementation

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user)):
    return {"message": f"Hello user {user_id}"}
```

### Permission Patterns

```python
from functools import wraps
from fastapi import HTTPException

def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user=Depends(get_current_user), **kwargs):
            if permission not in user.permissions:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@app.delete("/users/{user_id}")
@require_permission("users:delete")
async def delete_user(user_id: str, user=Depends(get_current_user)):
    # Only users with 'users:delete' permission can execute this
    pass
```

## Rate Limiting

### Rate Limit Strategies

1. **Fixed Window** - Simple but allows bursts
2. **Sliding Window** - Smoother distribution
3. **Token Bucket** - Allows bursts up to limit
4. **Leaky Bucket** - Smooths traffic

### Implementation Example

```python
from fastapi import Request, HTTPException
import redis
import time

r = redis.Redis(host='localhost', port=6379)

async def rate_limit(request: Request, max_requests: int = 100, window: int = 60):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    current = r.get(key)
    if current and int(current) >= max_requests:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(window)}
        )

    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    pipe.execute()

@app.get("/api/data")
async def get_data(request: Request):
    await rate_limit(request, max_requests=100, window=60)
    return {"data": "..."}
```
