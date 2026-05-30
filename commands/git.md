---
description: Commit changes, check for docs updates changed and push.
---

1. **Inventory** — Show `git status`, `git diff`, `git diff --cached`, `git log --oneline -10`
2. **Commit code changes** — Stage all files with `git add`, then commit following `@CLAUDE.md` format: `<type>(<scope>): <imperative summary>`
3. **Audit docs** — For each changed file, check if any corresponding documentation need updating.
4. **Commit docs separately** — With message `docs: update documentation for <feature>`
5. **Push** — `git push`

### Rules

- **Atomic commits** — code and docs never mix in the same commit
- **No force push** — use `git push` only
- **Stopping** — If nothing to commit, report "nothing to commit" and stop
