# Mandatory Output Structure

Every completed task must be reported in this format:

## 1. Discovery Report

- **Found Patterns:** [e.g., "Project uses Pydantic for all validation"]
- **Affected Areas:** [Files/modules that reference the changed code]
- **Missing Guidelines:** [Any files from Section 3 that were absent]
- **Coverage Baseline:** [Current coverage vs. thresholds — note any gaps]

## 2. Strategic Plan

- **Primary Objective:** [Single-sentence goal]
- **Surgical Scope:** [Exact functions, classes, or line ranges targeted]
- **Non-Goals:** [What is explicitly out of scope]
- **Skill Pipeline:** [Which skills were invoked and in what order]

## 3. Assumptions & Risks

- **Assumption:** [e.g., "API always returns UTF-8 encoded responses"]
- **Risk:** [e.g., "New dependency adds ~5MB to binary size"]
- **Security Scan Findings:** [Any safety/bandit results, or "none"]

## 4. Proposed Changes

- [file.py] → [Action taken] — (Reason)

## 5. Skipped Candidates

- [file.py:item] → Skipped — (Reason: public API / thin coverage / out of scope / etc.)

## 6. Verification Pyramid

- [ ] Static: [Linter + type-checker output]
- [ ] Diff: [Behavior delta between main and changes — confirm only intended behavior changed]
- [ ] Positive: [Test proving expected behavior works]
- [ ] Negative: [Test proving bad input is rejected]
- [ ] Regression: [Proof existing tests still pass]
- [ ] Rollback: [Proof the revert path works]
- [ ] Elegance: [Would a staff engineer approve this without hesitation? If no — explain why it was accepted anyway]
