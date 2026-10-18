---
name: chapter-pipeline
description: |
  Create the next chapter of the "Advance Network Automation" book (advance-network-automation
  repo) — Nornir training material built from CBT Nuggets videos. Orchestrates the full
  phase-gated workflow: discover book context, analyze the source video (uses the `watch`
  skill), ground the chapter in the real netlab lab (uses the `netlab` skill), write the
  outline and chapter, run the mechanical verify gate, prove it on the lab, and commit.
  Use when the user says "run the chapter pipeline", "create the next chapter", "draft
  chapter N", "analyze the video and write the next chapter", or similar.
---

# Chapter Pipeline (Advance Network Automation book)

Orchestrated, phase-gated workflow to add one chapter to the book. Each phase has an
**exit criterion**; do not proceed until it is met. Surface problems to the user at gates
rather than silently pushing past them.

## Repos & context

| Item                | Path                                                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Book source         | `advance-network-automation/docs/source/` (MyST Markdown)                                                        |
| Lab                 | `netlab-lab/` (netlab + containerlab, Cisco IOL R1–R4; not a git repo)                                           |
| Runbooks            | `nornir-automation/` (config.yaml + inventory + scrapli-/netmiko-/napalm-runbooks/)                              |
| Project rules       | workspace `CLAUDE.md` (read first)                                                                               |
| Chapter conventions | each chapter = `NN_topic/` dir with `index.md` + one content file; entry added to `docs/source/index.md` toctree |
| Working repo        | `advance-network-automation` (git; commit per chapter)                                                           |

### Book rules (non-negotiable)

1. **No camera wording**: never "the video", "the nugget", "the course", "in the video".
   Source video is author context only; chapters stand alone as reference docs.
2. **MyST anchors**: explicit labels use the standalone form
   `(anchor-name)=` on the line **above** the heading, referenced as `[Text](#anchor-name)`.
   **Never** `## Heading {#anchor}` — with myst-parser 5.1.0 that renders the `{#anchor}`
   as literal heading text (breaks PDF; see `02_runbook/lab.md` and `05_groups/groups.md`
   for the working syntax).
3. **Glyphs**: any new non-ASCII char in a code block needs a matching
   `\DeclareUnicodeCharacter{XXXX}{...}` line in `docs/source/conf.py` (top-verified by the
   verify script; `make latexpdf` is the ground truth).
4. **Venv only**: never `pip install --break-system-packages`. Use `.venv` (Python 3.12).
5. **Lab naming**: real lab = `192.168.121.101–104`, groups `uk_site`/`usa_site`/`iol`,
   four routers `R1`–`R4`. Do not use `192.168.31.x` or `euro_group`/`usa_group`
   (legacy debt in chapters 04–06 — leave it, don't copy it). Match the lab, not the video.

## Phase 0 — Discover context

- Read `CLAUDE.md`, `README.md` (chapter workflow + LaTeX glyph rule), `docs/source/index.md`
  toctree, the previous chapter's full content (tone/format) and its **"What's Next?"** hook
  — the hook defines this chapter's job.
- Determine the next chapter number and directory name (`NN_topic`).

**Exit:** chapter number, topic, and the promise from the previous chapter are stated.

## Phase 1 — Analyze the source video

Use the **`watch`** skill. Resolve the skill directory first — it exists in `~/.config/opencode/skills/watch` and `~/.claude/skills/watch`, and `$WATCH_SKILL_DIR` is **not** set by the harness:

```bash
WATCH_SKILL_DIR=$(ls -d ~/.config/opencode/skills/watch ~/.claude/skills/watch 2>/dev/null | head -1)
python3 "${WATCH_SKILL_DIR}/scripts/watch.py" "<video-or-url>" \
  --question "Extract everything needed to write a book chapter: topics in order, key concepts, all YAML/Python examples, diagrams/demos, stated rules."
```

- **Frames require a vision-capable model.** If the current model cannot read images, stop and
  ask the user to switch models — transcript-only evidence cannot establish visual facts
  (exact YAML values, code, output) and chapter content must be exact.
- Read **every** frame. Re-read code-critical frames individually to nail exact text.
- Reconcile transcript vs visuals; catalog exact snippets with source timestamps.

**Exit:** a verified list of the exact YAML, Python, error messages, and output the video shows.

## Phase 2 — Ground in the lab

Use the **`netlab`** skill. Do not trust the video's addresses/values — trust the repo:

```bash
cd netlab-lab && netlab status   # is it up? which provider? what IPs?
```

- Read `netlab-lab/topology.yml` (+ `clab.yml`), `nornir-automation/inventory/{hosts,groups,defaults}.yaml`,
  `nornir-automation/config.yaml`, and the runbook dirs.
- **Find the conflict/example already living in the inventory** — a chapter should explain
  real output, not invented numbers. Check whether an earlier chapter already published that
  output. Note `07_data/data.md` _runs_ `02_ntp_config_cmd.py` and shows its `changed : True`
  result, but the 3-way `ntp_server` resolution itself is first explained in ch08 — do not
  point readers at a resolution table in `07_data`.
- Decide lab state implications: which examples need `netlab up` vs none (e.g. `KeyError`
  needs no devices; connection errors do).

**Exit:** a table mapping real inventory → resolved values, and whether the lab must be up.

## Phase 3 — Outline + approval (gate)

- Write the outline to a plan file named `<chapter>-outline.md` and state its path in
  chat. Default shared location: `~/.opencode/plan/` (writable from any CLI); if the host
  agent has a native plan-file convention, use that instead and report where it went.
  Outline contents: main argument, files to create/edit (incl. the one toctree line),
  4–6 sections with `(anchor)=` labels, verbatim examples, skipped candidates,
  verification pyramid.
- Present it in chat. **Gate: user approves before any chapter file is written.**

## Phase 4 — Write

- Create `docs/source/NN_topic/index.md` (title, one-paragraph abstract, `{toctree}`
  with `:maxdepth: 2` listing the content file) + the content file, matching the voice of
  chapters 04–07 (tables, `>` callouts, runnable snippets, closing "What's Next?").
- Add the toctree line to `docs/source/index.md`.
- Keep runs reproducible from the book repo alone. The lab is a separate, unversioned
  folder (`netlab-lab/`) that readers recreate from the published topology — state that
  assumption if a chapter depends on it. No lab/inventory/runbook edits unless approved.

## Phase 5 — Verify (mechanical gate)

```bash
cd advance-network-automation && ./verify-book.sh docs/source/NN_topic
```

The script builds HTML + PDF, scans warnings/LaTeX errors, and greps for camera wording,
stale lab refs, and literal `{#`. **Gate: all gates green** before committing. If a gate
fails, fix and rerun; use the script's output as the fix list.

## Phase 6 — Prove it on the lab

If the chapter makes any device-touching claim (config push, show command):

```bash
cd ~/Projects/netlab-lab && netlab up && netlab status        # 4x iol Up
cd ~/Projects/nornir-automation && python scrapli-runbooks/02_ntp_config_cmd.py   # push
python scrapli-runbooks/03_ntp_show_cmd.py                                        # read back
```

Use absolute paths here — Phases 0–5 leave the agent's cwd inside `advance-network-automation`,
so a `../` hop from `netlab-lab` would resolve into the wrong directory.

- The chapter's published output must match a real run. If numbers differ, fix the chapter.
- Tear down when the user is done: `netlab down --cleanup`. It removes every file netlab
  generated (`clab.yml`, `ansible.cfg`, `hosts.yml`, `group_vars/`, `host_vars/`, `node_files/`,
  `netlab.snapshot.pickle`) while leaving the published `topology.yml` in place. Plain
  `netlab down` leaves those artifacts behind.

## Phase 7 — Commit + report

- Follow workspace `CLAUDE.md` git rules: commit on a feature branch (never `main`) and
  **ask the user before committing** — never commit unsolicited.
- Atomic commits per repo convention: `feat(docs): add chapter on <topic>`,
  `fix(docs): <what>` for any build/config fix.
- Report: files created/edited, gates passed, live-test evidence, lab state, skipped/flagged
  items (e.g. legacy chapter inconsistencies — flag, don't touch).

## Final report template

```
Chapter N — <topic>
- Files: ... created/edited (incl. toctree line)
- Source: <name> (author context only — never quote it in chapter prose)
- Lab grounding: <what was verified on the wire>
- verify-book.sh: N/N gates passed
- Commits: ...
- Lab state: <up/down>
- Flagged (out of scope): ...
```
