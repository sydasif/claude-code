---
description: Use the memo command to create and manage memory files for your project.
---

# Memory Management

When working with a user on a project, keep your **memory** up to date.

## Memory Workflow

- Update your memory and index files with new findings, decisions, and insights.
- Use those files to improve continuity and future interactions.

### Front-matter Conventions

- Use the following YAML front-matter as minimal template for all memo files

```yml
name: example-memo
description: A brief description of the memo's content
created: 2025-01-15
metadata:
  node_type: memory
  type: project
  originSessionId: xyz-1234-5678-90ab-cdef
tags: tag1, tag2, tag3
related: [[File1]], [[File2]]
last_update: 2026-02-26
```

- Add any additional metadata as needed for your project

### Maintenance of Memory and Index Files

- Review regularly to ensure accuracy and completeness.
- Remove outdated or incorrect information when it becomes obsolete.

## Guidelines

- **Context efficiency is paramount.** Future sessions pay for every token
- **Signal over noise.** The "why" matters more than the "what"
- **Point, don't duplicate.** Reference files instead of copying content
