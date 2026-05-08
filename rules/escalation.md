# Stop & Ask Triggers

Halt immediately and escalate if any of the following are true:

1. A **security vulnerability** is found in unrelated code.
2. The surgical scope has expanded to **more than 5 files outside the stated scope** (files legitimately touched by a cleanup or refactor batch do not count toward this limit).
3. Requirements are **contradictory** (e.g., "maximize speed" + "use this known-slow library").
4. The correct solution requires **bypassing existing architecture**.
5. A task requires a **destructive data operation** (see `rules/authority.md`).
6. A subagent returns a result that **conflicts with another subagent's output**.
