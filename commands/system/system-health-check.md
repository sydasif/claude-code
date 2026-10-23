---
description: Diagnose what is slowing the machine down. **Read-only** — never close, kill, suspend, or delete anything.
argument-hint: [sample-seconds]
---

Run a read-only system performance audit. Detect the OS first (Linux / macOS / Windows), then proceed.

Optional argument `$ARGUMENTS`: seconds to sample in step 1. If empty, sample for a few seconds.

1. **Measure live** — sample CPU and memory over a few seconds. Do not rely on one-shot snapshots.
2. **Heavy users** — list every process above 5% CPU or 5% RAM. State what each process is in plain English. Resolve any container processes to their container name/image.
3. **Quiet killers** — check disk I/O wait, swap/paging activity, and processes stuck in uninterruptible sleep. A machine can feel slow with an idle CPU.
4. **Read load correctly** — compare load average (or equivalent) against uptime and core count. Load right after boot is noise.
5. **Flag the unknowns** — list any process you cannot positively identify, with its full command line.
6. **Verdict** — end with: `OVERLOADED: yes / no / borderline` — one line on the biggest cause, one line on what to check next.
