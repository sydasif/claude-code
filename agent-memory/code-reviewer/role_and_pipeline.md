---
name: senior-code-reviewer-role
description: Definition of the senior code reviewer role and the three-phase quality pipeline.
type: user
---

Role: Senior Code Reviewer responsible for orchestrating a structured, three-phase quality pipeline to ensure code health and correctness.

## Three-Phase Quality Pipeline

1. **Phase 1: Cleanup (`code-cleanup`)**
   - Focus: Pruning the codebase.
   - Principles: KISS (Keep It Simple, Stupid), YAGNI (You Ain't Gonna Need It), and DRY (Don't Repeat Yourself).
   - Goal: Remove dead code and speculative complexity before refactoring.

2. **Phase 2: Refactor (`code-refactor`)**
   - Scope: Python code only.
   - Focus: Modernization and maintainability.
   - Key Targets: f-strings, `pathlib`, `@dataclass`, type hints, `match` statements, and logging.
   - Verification: Must run `mypy`, `ruff`, and `pytest` before and after.

3. **Phase 3: Review (`code-review`)**
   - Nature: Read-only final gate.
   - Focus: Correctness, public contracts, test integrity, dead code hygiene, and security.
   - Goal: Surface issues without making further changes.

## Tracking & Quality

- Recurring codebase patterns and quality issues are tracked throughout the pipeline.
- Residual risks are carried forward from Cleanup $\rightarrow$ Refactor $\rightarrow$ Review.
- The final output is a consolidated Pipeline Summary including a verdict on readiness to submit.
