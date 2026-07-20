#!/usr/bin/env python3
"""
vault_graph.py — structural analysis of an Obsidian vault's wikilink graph.

This does the part of the audit that's mechanical and doesn't need judgment:
resolving every [[wikilink]] to a real file (or not), and counting incoming
links per note. That gives us two of the four report sections for free:

  - orphan pages: zero incoming links
  - gaps: links that point at a note title with no matching file

Contradictions and outdated/superseded claims need to actually read and
compare note content, which is a job for Claude reading this script's JSON
output plus the note files themselves — not something to fake here with
regex. See SKILL.md for that half of the workflow.

Usage:
    python3 vault_graph.py /path/to/vault [--exclude PATTERN ...] [--out graph.json]

Output: JSON written to stdout (or --out path) with structure documented
in the OUTPUT SCHEMA comment below.
"""

import argparse
import json
import re
import sys
from pathlib import Path

WIKILINK_RE = re.compile(
    r"\[\[([^\]|#]+?)(?:#([^\]|]+?))?(?:\|[^\]]+)?\]\]"
)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)
FM_LIST_LINE_RE = re.compile(r"^\s*-\s*(.+?)\s*$")


def parse_frontmatter(text: str) -> dict:
    """Very small YAML-subset parser — just enough for aliases/tags/dates/related.
    Not a full YAML implementation on purpose: vault frontmatter is simple
    key: value / key: [list] / key:\\n  - item content, and pulling in a
    real YAML library isn't worth the dependency for this.

    Only zero-indented lines are treated as top-level keys. This matters for
    schemas that nest a sub-block under a key (e.g. a `metadata:` block with
    its own `type:`, `node_type:` etc underneath it) — those indented lines
    are deliberately skipped rather than misread as top-level fields that
    would collide with or shadow the real ones."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict = {}
    lines = m.group(1).splitlines()
    current_key = None
    for line in lines:
        if not line.strip():
            continue
        indented = line[0] in " \t"
        list_item = FM_LIST_LINE_RE.match(line)
        if list_item and indented and current_key:
            fm.setdefault(current_key, [])
            if isinstance(fm[current_key], list):
                fm[current_key].append(list_item.group(1).strip("'\""))
            continue
        if indented:
            continue  # nested sub-field of some other key's block — skip
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            current_key = key
            if val == "" or val == "[]":
                fm[key] = [] if val == "[]" else fm.get(key, "")
            elif val.startswith("[") and val.endswith("]"):
                fm[key] = [v.strip(" '\"") for v in val[1:-1].split(",") if v.strip()]
            else:
                fm[key] = val.strip("'\"")
    return fm


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline backticks so wikilink-looking
    text inside code doesn't get parsed as a real link."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    return text


def extract_headings(text: str) -> set[str]:
    """Extract all markdown headings from a note, normalized to lowercase.
    Strips punctuation (non-alphanumeric, non-space characters) from both
    headings and link targets, matching Obsidian's actual anchor resolution
    behavior where [[note#heading?]] resolves to ## heading! because
    punctuation is stripped before comparison."""
    headings: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                headings.add(_normalize_anchor(heading))
    return headings


def _normalize_anchor(text: str) -> str:
    """Strip punctuation and collapse whitespace, matching Obsidian's
    heading anchor resolution. Obsidian strips non-alphanumeric characters
    (keeping letters, digits, spaces) and lowercases before comparing."""
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split()).lower()


def normalize(title: str) -> str:
    return title.strip().lower()


def build_graph(vault_root: Path, exclude_patterns: list[str]):
    md_files = [
        p for p in vault_root.rglob("*.md")
        if not any(part.startswith(".") for part in p.relative_to(vault_root).parts)
    ]

    if exclude_patterns:
        md_files = [
            p for p in md_files
            if not any(pat.lower() in str(p.relative_to(vault_root)).lower() for pat in exclude_patterns)
        ]

    notes = {}          # relative path -> record
    title_lookup = {}    # normalized title/alias -> relative path (canonical key)

    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        title = path.stem
        norm = normalize(title)
        rel = str(path.relative_to(vault_root))
        aliases = fm.get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]

        display_title = fm.get("title") or title

        notes[rel] = {
            "title": display_title,
            "slug": title,
            "path": rel,
            "frontmatter": fm,
            "modified": fm.get("last_update") or fm.get("created") or path.stat().st_mtime,
            "headings": extract_headings(text),
            "outgoing": [],   # filled below
            "incoming": [],   # filled below
        }
        # Key lookups by path so duplicate slugs (e.g. many MEMORY.md index
        # files in different project dirs) don't collide and silently drop
        # notes from the graph.
        title_lookup[norm] = rel
        for alias in aliases:
            title_lookup[normalize(alias)] = rel
        # A note can be referenced either by its filename/slug or by its
        # frontmatter `title:` (they're often different — e.g. slug
        # "db-retries" vs title "DB Retry Strategy"). Register both so a
        # [[wikilink]] using either form resolves.
        if fm.get("title"):
            title_lookup[normalize(fm["title"])] = rel

    dangling = {}  # normalized target text -> {"display": str, "referenced_by": [note paths]}
    # links to a real note but a non-existent heading -> broken anchor
    broken_anchors = {}  # normalized target -> {"display", "heading", "referenced_by"}

    for src_key, rec in notes.items():
        path = vault_root / rec["path"]
        text = path.read_text(encoding="utf-8", errors="replace")
        body = strip_code(text)
        matches = list(WIKILINK_RE.finditer(body))

        # related: ["[[other-slug]]", ...] declares links in frontmatter
        # rather than (or in addition to) the body. Each list item is a
        # wikilink-shaped string, so run the same regex over it.
        related = rec["frontmatter"].get("related", [])
        if isinstance(related, str):
            related = [related]
        for item in related:
            matches.extend(WIKILINK_RE.finditer(item))

        seen_targets = set()
        for m in matches:
            raw_target = m.group(1)
            raw_heading = m.group(2)
            target_norm = normalize(raw_target)
            link_key = (target_norm, normalize(raw_heading) if raw_heading else None)
            if link_key in seen_targets:
                continue
            seen_targets.add(link_key)
            resolved = title_lookup.get(target_norm)
            if resolved and resolved in notes:
                rec["outgoing"].append(notes[resolved]["title"])
                notes[resolved]["incoming"].append(rec["title"])
                if raw_heading and _normalize_anchor(raw_heading) not in notes[resolved]["headings"]:
                    entry = broken_anchors.setdefault(target_norm, {
                        "display": raw_target.strip(),
                        "heading": raw_heading.strip(),
                        "referenced_by": [],
                    })
                    entry["referenced_by"].append(rec["path"])
            else:
                entry = dangling.setdefault(target_norm, {"display": raw_target.strip(), "referenced_by": []})
                entry["referenced_by"].append(rec["path"])

    orphans = [
        {"title": rec["title"], "path": rec["path"]}
        for rec in notes.values()
        if len(rec["incoming"]) == 0
    ]
    orphans.sort(key=lambda r: r["path"])

    gaps = [
        {
            "referenced_as": v["display"],
            "reference_count": len(v["referenced_by"]),
            "referenced_by": sorted(v["referenced_by"]),
        }
        for v in dangling.values()
    ]
    gaps.sort(key=lambda g: -g["reference_count"])

    broken_anchors = [
        {
            "referenced_as": v["display"],
            "heading": v["heading"],
            "reference_count": len(v["referenced_by"]),
            "referenced_by": sorted(v["referenced_by"]),
        }
        for v in broken_anchors.values()
    ]
    broken_anchors.sort(key=lambda a: (a["referenced_as"], a["heading"]))

    notes_out = [
        {
            "title": rec["title"],
            "path": rec["path"],
            "tags": rec["frontmatter"].get("tags", []),
            "modified": rec["modified"],
            "outgoing_count": len(rec["outgoing"]),
            "incoming_count": len(rec["incoming"]),
            "linked_to": sorted(set(rec["outgoing"])),
            "linked_from": sorted(set(rec["incoming"])),
        }
        for rec in notes.values()
    ]
    notes_out.sort(key=lambda n: n["path"])

    return {
        "vault_root": str(vault_root),
        "note_count": len(notes),
        "orphans": orphans,
        "gaps": gaps,
        "broken_anchors": broken_anchors,
        "notes": notes_out,
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze an Obsidian vault's wikilink graph.")
    parser.add_argument("vault_path", help="Path to the vault root (folder containing .md files)")
    parser.add_argument("--exclude", action="append", default=[],
                         help="Path substring to exclude (e.g. templates, archive). Repeatable.")
    parser.add_argument("--out", default=None, help="Write JSON here instead of stdout")
    args = parser.parse_args()

    vault_root = Path(args.vault_path).expanduser().resolve()
    if not vault_root.is_dir():
        print(f"error: {vault_root} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = build_graph(vault_root, args.exclude)
    output = json.dumps(result, indent=2)

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"wrote {args.out} ({result['note_count']} notes, "
              f"{len(result['orphans'])} orphans, {len(result['gaps'])} gaps, "
              f"{len(result['broken_anchors'])} broken anchors)", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
