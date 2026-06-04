---
name: dry-code
description: >
  Reduce meaningful duplication: repeated error mapping, shared fixtures,
  duplicated validation or serialization logic. Use when asked to deduplicate
  code, consolidate repeated logic, or extract shared helpers.
  Only targets duplication with real maintenance cost — not incidental similarity.
---

# DRY Cleanup

## Principle

Reduce duplication only when that duplication has maintenance cost: two call
sites that must change together, repeated policy logic that diverges silently,
or test fixtures reimplementing the same complex setup.

Do not abstract incidental similarity. Prefer a small, same-layer helper over a
new architectural layer.

---

## Pre-Flight Gates

Run these before any analysis or editing. Stop and confirm with the user if any
gate fails.

### Gate 1 — Git cleanliness

Run `git status`. If uncommitted user changes exist, confirm scope before
proceeding.

### Gate 2 — Test coverage baseline

If tests are absent or fewer than one per exported function/class, coverage is
thin. Escalate all findings to "needs care" and warn the user — extracting a
shared helper without tests can silently change behavior at one of the call
sites.

### Gate 3 — Project-level overrides

Read `CLAUDE.md` or `README.md` and any style/convention files. Project
guidance takes precedence. Note any overrides in the findings report.

---

## What to Look For

Good DRY candidates — duplication with real maintenance cost:

- **Repeated error mapping** — the same error-to-response translation in
  multiple handlers.
- **Repeated task or request setup** — identical boilerplate in test files or
  service constructors.
- **Repeated serialization or validation** — the same field-level rules
  implemented independently in multiple places.
- **Repeated result shaping** — multiple call sites producing the same output
  structure from different raw data.
- **Test fixtures** — multiple tests reimplementing the same nontrivial async
  fake, DB seed, or mock object.
- **Docs** — architecture descriptions duplicated across multiple doc files that
  will diverge when the code changes.

**Rule of Three**: tolerate one copy. On the third distinct occurrence, treat it
as a DRY candidate.

---

## When Not to Abstract

Skip DRY when any of the following is true:

- The two call sites are **similar but likely to evolve differently** — shared
  surface today, different policy tomorrow.
- A helper would **obscure a simple one-liner** — the abstraction costs more
  than it saves.
- The abstraction name would be **vaguer than the code it replaces** — if you
  can't name it cleanly, don't extract it.
- Forcing DRY would **conflict with KISS** — a shared helper that requires
  callers to pass extra flags to cover variant behavior is worse than the
  duplication.
- The duplication is **incidental similarity** — same shape, independent
  lifecycle.

---

## Ranking Findings

**Safe** — act directly:

- Byte-for-byte duplicated private helpers with no public surface.
- Test fixtures reimplementing identical nontrivial setup confirmed by `rg`.
- Docs duplicating stale architecture text with no behavioral significance.

**Needs care** — confirm before acting:

- Extracting a helper that crosses a module boundary.
- Deduplicating public or exported behavior — consumers may depend on the
  separate names.
- Any consolidation where test coverage is thin.

**Skip** — document with reason:

- Similar code likely to diverge (flag the similarity for awareness).
- One-liners where a helper would add indirection without savings.
- Abstractions that would require a new architectural layer.

---

## Making Changes

- Extract helpers at the **same architectural layer** as the repeated behavior.
  Do not create a new layer or cross module boundaries without explicit
  justification.
- One deduplication target per pass. Do not chain multiple extractions in a
  single diff.
- Separate the extraction commit from any formatting or naming changes.
- Preserve existing naming, error shape, and test style at the call sites.
- After extraction, confirm each call site behaves identically by running tests.

---

## Verify

Run the repo's lint and test commands after each extraction. If a consolidation
breaks a test, revert and report — do not weaken the test to make it pass.

---

## Reporting

### Exploration mode

```
## DRY Findings

### Pre-flight
- Git status: [clean / uncommitted changes]
- Test coverage: [adequate / thin / unknown — describe risk]
- Project overrides: [none / list any]

### Candidates (ordered by risk or payoff)
- [file:line] Description — category (safe / needs care / skip)
  Occurrences: [list of file:line for each duplicate]

### Safe extractions
Duplications removable without public contract risk.

### Risky extractions
Items that need confirmation before acting.

### Skipped
Items evaluated but not actioned, with reason (incidental similarity, likely
divergence, etc.).

### Verification plan
Lint and test commands to run. Doc sections to update if any.
```

### Implementation mode

```
## What changed
[summary of extractions, scoped to module or layer]

## What was verified
[lint/test output or reason verification was skipped]

## Residual risks
[skipped candidates, thin coverage areas, public API concerns]
```

---

## Agentic Notes

- Track progress in the conversation. Do not create a progress file unless
  explicitly asked.
- Never weaken a failing test to make an extraction pass. Surface and stop.
- If an extraction introduces a regression you cannot resolve, revert and
  report.

---

## See Also

- `kiss-code` — Simplify over-complex implementations
- `yagni-code` — Remove dead/speculative code
- `refactor-code` — Modernize Python code after cleanup
