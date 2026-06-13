---
description: Run the full optimization + testing pipeline on project.
---

Run the full optimization + testing pipeline:

1. **cleanup-code** — Apply YAGNI, DRY, KISS. Remove dead code, prune unused imports/variables,
   eliminate duplication, simplify over-abstraction. Do not change behavior.

2. **refactor-code** — Modernize Python code with comprehensive type hints, dataclasses (+slots),
   pathlib, f-strings, logging.exception over logging.error, datetime.UTC over datetime.timezone.utc,
   and any other modern Python 3.11+ patterns. Do not change behavior.

3. **review-code** — Final-gate adversarial review. Check for:
   - Security issues (XXE, subprocess without check, blind exception catches)
   - Contract breaks (changed signatures, removed exports)
   - Correctness regressions
   - Any issues the prior two stages missed

4. **functional-testing** — After all code changes are verified clean:
   - Import and call every public function/tool at least once with real inputs
   - Test normal operation paths (happy path)
   - Test error edge cases (empty input, missing resources, network failures)
   - Test all return type variants (markdown, JSON/structured, ErrorResponse)
   - Verify logging and error messages are clear and actionable
   - Confirm no crashes, hangs, or unhandled exceptions

Use the project's existing tooling (ruff, mypy, pytest) to verify at each stage.
Commit after stage 4 if all checks pass. No behavior changes.
