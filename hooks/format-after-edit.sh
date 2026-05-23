#!/usr/bin/env bash
# Read JSON input from stdin
input=$(cat)

# Extract the file path(s)
files=$(jq -r '(.tool_input.files // .tool_input.path // .tool_input.file_path) | if type == "array" then .[] else . end' <<< "$input")

# Process each file found
for file_path in $files; do
    if [[ -z "$file_path" || "$file_path" == "null" ]]; then
        continue
    fi

    if [[ ! -f "$file_path" ]]; then
        continue
    fi

    if [[ "$file_path" == *.py ]]; then
        # Python: Ruff lint and format
        uv run ruff check --fix --quiet "$file_path" 2>/dev/null
        uv run ruff format --quiet "$file_path" 2>/dev/null
    elif [[ "$file_path" == *.md || "$file_path" == *.yaml || "$file_path" == *.yml || "$file_path" == *.json ]]; then
        # Markdown, YAML, JSON: Prettier
        npx prettier --write "$file_path" 2>/dev/null
    fi
done

exit 0
