# Engineering Lifecycle

## Phase 1 · Discovery — "Read Before Write"

1. **Call-Site Search** — Who calls this code? Find every reference.
2. **Pattern Search** — How does the project solve similar problems?
3. **History Search** — What do recent commits reveal about intent?
4. **Guideline Check** — Read the relevant file from Section 3 before forming a plan. Verify the file exists first; if missing, note it and proceed with project conventions.

## Phase 2 · Strategic Planning

### Plan Node Default

- Enter plan mode for **any non-trivial task** (3+ steps or architectural decisions) — write the plan to `tasks/todo.md` before touching code.
- Write detailed specs upfront to reduce ambiguity. A plan that takes 5 minutes to write saves 30 minutes of wrong-direction execution.
- Use plan mode for verification steps too, not just building.
- **If something goes sideways mid-execution: STOP and re-plan immediately.** Do not keep pushing into a broken state. Revert to last known good, update the plan, then proceed.

### Planning Checklist

- **Negative Plan:** State explicitly what will NOT change.
- **Rollback Path:** Define how to revert if production breaks.
- **Subagent Scope:** Label tasks as "Pure" (no side effects) or "Side-Effect" before parallelizing.

### Subagent Scoping Rules

Subagents keep the main context window clean and enable parallel analysis — but only for isolated, deterministic work. Before delegating:

- Define the exact input it receives and the exact output it must return.
- "Pure" tasks (safe to parallelize): read-only analysis, isolated transformations with no shared state, report generation, research and exploration.
- "Side-Effect" tasks (never parallelize): file writes, API calls, database operations — sequence these explicitly.
- Pass full context explicitly. Subagents have no memory of the parent task.
- One task per subagent. Do not bundle multiple concerns into one subagent call.
- If a subagent returns a result that conflicts with another, halt and surface the conflict. Do not resolve it unilaterally.

## Phase 3 · Surgical Execution

- **Skill Chain:** Invoke the appropriate skill pipeline.
- **Atomic Commits:** One logical change per commit.
- **No-Noise Policy:** Strip all debug logs before submission.
- **Idiomatic Alignment:** Follow project conventions — not personal preference.
- **Batch Size:** Change one module or layer per pass. Do not accumulate a multi-module diff in a single step.

### Demand Elegance

For non-trivial changes, pause before submitting and ask: *"Is there a more elegant way?"*

- If a fix feels hacky: *"Knowing everything I know now, implement the elegant solution."*
- Skip this for simple, obvious fixes — do not over-engineer.
- Challenge your own work before presenting it.
- The bar: **would a staff engineer approve this without hesitation?**

### Autonomous Bug Fixing

When given a bug report — fix it. Do not ask for hand-holding.

- Point at logs, errors, and failing tests — then resolve them.
- Zero context switching required from the user.
- Go fix failing CI tests without being told how.
- Find root causes. No temporary patches. No workarounds that defer the problem.
