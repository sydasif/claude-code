---
name: debug-code
description: >-
  Systematic debugging skill. Use this whenever you encounter an error,
  unexpected behavior, test failure, or any "why doesn't this work" question.
  This includes config errors, import failures, runtime exceptions, wrong
  output, flaky tests, and "it works on my machine" problems. Do NOT just
  guess or fix the surface symptom — follow the full investigation pipeline
  to find the root cause. This skill also applies when the user asks you
  to "debug", "investigate", "figure out why", "trace this error",
  "find the root cause", or "fix this bug".
---

# Debug Code

A systematic investigation pipeline. Follow these steps in order. Do not
skip steps. Do not jump to conclusions. Each step builds on the last.

## Pipeline

### Step 1: Identify the error

- Read the **full error message**, not just the last line.
- Note the **exact file, line number, and error type**.
- Check if the error is reproducible — run it twice.
- Ask: _what did I expect to happen, and what actually happened?_

### Step 2: Search the web / GitHub

Use your search tools (WebSearch, WebFetch) to find:

- **Exact error messages** — others have hit this, solutions may exist.
- **Related issues** on GitHub (search the project's issue tracker).
- **Known limitations** — sometimes the library simply doesn't support something.
- **Alternative approaches** — how do other projects solve this?

Search for both the error _and_ the broader pattern (e.g. "Nornir env var expansion"
_and_ "Nornir SimpleInventory path configuration" — not just the error text).

### Step 3: Query library docs (Context7)

For any library or framework involved, use Context7 to check:

- **Official API docs** — what does the function actually accept?
- **Configuration reference** — what values are valid?
- **Known behaviors** — does it expand `~` but not `$HOME`?

This often reveals the _gap between what you assumed and what the library does_.

### Step 4: Inspect source code (gh api / direct read)

When the docs are unclear or contradict your observation, **go to the source**:

- Use `gh api` to pull the actual source files from GitHub.
- Search for the specific function/method involved.
- Look for string handling, path resolution, env var usage.
- Compare with **similar OSS implementations** — search for other projects
  doing the same thing and see how they handle it.

This is where the real root cause lives. The preceding steps build context so
you know _what to look for_ when you open the source.

### Step 5: Compare with other implementations

Search for other OSS projects solving the same problem. Ask:

- Do they have the same issue?
- Did they work around it? How?
- Is there a consensus pattern (e.g. "always expand vars yourself before passing to the library")?

This prevents implementing a solution that other projects already proved wrong.

### Step 6: Implement the fix

Based on the root cause found in steps 2-5:

- Focus on the **minimal change** that fixes the root cause, not the symptom.
- If the fix is in library code (you don't control it), wrap it in your own
  code — load → expand → pass, or monkey-patch as a last resort.
- If the fix is in your own code, apply it directly.

### Step 7: Verify

- **Static checks** pass (lint, types).
- **Existing tests** still pass.
- **New test** covers the fixed case (positive + negative).
- **Live run** — exercise the actual system, not just the test suite.
- **Edge case** — test `~`, `$HOME`, relative paths, etc. if path-related.

## Why this order

Errors are symptoms, not causes. The most common debugging mistake is
treating the surface error as the problem and fixing it directly, which
either breaks something else or leaves the real bug untouched.

Each step narrows the search space:

- Step 2 tells you if this is a known problem with a known fix.
- Step 3 tells you what the library _intends_ to do.
- Step 4 tells you what it _actually_ does.
- Step 5 tells you how others navigated the gap.
- By step 6 you understand the root cause well enough to fix it correctly.

If you hit a dead end at any step, go back to Step 2 with what you learned
and search again with more specific terms.
