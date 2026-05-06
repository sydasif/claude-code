---
name: code-review
description: Final-gate review of completed changes using a systematic, fresh-eyes verification approach. Run after code-cleanup and/or code-refactor passes to catch errors, verify completeness, and confirm quality standards before submitting work.
---

# Code Review — Final Gate

> **When to use**: After completing a `code-cleanup`, `code-refactor`, or any significant implementation task.
> This skill is the last check before work is considered done. It does not make changes — it surfaces problems.

---

## Purpose

Provide a structured, code-aware methodology for reviewing completed work to catch errors, verify correctness, confirm completeness, and ensure nothing was silently broken or left unresolved.

---

## Review Process

### 1. Orient to the Work

Before reviewing, gather context:

- What task was completed? (cleanup, refactor, feature, fix)
- What files were changed? Run `git diff --name-only` or equivalent.
- Are there residual risk notes from a prior `code-cleanup` or `code-refactor` pass? If so, review those first — they are the highest-priority items to verify.
- What is the stated scope? Flag anything in the diff that falls outside it.

### 2. Structural Verification

Inspect the file system to confirm expected outputs:

- All expected files and directories are present.
- No files were accidentally deleted or left with placeholder content.
- No unintended new files were created outside the stated scope.
- Import paths, relative links, and cross-references still resolve correctly.

### 3. Code-Specific Checklist

Work through this checklist against the actual diff, not from memory.

**Correctness**
- [ ] Logic changes preserve the original behavior (or the deviation is intentional and documented)
- [ ] Edge cases are handled: empty inputs, None, zero, out-of-range values
- [ ] Error handling is specific — no new bare `except:` blocks introduced
- [ ] No silent failures: errors surface rather than being swallowed

**Public contracts**
- [ ] No public function signatures changed without explicit user approval
- [ ] No exported names renamed or removed
- [ ] No config key names or environment variable names changed
- [ ] API response shapes preserved

**Tests**
- [ ] All tests pass at the same rate as the pre-change baseline
- [ ] No tests were deleted, weakened, or skipped to make the diff pass
- [ ] New helpers or changed shared utilities have test coverage
- [ ] Coverage did not meaningfully drop from baseline

**Dead code and hygiene**
- [ ] No new unused imports were introduced
- [ ] No debug `print` statements or commented-out code left in
- [ ] No TODO/FIXME comments introduced without a tracking reference

**Documentation and references**
- [ ] Inline comments reflect current behavior, not prior behavior
- [ ] Any updated public APIs are reflected in docstrings
- [ ] Cross-skill references (`code-cleanup`, `code-refactor` notes) are resolved or explicitly deferred

**Security and safety (flag, do not fix)**
- [ ] No secrets, tokens, or credentials appear in the diff
- [ ] No new shell injection vectors (unescaped user input in subprocess calls, etc.)
- [ ] No new file path traversal risks
- [ ] Dependencies added or upgraded are from known, maintained sources

### 4. Fresh-Perspective Questions

Answer each question based on evidence in the code, not intuition:

- Does this solve the original problem completely, or partially?
- Is there anything in the diff that is surprising — behavior that doesn't match the task description?
- Is the implementation something a new team member could follow without needing to ask questions?
- Did the change stay within its stated scope, or did it drift?
- Are there any residual risks from the prior pass that were flagged but not resolved?

---

## Output Format

Always produce a structured review report — do not summarize in prose only.

```
## Code Review Report

### Orientation
- Task type: [cleanup / refactor / feature / fix / other]
- Files changed: [count and list or reference to git diff]
- Prior pass residual risks reviewed: [yes / no / none present]

### Checklist Results
- Correctness: [pass / issues found]
- Public contracts: [pass / issues found]
- Tests: [pass / issues found]
- Dead code and hygiene: [pass / issues found]
- Documentation: [pass / issues found]
- Security flags: [none / list any]

### Issues Found
For each issue:
- File and line reference
- Description of the problem
- Severity: [blocking / should fix / minor]
- Recommended action

### Residual Risks Not Resolved
Items flagged in prior passes that remain open.

### Verdict
[ ] Ready to submit — no blocking issues found
[ ] Needs fixes — blocking issues listed above
[ ] Needs discussion — questions that require user input before proceeding
```

---

## Notes for Agentic Operation

- This skill **does not make changes**. If issues are found, report them. Do not fix them inline during review — that conflates review with implementation and makes the diff harder to reason about.
- If a blocking issue is found, stop and surface it before proceeding with any further work.
- If the review uncovers scope drift (the diff contains changes outside what was asked), flag it explicitly rather than silently accepting it.
- Security flags are always reported, even if they appear minor. Do not evaluate severity yourself — surface them for the user.