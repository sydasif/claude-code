---
description: Audit what runs at boot and classify what is essential, needed, or bloat. **Read-only** — never disable or modify anything.
---

Run a read-only boot audit. Detect the OS first (Linux / macOS / Windows), then proceed.

1. **Boot timing** — report total boot time and how long each phase took (firmware/BIOS, bootloader, kernel, userspace). Show the critical chain so the longest blocking service is visible.
2. **Enabled services** — list all enabled services and sort them into three buckets:
   - **Essential**: the OS cannot function without these (network, display, logging, power management)
   - **Needed for your work**: services directly relevant to what you actually do (containers, VMs, VPN, remote access, development tooling)
   - **Bloat**: services that add boot delay or run idle with no clear purpose for this machine
3. **Identify the biggest delays** — name the top 3–5 services consuming the most start time and flag any that sit on the critical path vs. ones that start in parallel.
4. **Autostart items** — check desktop autostart entries (GNOME/KDE/XDG autostart on Linux, Login Items on macOS, Startup folder on Windows). List anything beyond the desktop session itself.
5. **Verdict** — end with:
   - Estimated reclaimable boot time if bloat services were disabled
   - The single biggest win (one service to disable for the most impact)
   - A short list of services worth investigating further (unknown purpose, no clear reason to be enabled)
