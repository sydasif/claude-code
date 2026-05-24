# Claude Code Global Configuration

## Structure

```
~/.claude/
├── CLAUDE.md           # Core process, authority, output format
├── settings.json       # Hooks, permissions, plugins, environment
├── README.md           # This file
├── hooks/              # Pre/Post tool execution hooks
│   ├── protect-secrets.js       # Blocks secret exposure (SAFETY_LEVEL=high)
│   ├── block-dangerous-commands.js # Blocks catastrophic shell commands
│   ├── format-code.js           # Auto-formats Python (ruff) + web files (prettier)
│   └── statusline.sh            # Git-integrated status line
├── rules/              # Auto-loaded via InstructionsLoaded event
│   ├── python-style.md          # Toolchain, typing, security
│   └── python-testing.md        # pytest, coverage, AAA pattern
├── skills/             # Custom skills (invoked by Claude)
│   ├── cleanup-code/            # YAGNI, DRY, KISS cleanup
│   ├── refactor-code/           # Modern Python patterns
│   └── review-code/             # Final gate verification
├── agents/             # Subagents with isolated context windows
│   ├── cleanup-code.md
│   ├── refactor-code.md
│   └── review-code.md
└── templates/          # Boilerplate templates
    └── ci-python.yml   # GitHub Actions workflow
```

## Core Workflow

**Skill pipeline (structured Python maintenance):**
```
cleanup-code → refactor-code → review-code
```

**Invoke via:**
- `@cleanup-code` - Remove dead code, duplication, over-abstraction
- `@refactor-code` - Modernize with type hints, dataclasses, pathlib
- `@review-code` - Fresh-eyes verification before submit

## Hooks Summary

| Hook | Trigger | Action |
|------|---------|--------|
| `protect-secrets.js` | Read/Edit/Write/Bash | Blocks secret exposure |
| `block-dangerous-commands.js` | Bash | Blocks `rm -rf ~`, `dd`, fork bombs |
| `format-code.js` | Write/Edit | Auto-formats Python + web files |
| `statusline.sh` | Status bar | Shows dir, model, git status |

## Safety Levels

Edit `SAFETY_LEVEL` in hook files:
- `critical` - Catastrophic disasters only
- `high` (default) - Disasters + data loss + secrets
- `strict` - Maximum restriction

## Python Requirements

- Minimum: Python 3.10
- Target: Python 3.12+
- Toolchain: `uv`, `ruff`, `mypy`, `pytest`

## External Dependencies

Hooks require:
- `node` (for JS hooks)
- `bash` (for statusline)
- `git` (for statusline)
- `jq` or `python3` (JSON parsing fallback)

Optional for formatting:
- `ruff` (Python formatting)
- `prettier` (web file formatting)
