---
description: Provide a comprehensive overview of a library from its codebase
---

1. **Identify purpose** — Read the README, module docstrings, and package metadata (`setup.cfg`, `pyproject.toml`, `package.json`, `Cargo.toml`) to determine the library's domain and problem it solves.
2. **Map public API** — List exported symbols, top-level functions, classes, and entry points. Distinguish public surface from internal implementation.
3. **Document features** — For each major module or namespace, describe its role and the capabilities it provides with concrete examples.
4. **Describe architecture** — Outline the high-level design: layered vs. hexagonal, sync vs. async, plugin system, or pipeline. Note key abstractions and how modules interact.
5. **Identify dependencies** — List runtime dependencies and what each is used for. Flag any optional or platform-specific dependencies.
6. **Review configuration surface** — Document environment variables, config files, constructor parameters, and their defaults.
7. **Synthesize overview** — Produce a structured report with sections: **Purpose**, **Features**, **Architecture**, **Public API**, **Dependencies**, **Configuration**.
