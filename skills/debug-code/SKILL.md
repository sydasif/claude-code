---
name: debug-code
description: Debug errors, failed commands, test failures, runtime exceptions, wrong output, flaky behavior, regressions, config/import issues, and bug-fix requests using a local-first CLI workflow with Context7, GitHub CLI, and web-search MCP for external evidence.
---

# Debug Code

## Operating Principle

Treat errors as symptoms until evidence shows the cause. Work from the most concrete signal available: exact command, full output, local code, recent changes, tests, current docs/source for external dependencies, then the smallest fix that explains all observed behavior.

Do not jump straight from an error string to an edit. First reproduce, isolate, explain, then change.

## Tool Priority

Use the best available tool for the evidence needed. Do not block debugging just because a preferred tool is missing.

- Local CLI first: `rg`, `rg --files`, `git status`, `git diff`, focused tests, logs, dependency manifests, lockfiles, and local dependency source.
- Context7: use for current, version-aware library/framework documentation and code examples when dependency behavior matters. Context7 supports CLI/skills and MCP modes.
- GitHub CLI (`gh`): use for GitHub-native evidence such as issues, PRs, checks, releases, repo metadata, source files, and API calls from the terminal.
- web-search MCP: use for real-time web/news search, domain-specific docs search, and clean page extraction when current external information or non-GitHub sources matter.
- Fallback: if MCP tools or `gh` are unavailable, use local files and official web sources. Report unavailable tools only when that limits confidence or verification.

## Tool Sources

- Context7 for current library/framework docs and examples. Source: https://github.com/upstash/context7
- GitHub CLI `gh` for issues, PRs, checks, releases, source/API access. Source: https://cli.github.com/
- web-search MCP for web search, domain docs search, and page extraction. Source: https://github.com/sydasif/web-search-mcp

## CLI Workflow

### 1. Capture The Failure

- Record the exact command, inputs, environment assumptions, full error output, file paths, line numbers, versions, and current working directory.
- Re-run once when safe to confirm the failure is reproducible. For flaky failures, run enough times to identify the pattern.
- Separate expected behavior from actual behavior in one sentence.
- If the user provided only a fragment, inspect logs/tests/code before asking for more.

### 2. Check Local State First

Use local evidence before external lookup:

- Inspect nearby code, call sites, config, fixtures, generated files, dependency manifests, lockfiles, and recent diffs.
- Prefer fast shell tools: `rg`, `rg --files`, `git diff`, `git status`, targeted test commands, and focused log inspection.
- Read enough context around each relevant symbol to understand the contract, not just the failing line.
- Check local dependency source when available before assuming external behavior.
- Protect unrelated user changes. Do not revert or overwrite changes you did not make.

### 3. Form Testable Hypotheses

Maintain a small hypothesis list:

- What could produce this exact symptom?
- What observation would prove or disprove each candidate?
- Which candidate best explains all evidence, including edge cases?

Prefer experiments that narrow the search space quickly: focused tests, minimal reproduction commands, temporary logging/inspection that can be removed, or reading the implementation path.

### 4. Pull Current External Evidence

Use external sources when the issue depends on dependency, framework, CLI, API, OS, or standards behavior that may have changed, or when local code delegates behavior to something outside the repo.

Use this order when applicable:

- Context7 for library/framework docs, APIs, configuration, version-specific examples, and known edge cases.
- `gh issue list`, `gh issue view`, `gh pr view`, `gh pr checks`, `gh release view`, `gh repo view`, and `gh api` for upstream GitHub issues, PRs, releases, metadata, checks, and raw source.
- web-search MCP `search_web` for broad known-error searches, `search_domain` for official docs or specific sites, and `fetch_page` for reading a specific page cleanly.

Prefer primary sources: official docs, changelogs, release notes, source code, and upstream issues. Use community posts only as leads unless they include reproducible evidence.

### 5. Confirm Root Cause Before Editing

Before making code changes, be able to state:

- The root cause.
- Why the observed failure follows from that cause.
- What evidence ruled out the main alternatives.
- Which behavior the fix must preserve.

If the root cause is still uncertain, keep investigating. If uncertainty remains after reasonable investigation, report the evidence, the uncertainty, and the next best diagnostic step instead of shipping a speculative fix.

### 6. Implement The Smallest Correct Fix

- Fix the cause, not only the immediate symptom.
- Follow the repository's existing style, abstractions, and ownership boundaries.
- Keep changes scoped. Avoid opportunistic refactors unless they are necessary to fix safely.
- For dependency limitations, adapt at your boundary: validate, normalize, wrap, pin, or document behavior in code/tests as appropriate.
- Remove temporary debug prints, probes, and scratch artifacts before finishing.

### 7. Verify The Fix

Verification should match risk:

- Re-run the original failing command or reproduction.
- Run the narrowest relevant test first, then broader tests if the change touches shared behavior.
- Add or update a regression test when the bug is non-trivial, user-facing, shared, or likely to recur.
- Cover edge cases that were part of the root cause.
- Run static checks when the repository has an obvious command for them.
- Use `gh pr checks` or `gh run view` when CI state is part of the failure or verification.

If a verification command cannot be run, say exactly why and what remains unverified.

## Flaky Or Intermittent Failures

For flakiness, do not rely on a single pass:

- Run repeated attempts or targeted subsets to estimate frequency.
- Look for ordering, timing, randomness, shared state, network, timezone, locale, filesystem, cache, and parallelism dependencies.
- Capture seed, timestamps, worker count, and environment details when available.
- Check upstream issues/releases with `gh` and web-search MCP when the flake may come from a dependency or hosted service.
- Prefer deterministic fixes over retries. Retries are acceptable only when the underlying operation is inherently unreliable and the retry policy is bounded and justified.

## Reporting Back

When finished, keep the summary evidence-based:

- Root cause in plain language.
- Files changed and why.
- Verification commands and outcomes.
- External sources used, if they affected the conclusion.
- Remaining risk or unverified areas, if any.
