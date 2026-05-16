# MCP Server Evaluation Guide

## Overview

This document provides guidance on creating comprehensive evaluations for MCP servers. Evaluations test whether LLMs can effectively use your MCP server to answer realistic, complex questions using only the tools provided.

## Quick Reference

### Evaluation Requirements

- Create 10 human-readable questions
- Questions must be READ-ONLY, INDEPENDENT, NON-DESTRUCTIVE
- Each question requires multiple tool calls (potentially dozens)
- Answers must be single, verifiable values
- Answers must be STABLE (won't change over time)

### Output Format

```xml
<evaluation>
   <qa_pair>
      <question>Your question here</question>
      <answer>Single verifiable answer</answer>
   </qa_pair>
</evaluation>
```

---

## Question Guidelines

### Core Requirements

1. **Questions MUST be independent** - Each question should NOT depend on the answer to any other question
2. **Questions MUST require ONLY NON-DESTRUCTIVE operations** - Should not modify state
3. **Questions must be REALISTIC and COMPLEX** - Require multiple tool calls

### Complexity

- Multi-hop questions requiring sequential tool calls
- May require extensive paging
- Must require deep understanding

### Stability

- Answers must NOT change over time
- Do not rely on "current state" which is dynamic

---

## Answer Guidelines

1. **Verifiable**: Single, verifiable value for direct string comparison
2. **Readable**: Prefer human-readable formats (names, dates)
3. **Stable**: Based on "closed" concepts that won't change
4. **Clear**: Single, unambiguous answer
5. ** Diverse**: Various modalities and formats

---

## Evaluation Process

1. **Documentation Inspection** - Read API docs, understand endpoints
2. **Tool Inspection** - List available tools, understand schemas
3. **Developing Understanding** - Iterate, understand task patterns
4. **Content Inspection** - Use READ-ONLY operations to identify content
5. **Task Generation** - Create 10 human-readable questions

---

## Output Format

```xml
<evaluation>
   <qa_pair>
      <question>Find the project created in Q2 2024 with most completed tasks</question>
      <answer>Project Name</answer>
   </qa_pair>
   <qa_pair>
      <question>Search for issues labeled as "bug" closed in March 2024</question>
      <answer>username</answer>
   </qa_pair>
</evaluation>
```

---

## Good Question Examples

**Multi-hop question**:

```xml
<qa_pair>
   <question>Find the repository archived in Q3 2023 with most forks. What language?</question>
   <answer>Python</answer>
</qa_pair>
```

This is good because:

- Requires multiple searches
- Needs historical data analysis
- Answer is a simple verifiable value
- Based on closed data that won't change
