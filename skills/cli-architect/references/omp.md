# omp — config surface

omp is a terminal coding agent built by Stencil (omp.sh), Rust core + TypeScript extension layer. Ships subagents, plan mode, LSP, DAP, hindsight memory, hashline edits, and "time-traveling rules" (TTSR). Fast-moving project — sections below are marked **(confirmed)** where sourced from omp's own docs pages/GitHub docs, vs. general description where only the feature's existence (not its exact schema) is established. Re-check exact flags/schema against `omp --help` or live docs before shipping config, since this project ships fast.

## Project context discovery
- omp discovers project context from multiple config directory formats already on disk, in their native shape — no migration needed. Confirmed formats include `.omp`, `.claude`, `.codex`, `.gemini` (it reads Cursor MDC, Cline `.clinerules`, Codex `AGENTS.md`, Copilot `applyTo`, and others without converting them).
- This means: if the user's repo already has a `CLAUDE.md`/`AGENTS.md`/etc. from another tool, omp likely already reads it — don't recommend duplicating that content into a new omp-specific file without checking first.

## System prompt layering
- Global fallback: `~/.oh-omp/agent/SYSTEM.md`.
- `--system-prompt` on the CLI overrides the file-based system prompt entirely.
- `--append-system-prompt` adds to it rather than replacing it — this is the right lever for "add one more rule" without duplicating the whole prompt.

## Models / providers
- Custom providers/models configured via `~/.oh-omp/agent/models.yml` (the modern format; `models.json` still supported for legacy configs). Lets the user point omp at local providers (e.g., Ollama, llama.cpp) or add model metadata (cost, context window, max tokens) per provider.

## Delegation / capability primitives

- **Subagents** (confirmed via `omp.sh/docs/subagent-authoring`) — one Markdown file per subagent. omp resolves the `agent` parameter by scanning these roots in order, first match by name wins (exact-name, case-sensitive):
  1. `.omp/agents/<name>.md` — project, omp-managed
  2. `~/.omp/agent/agents/<name>.md` — user, omp-managed
  3. `<plugin>/agents/<name>.md` — plugin-provided
  4. Eight bundled agents as the fallback: `explore`, `plan`, `designer`, `reviewer`, `librarian`, `oracle`, `task`, `quick_task`
  Dropping a file with the same name as a bundled agent overrides it. This is the concrete answer to "where do I put a custom subagent" — no invention needed.

- **Skills** (confirmed via `oh-omp/docs/skills.md`) — named, optional capability packs selected by task context or explicitly requested. Resolved via `skill://` URLs: `skill://pdf` → `<pdf-base>/SKILL.md`, `skill://pdf/references/tables.md` → `<pdf-base>/references/tables.md` (path traversal and absolute paths rejected; no fallback search for missing assets). If `skills.enableSkillCommands` is true, interactive mode registers one slash command per discovered skill (`/skill:<name>`). Task-tool subagents receive the session's already-discovered skill list — there's no per-task skill pinning override. **Cross-tool reuse confirmed**: skills already sitting in `~/.claude/skills/` or `.claude/skills/` for Claude Code are picked up by omp automatically — don't recommend duplicating a Claude Code skill into an omp-specific location.

- **AGENTS.md / context-file discovery** (confirmed) — `src/discovery/agents-md.ts` walks ancestor directories from cwd looking for standalone `AGENTS.md` files, up to depth 20, skipping hidden-directory segments; merged by level/depth rules. Project-local `.omp/` config overrides global config for that project's scope. Practical implication: omp already reads a repo's existing `CLAUDE.md`/`AGENTS.md` — same point as project-context discovery above, confirmed twice independently.

- **Rules — two distinct systems, don't conflate them**:
  - **Sticky rules** (`RULES.md`, separate from `AGENTS.md`) — hard prohibitions ("don't push without asking") that omp keeps resurfacing near the current turn in long sessions, rather than letting them scroll out of context. Put standing prohibitions here, not in AGENTS.md.
  - **TTSR — "time-traveling rules"** (confirmed via `omp.sh/docs/ttsr`) — mechanically-enforced guardrails, one Markdown file per rule under `.omp/rules/` (or the active profile's `rules/` dir), extension `.md` or `.mdc`. Frontmatter: `description`, `condition` (a regex matched against tool output/input), `scope` (e.g. `tool:edit(*.rs)`, `tool:write(*.rs)`). Body is the correction text, only shown to the model when the rule fires. Filename becomes the rule's name. **Discovered at session start only** — a new session is required after adding/editing a rule file. Test a rule in isolation before trusting discovery:
    ```
    omp ttsr test \
      --rule .omp/rules/no-box-leak.md \
      --source tool --tool edit --path src/lib.rs \
      'let value = Box::leak(Box::new(input));'
    ```
    Debug a rule that isn't firing with `omp config get ttsr.enabled`, `omp config get ttsr.disabledRules`, `omp config get ttsr.builtinRules`, and `--verbose` on the same `ttsr test` command. This is the closest omp equivalent to a Claude Code hook — use it for anything that must be mechanically caught (a banned pattern in a diff), not just requested via prompt.

- **Plan mode** (confirmed) — `/plan` runs a separate planning turn; refine the proposal, then decide when to execute. Recommended for migrations, architectural changes, and anything order-of-operations-sensitive — the omp-native equivalent of "plan then execute" workflows.

- **LSP/DAP integration** — IDE-grade operations (symbol navigation, diagnostics, refactors that update re-exports/barrel files/aliased imports) and direct debugger control (attach lldb/dlv/debugpy, set breakpoints, inspect frames/variables). Means some "run it and read the output" loops can become a single direct tool call instead.

- **Memory** (namespace confirmed via `omp.sh/docs/settings`, mechanics not fully documented in what's fetchable) — settings live under `memory`, `autolearn`, `memories`, `mnemopi`, and `hindsight` config keys. `memory://root` opens the memory store with a plain read from inside the harness (per a third-party setup writeup, not official docs — treat as likely-true, verify before depending on it). Don't guess at write/query semantics beyond this; check `omp config get memory` / current docs for the session in question.

- **Hashline edits** — a hash-anchored edit mechanism for unambiguous file edits (vs. plain diff/patch matching). Reduces the failure mode where an edit tool matches the wrong occurrence of a text block.

- **git-aware commit tooling** — reads the working tree via `git_overview`/`git_file_diff`/`git_hunk`, splits unrelated changes into atomic, dependency-ordered commits (cycles rejected before writing); source files weighted above tests/docs/config, lock files excluded entirely.

- **Inspecting merged config** — `omp config get <key>` prints the merged value of a setting across all config layers (global/user/project) at once — the direct way to answer "which config actually won" instead of guessing from file precedence rules. `omp stats` shows token/dollar spend by project and session, including subagents — the direct way to verify a token-optimization change actually helped (see framework §7 in SKILL.md).

- **Settings namespaces** (confirmed via `omp.sh/docs/settings`, exact schema not fetchable) — memory (`memory`, `autolearn`, `memories`, `mnemopi`, `hindsight`), files (`edit`, `readLineNumbers`, `read`, `lsp`), shell (`shellPath`, `bash`, `bashInterceptor`, `shellMinimizer`, `eval`, `python`, `ruby`, `julia`), tools (`tools`, `todo`, `glob`, `grep`, `astGrep`, `astEdit`, `debug`, `launch`, `mcp`, `browser`, etc.), tasks (`plan`, `goal`, `title`, `task`, `worktree`, `skills`, `commands`), providers/auth. Useful for knowing *what category* a setting lives under when telling the user where to look — confirm the exact key path with `omp config get` before writing it into a file for them.

## Verification note
Confirmed items above come from omp's own docs pages (`omp.sh/docs/subagent-authoring`, `/docs/ttsr`, `/docs/settings`) and its GitHub docs (`docs/skills.md`), reached via search snippets rather than a full page fetch (the live site is JS-rendered and didn't return body content to a direct fetch) — reliable for structure and names, but re-check exact frontmatter field names and command flags against the installed version before shipping config, since this project ships fast.
