---
description: Review codebase for coding best practices and industry standards
---

1. **Scan for conventions** — Check naming style, file organization, import ordering, and formatting against language-specific community standards (PEP 8, Standard JS, Google style guides, etc.).
2. **Audit readability** — Identify overly long functions, deeply nested conditionals, magic numbers/strings, unclear variable names, and missing type annotations.
3. **Evaluate maintainability** — Flag duplicated code, large modules, tight coupling, missing abstractions, and hardcoded configuration values.
4. **Profile efficiency** — Look for obvious performance anti-patterns: N+1 queries, unnecessary allocations, repeated computations, and synchronous blocking in async paths.
5. **Check error handling** — Verify consistent use of specific exceptions, proper error propagation, and absence of bare `except:` / `catch-all` blocks.
6. **Review dependency health** — List outdated packages, deprecated APIs, and unused imports or dependencies.
7. **Produce action items** — For each issue found, provide: file location, severity (low/medium/high), suggested fix, and expected impact.
