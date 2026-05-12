#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from pathlib import Path

PRETTIER_EXTENSIONS = {
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".mts",
    ".cts",
    ".css",
    ".scss",
    ".less",
    ".html",
    ".htm",
    ".vue",
    ".json",
    ".json5",
    ".jsonc",
    ".yaml",
    ".yml",
    ".md",
    ".mdx",
    ".graphql",
    ".gql",
}


def format_prettier(file_path):
    try:
        subprocess.run(["prettier", "--write", file_path], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def should_format_file(file_path, tool_name):
    if not os.path.exists(file_path):
        return False
    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        return False
    return True


def main():
    hook_input = sys.stdin.read().strip()
    if not hook_input:
        sys.exit(0)

    try:
        hook_data = json.loads(hook_input)
        tool_name = hook_data.get("tool_name", "")
        tool_input = hook_data.get("tool_input", {})
        file_path = tool_input.get("file_path")

        if not file_path or not should_format_file(file_path, tool_name):
            sys.exit(0)

        extension = Path(file_path).suffix.lower()
        if extension not in PRETTIER_EXTENSIONS:
            sys.exit(0)

        if format_prettier(file_path):
            print(f"Formatted {file_path}")
    except (json.JSONDecodeError, KeyError):
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
