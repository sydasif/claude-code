#!/usr/bin/env python3

"""
Claude Code Audit Logger
Tracks all tool usage for compliance and debugging
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_audit_log_path():
    """Get the audit log file path."""
    claude_dir = Path.home() / ".claude"
    claude_dir.mkdir(exist_ok=True)
    return claude_dir / "audit.log"


def rotate_log_if_needed(log_path, max_bytes=10 * 1024 * 1024):
    """Rotate log with timestamped backup if it exceeds max_bytes."""
    try:
        if log_path.exists() and log_path.stat().st_size > max_bytes:
            timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
            rotated = log_path.with_name(f"{log_path.name}.{timestamp}")
            log_path.rename(rotated)
    except OSError:
        pass


def extract_command_info(hook_data_str):
    """Extract relevant command information from PostToolUse hook data."""
    try:
        hook_data = json.loads(hook_data_str)
        # Build comprehensive audit record
        info = {
            "session_id": hook_data.get("session_id", "unknown"),
            "tool_name": hook_data.get("tool_name", "Unknown"),
            "hook_event": hook_data.get("hook_event_name", "PostToolUse"),
            "timestamp": datetime.now().isoformat(),
            "user": os.environ.get("USER", "unknown"),
            "working_dir": hook_data.get("cwd", "unknown"),
            "project": os.path.basename(hook_data.get("cwd", "unknown")) or "unknown",
            "transcript_path": hook_data.get("transcript_path", ""),
        }

        # Extract tool input metadata only (no content for compliance)
        tool_input = hook_data.get("tool_input", {})
        if tool_input:
            # Log metadata only for compliance
            metadata = {}
            if "file_path" in tool_input:
                metadata["file_path"] = tool_input["file_path"]
            if "command" in tool_input:
                metadata["command"] = tool_input["command"][
                    :100
                ]  # First 100 chars only
            if "content" in tool_input:
                metadata["content_size"] = len(str(tool_input["content"]))
            if "new_string" in tool_input:
                metadata["new_string_size"] = len(str(tool_input["new_string"]))
            if "old_string" in tool_input:
                metadata["old_string_size"] = len(str(tool_input["old_string"]))
            # Keep small metadata intact
            for key, value in tool_input.items():
                if (
                    key not in ["content", "new_string", "old_string"]
                    and len(str(value)) < 200
                ):
                    metadata[key] = value
            info["tool_metadata"] = metadata

        # Extract tool response metadata only
        tool_response = hook_data.get("tool_response", {})
        if tool_response:
            # Log response metadata, not full content
            response_metadata = {}
            if isinstance(tool_response, dict):
                for key, value in tool_response.items():
                    if len(str(value)) < 200:  # Small responses only
                        response_metadata[key] = value
                    else:
                        response_metadata[f"{key}_size"] = len(str(value))
            else:
                response_metadata = {"response_size": len(str(tool_response))}
            info["response_metadata"] = response_metadata
        return info
    except json.JSONDecodeError as e:
        return {
            "tool_name": "Unknown",
            "hook_event": "PostToolUse",
            "timestamp": datetime.now().isoformat(),
            "user": os.environ.get("USER", "unknown"),
            "project": os.path.basename(os.getcwd()),
            "error": f"Failed to parse hook data: {str(e)}",
            "raw_data": hook_data_str[:200] + "..."
            if len(hook_data_str) > 200
            else hook_data_str,
        }


def log_audit_entry(info):
    """Write audit entry to log file."""
    try:
        audit_log = get_audit_log_path()
        rotate_log_if_needed(audit_log)
        log_entry = json.dumps(info, separators=(",", ":"))
        with open(audit_log, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        # Fallback to stderr if logging fails
        print(f"Audit logging failed: {e}", file=sys.stderr)


def main():
    """Main audit logging function."""
    # Hook data comes via stdin as JSON
    hook_input = sys.stdin.read().strip()
    if not hook_input:
        sys.exit(0)
    # Extract and log the command information
    info = extract_command_info(hook_input)
    log_audit_entry(info)
    # Exit successfully
    sys.exit(0)


if __name__ == "__main__":
    main()
