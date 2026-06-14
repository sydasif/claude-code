---
description: "Live-test all public functions/tools with real data to verify end-to-end functionality."
---

**live-test** — Call every public function/tool in the current project with real inputs to verify nothing is broken after changes.

1. Identify all public tools/functions in the project (check `server.py`, `__init__.py` exports, or CLI entry points)
2. Write a temporary test script that imports and calls each one with a realistic query
3. Run the script, capture results (PASS/FAIL per tool, elapsed time, result type preview)
4. Report a summary table with pass/fail/skip counts
5. **Delete the temp script after testing** — it's throwaway
6. Exit non-zero if any tool crashes (unhandled exception = FAIL)

## Rules

- Accept `ErrorResponse` as valid if the error is handled gracefully (missing API keys, rate limits, etc.)
- Skip tools that require missing env vars — note them in the summary
- Each call gets a 30s timeout to prevent hangs
- Network-dependent: tools require internet access
