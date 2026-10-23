---
description: Audit what is eating disk space. **Read-only** — never delete or move anything.
---

Run a read-only disk usage scan of the user home directory. Detect the OS first (Linux / macOS / Windows), then proceed. Always report total disk size and % free before interpreting sizes.

1. **Top-level breakdown** — biggest folders at the user root level, sorted by size.
2. **Cache directories** — scan common caches (build caches, package manager caches, browser caches, container runtimes). State for each whether it is safe to clear.
3. **VM / container images** — list sizes for Docker images, Vagrant boxes, WSL distros, and other virtual machines.
4. **Package manager bloat** — snap, flatpak, Homebrew, Chocolatey, Scoop, conda — whichever are in use.
5. **Application data** — session logs, databases, caches, thumbnails in app-specific data dirs. Include Trash/Recycle Bin size.
6. **Cloud-synced storage** — OneDrive, Google Drive, iCloud, Dropbox. Report total size and whether files are online-only or locally cached.
7. **Old installers and archives** — `.iso`, `.dmg`, `.pkg`, `.exe`, `.deb`, `.zip`, `.tar.*` and similar over 10 MB outside known caches. List path, size, date.
8. **Downloads folder** — large files that look like they've already been used or installed.
9. **Photos and media** — count files, flag any individual file over 100 MB, note duplicates if detectable.
10. **Verdict** — end with a table: `| Rank | Consumer | Size | Reclaimable? | Risk |` Top 10 rows. Never suggest deleting — only report.
