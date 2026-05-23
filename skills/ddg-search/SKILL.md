---
name: ddg-search
description: Web search, documentation search and real-time info retrieval, using DuckDuckGo.
---

# Web Search Instructions

Use the following instructions to perform web searches with the `ddg_search` mcp for real-time information retrieval.

## 1. Tool Mapping

| Goal                   | Tool          | Key Parameter                  |
| :--------------------- | :------------ | :----------------------------- |
| Broad search / News    | `web_search`  | `search_type='news' \| 'text'` |
| Official Documentation | `search_docs` | `domain='docs.example.com'`    |
| Deep Page Reading      | `fetch_page`  | `output_format='markdown'`     |

## 2. API Reference

### `web_search`

- **Use**: Broad topics, trending news.
- **Params**: `query`, `search_type` ('text'/'news'), `time_range` ('d','w','m','y'), `region`.

### `search_docs`

- **Use**: Authoritative documentation, specific site search.
- **Params**: `query`, `domain`.

### `fetch_page`

- **Use**: Extracting full content from a specific URL.
- **Params**: `url`, `output_format` ('markdown','json','txt'), `include_tables` (bool).

## 3. Second Opinion Strategy

When results seem incomplete or outdated:

1. Verify with `fetch_page` on top results
2. Cross-check with `search_docs` on authoritative sites

> This MCP is designed for search tasks. For real-time data, ensure to use the latest search parameters and verify results against multiple sources.
