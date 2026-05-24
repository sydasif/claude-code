# Global Claude Code Configuration (~/.claude)

This directory contains the global configuration, rules, and hooks used to guide Claude Code across multiple projects.

## 📖 Core Guidance

Claude's behavior is governed by the following auto-loaded files:

- **`CLAUDE.md`**: Defines the operational process, authority levels, and high-level mandates.
- **`rules/python-style.md`**: Canonical toolchain and style requirements for Python (uv, ruff, mypy).
- **`rules/python-testing.md`**: Standards for pytest, coverage targets, and verification.

## 📂 Directory Layout

```text
~/.claude/
├── CLAUDE.md             # Global process and authority
├── rules/                # Domain-specific style and testing rules
│   ├── python-style.md
│   └── python-testing.md
├── skills/               # Custom Claude Agent Skills
├── agents/               # Specialized sub-agents
├── hooks/                # Tool execution hooks (Pre/Post)
│   ├── format-code.js    # Auto-formatting for Python, JS, TS, JSON, MD, YAML, HTML
│   ├── protect-secrets.js # Prevents secret exfiltration
│   ├── block-dangerous-commands.js # Prevents catastrophic shell operations
│   ├── block-websearch.sh # Controls WebSearch access
│   └── statusline.sh     # Custom status line indicator
├── templates/            # Boilerplate (e.g., ci-python.yml)
└── settings.json         # Harness settings, plugins, and hook registrations
```

## 🛠️ Hooks System

Hooks are registered in `settings.json` and execute automatically during tool use.

### 🎨 Formatting Hook (`format-code.js`)

Triggered on `Write` and `Edit` operations. It ensures consistent style across AI-generated changes:

- **Python**: Uses `ruff` for lint-fixing and formatting.
- **Web/Config**: Uses `prettier` for `.js`, `.ts`, `.json`, `.md`, `.yaml`, `.yml`, and `.html`.
- **Logs**: Activity is logged to `~/.claude/hooks-logs/YYYY-MM-DD.jsonl`.

### 🛡️ Safety Hooks

Prevent high-risk operations and data leaks:

- **`protect-secrets.js`**: Scans for and blocks the exposure of sensitive credentials.
- **`block-dangerous-commands.js`**: Blocks destructive shell commands (e.g., `rm -rf /`).
- **`block-websearch.sh`**: Provides a layer of control over external web access.

**Safety Levels**: Modify the `SAFETY_LEVEL` constant in the script:

- `critical`: Only blocks catastrophic disasters.
- `high`: (Recommended) Stops disasters, data loss, and leaks.
- `strict`: Maximum restriction for highly cautious environments.

## 🐍 Python Pipeline

When performing structured Python maintenance, follow this skill pipeline:
`cleanup-code` $\rightarrow$ `refactor-code` $\rightarrow$ `review-code`

All changes must be verified against the thresholds in `rules/python-testing.md`.
