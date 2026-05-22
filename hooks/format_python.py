#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path


def find_project_root(file_path: str) -> Path | None:
    """Return directory containing pyproject.toml or uv.lock, if any."""
    current = Path(file_path).resolve().parent
    for directory in (current, *current.parents):
        if (directory / "pyproject.toml").is_file() or (directory / "uv.lock").is_file():
            return directory
    return None


def ruff_prefix(project_root: Path | None) -> list[str]:
    if project_root is not None:
        return ["uv", "run", "ruff"]
    return ["ruff"]


def run_ruff(args: list[str], file_path: str, project_root: Path | None) -> bool:
    cmd = [*ruff_prefix(project_root), *args, file_path]
    cwd = str(project_root) if project_root else None
    try:
        subprocess.run(cmd, check=False, capture_output=True, cwd=cwd)
        return True
    except FileNotFoundError:
        return False


def should_format_file(file_path: str, tool_name: str) -> bool:
    if not Path(file_path).is_file():
        return False
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return False
    return Path(file_path).suffix.lower() == ".py"


def main() -> None:
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

        project_root = find_project_root(file_path)
        run_ruff(["format"], file_path, project_root)
        run_ruff(["check", "--fix"], file_path, project_root)

    except (json.JSONDecodeError, KeyError):
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
