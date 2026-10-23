---
description: Find every installed application, determine which ones have been actually used recently, and classify the rest. **Read-only** — never remove anything.
---

Run a read-only application usage audit. Detect the OS first (Linux / macOS / Windows), then proceed.

1. **Inventory** — list every installed application: package manager apps (.deb / snap / flatpak / Homebrew / winget / apt), user-installed tools (pipx, npm global, standalone installs in `~/.local/bin`), and desktop apps (`.desktop` files or Launchpad/Start menu entries).

2. **Usage evidence** — for each app, check for actual use, not just install:
   - Shell history entries
   - Config or data directory modification timestamps
   - Cache directory modification timestamps
   - Recently-used file lists (where available)
     Establish the machine's install/setup date first — anything installed at setup with no subsequent use signal is "unused since install."

3. **Classify** every app into one of three buckets:
   - **In use** — recent evidence of actual use. State the evidence.
   - **Safe to remove** — installed but no trace of use. State what the app is and why removal is safe.
   - **Came with system** — preinstalled OS/desktop components that are required. List them briefly; these should stay.

4. **Flag the uncertain** — apps where it's not obvious whether to keep or remove. State what would clarify the decision.

5. **Verdict** — end with:
   - Total estimated reclaimable disk space from "safe to remove" apps
   - Top 3–5 individual apps worth removing first (largest or most obviously unused)
   - A note on any dependencies to check before removing (e.g. ffmpeg required by yt-dlp)
