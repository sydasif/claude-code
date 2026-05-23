# ~/.claude

Global Claude Code config for Python work.

## Auto-loaded

- `CLAUDE.md` — process, authority, pipeline pointers (does not repeat rules)
- `rules/python-style.md` — toolchain, lint, types, security
- `rules/python-testing.md` — pytest, coverage

## Layout

```text
~/.claude/
├── CLAUDE.md
├── rules/
├── skills/          # cleanup-code, refactor-code, review-code, ddg-search, …
├── agents/          # matching subagents
├── hooks/           # ruff on .py save, statusline, safety hooks
├── templates/ci-python.yml
└── settings.json    # plugins: pyright-lsp, repomix-mcp
```

## Python pipeline

`cleanup-code` → `refactor-code` → `review-code` — verify per `rules/python-style.md`.

## Overrides

## Safety Hooks

Two hooks from `claude-code-hooks` are active:

- `block-dangerous-commands.js`: Prevents catastrophic shell commands.
- `protect-secrets.js`: Prevents secret exfiltration and access.

**Safety Levels:** Change the `SAFETY_LEVEL` constant at the top of each script in `~/.claude/hooks/`:

- `critical`: Only catastrophic disasters.
- `high`: Recommended. Stops disasters + data loss/leaks.
- `strict`: Maximum safety. Blocks cautious/risky actions.
