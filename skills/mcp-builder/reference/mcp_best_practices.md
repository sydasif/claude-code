# MCP Server Best Practices

## Quick Reference

### Server Naming

- **Python**: `{service}_mcp` (e.g., `slack_mcp`)
- **Node/TypeScript**: `{service}-mcp-server` (e.g., `slack-mcp-server`)

### Tool Naming

- Use snake_case with service prefix
- Format: `{service}_{action}_{resource}`
- Example: `slack_send_message`, `github_create_issue`

### Response Formats

- Support both JSON and Markdown formats
- JSON for programmatic processing
- Markdown for human readability

### Pagination

- Always respect `limit` parameter
- Return `has_more`, `next_offset`, `total_count`
- Default to 20-50 items

---

## Server Naming Conventions

**Python**: `{service}_mcp` (lowercase with underscores)
**Node/TypeScript**: `{service}-mcp-server` (lowercase with hyphens)

---

## Tool Design

1. **Naming**: snake_case with service prefix
2. **Descriptions**: Must match actual functionality
3. **Annotations**: Include readOnlyHint, destructiveHint, idempotentHint
4. **Operations**: Keep tools focused and atomic

---

## Response Formats

### JSON Format

- Machine-readable structured data
- Include all fields and metadata

### Markdown Format

- Human-readable formatted text
- Use headers, lists, timestamps in readable format

---

## Pagination

- Always respect `limit` parameter
- Return pagination metadata: `has_more`, `next_offset`, `total_count`
- Default to 20-50 items

---

## Transport Options

| Transport       | Best For                      |
| --------------- | ----------------------------- |
| Streamable HTTP | Remote servers, multi-client  |
| stdio           | Local integrations, CLI tools |

---

## Security Best Practices

- **Authentication**: Use OAuth 2.1 or API keys in environment variables
- **Input Validation**: Sanitize paths, validate URLs, use Pydantic/Zod
- **Error Handling**: Don't expose internal errors to clients
- **DNS Rebinding**: Validate Origin header, bind to 127.0.0.1
