# Python MCP Server Implementation Guide

## Overview

This document provides Python-specific best practices and examples for implementing MCP servers using the MCP Python SDK. It covers server setup, tool registration patterns, input validation with Pydantic, error handling, and complete working examples.

## Quick Reference

### Key Imports

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
```

### Server Initialization

```python
mcp = FastMCP("service_mcp")
```

### Tool Registration Pattern

```python
@mcp.tool(name="tool_name", annotations={...})
async def tool_function(params: InputModel) -> str:
    # Implementation
    pass
```

## MCP Python SDK and FastMCP

The official MCP Python SDK provides FastMCP, a high-level framework for building MCP servers. It provides:

- Automatic description and inputSchema generation from function signatures and docstrings
- Pydantic model integration for input validation
- Decorator-based tool registration with `@mcp.tool`

## Server Naming Convention

Python MCP servers must follow this naming pattern:

- **Format**: `{service}_mcp` (lowercase with underscores)
- **Examples**: `github_mcp`, `jira_mcp`, `stripe_mcp`

The name should be:

- General (not tied to specific features)
- Descriptive of the service/API being integrated
- Easy to infer from the task description
- Without version numbers or dates

## Tool Implementation

### Tool Naming

Use snake_case for tool names (e.g., "search_users", "create_project", "get_channel_info") with clear, action-oriented names.

**Avoid Naming Conflicts**: Include the service context to prevent overlaps:

- Use "slack_send_message" instead of just "send_message"
- Use "github_create_issue" instead of just "create_issue"

### Tool Structure with FastMCP

Tools are defined using the `@mcp.tool` decorator with Pydantic models for input validation:

```python
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("example_mcp")

class ServiceToolInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    param1: str = Field(..., description="First parameter", min_length=1, max_length=100)
    param2: Optional[int] = Field(default=None, description="Optional param", ge=0, le=1000)

@mcp.tool(
    name="service_tool_name",
    annotations={
        "title": "Human-Readable Tool Title",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def service_tool_name(params: ServiceToolInput) -> str:
    '''Tool description.'''
    # Implementation here
    pass
```

## Pydantic v2 Key Features

- Use `model_config` instead of nested `Config` class
- Use `field_validator` instead of deprecated `validator`
- Use `model_dump()` instead of deprecated `dict()`
- Validators require `@classmethod` decorator
- Type hints are required for validator methods

## Response Format Options

Support multiple output formats for flexibility:

```python
from enum import Enum

class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"
```

**Markdown format**:

- Use headers, lists, and formatting for clarity
- Convert timestamps to human-readable format
- Show display names with IDs in parentheses
- Omit verbose metadata

**JSON format**:

- Return complete, structured data suitable for programmatic processing
- Include all available fields and metadata

## Pagination Implementation

For tools that list resources:

```python
class ListInput(BaseModel):
    limit: Optional[int] = Field(default=20, description="Max results", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="Skip for pagination", ge=0)

async def list_items(params: ListInput) -> str:
    data = await api_request(limit=params.limit, offset=params.offset)
    # Return pagination info with has_more, next_offset, total
    pass
```

## See Also

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md)
