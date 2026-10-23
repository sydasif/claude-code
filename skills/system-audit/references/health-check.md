# Health check: what is slowing the machine down

**Read-only.** Never close, kill, suspend, or delete anything.

1. **Measure live.** Sample CPU and memory over a few seconds (e.g. `top -b -n 3 -d 2`, `vmstat 2 5`, `Get-Counter` on Windows). One-shot snapshots mislead because spikes and idle moments look identical.
2. **Heavy users.** List every process above 5% CPU or 5% RAM. State what each is in plain English. Resolve container processes to their container name and image (e.g. map PIDs to containers via `docker ps` / cgroup info).
3. **Quiet killers.** Check disk I/O wait, swap/paging activity, and processes stuck in uninterruptible sleep (state `D`). A machine can feel slow with an idle CPU.
4. **Read load correctly.** Compare load average (or the platform equivalent) against uptime and core count. Load right after boot is noise.
5. **Flag the unknowns.** List any process you cannot positively identify, with its full command line.
6. **Verdict.** End with:
   - `OVERLOADED: yes / no / borderline`
   - One line on the biggest cause
   - One line on what to check next
