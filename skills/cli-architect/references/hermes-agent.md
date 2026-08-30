# Hermes Agent — config surface

Hermes Agent is Nous Research's open-source, model-agnostic agent harness (distinct from the Hermes LLM line). Positioned as a persistent personal-assistant harness rather than a coding-only CLI — it can drive other coding CLIs (Claude Code, Codex CLI, OpenCode, itself, OpenHands) as delegated sub-agents. Fast-moving/young project, but the sections below are now sourced directly from Hermes's own docs site and GitHub `AGENTS.md`/`website/docs` (not just secondhand blog posts) — reliable for structure; re-check exact config keys/flags against the installed version before shipping.

**Design principle worth knowing up front** (from Hermes's own `AGENTS.md`): per-conversation prompt caching is treated as sacred — anything that mutates past context, swaps toolsets, or rebuilds the system prompt mid-conversation invalidates the cache and multiplies cost. This should shape any "add more context/tools mid-session" recommendation: prefer loading things at session start or via on-demand skill loading over mid-conversation prompt mutation.

## Mental model (per Hermes's own framing)
- **Memory** = durable context (stable facts, preferences, conventions, durable lessons — not temporary task notes, which belong in files/todos/project docs)
- **Skills** = reusable procedures
- **Tools** = actions Hermes can take
- **Sessions** = work history
- **Gateway** = where the user talks to Hermes (CLI, or messaging platforms — Telegram, Discord, Slack, WhatsApp, and many more)
- **Cron** = scheduled/autonomous runs
- **Profiles** = separate operating contexts
- **Subagents** = parallel or delegated work

## Distinguishing feature: self-improving skills
- Hermes autonomously creates skills from successful task trajectories and refines them with use — this is the harness's headline differentiator versus Claude Code/Codex/Gemini CLI, which don't have a built-in learning loop.
- Skills are compatible with the open `agentskills.io` standard, so they're portable to/from other harnesses.
- A companion project, `hermes-agent-self-evolution`, applies DSPy + GEPA to automatically optimize skills, tool descriptions, system prompts, and code — reading execution traces, proposing variants, evaluating against held-out traces, and gating results behind tests/size limits/human review before raising a PR.

## Persistent context files (confirmed via `hermes-agent.nousresearch.com/docs`)
Prompt assembly has a "stable" layer (identity, tool/model guidance, skills index, environment hints) and a "context" layer (caller-supplied message + project context files). The supported customization surface — not the Python prompt-builder code:
- `~/.hermes/SOUL.md` — replaces the built-in default identity/persona block.
- `~/.hermes/MEMORY.md` and `~/.hermes/USER.md` — durable cross-session facts and user-profile data, snapshotted into new sessions.
- Project context files: `.hermes.md`, `HERMES.md`, `AGENTS.md`, `CLAUDE.md`, or `.cursorrules` — repo-specific working rules. **Only the top-level `AGENTS.md` from cwd loads at session start**; subdirectory `AGENTS.md` files are discovered lazily during tool calls and injected into tool results, not loaded upfront — so don't assume a nested `AGENTS.md` is already in context the way it would be in Claude Code.
- Skills — reusable workflows, loaded on demand rather than edited into the core prompt.
- Optional system-prompt config / API overrides for deployment-specific instruction text.

Every character in a context file counts against the token budget every single message, since they're injected every turn — keep these lean.

## Memory (confirmed via `website/docs/user-guide/features/memory.md`)
- Built-in memory + user profile stored in `~/.hermes/memories/`, injected into the system prompt as a **frozen snapshot at session start** (not re-read live mid-session). The agent manages its own memory via a `memory` tool (add/replace/remove).
- Config (`~/.hermes/config.yaml`): `memory.memory_enabled`, `memory.user_profile_enabled`, `memory.memory_char_limit` (default 2200, ~800 tokens), `memory.user_char_limit` (default 1375, ~500 tokens), `memory.write_approval` (default `false` = write freely). Setting both `_enabled` flags false drops the memory tool from the schema entirely — the model is never told about a tool it can't use, which is the correct move if you don't want memory writes at all rather than telling it not to use the tool.
- No auto-compaction: a write that would exceed the char limit errors instead of silently dropping data; the agent must consolidate/remove entries itself in the same turn before retrying.
- **One agent per Hermes home** — don't point two agent processes at the same home directory; memory writes are automatic and unscoped writers will compound each other's entries. Memory is scoped per **profile** by design; give a second agent its own profile, or use an external memory provider (set via `memory.provider`: Hindsight, Mem0, Honcho, …) for deliberately shared memory.
- Hermes's own guidance: memory is for "what" (facts — environment, preferences, project locations, things learned about the user); skills are for "how" (procedures). This is the load-bearing distinction when deciding where a piece of information goes.

## Skills (confirmed via `website/docs/user-guide/features/skills.md` + third-party authoring writeup)
- On disk: `~/.hermes/skills/<name>/SKILL.md` (optionally nested under a category dir like `devops/` or `research/`); everything past `SKILL.md` is optional structure for when instructions would otherwise sprawl.
- Invocation generates a fresh user message at invoke time (`/​<skill-name>` or a skill bundle) — **no system prompt mutation**, consistent with the cache-preservation principle above.
- **Skill bundles**: a YAML alias under `~/.hermes/skill-bundles/` that groups several skills behind one command (e.g. `/release-prep`) for a recurring multi-skill task — it does not install the underlying skills, it just aliases ones that must already exist; missing ones are silently skipped on invocation.
- **External skill directories**: supported and non-existent configured paths are silently ignored (safe for optional shared dirs not present on every machine). Local precedence: a same-named local skill shadows an external one. External skills otherwise integrate fully (system-prompt index, `skills_list`, `skill_view`, `/skill-name`) — not a second-class citizen. If an external dir is writable by the Hermes process, agent-driven skill updates can modify it — use filesystem permissions or a separate profile if it must stay read-only.
- **Self-authoring**: the agent creates/updates/deletes its own skills via a `skill_manage` tool — this is Hermes's procedural memory: when it works out a non-trivial (5+ step) workflow it expects to repeat, it's meant to save it as a skill rather than re-deriving it next time. A `/learn` command can also distill an external source (a doc, a URL) into a new skill via a standards-guided prompt — it synthesizes structure (frameworks, decision rules, anti-patterns) and is designed not to reproduce source-text passages verbatim.
- Skills are compatible with the open `agentskills.io` standard for portability across harnesses.
- A companion project, `hermes-agent-self-evolution`, applies DSPy + GEPA to automatically optimize skills, tool descriptions, system prompts, and code from execution traces, gated behind tests/size limits/human review before raising a PR — a further, offline optimization layer on top of the agent's own in-session skill authoring.

## Delegating to other coding CLIs
- First-party skills under `official/autonomous-ai-agents/` let Hermes drive Claude Code, Codex CLI, OpenCode, itself, or OpenHands as sub-agent coding workers via terminal/process tools, typically in isolated workdirs/worktrees for parallel task execution.
- For Claude Code specifically: Hermes prefers **print mode** (`claude -p '<task>' --allowedTools 'Read,Edit' --max-turns 10`, run via `terminal(...)` with a workdir/timeout) for one-shot delegated tasks — no PTY/interactive-prompt handling needed, cleanest integration path.
- This means: if the user is running Hermes *on top of* Claude Code (or another CLI) rather than using Hermes's own native execution, the architecture question is really "what belongs in the Hermes skill/memory layer vs. what belongs in the delegated CLI's own config (CLAUDE.md, etc.)" — don't collapse the two.

## Other capabilities (confirmed to exist)
- Persists memory, skills, and session history in SQLite across restarts.
- MCP connectivity for external tool capabilities.
- Runs as CLI, TUI (`hermes --tui`), messaging gateway (~20+ platforms), IDE integration (VS Code/Zed/JetBrains via ACP), or an OpenAI-compatible `/v1/chat/completions` API server with cron job management.
- Local subscription proxy for OAuth-backed providers (Claude Pro, ChatGPT Pro, SuperGrok) — lets Hermes (or a delegated CLI) run against an existing subscription instead of a separate API key.
- Tools are grouped into toolsets (filesystem, web, browser, code, mcp, vision, audio, …), enabled/disabled by toolset rather than tool-by-tool; a disabled toolset is completely absent from the system prompt (saves tokens, and the model never learns a tool exists that it can't use — same pattern as the memory `_enabled` flags above). Tool count is documented inconsistently ("~40+", "47 built-in") — Hermes's own `AGENTS.md` says the filesystem is the canonical source and warns not to hard-code the number.
- Shell/code-execution tools route through an environment abstraction (`tools/environments/`) — same tool surface, different blast radius (local vs. Docker vs. remote) — the model itself doesn't know which environment it's in, only the operator's config determines it.

## Delegating to other coding CLIs
- First-party skills under `official/autonomous-ai-agents/` let Hermes drive Claude Code, Codex CLI, OpenCode, itself, or OpenHands as sub-agent coding workers via terminal/process tools, typically in isolated workdirs/worktrees for parallel task execution.
- For Claude Code specifically: Hermes prefers **print mode** (`claude -p '<task>' --allowedTools 'Read,Edit' --max-turns 10`, run via `terminal(...)` with a workdir/timeout) for one-shot delegated tasks — no PTY/interactive-prompt handling needed, cleanest integration path.
- This means: if the user is running Hermes *on top of* Claude Code (or another CLI) rather than using Hermes's own native execution, the architecture question is really "what belongs in the Hermes skill/memory layer vs. what belongs in the delegated CLI's own config (CLAUDE.md, etc.)" — don't collapse the two. Also don't assume the user is doing this at all — Hermes has substantial native execution capability (filesystem, shell, browser, code) and delegating to another CLI is one option, not the default.

## What to put where (Hermes's own guidance, confirmed via docs "Tips & Best Practices")
- Memory → durable facts (environment, preferences, project locations, learned facts about the user). Not stale task progress, PR numbers, or one-week-relevant facts.
- Skills → repeatable procedures: commands, pitfalls, verification steps. If a task takes 5+ steps and will recur, that's the skill threshold.
- Current prompt / a project file / a Kanban-style note → temporary task context.
- Session search / session history → past-session recall, rather than trying to keep everything in active memory.
- Cron → scheduled/recurring work.
- Rule of thumb for anything being added to the system prompt: "should this still steer the agent three months from now?" If not, it belongs in a skill, memory, a report, or a scheduled job instead — this is the direct Hermes-flavored version of this skill's general "what belongs in the always-loaded file vs. loaded on demand" question.

## Verification note
Sourced from Hermes's own docs site (`hermes-agent.nousresearch.com/docs/...`) and GitHub (`NousResearch/hermes-agent`), reached via search snippets rather than full page renders — solid for structure, file paths, and config key names above. Still confirm exact YAML schema and current CLI flags against the installed version before shipping config, since defaults and toolset counts are explicitly called out (in Hermes's own repo) as shifting between releases.
