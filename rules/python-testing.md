# Testing Standards — Mandatory

## Pre-Change Gate

All existing tests must pass before any changes are made. If tests are already failing before you touch anything, document this in the Discovery Report and do not treat subsequent failures as your regressions.

## Coverage Thresholds (branch coverage)

These are **targets**, not hard gates that block all work on a new or under-tested codebase. When starting below these thresholds, note the gap in the Discovery Report and treat all cleanup/refactor candidates as "needs care" until coverage reaches the minimum.

| Scope          | Minimum Target |
| -------------- | -------------- |
| Business logic | ≥ 95%          |
| APIs           | ≥ 90%          |
| Models         | ≥ 85%          |

## Every Task Requires

- [ ] Static checks pass (lint + types)
- [ ] Positive test case (expected behavior)
- [ ] Negative test case (bad/edge input)
- [ ] Regression tests still pass
- [ ] Rollback procedure validated

## Test Authoring Rules

- Tests are fully **independent** — no shared state between tests.
- Follow **AAA pattern**: Arrange → Act → Assert.
- No test chaining; no flaky tests; minimize mocking.
- **Never delete, weaken, or skip a test to make a diff pass.** Surface the failure instead.

## Pre-commit Commands

```bash
uv run pytest
uv run pytest --cov=src --cov-branch --cov-fail-under=90
```

---

## See Also

- `@rules/python-style.md` — Type checking, linting, security scans
