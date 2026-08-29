---
name: workflow-pipeline
description: Orchestrated skill pipeline for code quality: cleanup → refactor → review → test
user-invocable: true
---

# Workflow Pipeline Skill

> **Orchestrated code quality pipeline**: cleanup-code → refactor-code → review-code → test-code
> 
> Runs the full code quality workflow in a single flow with context isolation between stages.
> 
> ## Pipeline Stages
> 
> 1. **cleanup** - Prune YAGNI/DRY/KISS violations
> 2. **refactor** - Modernize Python code patterns
> 3. **review** - Security audit + correctness gate
> 4. **test** - End-to-end QA validation
> 
> ## Usage
> 
> ```bash
> # Run the full pipeline on a project
> claude run skill://workflow-pipeline /path/to/project
> 
> # Run individual stages
> claude run skill://workflow-pipeline:cleanup /path/to/project
> claude run skill://workflow-pipeline:refactor /path/to/project
> claude run skill://workflow-pipeline:review /path/to/project
> claude run skill://workflow-pipeline:test /path/to/project
> ```

## Pipeline Design

### Context Isolation

Each stage operates with **minimal, focused context** - only the files relevant to that stage:

| Stage | Context Scope | Why |
|-------|--------------|-----|
| `cleanup` | Files with unused imports, dead helpers, stale docs | Avoids loading entire codebase |
| `refactor` | Files that passed cleanup; type-annotated files only | Skip already-pruned code |
| `review` | Changed files + their callers | Focus on regression risk |
| `test` | Files modified in current session | Real-user operation simulation |

### Pipeline Flow

```
User Edit → Pre-edit Analysis (hook) → Edit → Post-edit Formatting (hook) → 
Post-edit Lint (hook) → Pipeline: cleanup → refactor → review → test
```

### Stage Details

#### Stage 1: cleanup

Runs `cleanup-code` skill with these constraints:
- **Target**: Only files modified in current session OR files matching patterns: `*.py` in `nornir_napalm_mcp/`, `tests/`
- **Exclude**: Virtual environments, cache directories, generated files
- **Output**: Summary of findings (unused imports, dead helpers, YAGNI violations)
- **Decision rule**: If `needs care` items found, flag for user review; safe items auto-pruned

#### Stage 2: refactor

Runs `refactor-code` skill **only if** cleanup passed or had only safe items:
- **Minimum Python version**: 3.11 (from pyproject.toml)
- **Legacy patterns checked**: f-strings, pathlib, dataclasses, type hints
- **Skip conditions**: Already-clear code, version-gated changes, generated files
- **Quality baseline**: Run mypy/ruff/pytest before and after; flag any new failures

#### Stage 3: review

Runs `review-code` skill as final gate:
- **Security audit**: Check for secrets, SQL injection, password hashing issues
- **Correctness**: Verify all call sites updated; no missed references
- **Completeness**: Ensure docs match implementation
- **Output**: Pass/fail with detailed report; blocks merge if fails

#### Stage 4: test

Runs `test-code` skill:
- **Real-user QA**: Launch actual program, exercise changed paths
- **Observable verification**: Terminal interaction, output, or state
- **Acceptance**: No new failures, coverage matches baseline, behavioral test passes
- **Note**: Does NOT run full project test suite (too heavy); runs targeted smoke tests

## Integration with Hooks

The pipeline is **automatically triggered** by the Claude Code hook system:

1. **Pre-edit** (`PreToolUse`): Runs `pre-edit-analysis.js` to surface cleanup candidates
2. **Post-edit** (`PostToolUse`): Runs pipeline in sequence:
   - `format-code.js` (ruff + prettier)
   - `post-edit-validation.js` (ruff check + syntax)
   - **Optional**: Invoke `skill://workflow-pipeline` for full pipeline

## Configuration

Pipeline behavior configured via `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [
        {"type": "command", "command": "node /home/zulu/.claude/hooks/format-code.js"},
        {"type": "command", "command": "node /home/zulu/.claude/hooks/post-edit-validation.js"},
        {"type": "command", "command": "python3 /home/zulu/.claude/skills/workflow-pipeline/index.py"}
      ]
    }]
  }
}
```

## See Also

- `cleanup-code` skill - Stage 1: YAGNI/DRY/KISS pruning
- `refactor-code` skill - Stage 2: Python modernization
- `review-code` skill - Stage 3: Final quality gate
- `test-code` skill - Stage 4: End-to-end validation