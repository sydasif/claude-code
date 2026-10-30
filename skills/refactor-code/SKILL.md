---
name: refactor-code
description: Refactor, modernize, clean up, or restructure Python code in two complementary ways - (1) modernize syntax and structure (type hints, dataclasses, pathlib, f-strings, match, logging, context managers, async hygiene), and (2) separate pure business logic from side effects ("functional core, imperative shell") so code is testable without heavy mocking. Use this skill whenever the user asks to refactor, modernize, update, clean up, simplify, decouple, or make Python code testable; shares a function that mixes DB/API/file/network/email/device I/O with validation, calculations, formatting, or decision logic; complains that tests need lots of mocks; or is writing new Python that touches both logic and I/O, even if they never say "pure functions" or "refactor". Run cleanup-code first to prune dead code.
---

# Refactor Code (Python)

Two passes, in this order, each optional depending on what the user asked for and what the code needs:

- **Pass A - Modernize:** mechanical, low-risk updates to syntax and types.
- **Pass B - Separate logic from effects:** move decisions and transformations into pure functions; push I/O to the edges.

> Prune with `cleanup-code` first. Refactor code that _should exist_, not code that should be deleted.

Modernizing first keeps Pass B diffs small and readable, because the structural change is not mixed with style noise. If the user only wants one pass ("just add type hints", "make this testable"), do only that one.

## Ground rules

- **Preserve behavior.** Outputs, error types, and the order of side effects stay identical unless the user asks otherwise. Anything you notice but don't change goes in the final report.
- **Pragmatism over purity.** Skip a change if the code is already short and clear, the change is gated on a newer Python than the project supports, the file is generated or one-off, or the new abstraction is heavier than what it replaces.
- **One pattern at a time, tests after each.** A failing test then points at exactly one change.
- **Stay in the user's style.** Match their naming, typing conventions, and test framework (pytest by default).

## Process

### 1. Assess

1. **Find the minimum Python version** in `pyproject.toml`, `setup.cfg`, `.python-version`, or CI config. Only use features available at or below that floor.
2. **Inventory legacy patterns** against `references/checklist.md`. Mark each item _applies and safe_, _applies but needs a version check_, _changes behavior - confirm first_, or _not present_.
3. **Mark each line of the target code** as logic (decision or transformation) or effect (I/O). If a function mixes both, it is a Pass B candidate.

### 2. Baseline

Run the project's tests, type checker, and linter before touching anything, and record the results. Flag existing failures as pre-existing so they are not mistaken for regressions. Defaults for a `uv` project (adapt to the project's actual tooling and layout):

```bash
uv run mypy src/
uv run ruff check .
uv run pytest --tb=short
uv run pytest --cov=src --cov-report=term-missing
```

If there are no tests around the code you are about to restructure, say so, and offer to write characterization tests first. Pass B is much riskier without them.

### 3. Pass A - Modernize

Run `pyupgrade` or `ruff --fix` first for bulk mechanical changes (f-strings, `pathlib` suggestions, type syntax), and reserve manual work for structural changes. Then work through `references/checklist.md`. Concrete before/after code for the common cases is in `references/scenarios.md`.

Some checklist items change behavior and are marked as such there (e.g. `print` to `logging` changes what reaches stdout, `configparser` to `tomllib` changes the config file format, narrowing a broad `except` changes what gets caught). Apply these only when the user wants them, or list them as suggestions in the report.

### 4. Pass B - Separate logic from effects

**Core rule: pure functions are the logic; side effects are the shell. Keep them apart.** Business logic that is pure can be unit tested with plain inputs and outputs, reused (API response, UI preview, CLI, export), and left untouched when the transport or storage changes.

A function is pure when it depends only on its arguments (no globals, clock, randomness, env vars, or hidden state), has no side effects (no file writes, printing, logging, network, DB, or mutating its inputs), and returns the same output for the same input.

**Three layers.** Dependencies point inward: orchestration calls core and effects; core never calls effects.

| Layer | Role | Examples |
|---|---|---|
| Core logic | Pure, reusable, unit-testable without mocks | validation, business rules, message/report building, calculations, transforming API responses |
| Orchestration | Fetches inputs, calls core functions, decides when effects fire | handlers, views, CLI entry points, `process_*` functions |
| Side effects | The actual I/O | DB calls, HTTP requests, SMTP, file and device access |

**Steps:**

1. **Extract logic** into small, single-purpose functions that take plain data in and return plain data out (dicts, dataclasses, tuples). Return a description of what to do (e.g. an email dict) rather than doing it.
2. **Isolate effects** into thin functions that only do the I/O and contain no branching business rules.
3. **Write the orchestration function** that sequences: fetch, decide, build, send/save.
4. **Name by intent.** Pure functions: `is_`, `build_`, `calculate_`, `format_`, `parse_`. Effect functions say what they touch: `send_`, `save_`, `fetch_`.

**Where to look first:** data validation; business rules and eligibility checks; email, notification, and message generation; report and output formatting; calculations and scoring; transforming or normalizing API responses.

**Before (mixed):**

```python
def send_welcome_email(user_id):
    user = db.get_user(user_id)
    if user and not user.has_signed_in:
        email = generate_email(user)
        smtp.send(email)
```

**After (layered):**

```python
def build_welcome_email(user):            # pure
    return {
        "to": user.email,
        "subject": "Welcome!",
        "body": f"Hello {user.name}, thanks for joining us!",
    }

def send_email(email):                    # effect
    smtp.send(email)

def process_new_user(user_id):            # orchestration
    user = db.get_user(user_id)
    if user and not user.has_signed_in:
        send_email(build_welcome_email(user))
```

`build_welcome_email` is testable with a fake user, reusable for an API response or Slack message, and the transport can change without touching the rules. A one-line condition like `not user.has_signed_in` stays inline; extract it only when it grows into a real business rule.

For a longer multi-step example (order submission with invoice and PDF) and matching tests, read `references/pure-functions-example.md`.

**Guardrails for Pass B:**

- **Aim for the core ~80% of logic, not 100%.** Do not force tiny wrappers, class hierarchies, or functional-programming idioms. If a function is already small and has one clear job, leave it alone.
- **Watch for hidden impurity:** `datetime.now()`, `random`, `os.environ`, mutable default arguments, in-place mutation of arguments, logging inside logic. Pass clocks, random sources, and config in as parameters (e.g. `now`) so the function stays pure.
- **Logging and error handling live at the edges.** This is where the two passes meet: when Pass A replaces `print` with `logging`, put the `logger.*` calls in orchestration or effect code, not inside pure functions. Pure functions may raise on invalid input and return data; the caller logs, retries, falls back, and handles I/O errors. Use `%`-style arguments in `logger.*` calls (lazy formatting), not f-strings.
- **Don't test the pure core through mocks.** If a test has to patch a pure function, the layers are probably tangled.

### 5. Tests

- Pure functions get plain input/output tests with no mocks.
- Orchestration gets one or two tests with the effects mocked (the effects fire in the right order, and nothing fires on invalid input).
- Add tests before refactoring if coverage of the target code is thin, and keep the existing ones passing.

### 6. Quality assurance

Re-run the baseline commands. Pass criteria: no new mypy errors, no new lint violations, test pass rate same or better, coverage at or above baseline. Verify that behavior is identical.

## Output format

When refactoring existing code, respond with:

1. The refactored code, layered as above.
2. A short note listing which functions are pure, effect, and orchestration (skip when only Pass A applied).
3. Tests for the new pure functions.
4. Baseline vs. after results for tests, types, and lint.
5. Behavior changes or risks you noticed but intentionally left unchanged, plus any behavior-changing modernizations you held back for the user to approve.

## See also

- `cleanup-code` - run first to prune dead code
- `review-code` - final gate review after refactoring

## Source

Pass B is based on "The One Refactor That Cleaned Up 80% of My Python Code" by mata (The Pythonworld, Aug 2025). The "80%" figure is the author's own claim; the underlying principle is the well-established "functional core, imperative shell" pattern.
