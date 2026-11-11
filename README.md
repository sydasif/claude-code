# Claude Code Python Development Environment

A configuration for Claude Code to maintain code quality, security, and structure in Python projects.

---

## Features

- **Optimization pipeline**: `cleanup-code` (KISS → YAGNI → DRY), `modernize-python` (mechanical modernization), `function-first-refactor` (logic/I-O separation), and `review-code` (final gate)
- **Security hooks**: Block dangerous commands (like `rm -rf ~` or force pushes to main), protect secrets, and prevent exfiltration
- **Externalized secrets**: `settings.json` carries non-secret config only (model, base URL, hooks, plugins); `ANTHROPIC_AUTH_TOKEN` and other secrets live in `~/.claude/.env` (chmod 600) and are loaded by the shell at startup
- **Auto-formatting**: Run `ruff` on Python and `prettier` on JS/TS/JSON/Markdown after every edit
- **Python standards**: Use `uv`, `ruff`, `mypy --strict`, `pytest`, Google docstrings, `pathlib`, f-strings, and dataclasses
- **Testing standards**: Use the AAA pattern, target 95% business logic coverage, and run pre-change test gates
- **Status line**: Display `📁 path | 🧠 model | 🌿 branch +files` for context awareness

---

## Quick Start

```bash
# Clone this repository to ~/.claude (or symlink)
git clone <this-repo> ~/.claude

# Claude Code applies this configuration automatically.
# Canonical pyproject.toml / CI workflow for new Python projects:
#   skills/python-standards/references/core/conventions.md
#   skills/python-standards/references/tooling/package-management.md
```

### Secrets

`settings.json` is safe to commit. Sensitive values (e.g. `ANTHROPIC_AUTH_TOKEN`) belong in a user-local `~/.claude/.env` file that the shell loads at startup.

```bash
# Create the secrets file (one KEY=VALUE per line, # for comments)
touch ~/.claude/.env
chmod 600 ~/.claude/.env
# Edit with your editor — the agent's protect-secrets hook will block
# it from reading or modifying this file on your behalf.
$EDITOR ~/.claude/.env
```

Add the loader once to your shell rc (already present in the recommended `~/.dotfiles/.zshrc` and `~/.bashrc`):

```sh
# Load opencode secrets (token, etc.) from ~/.claude/.env
if [ -f "$HOME/.claude/.env" ]; then
  while IFS='=' read -r key value; do
    case "$key" in ''|\#*) continue ;; esac
    export "$key"="$value"
  done < "$HOME/.claude/.env"
  unset key value
fi
```

Then reload and verify:

```sh
source ~/.zshrc
[ -n "${ANTHROPIC_AUTH_TOKEN+x}" ] && echo "token loaded" || echo "token missing"
```

Put **secrets** in `~/.claude/.env` only — `ANTHROPIC_AUTH_TOKEN` must never appear in `settings.json`. Non-secret environment config can live in either place: today the `env` block in `settings.json` holds `ANTHROPIC_BASE_URL`, the default model names, and `MCP_TIMEOUT`, while the shell loader supplies the token. The `protect-secrets` hook intentionally blocks the agent from creating, reading, or modifying `.env` files — you manage the file yourself.

---

## Key Files

| Path | Purpose |
| ---- | ------- |
| `CLAUDE.md` | Base instructions – security-first, hooks & safety, skills, agents, stop triggers |
| `settings.json` | Hooks, permissions, plugins, status line, model + `env` block (non-secret config only) |
| `~/.claude/.env` | **User-local**, `chmod 600` — secrets (e.g. `ANTHROPIC_AUTH_TOKEN`); not tracked |
| `hooks/*.js` | Pre/Post tool hooks – block dangerous commands, protect secrets, format code |
| `skills/*/SKILL.md` | Reusable capabilities — see Skills below |
| `agents/*.md` | Specialized sub‑agents with tool restrictions (cleanup-code, refactor-code, review-code) |

---

## Python Documentation

Reference files of the `python-standards` skill (paths relative to `~/.claude/`).

| Path | Section | Purpose |
| ---- | ------- | ------- |
| `skills/python-standards/SKILL.md` | Entry | Skill entry point; table mapping a task to the reference to read |
| `skills/python-standards/references/index.md` | Index | Topic → owning file map; the hub |
| `skills/python-standards/references/core/conventions.md` | Core | Rules + pyproject template; canonical tool configuration |
| `skills/python-standards/references/core/conventions-examples.md` | Core | Before/after code for each convention |
| `skills/python-standards/references/core/style-toolchain.md` | Core | uv, ruff, mypy, naming, imports, modern Python |
| `skills/python-standards/references/core/typing.md` | Core | mypy --strict, protocols, generics, TypedDict, Self, @override |
| `skills/python-standards/references/core/docstrings.md` | Core | Google-style docstrings (Args/Returns/Raises) |
| `skills/python-standards/references/core/version.md` | Core | Version policy + feature table (3.10–3.13) |
| `skills/python-standards/references/safety/error-handling.md` | Safety | Specific exceptions, raise…from, logging |
| `skills/python-standards/references/safety/security.md` | Safety | Secrets, eval/exec, SQL, subprocess, password hashing |
| `skills/python-standards/references/safety/testing.md` | Safety | AAA pattern, coverage thresholds, pytest |
| `skills/python-standards/references/concurrency/performance.md` | Concurrency | Generators, itertools, lru_cache, set/heapq |
| `skills/python-standards/references/concurrency/async.md` | Concurrency | async/await, gather, TaskGroup, timeout |
| `skills/python-standards/references/frameworks/frameworks.md` | Frameworks | FastAPI, Django, Flask specifics |
| `skills/python-standards/references/tooling/package-management.md` | Tooling | uv workflows, project/script flow, CI/CD |
| `skills/python-standards/references/tooling/docker-management.md` | Tooling | Containerizing Python apps with uv |

`references/index.md` is the hub; the Section column groups the rest (Core / Safety / Concurrency / Frameworks / Tooling).

---

## Skills

### Core Pipeline Skills

| Skill | Purpose |
|-------|---------|
| `cleanup-code` | YAGNI/DRY/KISS cleanup, prune first |
| `modernize-python` | Modernize Python — type hints, dataclasses, pathlib, f-strings, logging.exception |
| `function-first-refactor` | Separate pure business logic from side effects (functional core, imperative shell) |
| `review-code` | Final-gate adversarial review — security, contracts, correctness |

### Specialized Skills

| Skill | Purpose |
|-------|---------|
| `python-standards` | Python house rules — typing, tooling, async, testing, frameworks, Docker |
| `codebase-tidiness` | Obsolete code, stale comments, outdated docstrings |
| `netlab` | Virtual network labs from YAML topology |
| `chapter-pipeline` | Advance Network Automation book chapter workflow |
| `cli-architect` | Agent CLI configuration review (Claude Code, omp, Hermes) |
| `system-audit` | Read-only machine audit and backup/dotfiles drift check |
| `blog-expert` | Technical blog post authoring |
| `blog-seo` | SEO-optimized content creation |
| `agnes-image` | AI image generation workflows |
| `agnes-video` | AI video generation workflows |

---

## Commands (Slash Commands)

| Command | Description |
|---------|-------------|
| `/codebase-pipeline` | Run full optimization + testing pipeline (cleanup → refactor → review) |
| `/generate-readme` | Generate detailed README.md from codebase |
| `/genrate-graph` | Generate self-contained HTML codebase graph with interactive diagram |
| `/analyze-library` | Analyze a library for integration |
| `/review-best-practices` | Review code against best practices |
| `/review-structure` | Review project structure |
| `/suggest-tests` | Suggest test cases for code |

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) – the agent runtime
- Node.js (for hooks) – `node` must be in `$PATH`
- Bash (for status line)
- Optional: `uv`, `ruff`, `mypy`, `pytest`, `prettier` – used by hooks and skills (install per project)

---

## License

MIT – use freely, adapt to your team's needs.