# Documentation Guidelines

Documentation guidance for Python projects. Use `api-design.md` for API behavior and `database.md` for database-specific decisions.

## README Standards

### Required README Sections

Every project should have a README.md with at minimum:

- Project name and 1-2 sentence description
- Core features
- Installation
- Usage or quickstart
- API documentation link or key endpoints
- Development setup and test commands
- Contributing and license links

### README Best Practices

1. **Start with a clear description** - What does it do? Why does it exist?
2. **Include a quickstart** - Get users running in < 5 minutes
3. **Add badges** - Build status, version, license
4. **Keep it updated** - Outdated docs are worse than no docs
5. **Add screenshots/GIFs** - For UI projects
6. **Link to detailed docs** - Don't clutter README

## Code Documentation

### Inline Comments

```python
# Good - Explains WHY, not WHAT
def calculate_discount(price, user):
    # VIP users get additional 10% off during promotional periods
    if user.is_vip and is_promotional_period():
        return price * 0.80
    return price * 0.90

# Avoid - Redundant comments
def calculate_discount(price, user):  # Calculate discount
    if user.is_vip:  # Check if user is VIP
        return price * 0.80  # Return 80% of price
```

### Docstring Standards

Use Google-style docstrings for all public APIs:

```python
def process_payment(amount: float, currency: str, user_id: int) -> dict:
    """Process a payment transaction.

    Validates the payment details, charges the user's payment method,
    and records the transaction in the database.

    Args:
        amount: The payment amount in the specified currency.
        currency: Three-letter currency code (USD, EUR, etc.).
        user_id: The unique identifier of the user making the payment.

    Returns:
        A dictionary containing the transaction details:
        {
            'transaction_id': str,
            'status': 'completed' | 'pending' | 'failed',
            'timestamp': datetime,
            'amount_charged': float
        }

    Raises:
        ValueError: If amount is negative or currency is invalid.
        InsufficientFundsError: If user doesn't have enough balance.
        PaymentGatewayError: If the payment processor fails.

    Example:
        >>> result = process_payment(99.99, 'USD', 12345)
        >>> print(result['status'])
        'completed'
    """
```

### Module Documentation

Every module should have a module-level docstring:

```python
"""Database connection and query utilities.

This module provides high-level database operations with connection
pooling, transaction management, and query building utilities.

Example:
    >>> from db_utils import Database
    >>> db = Database()
    >>> users = db.query(User).filter(User.active == True).all()

Attributes:
    DEFAULT_POOL_SIZE: Default number of connections in the pool.
    MAX_OVERFLOW: Maximum number of overflow connections allowed.
"""
```

## Architecture Decision Records (ADRs)

### When to Write ADRs

- New technology choices
- Significant architectural changes
- Deprecation decisions
- Performance optimizations
- Security-related changes

### ADR Template

```markdown
# ADR-001: Decision Title

## Status

Proposed | Accepted | Deprecated | Superseded

## Context

What problem, constraint, or requirement forces a decision?

## Decision

What option did the team choose?

## Consequences

### Positive

- Expected benefits

### Negative

- Known costs and risks

## Alternatives Considered

- Alternative: why it was not chosen

## References

- Links to source material
```

### ADR Storage

Store ADRs in `docs/adr/` directory:

```text
docs/
└── adr/
    ├── 001-use-postgresql.md
    ├── 002-migrate-to-fastapi.md
    └── 003-adopt-ruff-for-linting.md
```

## API Documentation

### OpenAPI/Swagger

Use automatic API documentation generation:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    description="API for managing users and orders",
    version="1.0.0"
)

class User(BaseModel):
    """User model representing a registered user."""
    id: int
    name: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com"
            }
        }

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Retrieve a user by ID.

    Returns detailed information about a specific user.

    Args:
        user_id: The unique identifier of the user

    Returns:
        User object with all profile information

    Raises:
        HTTPException: If user not found (404)
    """
    pass
```

### API Documentation Best Practices

1. **Include examples** for every endpoint
2. **Document error responses** with status codes
3. **Add authentication requirements**
4. **Version your API docs**
5. **Keep examples up-to-date**

## Code Examples

### Repository Documentation Structure

```text
project/
├── README.md                 # Project overview
├── docs/
│   ├── api/                  # API documentation
│   │   ├── authentication.md
│   │   └── endpoints.md
│   ├── adr/                  # Architecture decisions
│   ├── development/          # Development guides
│   │   ├── setup.md
│   │   └── testing.md
│   └── deployment/           # Deployment guides
│       └── production.md
├── CONTRIBUTING.md           # Contribution guidelines
├── CHANGELOG.md              # Version history
└── LICENSE                   # License file
```

### Documentation Maintenance

- **Update docs with code changes** - Outdated docs are harmful
- **Review docs in PRs** - Treat docs like code
- **Automate where possible** - Generate API docs from code
- **Use linting** - markdownlint for consistency
- **Test code examples** - Ensure they actually work

## Writing Style

### General Guidelines

1. **Be concise** - Get to the point quickly
2. **Use active voice** - "Run the command" not "The command should be run"
3. **Address the reader** - Use "you" and "your"
4. **Use code blocks** - For commands, code, and output
5. **Add diagrams** - For complex architectures (Mermaid, PlantUML)

### Formatting Standards

```markdown
# Use H1 for title only

## Use H2 for main sections

### Use H3 for subsections

**Bold** for emphasis and UI elements
`code` for inline code, file names, and commands

> Use blockquotes for important notes or warnings

- Use bullet points for lists
- Keep them parallel in structure

1. Use numbered lists for sequential steps
2. Each step should be actionable
```

## Documentation Tools

### Recommended Tools

- **MkDocs** - Static site generator for project docs
- **Sphinx** - Python documentation generator
- **Docusaurus** - React-based documentation site
- **Swagger UI** - Interactive API documentation
- **Redoc** - Alternative OpenAPI documentation

### MkDocs Configuration Example

```yaml
# mkdocs.yml
site_name: My Project Documentation
site_description: Documentation for My Project
site_author: Your Name

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo

nav:
  - Home: index.md
  - Getting Started:
      - Installation: getting-started/installation.md
      - Quick Start: getting-started/quickstart.md
  - API:
      - Authentication: api/authentication.md
      - Endpoints: api/endpoints.md
  - Development:
      - Setup: development/setup.md
      - Contributing: development/contributing.md

plugins:
  - search
  - minify

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
  - toc:
      permalink: true
```

---

**Related Guidelines:**

- [Python Guidelines](python.md) - Code style and docstrings
- [API Design Guidelines](api-design.md) - API documentation
- [Database Guidelines](database.md) - Database decisions and operations
