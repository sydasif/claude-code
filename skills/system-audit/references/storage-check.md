# Storage check: what is eating disk space

**Read-only.** Never delete or move anything. Scope is the user's home directory.

Always report total disk size and % free before interpreting any sizes.

1. **Top-level breakdown.** Biggest folders at the user root level, sorted by size.
2. **Cache directories.** Scan common caches (build caches, package manager caches, browser caches, container runtimes). State for each whether it is safe to clear.
3. **VM / container images.** Sizes for Docker images, Vagrant boxes, WSL distros, and other virtual machines.
4. **Package manager bloat.** snap, flatpak, Homebrew, Chocolatey, Scoop, conda: whichever are in use.
5. **Application data.** Session logs, databases, caches, thumbnails in app-specific data dirs. Include Trash/Recycle Bin size.
6. **Cloud-synced storage.** OneDrive, Google Drive, iCloud, Dropbox. Report total size and whether files are online-only or locally cached.
7. **Old installers and archives.** `.iso`, `.dmg`, `.pkg`, `.exe`, `.deb`, `.zip`, `.tar.*` and similar over 10 MB outside known caches. List path, size, date.
8. **Downloads folder.** Large files that look like they have already been used or installed.
9. **Photos and media.** Count files, flag any individual file over 100 MB, note duplicates if detectable.
10. **Verdict.** End with a table of the top 10 rows:

    `| Rank | Consumer | Size | Reclaimable? | Risk |`

    Only report. Never suggest deleting; "Reclaimable?" and "Risk" describe the facts, not an instruction.
