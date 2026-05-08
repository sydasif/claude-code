# Core Principles

## Security-First Engineering

- **Input is Poison** — Validate all external input: type, length, format.
- **Least Privilege** — Request only the minimum permissions necessary.
- **No Secrets in Code** — Use environment variables exclusively.

## The Simplicity Tax

- Every line of code is a maintenance liability.
- Make every change as simple as possible. Impact minimal code.
- **Staff Engineer Test:** Would a staff engineer approve this without hesitation?

## No Laziness

- Find root causes. No temporary fixes. No workarounds that defer the problem.
- Senior developer standards apply to every change, regardless of size.

## Minimal Impact

- Changes should only touch what is necessary.
- Avoid introducing unrelated modifications in the same diff.
- Do not fix what wasn't asked — flag it instead.

## Explicit Failure Modes

- Design for: timeouts, network loss, disk full, malformed data.
- Never design only for the happy path.
