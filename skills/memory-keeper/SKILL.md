---
name: memory-keeper
description: Maintain project memory so context survives across sessions. Update memory any time you learn something worth knowing next session — architectural decisions, debugging insights, gotchas, why choices were made, code style preferences, conventions established, unresolved issues. Do not use for one-off, throwaway, or purely exploratory tasks that won't recur across sessions.
---

## When to Write an Auto Memory

Saves notes for yourself as you work: build commands, debugging insights, architecture notes, code style preferences, and workflow habits. Doesn't save something every session — decides what's worth remembering based on whether the information would be useful in a future conversation.

Write one when something is:

- An architectural or design decision, especially one with a non-obvious "why"
- A gotcha, workaround, or constraint discovered the hard way, a "lesson learned"
- A convention or pattern established for the project
- Anything you'd otherwise have to re-derive or re-discover next session
- An unresolved issue that will need to be addressed in the future
- Something that will help future sessions make better decisions

Skip it for:

- Routine changes with no lasting "why"
- Anything already obvious from reading the code
- One-off exploratory or throwaway work
- Anything that is already documented in the project `CLAUDE.md` or `README.md`

Rule of thumb: would a future session without this memo make a worse decision? If no, don't write it.

## Writing or Updating a Memo

- Create or update `~/.claude/projects/<project-name>/memory/<topic-name>.md`
- All memory notes use built-in front-matter as below:

```yaml
---
name: test-memory
description: Initial test memory entry for testing memory system
metadata:
  node_type: memory
  type: reference
  originSessionId: aaa91fc4-59d8-49ad-9a3c-72590cba5ac5
---
```

- Add these other fields flat at top level are mandatory for all memory notes:

```yaml
---
title: Title for Memo
tags: [tag1, tag2, tag3] # only add max 3 tags
created: YYYY-MM-DD
last_update: YYYY-MM-DD
related: ["[[other-topic-slug]]"] # use [[wikilinks]], quoted in YAML
---
```

- Do not nest any of these fields under `metadata` — they are top-level fields.
- Prefer editing an existing memo over creating a near-duplicate one.
- Point to files/line numbers instead of pasting code into the memo.

## Updating the Index

`MEMORY.md` stays small — one line per memo, not a summary of its contents:

```markdown
# Index - project-name

- [[auth-strategy]] — JWT over sessions; see rationale
- [[db-retries]] — exponential backoff, gotcha with connection pool
```

Add or update a line here every time you write or update a memo.

## Maintenance

- Stale, incorrect, or superseded memo? Fix or remove it immediately — delete the file and remove its line from the index. Don't let it linger.
- Treat the index as the source of truth for what memory exists — if it's not linked there, it doesn't count as remembered.

## Guiding Principles

- **Context efficiency is paramount** — future sessions pay the token cost of everything here.
- **Signal over noise** — the "why" matters more than the "what."
