---
description: "Run functional tests to verify all public functions/tools work as expected."
---

**function-test** — After code changes are verified clean, test every public function/tool for correctness.

1. Identify all public functions/tools (check `__init__.py` exports, `server.py` registrations, or CLI entry points)
2. For each function, test:
   - **Happy path** — call with valid, realistic inputs
   - **Error edge cases** — empty input, missing resources, invalid types
   - **Return types** — verify all variants (strings, models, ErrorResponse, None) are handled
3. Confirm no crashes, hangs, or unhandled exceptions
4. Report a summary: function name, inputs used, result type, status (PASS/FAIL/SKIP)

## Rules

- Use real calls, not mocks — catch integration issues early
- Accept `ErrorResponse` as valid if the error is handled gracefully
- Note any functions that require missing env vars or auth — don't fail the test for them
- Exit non-zero if any function crashes
