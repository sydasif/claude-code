# Node/TypeScript MCP Server Implementation Guide

## Overview

This document provides Node/TypeScript-specific best practices for implementing MCP servers using the MCP TypeScript SDK.

## Quick Reference

### Key Imports

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import express from "express";
import { z } from "zod";
```

### Server Initialization

```typescript
const server = new McpServer({
  name: "service-mcp-server",
  version: "1.0.0",
});
```

### Tool Registration

```typescript
server.registerTool(
  "tool_name",
  {
    title: "Tool Display Name",
    description: "What the tool does",
    inputSchema: { param: z.string() },
  },
  async ({ param }) => {
    return {
      content: [{ type: "text", text: JSON.stringify(result) }],
    };
  },
);
```

## Server Naming

- **Format**: `{service}-mcp-server` (lowercase with hyphens)
- **Examples**: `github-mcp-server`, `jira-mcp-server`

## Project Structure

```
{service}-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # Main entry point
│   ├── types.ts          # Type definitions
│   ├── tools/            # Tool implementations
│   ├── services/         # API clients
│   └── schemas/          # Zod validation
└── dist/                 # Built output
```

## Tool Implementation

Use Zod schemas for input validation:

```typescript
const ToolInputSchema = z
  .object({
    param1: z.string().min(1).max(100),
    param2: z.number().optional(),
  })
  .strict();

server.registerTool(
  "tool_name",
  {
    title: "Tool Title",
    description: "What the tool does",
    inputSchema: ToolInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
    },
  },
  async (params) => {
    // Implementation
  },
);
```

## Transport Options

- **Streamable HTTP**: Remote servers, multi-client
- **stdio**: Local integrations, CLI tools

## See Also

- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
