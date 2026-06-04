---
name: kiss-code
description: >
  Simplify code by removing accidental complexity: one-use helpers, unnecessary
  indirection, overly defensive branching, and implementation-detail tests.
  Use when asked to simplify, reduce complexity, or make code more readable.
---

# KISS Cleanup

## Principle

Prefer the simplest implementation that preserves correct behavior, clear error
semantics, and the existing public API. Remove accidental complexity — do not
flatten inherent domain complexity.

**Apply KISS relative to the idioms of the language and framework in use.** Go
error returns, Rust trait bounds, Java interface patterns, and similar
conventions are expected, not accidental. Use the team's conventions as the
baseline, not an idealized minimum.

> KISS means "don't add accidental complexity," not "avoid all complexity."

---

## Pre-Flight Gates

Run these before any analysis or editing. Stop and confirm with the user if any
gate fails.

### Gate 1 — Git cleanliness

Run `git status`. If uncommitted user changes exist, confirm scope before
proceeding.

### Gate 2 — Test coverage baseline

If tests are absent or fewer than one per exported function/class, coverage is
thin. Escalate all findings to "needs care" and warn the user — KISS changes
without tests can break behavior silently.

### Gate 3 — Project-level overrides

Read `CLAUDE.md` or `README.md` and any style/convention files. Project
guidance takes precedence over this skill. Note any overrides in the findings
report.

---

## What to Look For

Candidates for KISS cleanup:

- **One-use helpers** that wrap a single direct call with no added semantics.
- **Mapper functions** representable as a plain data lookup on the relevant type.
- **Overly defensive branching** around impossible or already-guarded states.
- **Tests that assert implementation details** rather than protecting observable
  behavior.
- **Stale comments** describing removed behavior (also a YAGNI signal — flag
  for that pass too).
- **Unnecessary indirection**: interfaces, base classes, or wrapper types with a
  single implementation and no extension point in active use.

---

## Ranking Findings

**Safe** — act directly:

- One-use private helpers with zero external call sites that wrap a trivial
  expression.
- Comments that describe code structure that no longer exists.
- Tests that pin internal implementation details with no behavioral assertion.

**Needs care** — confirm before acting:

- Public or exported names, even if the implementation looks trivial.
- Anything where test coverage is thin.
- Indirection that may encode a real domain boundary, even if currently
  single-implementation.

**Skip** — document with reason:

- Abstractions that exist for testability (dependency injection, interface
  seams).
- Patterns idiomatic to the language or framework in use.
- Wrappers with known external consumers.

---

## Making Changes

- One module or layer per pass. Do not sweep the whole codebase.
- Separate formatting-only changes from semantic simplification — never mix in
  the same diff.
- Do not introduce a new abstraction to simplify: inline directly.
- Preserve existing naming, error shape, and test style.
- If inlining a helper would make a call site harder to test, keep the helper
  and note why.

---

## Verify

Run the repo's lint and test commands after each module-level batch. If a
simplification introduces a failure, revert and report — do not work around it.

---

## Reporting

### Exploration mode

```
## KISS Findings

### Pre-flight
- Git status: [clean / uncommitted changes]
- Test coverage: [adequate / thin / unknown — describe risk]
- Project overrides: [none / list any]

### Candidates (ordered by risk or payoff)
- [file:line] Description — category (safe / needs care / skip)

### Safe simplifications
What can be inlined or removed without public contract risk.

### Risky simplifications
What needs confirmation before acting.

### Skipped
Items evaluated but not actioned, with reason.

### Verification plan
Lint and test commands to run.
```

### Implementation mode

```
## What changed
[summary of simplifications, scoped to module or layer]

## What was verified
[lint/test output or reason verification was skipped]

## Residual risks
[skipped candidates, thin coverage areas, public API concerns]
```

---

## Agentic Notes

- Track progress in the conversation. Do not create a progress file unless
  explicitly asked.
- Never weaken a failing test to make cleanup pass. Surface and stop.
- If a change introduces a regression you cannot resolve, revert and report.

---

## See Also

- `yagni-code` — Remove speculative/dead code
- `dry-code` — Reduce meaningful duplication
- `refactor-code` — Modernize Python code after cleanup
