---
name: workflow-pipeline
description: Orchestrated skill pipeline for code quality: cleanup → refactor → review
user-invocable: true
---

# Workflow Pipeline Skill

> **Orchestrated code quality pipeline**: cleanup-code → refactor-code → review-code
> 
> Runs the full code quality workflow in a single flow with context isolation between stages.

## Pipeline Stages

1. **cleanup** - Prune YAGNI/DRY/KISS violations
2. **refactor** - Modernize Python code patterns
3. **review** - Security audit + correctness gate

## Pipeline Design

### Context Isolation

Each stage operates with **minimal, focused context** - only the files relevant to that stage:

| Stage | Context Scope | Why |
|-------|--------------|-----|
|  | Files with unused imports, dead helpers, stale docs | Avoids loading entire codebase |
|  | Files that passed cleanup; type-annotated files only | Skip already-pruned code |
|  | Changed files + their callers | Focus on regression risk |

### Pipeline Flow



### Stage Details

#### Stage 1: cleanup

Runs  skill with these constraints:
- **Target**: Only files modified in current session OR files matching patterns:  in project, 
- **Exclude**: Virtual environments, cache directories, generated files
- **Output**: Summary of findings (unused imports, dead helpers, YAGNI violations)
- **Decision rule**: If  items found, flag for user review; safe items auto-pruned

#### Stage 2: refactor

Runs  skill **only if** cleanup passed or had only safe items:
- **Minimum Python version**: 3.11 (from pyproject.toml)
- **Legacy patterns checked**: f-strings, pathlib, dataclasses, type hints
- **Skip conditions**: Already-clear code, version-gated changes, generated files
- **Quality baseline**: Run mypy/ruff before and after; flag any new failures

#### Stage 3: review

Runs  skill as final gate:
- **Security audit**: Check for secrets, SQL injection, password hashing issues
- **Correctness**: Verify all call sites updated; no missed references
- **Completeness**: Ensure docs match implementation
- **Output**: Pass/fail with detailed report; blocks merge if fails

## Integration with Hooks

The post-edit hooks automatically format and lint modified files via  and .

## See Also

-  skill - Stage 1: YAGNI/DRY/KISS pruning
-  skill - Stage 2: Python modernization
-  skill - Stage 3: Final quality gate
