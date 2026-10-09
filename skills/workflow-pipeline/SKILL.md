---
name: workflow-pipeline
description: Orchestrated skill pipeline for code quality: cleanup → refactor → review
user-invocable: true
---

# Workflow Pipeline Skill

> **Orchestrated code quality pipeline**: `cleanup-code` → `refactor-code` → `review-code`
>
> Runs the full code quality workflow in a single flow with context isolation between stages.

## Pipeline Stages

1. **cleanup** — Prune YAGNI/DRY/KISS violations
2. **refactor** — Modernize Python code patterns
3. **review** — Security audit + correctness gate

## Pipeline Design

### Context Isolation

Each stage operates with **minimal, focused context** — only the files relevant to that stage:

| Stage    | Context Scope                                        | Why                            |
| -------- | ---------------------------------------------------- | ------------------------------ |
| cleanup  | Files with unused imports, dead helpers, stale docs  | Avoids loading entire codebase |
| refactor | Files that passed cleanup; type-annotated files only | Skip already-pruned code       |
| review   | Changed files + their callers                        | Focus on regression risk       |

### Pipeline Flow

```text
cleanup-code → refactor-code → review-code
     │               │              │
  prune dead    modernize py    final gate:
     │               │              │
  report ──────▶ report ──────▶ pass / needs fixes
```

### Stage Details

#### Stage 1: cleanup

Runs the `cleanup-code` skill with these constraints:

- **Target**: Only files modified in the current session, or files matching the patterns named by the caller in the project
- **Exclude**: Virtual environments, cache directories, generated files
- **Output**: Summary of findings (unused imports, dead helpers, YAGNI violations)
- **Decision rule**: If blocking items are found, flag them for review; safe items are auto-pruned

#### Stage 2: refactor

Runs the `refactor-code` skill **only if** cleanup passed or had only safe items:

- **Minimum Python version**: Read it from `pyproject.toml` (default floor 3.11 when absent)
- **Legacy patterns checked**: f-strings, pathlib, dataclasses, type hints
- **Skip conditions**: Already-clear code, version-gated changes, generated files
- **Quality baseline**: Run mypy/ruff before and after; flag any new failures

#### Stage 3: review

Runs the `review-code` skill as the final gate:

- **Security audit**: Check for secrets, SQL injection, password hashing issues
- **Correctness**: Verify all call sites updated; no missed references
- **Completeness**: Ensure docs match implementation
- **Output**: Pass/fail with detailed report; blocks merge on failure

## See Also

- `cleanup-code` — Stage 1: YAGNI/DRY/KISS pruning
- `refactor-code` — Stage 2: Python modernization
- `review-code` — Stage 3: Final quality gate
