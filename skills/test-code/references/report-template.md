---
name: QA Test Report Template
description: A structured Markdown template used during the final reporting phase of the test-code skill to document test results, bug findings, and project readiness.
---

# QA Test Report Template

Always produce this structured report. Do not replace it with prose-only summaries.

```markdown
## QA Test Report

### Application Under Test

- Type: [CLI / Web app / API / Automation script / Library / Other]
- Network automation layer: [yes (list tools) / no]
- Description: [one-line summary of what the app does]

### Test Environment

- Setup method: [venv / container / temp dir / existing env]
- Dependencies installed: [yes / partial - list missing]
- Required services: [reachable / unreachable - list which]
- Config and env vars: [configured / missing - list which]

### Test Cases Executed

| #   | Test case     | Result    | Notes             |
| --- | ------------- | --------- | ----------------- |
| 1   | [description] | pass/fail | [relevant detail] |

### Bugs Found

(Repeat for each bug:)

- **Location**: file and line, or user-visible behavior
- **Description**: What went wrong and under what conditions
- **Reproduction**: Steps to trigger
- **Fix applied**: [description / not yet fixed]
- **Verification**: [re-test result]

### Remaining Risks

- [risk or open question]

### Verdict

- [ ] Ready to ship
- [ ] Needs more work - [specific blockers]
- [ ] Blocked on [dependency or decision]
```
