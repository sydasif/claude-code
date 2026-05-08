# Security Rules — Always Enforced

## Input & Queries

- Validate and sanitize all inputs; enforce length limits.
- Use parameterized queries only — no string-concatenated SQL.
- Escape all output to prevent XSS.

## Secrets & Auth

- Never store secrets in code — use environment variables or secure vaults.
- Hash passwords with `bcrypt` or `Argon2` only.

## Execution Safety

- Never use `eval` or `exec` with user-controlled input.
- Always use `subprocess` with `shell=False`.
- Use secure, hardened XML parsers.

## Transport & Errors

- Enforce HTTPS for all external communication.
- Never expose sensitive data, stack traces, or internal paths in error responses.

## File Handling

- Validate file type and size before processing.
- Store uploads outside the web root.
- Apply strict filesystem permissions.
