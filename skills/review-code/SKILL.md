---
name: review-code
description: Final-gate review of completed code changes using a systematic verification approach. Use when the user asks to "review my code", "check my changes", or after a cleanup, refactor, feature, or fix.
---

# Code Review — Final Gate

> Surface problems only. Do **not** modify code.
> Report issues clearly and stop. Do not attempt inline fixes.

**When to use**: After a `cleanup-code`, `refactor-code`, feature implementation, or bug fix.
Last check before finishing work.

---

## Review Process

### 1. Orient to the Work

Gather context:

- What task was completed? (cleanup, refactor, feature, fix)
- Which files changed? Run `git diff --name-only HEAD` if in a git repo; otherwise list changed files from context or ask the user.
- If `git` is unavailable, ask the user for the diff or file list.
- Review residual risk notes from prior `cleanup-code` or `refactor-code` passes first.
- Which scope was stated? Flag changes outside it.

### 2. Structural Verification

Inspect the file system to confirm expected outputs:

- All expected files and directories are present.
- No files were accidentally deleted or left with placeholder content.
- No unintended new files created outside stated scope.
- Import paths, relative links, and cross-references still resolve.

### 3. Code-Specific Checklist

Check each item against the diff. Record a result (pass / issue found) for each.

**Correctness**

- Logic changes preserve original behavior, or the deviation is intentional and documented.
- Edge cases handled: empty inputs, None/null, zero, out-of-range values.
- Error handling is specific — no bare `except:` / `catch (e) {}` blocks.
- Errors surface rather than being swallowed.

**Public contracts**

- No public function signatures changed without explicit user approval.
- No exported names renamed or removed.
- No config key or environment variable names changed.
- API response shapes preserved.

**Tests**

- All tests pass at the same rate as the pre-change baseline.
- No tests deleted, weakened, or skipped to make the diff pass.
- New helpers or changed shared utilities have test coverage.
- Coverage matches baseline.

**Dead code and hygiene**

- No new unused imports.
- No debug `print` / `console.log` statements or commented-out code.
- No TODO/FIXME comments without a tracking reference.

**Documentation and references**

- Inline comments reflect current behavior.
- Docstrings reflect updated public APIs.
- Cross-skill references (`cleanup-code`, `refactor-code` notes) are resolved or deferred.

**Security (always flag, never evaluate severity yourself)**

- No secrets, tokens, or credentials in the diff.
- No new shell injection vectors (unescaped user input in subprocess calls, etc.).
- No new file path traversal risks.
- Dependencies added or upgraded are from known, maintained sources.

### 4. Fresh-Perspective Questions

Answer based on evidence, not intuition:

- Does this solve the original problem completely, or only partially?
- Is there anything surprising in the diff — behavior that doesn't match the task description?
- Could a new team member follow this implementation without asking questions?
- Did the change stay within scope, or did it drift?
- Are there residual risks from a prior pass that were flagged but not resolved?

---

## Output Format

Always produce this structured report. Do not replace it with prose-only summaries.

```markdown
## Code Review Report

### Orientation

- Task type: [cleanup / refactor / feature / fix / other]
- Files changed: [count and list, or reference to git diff]
- Prior pass residual risks reviewed: [yes / no / none present]

### Checklist Results

- Correctness: [pass / issues found]
- Public contracts: [pass / issues found]
- Tests: [pass / issues found]
- Dead code and hygiene: [pass / issues found]
- Documentation: [pass / issues found]
- Security flags: [none / list any]

### Issues Found

(Repeat for each issue:)

- **File and line**: e.g., `src/auth.py:42`
- **Description**: What the problem is and why it matters.
- **Severity**: blocking / should fix / minor
- **Recommended action**: What to do about it.

### Residual Risks Not Resolved

Items flagged in prior passes that remain open. If none, write "None."

### Verdict

- Ready to submit — no blocking issues found
- Needs fixes — blocking issues listed above
- Needs discussion — questions requiring user input before proceeding
```

**Example — clean review:**

```markdown
## Code Review Report

### Orientation

- Task type: refactor
- Files changed: 4 (auth.py, utils.py, tests/test_auth.py, README.md)
- Prior pass residual risks reviewed: yes (2 items from refactor-code pass, both resolved)

### Checklist Results

- Correctness: pass
- Public contracts: pass — no signatures changed
- Tests: pass — coverage unchanged at 87%
- Dead code and hygiene: pass
- Documentation: pass
- Security flags: none

### Issues Found

None.

### Residual Risks Not Resolved

None.

### Verdict

Ready to submit — no blocking issues found.
```

---

## Notes for Agentic Operation

- **This skill does not modify code.** Report issues and stop. Do not fix inline.
- Stop and surface blocking issues before further work.
- Flag scope drift explicitly — do not silently accept it.
- Report all security flags regardless of apparent severity. Surface them for the user.
- If `git` is unavailable and the user hasn't provided a diff, ask: "Can you share the diff or list the changed files so I can review them?"
