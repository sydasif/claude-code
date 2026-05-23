#!/usr/bin/env bash
# Read JSON input from stdin
input=$(cat)

# Extract the file path(s)
# 1. Check for .tool_input.files (MultiEdit)
# 2. Fallback to .tool_input.path or .tool_input.file_path (Write/Edit)
files=$(jq -r '(.tool_input.files // .tool_input.path // .tool_input.file_path) | if type == "array" then .[] else . end' <<< "$input")

# Process each file found
for file_path in $files; do
    if [[ "$file_path" == *.py ]] && [[ -f "$file_path" ]]; then
        uv run ruff check --fix --quiet "$file_path" 2>/dev/null
        uv run ruff format --quiet "$file_path" 2>/dev/null
    fi
done

exit 0
