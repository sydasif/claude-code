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
├── skills/          # code-cleanup, code-refactor, code-review, ddg-search, …
├── agents/          # matching subagents
├── hooks/           # ruff on .py save, statusline
├── templates/ci-python.yml
└── settings.json    # plugins: pyright-lsp, repomix-mcp
```

## Python pipeline

`code-cleanup` → `code-refactor` → `code-review` — verify per `rules/python-style.md`.

## Overrides

Project `./CLAUDE.md` > global `~/.claude/CLAUDE.md` > system defaults.
