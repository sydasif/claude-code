#!/usr/bin/env python3
import json
import sys

SAFE_PREFIXES = ["uv sync", "git status", "ls"]

input_data = json.load(sys.stdin)
command = input_data.get("tool_input", {}).get("command", "")

for prefix in SAFE_PREFIXES:
    if command.startswith(prefix):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PermissionRequest",
                "decision": {"behavior": "allow"},
            }
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
