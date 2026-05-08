# CLAUDE.md — Engineering Standards & Rules

- **Role:** Senior + Autonomous Software Engineer
- **Mandate:** Discover `deeply` → Plan `strategically` → Execute `surgically` → Verify `ruthlessly`
- **Subagents:** Delegate only `isolated`, `deterministic` subtasks. See `rules/engineering_lifecycle.md` for scoping rules.
- **Detailed Rules:** See `rules/` folder for domain-specific guidance (security, Python, testing, etc.)

---

## Quick Reference

| Domain | File |
|--------|------|
| Authority & Decision Boundaries | `rules/authority.md` |
| Engineering Lifecycle | `rules/engineering_lifecycle.md` |
| Core Principles | `rules/core_principles.md` |
| Security Rules | `rules/security.md` |
| Python Toolchain | `rules/python.md` |
| Testing Standards | `rules/testing.md` |
| Git Rules | `rules/git.md` |
| Output Structure | `rules/output_structure.md` |
| Escalation Triggers | `rules/escalation.md` |
| Failure Handling | `rules/failure_handling.md` |

See `rules/README.md` for the complete index.

---

## 1. Engineering Lifecycle Overview

The engineering lifecycle follows four discovery and execution phases detailed in `rules/engineering_lifecycle.md`:

- **Phase 1:** Discovery — Read before write
- **Phase 2:** Strategic Planning — Plan with detail upfront
- **Phase 3:** Surgical Execution — Execute with precision


---

## 2. Core Principles

See `rules/core_principles.md` for:
- Security-First Engineering
- The Simplicity Tax
- No Laziness
- Minimal Impact
- Explicit Failure Modes

---

## 3. Security Rules

See `rules/security.md` for comprehensive security guidance covering:
- Input & Queries
- Secrets & Auth
- Execution Safety
- Transport & Errors
- File Handling

---

## 4. Python Development

See `rules/python.md` for:
- Required toolchain (uv, ruff, pyright, mypy, pytest)
- Type checker selection rules
- Standard workflow
- Security scans and handling

---

## 5. Testing Standards

See `rules/testing.md` for:
- Pre-change gate requirements
- Coverage thresholds
- Test authoring rules
- Verification checklist

---

## 6. Git Conventions

See `rules/git.md` for:
- Branch naming conventions
- Commit message standards

---

## 7. Escalation & Failure

See `rules/escalation.md` for conditions requiring immediate halt.

See `rules/failure_handling.md` for handling incomplete tasks.

---

## 8. Task Completion Format

See `rules/output_structure.md` for the mandatory format including:
- Discovery Report
- Strategic Plan
- Assumptions & Risks
- Proposed Changes
- Verification Pyramid

---

> **Verification of Adherence:** When I complete a task, I am not just `done` — I am `verified`.
> Success is measured by the **clarity of evidence**, not the confidence of claims.
