# Claude Code Python Development Environment

A configuration for Claude Code to maintain code quality, security, and structure in Python projects.

---

## Features

- **Optimization pipeline**: `cleanup-code` agent (KISS → YAGNI → DRY), `refactor-code` (modernization), and `review-code` (final gate)
- **Security hooks**: Block dangerous commands (like `rm -rf ~` or force pushes to main), protect secrets, and prevent exfiltration
- **Externalized env**: All `ANTHROPIC_*` (and any other) environment variables live in `~/.claude/.env` (chmod 600) and are loaded by the shell at startup; `settings.json` carries config only, no env block
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
# Copy the CI template for new Python projects:
cp ~/.claude/templates/ci-python.yml .github/workflows/ci.yml
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

Put **all** environment variables in `~/.claude/.env` — secrets and non-secrets alike (base URL, model names, anything `ANTHROPIC_*`). `settings.json` carries no `env` block; the shell loader is the single source. The `protect-secrets` hook intentionally blocks the agent from creating, reading, or modifying `.env` files — you manage the file yourself.

---

## Key Files

| Path | Purpose |
| ---- | ------- |
| `CLAUDE.md` | Base instructions – security-first, hooks & safety, skills, agents, stop triggers |
| `settings.json` | Hooks, permissions, plugins, status line — config only, no env block |
| `~/.claude/.env` | **User-local**, `chmod 600` — all `ANTHROPIC_*` env and other secrets; not tracked |
| `hooks/*.js` | Pre/Post tool hooks – block dangerous commands, protect secrets, format code |
| `skills/*/SKILL.md` | Reusable capabilities (cleanup, refactor, review, test, blog, agnes, obsidian, tidiness) |
| `agents/*.md` | Specialized sub‑agents with tool restrictions (cleanup-code, refactor-code, review-code) |
| `docs/index.md` | Modular Python standards — style, typing, security, performance, frameworks |
| `docs/python/safety/testing.md` | Testing standards, coverage thresholds, commands |
| `templates/ci-python.yml` | GitHub Actions workflow template |

---

## Skills

### Core Pipeline Skills

| Skill | Purpose |
|-------|---------|
| `cleanup-code` | YAGNI/DRY/KISS pruning — remove dead code, simplify over-abstraction |
| `refactor-code` | Modernize Python — type hints, dataclasses, pathlib, f-strings, logging.exception |
| `review-code` | Final-gate adversarial review — security, contracts, correctness |
| `test-code` | End-to-end QA validation as a real user/operator |

### Specialized Skills

| Skill | Purpose |
|-------|---------|
| `blog-expert` | Technical blog post authoring |
| `blog-seo` | SEO-optimized content creation |
| `agnes-image` | AI image generation workflows |
| `agnes-video` | AI video generation workflows |
| `obsidian-lint` | Obsidian vault linting and validation |
| `codebase-tidiness` | Repository organization and cleanup |

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

## Python Documentation

```
docs/
├── index.md                      # This index (cross-links everything below)
├── python/
│   ├── core/                     # foundational rules + style
│   │   ├── conventions.md        # naming, typing, docstrings, imports, logging, testing, async
│   │   ├── conventions-examples.md  # before/after code for each convention
│   │   ├── style-toolchain.md   # uv, ruff, mypy, workflow, naming, imports, modern Python
│   │   ├── typing.md            # mypy --strict, protocols, generics, TypedDict
│   │   ├── docstrings.md        # Google-style docstrings, Args:, Returns:, Raises:
│   │   └── version.md           # minimum versions, feature tables, EOL policy
│   ├── safety/                  # correctness & security
│   │   ├── error-handling.md    # specific exceptions, raise from, context managers, logging
│   │   ├── security.md          # secrets, eval(), SQL injection, subprocess, password hashing
│   │   └── testing.md           # AAA pattern, coverage, pytest
│   ├── concurrency/             # performance + async
│   │   ├── performance.md       # generators, itertools, lru_cache, set, heapq, str.join
│   │   └── async.md             # async/await, gather, TaskGroup, timeout, async with
│   └── frameworks/              # framework specifics
│       └── frameworks.md        # FastAPI, Django, Flask specifics
└── tooling/                     # unchanged
    ├── package-management.md    # uv workflows, project vs script flow, CI/CD
    └── docker-management.md     # Containerizing Python apps with uv
```

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) – the agent runtime
- Node.js (for hooks) – `node` must be in `$PATH`
- Bash (for status line)
- Optional: `uv`, `ruff`, `mypy`, `pytest`, `prettier` – used by hooks and skills (install per project)

---

## License

MIT – use freely, adapt to your team's needs.