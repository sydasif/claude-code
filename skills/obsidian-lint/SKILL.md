---
name: obsidian-lint
description: Audit an Obsidian vault (a folder of markdown notes linked with [[wikilinks]]) for consistency problems — contradicting notes, claims that newer notes have superseded, orphan pages with no incoming links, and topics that get referenced but never got their own note. Use this whenever the user mentions their Obsidian vault, a "second brain" / PKM / Zettelkasten setup, wikilinks, backlinks, or asks to lint, audit, clean up, or find problems in a folder of interlinked markdown notes. Produces a single read-only report — never deletes or edits vault content.
---

# Obsidian Vault Lint

Audits a vault of interlinked markdown notes and reports four kinds of problems:
contradictions between notes, claims that a newer note has superseded, orphan
pages nothing links to, and gaps — topics referenced via `[[wikilink]]` that
never got written.

**This skill only reads and reports. It never edits, deletes, or moves any
file in the vault.** The output is a single markdown report the user reviews
and acts on themselves.

## Why this is a two-part job

Two of the four checks are structural — resolving links to files and counting
who points at whom is pure graph traversal, and a script does that faster and
more reliably than reading every note yourself. The other two — contradictions
and superseded claims — require actually understanding what each note _says_,
which is a judgment call a script can't make. Trying to force either half
into the other tool's approach produces worse results: don't try to regex
your way to detecting contradictions, and don't manually eyeball the whole
vault for backlink counts when the script gives you exact ones instantly.

## Step 1: Locate the vault

The vault is a folder of `.md` files, usually with a `.obsidian/` config
folder alongside them (though that folder isn't required for this to work).
Figure out where it lives:

- If the user gave a path directly, use it.
- If they uploaded a `.zip` of the vault, extract it to a working directory first.
- If neither, ask for the path rather than guessing — don't assume a default
  location like `~/Documents/Obsidian`, since vault locations vary a lot and
  guessing wrong wastes a full read-through.

## Step 2: Run the structural analysis

```bash
python3 scripts/vault_graph.py /path/to/vault --out /tmp/graph.json
```

This resolves every `[[wikilink]]` in the vault — both in the note body and
inside a frontmatter `related:` list, if the vault declares relations there
instead of (or as well as) inline — following `#heading` and `|alias` syntax,
and matching against frontmatter `aliases:` and `title:` too, since a note's
filename/slug and its display title are often different. It produces JSON
with, for every note: its tags, a modified date (prefers frontmatter
`last_update`, then `created`, then falls back to file mtime), and who it
links to and from. It also pre-computes:

- **`orphans`** — notes with zero incoming links. This is check 3, done.
- **`gaps`** — link targets that don't resolve to any file, grouped by target
  name with a count and the list of notes that reference them. This is check
  4, done: these are exactly the topics the user references but never developed.
- **`broken_anchors`** — links that resolve to a real note but point at a
  heading that doesn't exist in the target (e.g. `[[note#nonexistent]]` where
  `note` exists but has no `#nonexistent` heading). Matching uses Obsidian's
  own anchor rules: case-insensitive, punctuation stripped before comparison,
  so `[[note#heading!]]` resolves to `## heading?`. Grouped by target with the
  heading text and the notes that reference it.

If the vault has index/MOC (map-of-content) notes that are meant to be entry
points rather than destinations — including a dedicated index file like
`MEMORY.md` that lists one line per note — they'll show up in `orphans` too.
That's correct output, not a bug, but worth calling out separately in the
report since "nothing links to my index" reads differently from "nothing
links to this random note that got orphaned by accident." Look at the note's
content/tags to tell the two apart; don't guess from the filename alone. And
if there's an index file, cross-check it against the note list: a note
missing from the index (or an index line pointing at a note that no longer
exists) is worth a mention even though it's not strictly an orphan or a gap.

Use `--exclude <substring>` (repeatable) to skip folders like `templates/`
or `archive/` that would otherwise pollute the results with intentionally
unlinked scaffolding.

Use `--ignore-dangling <substring>` (repeatable) to suppress gap warnings for
wikilinks that are intentional semantic labels rather than note references
(e.g., `--ignore-dangling "-config"` to skip `[[litellm-proxy-config]]`). The
check is a case-insensitive substring match — any dangling target whose name
contains the pattern is excluded from the gap report. Unlike `--exclude` which
filters source files, this only filters the gap output: the dangling links
still appear in each note's `linked_to`, just not in the gap list.

Use `--` before patterns that start with `-` to prevent argparse from
interpreting them as flags:

```bash
python3 scripts/vault_graph.py /path/to/vault --out /tmp/graph.json \\
    --ignore-dangling "-config" --ignore-dangling "-project"
```

## Step 3: Find contradictions and superseded claims

This is the part that needs you to actually read notes, not just the graph.
Reading the whole vault note-by-note in isolation is a bad way to find
contradictions — you need to compare notes that are _about the same thing_,
and the graph JSON already tells you which notes cluster together: notes
that link to each other, notes that share tags, and notes that link to the
same target are almost always discussing overlapping subject matter.

Work through it like this:

1. **Group candidate notes.** Using the `notes` array from the graph JSON,
   cluster by shared tags first, then by direct links between them (a note
   and everything in its `linked_to`/`linked_from`). A cluster of 2-6 notes
   sharing a topic is the right unit to compare — much better signal than
   comparing two random notes from opposite corners of the vault.

2. **Read the notes in each cluster.** For vaults under ~150 notes, working
   through every cluster is usually feasible. For larger vaults, say so
   explicitly and prioritize: notes with the most incoming links (they're
   load-bearing — a contradiction there affects more of the vault), notes
   that share tags with many others, and notes that were modified recently
   (more likely to have introduced a change that conflicts with an older
   note). Tell the user you're prioritizing rather than silently doing a
   partial job.

3. **Look for contradictions**: two notes making incompatible factual claims
   about the same entity — different values, different statuses, opposite
   conclusions. Quote the specific conflicting lines from each (a short
   phrase, not a full paragraph) and name both files.

4. **Look for superseded claims**: a note that's older (check frontmatter
   `date`/`updated` fields first, fall back to file modified time) whose
   claim is contradicted or explicitly revised by a newer note. Explicit
   language like "supersedes", "deprecated", "see updated version", or a
   `status: outdated` frontmatter field is a strong signal — but also
   flag cases where two notes on the same topic simply disagree and one is
   clearly more recent, even without explicit cross-referencing language.

Don't force a finding where there isn't one — an empty section in the report
is a completely valid outcome and better than a stretched, low-confidence
"contradiction" that's really just two notes covering different aspects of
a topic.

## Step 4: Write the report

Produce one markdown file. Use this structure:

```markdown
# Vault Audit Report

Vault: <path> — <N> notes analyzed

## Summary

- N contradictions found
- N superseded claims found
- N orphan pages
- N undeveloped topics (gaps)
- N broken heading anchors

## Contradictions

### <Topic>

- **[[Note A]]**: "<short quoted claim>"
- **[[Note B]]**: "<short quoted claim>"
- Why these conflict: <one line>

(repeat per contradiction; if none found, say so explicitly)

## Superseded / outdated claims

### <Topic>

- **[[Older Note]]** (modified <date>): "<claim>"
- Superseded by **[[Newer Note]]** (modified <date>): "<newer claim>"

(repeat; if none found, say so explicitly)

## Orphan pages

Pages with no incoming links, grouped by whether they look like intentional
entry points (MOCs/indexes) or likely-accidental orphans:

**Likely accidental:**

- [[Note]] — <path>

**Entry points (expected to have no incoming links):**

- [[Note]] — <path>

## Gaps — referenced but undeveloped

Topics linked from other notes that have no note of their own, sorted by
how often they're referenced:

- **<Topic>** — referenced by N notes: [[Note A]], [[Note B]]

## Broken heading anchors

Links that point at a real note but a heading that doesn't exist in it,
sorted by how many notes reference them:

- **[[Note]]#<heading>** — referenced by N notes: [[Source A]], [[Source B]]

(if none found, say so explicitly)

## Notes on scope

<Only if you had to prioritize/sample for the contradiction pass on a large
vault — say what you covered and what you skipped, so the user knows the
gaps in the gap analysis.>
```

Save it as `vault-audit-report.md`. Present it to the user; don't touch any
file inside the vault itself.
