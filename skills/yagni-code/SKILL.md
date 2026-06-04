---
name: yagni-code
description: >
  Remove code that exists only for hypothetical future use: unused helpers,
  dead imports, speculative parameters, stale compatibility shims, and
  convenience wrappers with no active call sites.
  Use when asked to remove dead code, prune unused exports, or trim speculative complexity.
---

# YAGNI Cleanup

## Principle

Remove code whose current need is not demonstrated — no call sites, no tests,
no docs, no framework hook. Do not remove structural seams that make future
change possible.

> **Guardrail**: YAGNI targets speculative _implementations_, not structural
> _seams_. If removing something forecloses an obvious, reasonable extension
> point with no clear path to add it back, pause and flag it instead.

---

## Pre-Flight Gates

Run these before any analysis or editing. Stop and confirm with the user if any
gate fails.

### Gate 1 — Git cleanliness

Run `git status`. If uncommitted user changes exist, confirm scope before
proceeding. In-progress work is not a cleanup target.

### Gate 2 — Test coverage baseline

If tests are absent or fewer than one per exported function/class, coverage is
thin. Escalate all findings to "needs care" and warn the user — dead code
without tests is harder to verify as truly unused.

### Gate 3 — Project-level overrides

Read `CLAUDE.md` or `README.md` and any style/convention files. Project
guidance takes precedence. Note any overrides in the findings report.

---

## What to Look For

Candidates for YAGNI removal:

- **Unused imports** — not referenced anywhere in the file.
- **Dead helpers** — private functions/methods with zero call sites after `rg`
  search across all file types.
- **Unused parameters** — function arguments that are never read in the body
  and not part of a public interface contract.
- **Speculative config options** — options parsed and stored but never read by
  any runtime path.
- **Convenience APIs** — exported functions that only call a generic API with
  hardcoded arguments, with no distinct behavior of their own.
- **"Future-proof" compatibility logic** — parsing branches or adapters with no
  tests, no docs, and no active call sites.
- **Stale comments** — comments describing behavior that no longer exists in the
  code.
- **Unused validators or adapters** — registered or defined but never invoked.

---

## Safety Checklist Before Removing Anything

Before removing any function, class, exported name, or config key, confirm all
of the following with `grep`/`rg` — never rely on memory for call-graph
analysis:

- [ ] Zero call sites across all file types (`.ts`, `.js`, `.py`, `.yaml`,
      `.json`, template files, test files, etc.)
- [ ] Not documented as public surface in README, API docs, or changelogs.
- [ ] Not imported outside this module.
- [ ] Not needed for a framework hook, plugin registration, or generated schema.
- [ ] No test depends on the current contract.
- [ ] Removing it does **not** foreclose a near-term, reasonable extension point
      without a clear path to restore it.

If any answer is "yes" or "unclear," report as a compatibility risk — do not
delete.

---

## Ranking Findings

**Safe** — act directly:

- Unused imports with zero references in the file.
- Private helpers with zero call sites confirmed by `rg`.
- Stale inline comments describing removed behavior.
- Dead branches guarding conditions that are now structurally impossible.

**Needs care** — confirm before acting:

- Exported or public names, even with zero apparent call sites (consumers may
  be outside the repo).
- Test fixtures — may be used by external consumers.
- Anything where test coverage is thin.
- Config keys — downstream tooling or deployment scripts may reference them.

**Skip** — document with reason:

- Compatibility shims with known external users.
- Framework registration hooks that appear unused but are invoked by convention.
- Structural seams (base classes, interfaces, extension points) with no current
  implementations but plausible near-term use.

---

## Making Changes

- One module or layer per pass.
- Use `rg` to search both call sites and string references across all file
  types before deleting anything. Zero IDE-visible call sites does not mean
  zero usages.
- Do not generalize before deleting — prefer deletion over adding abstraction.
- Preserve existing naming and error shape for anything that remains.
- If a removal forecloses an obvious extension point, flag it rather than
  deleting silently.

---

## Verify

Run the repo's lint and test commands after each module-level batch. If a
removal breaks a test, revert and report — do not weaken the test.

---

## Reporting

### Exploration mode

```
## YAGNI Findings

### Pre-flight
- Git status: [clean / uncommitted changes]
- Test coverage: [adequate / thin / unknown — describe risk]
- Project overrides: [none / list any]

### Candidates (ordered by risk or payoff)
- [file:line] Description — category (safe / needs care / skip)

### Safe removals
Dead code confirmed removable without public contract risk.

### Risky removals
Items that need confirmation before acting.

### Skipped
Items evaluated but not removed, with reason.

### Verification plan
Lint and test commands to run. Doc sections to update if any.
```

### Implementation mode

```
## What changed
[summary of removals, scoped to module or layer]

## What was verified
[lint/test output or reason verification was skipped]

## Residual risks
[skipped candidates, thin coverage areas, public API concerns]
```

---

## Agentic Notes

- Track progress in the conversation. Do not create a progress file unless
  explicitly asked.
- Never weaken a failing test to make removal pass. Surface and stop.
- If a removal introduces a regression you cannot resolve, revert and report.

---

## See Also

- `kiss-code` — Simplify over-complex implementations
- `dry-code` — Reduce meaningful duplication
- `refactor-code` — Modernize Python code after cleanup
