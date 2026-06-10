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

| Path                      | Purpose                                                                            |
| ------------------------- | ---------------------------------------------------------------------------------- |
| `CLAUDE.md`               | Base instructions – security-first, hooks & safety, skills, agents, stop triggers |
| `settings.json`           | Hooks, permissions, plugins, status line — config only, no env block               |
| `~/.claude/.env`          | **User-local**, `chmod 600` — all `ANTHROPIC_*` env and other secrets; not tracked |
| `hooks/*.js`              | Pre/Post tool hooks – block dangerous commands, protect secrets, format code       |
| `skills/*/SKILL.md`       | Reusable capabilities (cleanup, refactor, review, blog writing, humanizing)        |
| `agents/*.md`             | Specialized sub‑agents with tool restrictions                                      |
| `docs/index.md`           | Modular Python standards — style, typing, security, performance, frameworks        |
| `docs/python/testing.md`  | Testing standards, coverage thresholds, commands                                   |
| `templates/ci-python.yml` | GitHub Actions workflow template                                                   |

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) – the agent runtime
- Node.js (for hooks) – `node` must be in `$PATH`
- Bash (for status line)
- Optional: `uv`, `ruff`, `mypy`, `pytest`, `prettier` – used by hooks and skills (install per project)

---

## License

MIT – use freely, adapt to your team’s needs.
