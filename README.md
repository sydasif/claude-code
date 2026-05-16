# Claude CLI: Advanced Configuration & Customization Framework

This repository defines the core architecture for personalizing Claude Code across Python development workflows. It implements a tiered customization system designed to optimize context usage, enforce engineering standards, and automate domain-specific procedures.

## 1. System Architecture

The configuration follows a **Progressive Disclosure Strategy**, separating critical constraints from domain-specific reference material to maximize token efficiency.

### Tier 1: Always-On Constraints

- **Path:** `~/.claude/CLAUDE.md`
- **Behavior:** Automatically injected into every session.
- **Purpose:** Critical security, testing, and tool-chain requirements.

### Tier 2: Domain-Specific Reference

- **Path:** `~/.claude/skills/*/reference/`
- **Behavior:** Manual loading via the `Read` tool as needed.
- **Purpose:** Best practices for specific technologies or patterns (e.g., Python, REST APIs).
- **Efficiency:** Reduces baseline context by 60-80% by avoiding unnecessary data loading.

### Tier 3: Actionable Workflows (Skills)

- **Path:** `~/.claude/skills/`
- **Behavior:** Triggered on-demand via intent detection or explicit activation.
- **Structure:** Markdown bundles with YAML metadata defining step-by-step procedures.
- **Example:** `code-refactor/SKILL.md` defines modernization sequences (Pathlib, Type Hints, etc.).

### Tier 4: Task Isolation (Subagents)

- **Path:** `~/.claude/agents/`
- **Behavior:** Spawned for deterministic, isolated subtasks.
- **Control:** Supports strict permissioning and model-specific selection (gemma-4-26b, gemini-3.1-flash, gemma-4-31b).

---

## 2. Directory Structure

```text
~/.claude/
├── CLAUDE.md                # Core engineering mandates (auto-loaded)
├── rules/                   # Domain-specific rules (git, testing, python)
├── skills/                  # Intent-based workflows
│   ├── code-cleanup/        # YAGNI/DRY/KISS cleanup
│   ├── code-refactor/       # Python modernization
│   ├── code-review/         # Final gate review
│   ├── ddg-search/          # Web search & docs
│   ├── docker-expert/       # Container guidance
│   ├── mcp-builder/         # MCP server creation
│   ├── python-testing/     # Test patterns & coverage
│   └── repomix/             # Codebase packaging
└── agents/                  # TIER 4: Specialized subagents
    ├── cleanup.md           # YAGNI/DRY/KISS cleanup
    ├── refactor.md         # Python modernization
    ├── research.md          # Deep-dive research
    └── review.md            # Final-gate review
```

---

## 3. Configuration Hierarchy & Resolution

Claude resolves configurations using a specific priority order, allowing project-level overrides to supersede global defaults.

| Priority        | Scope       | Location                   | Usage                                              |
| :-------------- | :---------- | :------------------------- | :------------------------------------------------- |
| **1 (Highest)** | **Module**  | `path/to/module/CLAUDE.md` | Specific logic for a single service/package.       |
| **2**           | **Project** | `./CLAUDE.md`              | Tech stack, build commands, and local repo rules.  |
| **3**           | **Global**  | `~/.claude/CLAUDE.md`      | Personal style, safety rules, and global toolsets. |
| **4 (Lowest)**  | **System**  | Internal Defaults          | Default CLI behavior and safety guardrails.        |

---

## 4. Operational Workflows

### Loading Domain Context

To maintain a lean context window, only load guidelines relevant to the current task:

```bash
# For code cleanup tasks
Read ~/.claude/skills/code-cleanup/SKILL.md
```

### Executing Specialized Reviews

Utilize the read-only Subagent for semantic verification without risk of unintended side effects:

```bash
# Request a structured review
Use the review subagent to analyze the current diff for adherence to standards.
```

---

## 5. Security & Engineering Standards

All contributions to this configuration must adhere to the **Security-First Mandate**:

1.  **Least Privilege:** Subagents should be restricted to the minimum tools required.
2.  **No Secrets:** Never store API keys or sensitive strings in any `.md` or YAML file.
3.  **Explicit Failure:** Skills must include error-handling steps for edge cases (e.g., network loss, malformed input).

---

## 6. Maintenance

- **License:** MIT
- **Version Tracking:** Configuration changes should be versioned alongside project code when possible.
- **Documentation:** Updates to `rules/` or `guidelines/` must be reflected in the corresponding reference file.
