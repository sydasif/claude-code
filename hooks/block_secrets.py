#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def main():

    try:
        # Read and parse the hook input from stdin

        hook_input = sys.stdin.read()

        data = json.loads(hook_input)

        # Get the file path from the tool input

        file_path_str = data.get("tool_input", {}).get("file_path", "")

        if not file_path_str:
            sys.exit(0)  # Nothing to check

        file_path = Path(file_path_str)

        # Define the list of sensitive file extensions and prefixes

        sensitive_extensions = [
            ".env",
            ".pem",
            ".key",
            ".credential",
            ".token",
            ".p12",
            ".pfx",
            ".crt",
            ".cer",
            ".secret",
        ]

        name_lower = file_path.name.lower()

        # Check exact extension match (e.g. .env, .pem)
        if file_path.suffix.lower() in sensitive_extensions:
            blocking = True

        # Check prefix match for variant files (e.g. .env.production)
        # Requires trailing dot to avoid matching .envrc or .envfile
        elif any(
            name_lower == ext or name_lower.startswith(ext + ".") for ext in sensitive_extensions
        ):
            blocking = True

        # Check for dotted variants: name contains .key. or .pem. etc.
        # e.g. my.key.old → name is my.key.old, not a single suffix
        elif any(f".{ext.strip('.')}." in name_lower for ext in sensitive_extensions):
            blocking = True
        else:
            blocking = False

        if blocking:
            # This is a sensitive file, block the action

            # Construct a clear, helpful error message for Claude

            error_message = (
                f"SECURITY_POLICY_VIOLATION: Access to the sensitive file '{file_path.name}' is blocked. "
                f"Reason: Files with extensions like {', '.join(sensitive_extensions)} contain credentials and should not be accessed or modified by the AI. "
                "Please use environment variables or a secure secret management tool instead."
            )

            # Print the error message to stderr

            print(error_message, file=sys.stderr)

            # Exit with code 2 to block the action and feed the error to Claude

            sys.exit(2)

    except (json.JSONDecodeError, KeyError):
        # Fail silently if input is malformed

        sys.exit(0)

    # If no sensitive file is detected, exit with 0 to allow the action

    sys.exit(0)


if __name__ == "__main__":
    main()
