# App audit: what is installed, used, and removable

**Read-only.** Never remove anything.

1. **Inventory.** List every installed application: package manager apps (.deb / snap / flatpak / Homebrew / winget / apt), user-installed tools (pipx, npm global, standalone installs in `~/.local/bin`), and desktop apps (`.desktop` files or Launchpad/Start menu entries).
2. **Usage evidence.** For each app, check for actual use, not just install:
   - Shell history entries
   - Config or data directory modification timestamps
   - Cache directory modification timestamps
   - Recently-used file lists (where available)

   Establish the machine's install/setup date first. Anything installed at setup with no later use signal is "unused since install."
3. **Classify** every app into one bucket:
   - **In use**: recent evidence of actual use. State the evidence.
   - **Safe to remove**: installed but no trace of use. State what the app is and why removal is safe.
   - **Came with system**: preinstalled OS/desktop components that are required. List briefly; these should stay.
4. **Flag the uncertain.** Apps where keep-or-remove is not obvious. State what would clarify the decision.
5. **Verdict.** End with:
   - Total estimated reclaimable disk space from "safe to remove" apps
   - Top 3-5 individual apps worth removing first (largest or most obviously unused)
   - A note on dependencies to check before removing (e.g. ffmpeg required by yt-dlp)
