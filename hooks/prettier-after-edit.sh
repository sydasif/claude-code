#!/usr/bin/env bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

if [[ "$file_path" != *.py ]] && [[ -f "$file_path" ]]; then
  npx prettier --write "$file_path"
fi
exit 0
