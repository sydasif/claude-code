---
name: test-code
description: Use when the user wants end-to-end QA validation of a project as a real user/operator would experience it, not just syntax checks or running the existing test suite.
---

# QA Testing

Validate a project the way a real user or operator would - not just "does it compile" or "do the unit tests pass." The right testing strategy depends on the application type.

## Known Limitations

- Can't infer correct user workflow if documentation is missing - flag this.
- Can't fully test GUI apps without browser automation - say so.
- Can't validate ambiguous business logic - ask or list as open question.
- Can't safely exercise production integrations without test credentials - never touch prod without explicit go-ahead.
- Don't stop after the first fix. Keep testing to confirm it holds.

## Phase 1 - Understand the Application

- Inspect repository structure.
- Identify type: CLI, Web app, API, Desktop, Automation script, Library.
- Check for network automation signals (netmiko, nornir, napalm, scrapli, paramiko, ansible). If found, carry network automation testing through every later phase.
- Read documentation and reconstruct intended user workflow.
- List what's missing or unclear before testing.

## Phase 2 - Environment Setup

- Install dependencies. Create isolated test env (venv, container, temp dir).
- Check config files and required env vars.
- Verify required services/dependencies are reachable.
- Report setup problems as findings.

## Phase 3 - End-to-End Testing

Branch by application type. Read `references/testing-patterns.md` for type-specific patterns (CLI, Web/API, automation, libraries, network automation).

## Phase 4 - Bug Hunting

Read `references/bug-hunting.md` for the full checklist. For every bug: reproduce, explain, fix, re-test, confirm fix holds.

## Phase 5 - Final Report

Always end with a structured report:

- Application tested (type + network automation layer if applied)
- Test environment used
- Test cases executed
- Bugs found and fixes applied
- Remaining risks / open questions
- Final recommendation (ready to ship / needs more work / blocked on X)

## Scope Note

This is a strong general-purpose pass. For high-stakes projects (compliance-sensitive, safety-critical), recommend project-specific test strategy beyond what's described here.
