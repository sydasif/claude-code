---
name: test-code
description: End-to-end QA validation of a project as a real user/operator would experience it, not just syntax checks. Always prefer this over just running the existing test suite and calling it done.
---

# QA Testing

Acts as a senior QA engineer + developer validating a project the way a real
user or operator would experience it — not just "does it compile" or "do the
existing unit tests pass."

This is not a one-size-fits-all pass. The right testing strategy depends on
what kind of application this is, so the first job is always to figure that
out before touching anything.

## Known limitations (be upfront about these, don't paper over them)

- Can't infer the correct user workflow if documentation is missing or
  contradictory — flag this rather than guessing silently.
- Can't fully test GUI applications without extra tooling (browser automation,
  screenshot diffing, etc.) — say so if none is available.
- Can't validate business logic when expected behavior is ambiguous — ask, or
  list it as an open question in the final report rather than assuming.
- Can't safely exercise production integrations without test credentials, test
  data, or a lab/sandbox environment — never touch prod without an explicit
  go-ahead.
- Don't stop after fixing the first obvious error. Keep testing after a fix to
  confirm it actually holds and didn't shift the bug elsewhere.

## Phase 1 — Understand the application

- Inspect the full repository structure.
- Identify the application type:
  - CLI
  - Web application
  - API
  - Desktop application
  - Automation script
  - Library / package
- **Also check for network automation signals** (import of `netmiko`,
  `nornir`, `napalm`, `scrapli`, `paramiko`, `ansible`/`ansible-pynet`
  collections, inventory/hosts files, YAML device definitions). If present,
  this is a network automation project — carry it through every later phase
  using the network automation layer below, in addition to whatever base type
  (CLI / automation script / library) it also is. Don't wait to be told.
- Read whatever documentation exists (README, docstrings, CONTRIBUTING,
  comments) and reconstruct the intended user workflow.
- Explicitly list what's missing or unclear before testing starts — don't
  silently fill gaps with assumptions.

## Phase 2 — Environment setup

- Install dependencies.
- Create an isolated test environment (venv, container, temp dir — whatever
  fits).
- Check configuration files and required env vars.
- Verify required services/dependencies are actually reachable.
- Report setup problems as findings — don't quietly work around them and move
  on as if they don't matter to a real user hitting the same thing.

## Phase 3 — End-to-end testing

Run the application exactly as a user would, branching by type:

**CLI**
- Normal commands, invalid input, missing arguments, error messages, exit
  codes.

**Web / API**
- Start all required services.
- Walk through real user flows, not just individual endpoints in isolation.
- Test auth and validation paths, and failure scenarios (bad tokens, expired
  sessions, malformed payloads).

**Automation tools**
- Run complete workflows end to end.
- Validate generated output.
- Verify actual changes on target systems, not just "the script exited 0."
- Test connection failures and recovery paths.

**Libraries / packages**
- Import and use the package the way a consumer would.
- Test public functions with valid and invalid parameters.
- Check that exceptions are raised where they should be, with useful
  messages.

**Network automation add-on** (apply on top of the base type when detected in
Phase 1):
- Never assume a mocked/dry-run success means the real automation works.
- Test against a lab topology if one is available; if not, say clearly that
  device-level validation wasn't possible and why.
- Capture device state before and after execution and diff it — don't just
  trust the script's own "success" message.
- Check idempotency: running the script twice should not produce unwanted
  changes the second time.
- Explicitly test: unreachable devices, authentication failures, malformed
  inventory data, and partial command failures mid-run.

## Phase 4 — Bug hunting

Go past syntax errors. Look for:

- Runtime failures
- Incorrect logic
- Bad assumptions baked into the code
- Missing validation
- Security issues
- Dependency problems (pinning, known CVEs, version conflicts)
- Poor error handling (swallowed exceptions, unhelpful messages)
- User experience problems (confusing output, silent failures)

For every bug found:
1. Reproduce it.
2. Explain why it happens.
3. Fix it.
4. Re-run the relevant test.
5. Confirm the fix actually holds.

## Phase 5 — Final report

Always end with a structured report, not just a stream of findings:

- Application tested (type, and network-automation layer if applied)
- Test environment used
- Test cases executed
- Bugs found
- Fixes applied
- Remaining risks / open questions (including anything Phase 1 flagged as
  ambiguous or untestable)
- Final recommendation (ready to ship / needs more work / blocked on X)

## Notes on scope

This skill is a strong general-purpose pass for most projects, but it isn't a
substitute for a human writing project-specific test strategy where the
stakes are high (compliance-sensitive systems, safety-critical automation,
etc.) — say so if a project seems to warrant more than what's described here.
