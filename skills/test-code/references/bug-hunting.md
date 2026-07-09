# Bug Hunting Checklist

Go past syntax errors. Look for:

- Runtime failures
- Incorrect logic
- Bad assumptions baked into the code
- Missing validation
- Security issues
- Dependency problems (pinning, known CVEs, version conflicts)
- Poor error handling (swallowed exceptions, unhelpful messages)
- User experience problems (confusing output, silent failures)

## Fix workflow

For every bug found:

1. Reproduce it.
2. Explain why it happens.
3. Fix it.
4. Re-run the relevant test.
5. Confirm the fix actually holds.
