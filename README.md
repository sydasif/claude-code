# Claude Code Python Development Environment

A configuration for Claude Code to maintain code quality, security, and structure in Python projects.

---

## Features

- **Three-skill pipeline**: `cleanup-code` (YAGNI/DRY/KISS), `refactor-code` (modernization), and `review-code` (final gate)
- **Security hooks**: Block dangerous commands (like `rm -rf ~` or force pushes to main), protect secrets, and prevent exfiltration
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

---

## Key Files

| Path                      | Purpose                                                                      |
| ------------------------- | ---------------------------------------------------------------------------- |
| `CLAUDE.md`               | Base instructions – security‑first, structured outputs, stop triggers        |
| `settings.json`           | Hooks, permissions, plugins, status line                                     |
| `hooks/*.js`              | Pre/Post tool hooks – block dangerous commands, protect secrets, format code |
| `skills/*/SKILL.md`       | Reusable capabilities (cleanup, refactor, review, blog writing, humanizing)  |
| `agents/*.md`             | Specialized sub‑agents with tool restrictions                                |
| `docs/index.md`           | Modular Python standards — style, typing, security, performance, frameworks  |
| `docs/python/testing.md`  | Testing standards, coverage thresholds, commands                             |
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
