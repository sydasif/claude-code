# Claude Code — config surface

(Facts as of the assistant's training/knowledge; Claude Code ships updates often — verify anything version-sensitive against `claude --help` or current docs before prescribing it.)

## Persistent instruction / rules
- `CLAUDE.md` at repo root (and nested per-directory `CLAUDE.md`) — persistent project rules, conventions, always-loaded context. Keep this lean; large reference material belongs in a Skill instead, loaded on demand.
- `.claude/rules/` — additional rule files that can be organized by concern instead of one monolithic CLAUDE.md.
- `.claude/settings.json` (and `.claude/settings.local.json` for personal overrides) — permissions, hooks, model config, allowed/denied tools.

## Delegation primitives
- **Skills** — reusable workflows/domain knowledge, each a folder with `SKILL.md` (+ optional `scripts/`, `references/`, `assets/`). Loaded progressively: name+description always visible, body loaded when triggered, bundled resources loaded on demand. Live under `.claude/skills/` (project) or the user's personal skills directory.
- **Subagents** — isolated context, specialized system prompt/toolset, invoked for a scoped task so the main thread doesn't accumulate that work's exploration/reasoning. Defined as markdown files with frontmatter (name, description, tools) — use when the task benefits from a clean context window or a narrower toolset, not by default.
- **Agent teams** — multiple subagents working in parallel on genuinely independent pieces of a task, aggregated afterward. Only worth the overhead when the sub-tasks don't depend on each other's output.
- **Hooks** — deterministic, mechanically-enforced automation tied to lifecycle events (e.g., pre-tool-use, post-tool-use, session events), configured in settings. Use for anything that must *always* happen (formatting, test runs, guardrails) rather than trusting the model to remember an instruction every time.
- **MCP servers** — external tool/data-source integration when the task genuinely needs a capability outside the built-in toolset (e.g., a specific SaaS API, a database). Configured via `.mcp.json` or `claude mcp add`.
- **Plugins** — bundles of commands/skills/hooks/MCP config packaged together for reuse across projects or teams.
- **Commands** — `.claude/commands/*.md` custom slash commands for repeatable prompts.

## Memory / context management
- CLAUDE.md content is loaded into every session's context — the main lever for "what should the agent always know."
- Context that's only needed for one investigation belongs in a subagent's isolated context, not the main thread.
- `/compact` and context-window management exist for long sessions; large repeated file reads are a signal that the answer should be cached in CLAUDE.md, a skill reference file, or persisted some other way rather than re-derived each session.

## Model selection
- Model can be set per-session or per-subagent; heavier reasoning models for architecture/planning-type subagents, lighter/faster models for high-volume mechanical subagent work, when the CLI's config exposes that choice.

## Verification note
Exact hook event names, settings.json schema, and current skill/subagent directory conventions can change between Claude Code releases — before writing exact config for the user, check anything load-bearing against the installed version's `--help` output or current docs rather than relying purely on this summary.
