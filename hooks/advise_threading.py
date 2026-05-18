#!/usr/bin/env python3

"""
Python Async Advisor Hook
Warns when threading patterns are used and suggests async/await alternatives
"""

import json
import os
import re
import sys


def check_for_threading(content):
    """Check if content contains threading patterns."""
    if not content:
        return None
    # Patterns to detect threading usage
    threading_patterns = [
        (r"import\s+threading", "import threading"),
        (r"from\s+threading\s+import", "from threading import"),
        (r"threading\.Thread", "threading.Thread"),
        (r"Thread\s*\(", "Thread class instantiation"),
        (r"threading\.Lock", "threading.Lock"),
        (r"threading\.Event", "threading.Event"),
        (r"threading\.Semaphore", "threading.Semaphore"),
        (
            r"(from\s+concurrent\.futures\s+import.*ThreadPoolExecutor|concurrent\.futures\.ThreadPoolExecutor)",
            "ThreadPoolExecutor",
        ),
    ]
    detected_patterns = []
    for pattern, description in threading_patterns:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            detected_patterns.append(description)
    return detected_patterns if detected_patterns else None


def generate_async_suggestion(detected_patterns):
    """Generate suggestions for async/await alternatives."""
    suggestions = {
        "import threading": "Use: import asyncio",
        "from threading import": "Use: import asyncio",
        "threading.Thread": "Use: asyncio.create_task() or async def functions",
        "Thread class instantiation": "Use: async def function and asyncio.create_task()",
        "threading.Lock": "Use: asyncio.Lock()",
        "threading.Event": "Use: asyncio.Event()",
        "threading.Semaphore": "Use: asyncio.Semaphore()",
        "ThreadPoolExecutor": "Use: loop.run_in_executor() for CPU-bound, asyncio.create_task() for I/O-bound",
    }
    advice = []
    for pattern in detected_patterns:
        if pattern in suggestions:
            advice.append(f"• {pattern} → {suggestions[pattern]}")
        else:
            advice.append(f"• {pattern} → Consider async/await pattern")
    return advice


def main():
    """Main hook function."""
    try:
        # Hook data comes via stdin as JSON
        hook_input = sys.stdin.read().strip()

        if not hook_input:
            sys.exit(0)

        hook_data = json.loads(hook_input)

        tool_name = hook_data.get("tool_name", "") or os.environ.get(
            "CLAUDE_TOOL_NAME", ""
        )
        tool_input = hook_data.get("tool_input", {}) or hook_data

        # Only check Write, Edit, MultiEdit tools for Python content
        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        # Check if it's a Python file
        file_path = tool_input.get("file_path", "")
        if not file_path.endswith(".py"):
            sys.exit(0)

        # Get content to check
        content = None
        if tool_name == "Write":
            content = tool_input.get("content", "")
        elif tool_name == "Edit":
            content = tool_input.get("new_string", "")
        elif tool_name == "MultiEdit":
            # Check all edits
            edits = tool_input.get("edits", [])
            all_content = []
            for edit in edits:
                all_content.append(edit.get("new_string", ""))
            content = "\n".join(all_content)

        # Check for threading patterns
        detected = check_for_threading(content)
        if detected:
            # Generate helpful error message
            suggestions = generate_async_suggestion(detected)
            error_msg = f"""[ADVISORY] Threading detected in {file_path} — consider async/await instead

Detected patterns:
{chr(10).join(f"  - {pattern}" for pattern in detected)}

Recommended alternatives:
{chr(10).join(suggestions)}

Why async/await?
  - Better performance for I/O-bound operations
  - Easier debugging and testing
  - More predictable execution model
  - Better integration with modern Python frameworks

Example conversion:

```python
# Instead of:
import threading
def worker():
    # do work
    pass
thread = threading.Thread(target=worker)
thread.start()
thread.join()

# Use:
import asyncio
async def worker():
    # do async work
    pass
await worker()
```

Note: If you intentionally need threads (e.g. wrapping blocking I/O), use asyncio.to_thread() or loop.run_in_executor()."""
            print(error_msg, file=sys.stderr)
            sys.exit(0)  # Advisory only — does not block

        # No threading detected, allow operation
        sys.exit(0)
    except Exception as e:
        # Don't block on errors, just log
        print(f"Threading check failed: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
