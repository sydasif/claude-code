# Authority & Decision Boundaries

## Decision Tiers

| Tier                                  | Action                     | Examples                                                                                                                                                                                               |
| ------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Independence** — Proceed & Notify   | Act, then inform           | Implementation patterns, internal refactoring, minor/patch dependency bumps, test suite design                                                                                                         |
| **Collaboration** — Propose & Wait    | Align before acting        | Architecture shifts, public API signatures, new dependencies, conflicting requirements                                                                                                                 |
| **Strict Prohibition** — Do Not Touch | Never, under any condition | Secrets/auth logic, CI/CD/Docker/Terraform (unless requested), global auto-formatting, **any destructive data operation** (DROP, DELETE, TRUNCATE, bulk overwrites) without explicit user confirmation |

## Data Destruction Rule

If a task requires deleting records, dropping tables, wiping files, or any irreversible bulk operation — **stop**, describe exactly what will be destroyed, and wait for explicit confirmation before proceeding.
