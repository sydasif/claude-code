#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from pathlib import Path


def format_ruff(file_path):
    try:
        subprocess.run(["ruff", "format", file_path], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def lint_ruff(file_path):
    """Run ruff check --fix. Returns True if command ran (not whether issues were found)."""
    try:
        subprocess.run(["ruff", "check", "--fix", file_path], check=False, capture_output=True)
        return True
    except FileNotFoundError:
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

        if Path(file_path).suffix.lower() != ".py":
            sys.exit(0)

        formatted = format_ruff(file_path)
        linted = lint_ruff(file_path)

        if formatted or linted:
            print(f"Formatted and linted {file_path}")
    except (json.JSONDecodeError, KeyError):
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
