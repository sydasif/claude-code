# Boot audit: what runs at boot

**Read-only.** Never disable or modify anything.

1. **Boot timing.** Report total boot time and each phase: firmware/BIOS, bootloader, kernel, userspace (e.g. `systemd-analyze`, `systemd-analyze critical-chain`). Show the critical chain so the longest blocking service is visible.
2. **Enabled services.** List all enabled services and sort them into three buckets:
   - **Essential**: the OS cannot function without these (network, display, logging, power management)
   - **Needed for your work**: directly relevant to what the user actually does (containers, VMs, VPN, remote access, development tooling)
   - **Bloat**: adds boot delay or runs idle with no clear purpose for this machine
   Pitfall: `systemctl list-unit-files --state=enabled --no-user` is invalid — `--no-user` is not a recognized flag for `list-unit-files`. Use `systemctl list-unit-files --state=enabled --no-pager` instead (or pipe through `head` to limit output).
3. **Biggest delays.** Name the top 3-5 services by start time. Flag which sit on the critical path and which start in parallel (parallel ones rarely delay boot).
4. **Autostart items.** Check desktop autostart entries (GNOME/KDE/XDG autostart on Linux, Login Items on macOS, Startup folder on Windows). List anything beyond the desktop session itself.
5. **Verdict.** End with:
   - Estimated reclaimable boot time if bloat services were disabled
   - The single biggest win (one service to disable for the most impact)
   - A short list of services worth investigating further (unknown purpose, no clear reason to be enabled)
