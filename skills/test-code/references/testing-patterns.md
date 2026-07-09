# End-to-End Testing Patterns by Application Type

## CLI

- Normal commands, invalid input, missing arguments, error messages, exit codes.

## Web / API

- Start all required services.
- Walk through real user flows, not just individual endpoints in isolation.
- Test auth and validation paths, and failure scenarios (bad tokens, expired sessions, malformed payloads).

## Automation tools

- Run complete workflows end to end.
- Validate generated output.
- Verify actual changes on target systems, not just "the script exited 0."
- Test connection failures and recovery paths.

## Libraries / packages

- Import and use the package the way a consumer would.
- Test public functions with valid and invalid parameters.
- Check that exceptions are raised where they should be, with useful messages.

## Network automation add-on

Apply on top of the base type when network automation signals are detected (netmiko, nornir, napalm, scrapli, paramiko, ansible):

- Never assume a mocked/dry-run success means the real automation works.
- Test against a lab topology if one is available; if not, say clearly that device-level validation wasn't possible and why.
- Capture device state before and after execution and diff it - don't just trust the script's own "success" message.
- Check idempotency: running the script twice should not produce unwanted changes the second time.
- Explicitly test: unreachable devices, authentication failures, malformed inventory data, and partial command failures mid-run.
