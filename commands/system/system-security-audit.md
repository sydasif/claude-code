---
description: Find anything on the system that shouldn't be there. **Read-only** — never remove, disable, or modify anything.
---

Run a read-only security audit. Detect the OS first (Linux / macOS / Windows), then proceed.

1. **Process check** — list every running process. Flag any you cannot positively identify (unknown binary, suspicious path, unexpected user). State what each one is and why it should be there.
2. **Network connections** — list all active TCP/UDP connections. Separate localhost/internal from external internet connections. Flag anything connecting to the internet that you can't explain. Check whether a firewall is active.
3. **Browser and editor extensions** — list every installed browser extension and code editor extension. State what each one does. Flag any that don't match your work profile or that have known privacy concerns.
4. **Scheduled tasks** — list all cron jobs, systemd timers, and OS scheduled tasks. Flag any that connect to the internet or that you don't recognize.
5. **Package repositories** — list all third-party package repositories. Flag any that don't come from a known, trusted source.
6. **Error and anomaly signals** — check system logs for repeated errors, permission denials, or suspicious activity in the last 24 hours.
7. **Verdict** — end with:
   - A clear statement: is the system clean, or is there a specific concern?
   - A table of any items that warrant attention: `| Item | What it is | Concern | Risk level |`
   - Recommendations (do not execute them) for anything that should be investigated or fixed
