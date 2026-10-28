---
name: pure-functions-refactor
description: Refactor or write Python code by separating pure business logic from side effects ("functional core, imperative shell"). Use this skill whenever the user asks to clean up, simplify, refactor, make testable, or decouple Python code, or shares a function that mixes DB/API/file/network/email I/O with validation, calculations, formatting, or decision logic, or complains that tests need heavy mocking. Also use when writing new Python functions that touch both logic and I/O, even if the user doesn't mention "pure functions".
---

# Pure Functions Refactor

Keep business logic in pure functions and push side effects to the edges. This is the single refactor that most improves testability, reuse, and readability in Python code.

Core rule: **pure functions are the logic; side effects are the shell. Keep them apart.**

## What counts as pure

A function is pure when it:

1. Depends only on its arguments (no globals, clock, randomness, env vars, or hidden state).
2. Has no side effects (no file writes, printing, logging, network, DB, or mutating its inputs).
3. Returns the same output for the same input.

## Three layers

| Layer | Role | Example |
|---|---|---|
| Core logic | Pure, reusable, unit-testable without mocks | validation, business rules, message/report building, calculations, transforming API responses |
| Orchestration | Fetches inputs, calls core functions, decides when effects fire | handlers, views, CLI entry points, `process_*` functions |
| Side effects | The actual I/O | DB calls, HTTP requests, SMTP, file and device access |

Dependencies point inward: orchestration calls core and effects; core never calls effects.

## Workflow

1. **Read the target code** and mark each line as decision/transformation (logic) or I/O (effect).
2. **Extract logic** into small, single-purpose functions that take plain data in and return plain data out (dicts, dataclasses, tuples). Return a description of what to do (e.g. an email dict) rather than doing it.
3. **Isolate effects** into thin functions that do only the I/O and contain no branching business rules.
4. **Write an orchestration function** that sequences: fetch, decide, build, send/save.
5. **Name by intent.** Pure functions use verbs like `is_`, `build_`, `calculate_`, `format_`, `parse_`. Effect functions say what they touch: `send_`, `save_`, `fetch_`.
6. **Add or update tests.** Pure functions get plain input/output tests with no mocks. Orchestration gets at most one or two tests with mocked effects.
7. **Preserve behavior.** Do not change outputs, error types, or call order of effects unless the user asks. Mention anything you notice but didn't change.

## Where to look first

Extract pure functions for these before anything else:

- Data validation
- Business rules and eligibility checks
- Email, notification, and message generation
- Report and output formatting
- Calculations and scoring
- Transforming or normalizing API responses

## Before / after pattern

Before (mixed):

```python
def send_welcome_email(user_id):
    user = db.get_user(user_id)
    if user and not user.has_signed_in:
        email = generate_email(user)
        smtp.send(email)
```

After (layered):

```python
def is_first_visit(user):                 # pure
    return not user.has_signed_in

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
    if user and is_first_visit(user):
        send_email(build_welcome_email(user))
```

Gains: `build_welcome_email` is testable with a fake user, reusable for an API response, UI preview, or Slack message, and the transport can be swapped without touching the rules.

For a longer multi-step example (order submission with invoice and PDF), read `references/examples.md`.

## Guardrails

- **Pragmatism over purity.** Aim to move roughly the core 80% of logic into pure functions. Do not force it into tiny wrappers, class hierarchies, or functional-programming idioms.
- **Do not over-split.** If a function is already small and has one clear job, leave it alone.
- **Watch for hidden impurity**: `datetime.now()`, `random`, `os.environ`, mutable default args, in-place mutation of arguments, logging inside logic. Pass these in as parameters (e.g. `now`) so the function stays pure.
- **Keep error handling at the edges.** Pure functions may raise on invalid input; retries, fallbacks, and I/O error handling belong in orchestration or effect code.
- **Stay in the user's style.** Match their naming, typing, and test framework (pytest by default).

## Output format

When refactoring existing code, respond with:

1. The refactored code, layered as above.
2. A short note listing which functions are pure vs. effect vs. orchestration.
3. Tests for the new pure functions.
4. Any behavior or risks you noticed but intentionally left unchanged.

## Source

Based on "The One Refactor That Cleaned Up 80% of My Python Code" by mata (The Pythonworld, Aug 2025). The "80%" figure is the author's own claim; the underlying principle is the well-established "functional core, imperative shell" pattern.
