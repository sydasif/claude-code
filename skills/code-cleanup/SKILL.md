---
name: code-cleanup
description: Codebase cleanup workflow for applying YAGNI, DRY, and KISS principles. Use when asked to review, simplify, refactor, or clean up a project for unnecessary code, duplicated logic, over-abstraction, excessive complexity, stale tests, or docs that no longer match implementation.
---

# Cleanup Principles

## Overview

Use this skill to clean up a codebase with three practical rules:

- **KISS**: prefer direct, readable implementations over clever abstractions.
- **YAGNI**: remove code whose current need is not demonstrated or needed.
- **DRY**: reduce meaningful duplication without hiding simple behavior.

Treat these rules as engineering judgment, not slogans. Preserve public contracts unless the user explicitly wants breaking cleanup.

## Priority Order

Apply the rules in this order when they conflict:

1. **KISS**: keep the code easiest to understand and change.
2. **YAGNI**: remove unsupported future-proofing.
3. **DRY**: reduce duplication only when it lowers real maintenance cost.

Use these tie-breakers:

- Prefer simple duplication over a vague abstraction.
- Prefer deletion over generalization when code has no current call sites, tests, docs, or framework purpose.
- Prefer local explicit code when behavior is short and unlikely to change together.
- Prefer a shared helper when duplicated logic represents a real policy — error shape, security validation, serialization, timeout handling, or network execution.
- Preserve public APIs unless the user explicitly accepts breaking changes.

> **YAGNI guardrail (read before applying YAGNI)**: YAGNI is not a license for sloppy deletion. The goal is to remove speculative complexity, not to paint the codebase into a corner. Prefer removing _implementations_ of unused features over removing _seams_ that make future change possible. If a removal structurally forecloses an obvious and reasonable future extension point, pause and flag it rather than deleting silently.

---

## Pre-Flight Gates

Run these checks before any analysis or editing. Stop and confirm with the user if any gate fails.

### Gate 1 — Git cleanliness

Run `git status`. If there are uncommitted user changes, confirm the cleanup scope explicitly before proceeding. Do not mistake in-progress work for cleanup targets.

### Gate 2 — Test coverage baseline

Assess whether the codebase has meaningful automated test coverage before ranking anything as "safe cleanup." A rough heuristic: if there are no tests at all, or fewer than one test per exported function or class, treat coverage as thin. If test coverage is thin or absent, escalate all findings to "needs care" and warn the user. YAGNI and KISS cleanup without tests can break behavior silently.

### Gate 3 — Project-level overrides

Read `AGENTS.md`, `README.md`, contribution docs, and any style/convention files. If project-level guidance conflicts with the principles in this skill, **project guidance takes precedence**. Note any overrides in the findings report.

---

## Workflow

### 1. Inspect the project shape

- Read repository guidance: `AGENTS.md`, `README.md`, contribution docs, test commands.
- Map source, tests, docs, and public interfaces — skipping generated directories (`dist/`, `build/`, `__pycache__`, `.next/`, and similar output folders).
- Confirm git status is clean (Gate 1 above).
- Assess test coverage (Gate 2 above).
- Note any project-specific overrides (Gate 3 above).
- **If the repository is large (more than ~20 modules or top-level source files), confirm the intended scope with the user before proceeding.** Default to a single module or layer per session rather than sweeping the whole codebase.

### 2. Identify candidates with evidence

- Search call sites with `rg`.
- Compare implementation against docs and tests.
- Separate internal cleanup from public API removal.
- Use concrete file and line references — no broad claims.

### 3. Rank findings before editing

**Safe cleanup** — low risk, act directly:

- Unused imports, dead helpers with zero call sites, stale comments describing removed behavior.
- Duplicated branches with byte-for-byte identical behavior.
- Docs that describe code structure that no longer exists.

**Needs care** — confirm or flag before acting:

- Public tools, exported names, documented behavior, config formats.
- Test fixtures that may be used by consumers outside the repo.
- Anything where test coverage is thin.

**Usually skip** — document as skipped with reason:

- Tiny duplication that is clearer inline than abstracted.
- Abstractions that encode a real domain boundary.
- Compatibility shims with known external users.

Resolve conflicts using the priority order: KISS, then YAGNI, then DRY.

### 4. Make narrow, batched changes

- Scope edits to one module or layer per pass. Do not sweep the entire codebase in a single change.
- **Separate formatting/style-only changes** (whitespace, naming conventions, import ordering) **from semantic changes** (logic, structure, duplication removal) into distinct commits or passes. Never mix them in the same diff.
- Avoid mixing style cleanup with behavior changes in the same diff.
- Do not introduce a new abstraction unless it removes real complexity across multiple call sites.
- Preserve existing naming, error shape, and test style.
- If a removal structurally forecloses an obvious and reasonable future extension point, pause and flag it rather than deleting silently.

### 5. Verify behavior

- Run the repo's lint and test commands after each module-level batch.
- If sandbox restrictions block verification, surface that to the user before continuing.
- Add or update tests when cleanup touches shared helpers, public tool contracts, or previously untested forwarding behavior.

### 6. Update docs

Update docs when:

- Files move or are deleted.
- Helper ownership or location changes.
- Test coverage materially changes.
- Commands change.
- Public-facing behavior changes.

Do not update docs for invisible internal simplification unless those docs explicitly describe that internal structure.

---

## YAGNI Pass

Look for code that exists only for hypothetical future use:

- Unused helpers, imports, parameters, config options, validators, adapters, or wrappers.
- Convenience APIs that duplicate a generic API without adding behavior.
- "Future-proof" parsing or compatibility logic with no tests, docs, or call sites.
- Stale comments describing behavior that no longer exists.

**Before removing, ask:**

- Is it documented as public surface?
- Is it imported outside the module?
- Is it needed for a framework hook, plugin registration, or generated schema?
- Does a test depend on the current contract?
- Does removing it foreclose a reasonable, near-term extension point without a clear path to add it back?

If any answer is "yes" or "unclear," report it as a compatibility risk — do not delete.

> **YAGNI misapplication guard**: See the guardrail note in the Priority Order section above. YAGNI targets speculative _implementations_, not structural _seams_.

---

## DRY Pass

Reduce duplication only when the duplication has maintenance cost.

**Good DRY targets:**

- Repeated error mapping, task setup, serialization, validation, or result shaping across modules.
- Multiple tests reimplementing the same nontrivial fixture or async fake.
- Docs repeating stale architecture in several places.

**Rule of Three**: Duplicate code once if necessary. On the third occurrence across distinct call sites, treat it as a DRY candidate and extract a shared helper.

**Skip DRY when:**

- Two call sites are similar but likely to evolve differently (shared name, different policy).
- A helper would obscure a simple one-liner.
- The abstraction name would be vaguer than the code it replaces.
- Forcing DRY would conflict with KISS or YAGNI.

Good DRY cleanup creates one small helper at the same architectural layer as the repeated behavior. It does not create new layers or cross module boundaries without justification.

---

## KISS Pass

Simplify code that makes readers jump through unnecessary indirection:

- One-use helpers that hide a direct call.
- Mapper functions representable as data on the relevant type.
- Overly defensive branching around impossible states.
- Tests that assert implementation details without protecting behavior.
- Stale comments that describe removed behavior (also a YAGNI signal).

Prefer the simplest form that still preserves:

- Clear error semantics.
- Testability.
- Existing public API.
- Local architectural rules.

**Apply KISS relative to the idioms of the language and framework in use.** Do not flag idiomatic patterns as complexity — Go error returns, Rust trait bounds, Java interface patterns, and similar conventions are expected, not accidental complexity. Use the team's conventions as the baseline, not an idealized minimum.

> Note: simplicity is domain-relative. Some problems are inherently complex. KISS means "don't add accidental complexity," not "avoid all complexity."

---

## Reporting

### Exploration or review mode

Report findings before making any changes, unless the user asked to implement directly.

Use this shape:

```
## Findings

### Pre-flight
- Git status: [clean / uncommitted changes — describe]
- Test coverage: [adequate / thin / unknown — describe risk]
- Project overrides from AGENTS.md: [none / list any]

### Candidates (ordered by risk or payoff)
- [file:line] Description — category (safe / needs care / skip)
- ...

### Safe cleanup
Changes that can be made without public contract risk.

### Risky cleanup
Changes that need user confirmation before proceeding.

### Skipped candidates
Items evaluated but not actioned, with the reason for each.

### Verification plan
Lint and test commands to run. Doc sections to update.
```

### Implementation mode

Finish with:

```
## What changed
[summary of edits, scoped to module or layer]

## What was verified
[lint/test output or reason verification was skipped]

## Residual risks
[skipped candidates, thin coverage areas, public API concerns]
```

---

## Agentic Operation Notes

When operating as an agent across multiple passes or context windows:

- **Default:** Track progress in the conversation (implementation report or findings report). Do **not** create `cleanup-progress.md` unless the user explicitly asks for a persisted progress file (e.g. multi-day cleanup across sessions).
- **Opt-in only:** If the user requests it, write `cleanup-progress.md` at the repo root with: analyzed scope, changes made, pending work, unresolved risks. Remove or update it when the cleanup is finished, or leave removal to the user.
- Batch changes by module. Do not accumulate a multi-module diff and apply it in one step.
- Never weaken a failing test to make cleanup pass. Surface the failure and stop.
- If a cleanup action introduces a regression the agent cannot resolve, revert and report — do not work around it silently.

---

## See Also

- `code-refactor` skill — For modernizing Python code after cleanup
