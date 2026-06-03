---
description: Review codebase structure, suggest improvements for maintainability and scalability
---

1. **Map the terrain** — List top-level files and directories. Identify the build system, package manager, and framework configuration files (`package.json`, `Cargo.toml`, `pyproject.toml`, etc.).

2. **Audit directory layout** — Check for:
   - Flat vs. layered vs. feature-based organization
   - Naming conventions (kebab-case? snake_case? PascalCase?)
   - Separation of concerns (business logic vs. infrastructure vs. presentation)

3. **Evaluate module boundaries** — For each major directory, identify:
   - Public API surface vs. internal implementation
   - Circular dependency risk
   - Single Responsibility Principle compliance

4. **Assess scalability patterns** — Are there:
   - Repository/Service pattern or equivalent abstraction layers?
   - Dependency injection or service locator?
   - Clear interface definitions between modules?
   - Configuration externalization?

5. **Check documentation concordance** — Do README, ADRs, and inline docs match the actual structure?

6. **Synthesize findings** — Produce a report structured as:
   - **Strong patterns** (keep/reinforce)
   - **Improvement opportunities** (specific, actionable)
   - **Risks** (coupling, drift, tech debt hotspots)
   - **Suggested next actions** (refactoring targets, doc updates)
