# Claude Code Python Development Environment

A production‑grade, opinionated configuration for Claude Code that enforces code quality, security, and structured thinking in Python projects.

---

## What’s Inside

- **3‑skill pipeline** – `cleanup-code` (YAGNI/DRY/KISS) → `refactor-code` (modernization) → `review-code` (final gate)
- **Security hooks** – blocks dangerous commands (`rm -rf ~`, `dd`, force push to main), protects secrets (`.env`, SSH keys, AWS creds), prevents exfiltration
- **Auto‑formatting** – runs `ruff` on Python, `prettier` on JS/TS/JSON/Markdown after every write/edit
- **Canonical Python standards** – `uv`, `ruff`, `mypy --strict`, `pytest`, Google docstrings, `pathlib`, f‑strings, dataclasses
- **Testing discipline** – AAA pattern, coverage targets (95% business logic), pre‑change test gates
- **Status line** – shows `📁 path | 🧠 model | 🌿 branch +files` to keep Claude context‑aware

---

## Quick Start

```bash
# Clone this repository to ~/.claude (or symlink)
git clone <this-repo> ~/.claude

# The configuration is automatically applied when Claude Code starts.
# For a new Python project, copy the CI template:
cp ~/.claude/templates/ci-python.yml .github/workflows/ci.yml
```

---

## Key Files

| Path                      | Purpose                                                                      |
| ------------------------- | ---------------------------------------------------------------------------- |
| `CLAUDE.md`               | Base instructions – security‑first, structured outputs, stop triggers        |
| `settings.json`           | Hooks, permissions, plugins, status line                                     |
| `hooks/*.js`              | Pre/Post tool hooks – block dangerous commands, protect secrets, format code |
| `skills/*/SKILL.md`       | Reusable capabilities (cleanup, refactor, review, blog writing, humanizing)  |
| `agents/*.md`             | Specialized sub‑agents with tool restrictions                                |
| `docs/python-style.md`    | Canonical Python style, toolchain, type checking rules                       |
| `docs/python-testing.md`  | Testing standards, coverage thresholds, commands                             |
| `templates/ci-python.yml` | GitHub Actions workflow template                                             |

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) – the agent runtime
- Node.js (for hooks) – `node` must be in `$PATH`
- Bash (for status line)
- Optional: `uv`, `ruff`, `mypy`, `pytest`, `prettier` – used by hooks and skills (install per project)

---

## License

MIT – use freely, adapt to your team’s needs.
