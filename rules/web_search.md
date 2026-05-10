# Research Instructions

Use the following instructions to perform web searches with the `duck` mcp for real-time information retrieval.

## API Reference

### `search_web`

- **Use**: Broad topics, trending news.
- **Params**: `query`, `search_type` ('text'/'news'), `time_range` ('d','w','m','y'), `region`.

### `search_docs`

- **Use**: Authoritative documentation, specific site search.
- **Params**: `query`, `domain`.

### `fetch_page`

- **Use**: Extracting full content from a specific URL.
- **Params**: `url`, `output_format` ('markdown','json','txt'), `include_tables` (bool).

### `get_weather`

- **Workflow**: Use `get_location` to get `lat/long` $\rightarrow$ Pass to `get_weather`.
- **Weather Params**: `latitude`, `longitude`, `mode` ('current'/'forecast'), `days`.

> This MCP is designed for search tasks. For real-time data, ensure to use the latest search parameters and verify results against multiple sources.
