---
description: Run the full optimization + testing pipeline on project.
---

Run the full optimization + testing pipeline. This command is the single
orchestrator: `cleanup-code` → `modernize-python` → `review-code`, with an
optional `function-first-refactor` pass. Do not re-derive the stage order.

## Stage 0 — Preflight (stop if a gate fails)

1. **Git cleanliness**: run `git status`. If the tree is dirty, show what is
   uncommitted and confirm scope before touching anything. A clean baseline is
   what makes the later diffs reviewable.
2. **Test baseline**: run the project's tests and record the result. If there
   are none, say so explicitly — stages 1-3 then apply mechanical, behavior-
   preserving changes only, and any structural change is out of scope.
3. **Tooling**: detect `ruff`, `mypy`, `pytest` (and `uv`, if the project
   uses it). Note missing tools and skip them rather than substituting a
   different check. Never treat a skipped check as a pass.

## Stage 1 — `cleanup-code`

Apply YAGNI, DRY, KISS. Remove dead code, prune unused imports/variables,
eliminate duplication, simplify over-abstraction. Do not change behavior.
Preserve public contracts unless the user explicitly accepts a breaking change.
Report findings with `file:line` before editing when the change is not mechanical.

## Stage 2 — `modernize-python`

Modernize what survived cleanup: type hints, dataclasses (+slots), `pathlib`,
f-strings, `logging.exception` over `logging.error`, `datetime.UTC` over
`datetime.timezone.utc`, and other modern Python 3.11+ patterns.

Constraints carried from the skill:

- **Syntax and types only.** Do not restructure. Converting classes to
  functions, or splitting logic from I/O, is not this stage's job.
- Keep CLI user-facing `print` output; `print` → `logging` changes behavior.
- Use only features at or below the project's minimum Python floor; if no
  floor is declared, stay at the syntax the code already uses.
- No tests → mechanical changes only, and say so in the report.

**Optional, only if the user asked for it:** `function-first-refactor` separates
pure logic from side effects. It is a preference, not a required stage — run it
on the functions that actually mix decisions with I/O, at most 3-5 per round,
and only when a test baseline exists or the user accepts characterization tests.

## Stage 3 — `review-code`

Final-gate adversarial review. Surface problems only; do not modify code.

- Security: secrets, SQL/command injection, subprocess without `check`,
  blind exception catches
- Contracts: changed signatures, removed exports, altered CLI flags or output
  shape
- Correctness: regressions, ordering of side effects, missed call sites
- Completeness: every item the prior stages claimed is actually applied

End with a verdict: **ready**, **needs fixes**, or **needs discussion** — and
report checks that could not run as limitations, never as passes.

## Context scope per stage

| Stage | Load | Why |
| --- | --- | --- |
| Preflight | `git status`, test/tooling config | Establishes the baseline |
| cleanup | Files with unused imports, dead helpers, stale docs | Avoids loading the whole codebase |
| modernize | Files that passed cleanup | Skips code that should have been deleted |
| function-first-refactor | Ranked candidates only (finder output), not the whole tree | Keeps the pass reviewable |
| review | Changed files + their callers | Focuses on regression risk |
