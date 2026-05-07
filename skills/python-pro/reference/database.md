# Database Best Practices

Database guidance for Python applications. Use `python.md` for async and framework selection, and `api-design.md` when database behavior shapes API contracts.

## Database Connection Best Practices

### Connection Management

- Use connection pooling for production applications
- Always close connections properly (use context managers)
- Set appropriate connection timeouts
- Monitor connection pool usage

```python
# Good - Using context manager
with db_pool.acquire() as conn:
    result = conn.execute(query)

# Avoid - Manual connection management
conn = db_pool.acquire()
result = conn.execute(query)
conn.close()  # Easy to forget
```

### Connection Pool Configuration

```python
# Example with asyncpg
pool = await asyncpg.create_pool(
    dsn="postgresql://...",
    min_size=5,
    max_size=20,
    command_timeout=60,
    max_inactive_connection_lifetime=300
)
```

## ORM Guidelines

### When to Use ORM

**Use ORM when:**

- Complex object relationships
- Rapid prototyping
- CRUD-heavy applications
- Team familiar with ORM

**Use raw SQL when:**

- Complex queries (JOINs, aggregations, window functions)
- Performance-critical paths
- Database-specific features needed
- Simple data retrieval

### ORM Best Practices

```python
# Good - Efficient query with select_related
users = User.objects.select_related('profile').filter(is_active=True)

# Avoid - N+1 query problem
users = User.objects.filter(is_active=True)
for user in users:
    print(user.profile.bio)  # Queries database for each user
```

### SQLAlchemy 2.0 Patterns

```python
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# Modern async pattern
async with session.begin():
    stmt = (
        select(User)
        .options(joinedload(User.posts))
        .where(User.is_active == True)
    )
    result = await session.execute(stmt)
    users = result.scalars().unique().all()
```

## Query Best Practices

### Parameterized Queries

Always use parameterized queries to prevent SQL injection:

```python
# Good - Parameterized
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

# Never - String formatting
query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection risk!
```

### Query Optimization

```python
# Good - Select only needed columns
SELECT id, name, email FROM users

# Avoid - Selecting all columns
SELECT * FROM users

# Good - Use indexes for filtering
CREATE INDEX idx_users_email ON users(email);

# Good - Pagination
SELECT * FROM users LIMIT 20 OFFSET 40;
```

## Migration Strategies

### Schema Migration Tools

- **Alembic** (SQLAlchemy) - Most popular
- **Django Migrations** - Built into Django
- **Flyway** - Language-agnostic
- **Liquibase** - Language-agnostic

### Migration Best Practices

1. **Always test migrations** on a copy of production data
2. **Make migrations reversible** when possible
3. **Avoid data migrations** in schema migration files
4. **Run migrations in transactions** when supported
5. **Document breaking changes**

```python
# Alembic migration example
"""Add user_profile table

Revision ID: abc123
Revises: previous_migration
Create Date: 2024-01-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123'
down_revision = 'previous_migration'

def upgrade():
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )
    op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'])

def downgrade():
    op.drop_index('idx_user_profiles_user_id')
    op.drop_table('user_profiles')
```

## Database Design Principles

### Normalization

- **1NF**: Atomic values, no repeating groups
- **2NF**: No partial dependencies on composite keys
- **3NF**: No transitive dependencies

**When to denormalize:**

- Read-heavy workloads
- Complex reporting queries
- Performance-critical paths

### Indexing Strategy

```sql
-- Good - Index for filtering
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;

-- Good - Composite index for range queries
CREATE INDEX idx_orders_date_status ON orders(created_at, status);

-- Good - Partial index for common queries
CREATE INDEX idx_posts_published ON posts(published_at)
WHERE status = 'published';
```

### Primary Keys

- Use auto-increment integers or UUIDs
- Avoid natural keys (email, SSN) as primary keys
- UUIDs are better for distributed systems
- Integers are better for single-node performance

```python
# UUID primary key
from sqlalchemy import Column, UUID
import uuid

class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
```

## Transaction Management

### ACID Properties

- **Atomicity**: All or nothing
- **Consistency**: Database constraints maintained
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data survives crashes

### Transaction Patterns

```python
# Good - Explicit transaction
async with db.transaction() as tx:
    try:
        await tx.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        await tx.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
        await tx.commit()
    except Exception:
        await tx.rollback()
        raise

# Good - Context manager (auto-commit/rollback)
async with db.begin() as session:
    session.add(user)
    session.add(order)
    # Auto-commits on success, rolls back on exception
```

### Isolation Levels

| Level            | Dirty Read | Non-repeatable Read | Phantom Read |
| ---------------- | ---------- | ------------------- | ------------ |
| READ UNCOMMITTED | Yes        | Yes                 | Yes          |
| READ COMMITTED   | No         | Yes                 | Yes          |
| REPEATABLE READ  | No         | No                  | Yes          |
| SERIALIZABLE     | No         | No                  | No           |

**Default choices:**

- PostgreSQL: READ COMMITTED
- MySQL (InnoDB): REPEATABLE READ

## Async Database Operations

### Async Libraries

| Database   | Library                  |
| ---------- | ------------------------ |
| PostgreSQL | asyncpg                  |
| MySQL      | aiomysql                 |
| MongoDB    | motor                    |
| Redis      | redis-py (async support) |
| SQLite     | aiosqlite                |

### Async Patterns

```python
import asyncpg

# Good - Connection pooling
pool = await asyncpg.create_pool(dsn="postgresql://...")

async with pool.acquire() as conn:
    # Single query
    row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)

    # Multiple queries in transaction
    async with conn.transaction():
        await conn.execute("INSERT INTO logs ...")
        await conn.execute("UPDATE counters ...")

# Good - Concurrent queries
async with pool.acquire() as conn:
    results = await asyncio.gather(
        conn.fetch("SELECT * FROM users"),
        conn.fetch("SELECT * FROM orders"),
        conn.fetch("SELECT * FROM products")
    )
```

## Security Best Practices

### Database Security Checklist

- [ ] Use least privilege database users
- [ ] Encrypt data at rest (TDE)
- [ ] Encrypt connections (TLS/SSL)
- [ ] Rotate credentials regularly
- [ ] Audit sensitive queries
- [ ] Mask sensitive data in logs
- [ ] Use parameterized queries (prevent SQL injection)

### Credential Management

```python
# Good - Environment variables
import os

DB_URL = os.environ.get('DATABASE_URL')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Never - Hardcoded credentials
DB_PASSWORD = "super_secret_password123"  # Security risk!
```

## Performance Optimization

### Query Performance

1. **EXPLAIN ANALYZE** - Always check query plans
2. **Connection pooling** - Reduces connection overhead
3. **Batch operations** - Reduce round trips
4. **Proper indexing** - Based on query patterns
5. **Query result caching** - For frequently accessed data

### Caching Strategies

```python
# Redis caching example
import redis
import json

r = redis.Redis(host='localhost', port=6379)

def get_user(user_id):
    # Check cache first
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Fetch from database
    user = db.query(User).get(user_id)

    # Cache for future requests (TTL: 1 hour)
    r.setex(f"user:{user_id}", 3600, json.dumps(user.to_dict()))

    return user
```

## Monitoring and Maintenance

### Key Metrics to Monitor

- Query response time (p50, p95, p99)
- Connection pool utilization
- Slow queries log
- Deadlock frequency
- Disk I/O and CPU usage
- Replication lag (if using replicas)

### Maintenance Tasks

- Regular **VACUUM** (PostgreSQL) or **OPTIMIZE** (MySQL)
- Update statistics
- Archive old data
- Monitor disk space
- Test backups regularly

---

**Related Guidelines:**

- [Python Guidelines](python.md)
- [API Design Guidelines](api-design.md)
- [Documentation Guidelines](documentation.md)
