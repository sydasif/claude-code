---
name: system-audit
description: Read-only audits of the user's own machine (Linux, macOS, Windows) covering performance, boot, disk space, installed apps, security, plus a backup audit that compares the machine with its Ansible/dotfiles repo and fixes the repo. Use whenever the user says the computer is slow, laggy or overloaded, asks what is eating CPU/RAM/disk, why boot is slow or what runs at startup, what can be cleaned up or removed, or wants to check for anything suspicious (unknown processes, odd connections, extensions, cron jobs, third-party repos). Also use when they ask to audit or update their backup, backup playbook, Ansible setup repo or dotfiles, or say their settings have grown or drifted. Also for "audit my system", "health check", "full checkup". Never modifies the machine.
---

# System Audit

Six diagnostic playbooks for inspecting the machine Claude is running commands on. Every one is **read-only on the machine**: they report findings so the user can decide what to do. A user running an audit wants a trustworthy picture, and they can't trust it if the audit itself changed the system. The one extension is `backup-audit`, which also fixes the user's backup repo, but only in a separate clone on a branch.

## Shared rules (apply to every audit)

1. **Read-only on the machine, always.** (Sole exception: `backup-audit` edits a separate clone of the backup repo, as its playbook describes.) Never delete, remove, disable, kill, suspend, close, move, uninstall, or modify anything, and never run a command whose purpose is to do so. This holds even if a finding makes the fix obvious. Put fixes in the recommendations and let the user run them. If a command could write state (e.g. `apt autoremove`, `docker system prune`), do not run it, even with a dry-run flag you are unsure about; use a listing or simulation command that is certainly side-effect free.
2. **Detect the OS first** (Linux / macOS / Windows, and the distro or version), then choose commands for that platform. State the OS you detected in one line at the top.
3. **Measure, don't guess.** Base every claim on command output you actually saw. If a command is unavailable or needs privileges you don't have, say so and note what that leaves unchecked rather than filling the gap with assumptions. Avoid `sudo` unless the user has already allowed it.
4. **Identify in plain English.** When naming a process, package, service or file, say what it is and why it exists. "Unknown" is an acceptable answer; invented explanations are not.
5. **End with the verdict** defined in the playbook. The verdict is the part the user will act on, so keep it specific and ranked.

## Choose the playbook

Read only the reference file(s) that match the request.

| User intent | Playbook |
|---|---|
| Slow, laggy, high load, fans spinning, "what is using CPU/RAM" | `references/health-check.md` |
| Slow startup, what runs at boot, services, autostart | `references/boot-audit.md` |
| Disk full, what is eating space, what can be cleaned | `references/storage-check.md` |
| Installed apps, what is unused, what can be removed | `references/app-audit.md` |
| Anything suspicious, unknown processes, connections, extensions, scheduled tasks, repos | `references/security-audit.md` |
| Audit/update the backup: is the Ansible setup repo / dotfiles still accurate; what to add, remove or update in it (clones the repo and fixes it) | `references/backup-audit.md` |

If the request is vague ("check my system", "full audit"), run the first five in the order above, with one verdict per playbook, then a short combined summary of the three most important findings. Include the backup audit only when the user mentions their backup or setup repo or asks for it, since it clones and edits that repo. If it is ambiguous between two (e.g. "my machine is slow" could be health or boot), start with health-check and offer boot-audit as the follow-up.

## Output style

Lead with the verdict-relevant findings, not a dump of raw command output. Use tables where a playbook asks for one. Keep raw output out of the final answer unless it is the evidence for a specific flag (for example, the full command line of an unidentified process).
