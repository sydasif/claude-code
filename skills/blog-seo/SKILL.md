---
name: blog-seo
description: A quality loop for finished articles. Watches a /finished folder, scores each article 0-100 against SEO, AEO, and tone rules, then rewrites the weakest sections and rescores until the article reaches 85. Runs standalone or as a morning routine. Rules live in a separate rules.md so the owner can adjust weights and thresholds without touching the loop. Trigger on "seo aeo loop", "quality loop", "score my finished articles", "run the article loop", "/seo-aeo-loop".
---

# SEO/AEO Loop

An automation scores once and stops. This loop has a goal. Score 85. Below 85, it rewrites the weakest sections and scores again, on its own, until the article passes or the round cap hits.

## Folder contract

```bash
/finished    → articles waiting for the loop (drop .md or .txt here)
/optimized   → articles that passed 85, with metadata block on top
/reports     → one scorecard per article per run
loop-log.md  → memory file: what ran, rounds used, before/after scores
rules.md     → the scoring rules (created on first run, owner-editable)
```

If the folders do not exist, create them. If `rules.md` exists, ALWAYS load rules from it instead of the defaults below. The owner's edits win.

## Step 0 — What the loop needs

For each article in /finished:
1. **Target keyword.** Look for a `keyword:` line at the top of the file. If missing, extract the strongest candidate from the title and intro, and log the choice in the report.
2. **Tone reference.** If the folder contains a `voice.md` or `tone.md`, load it. The rewrite must survive in that voice. No tone file, then the rule is simpler, preserve the article's existing voice.

Never pause to interview the user. The loop runs unattended. Log assumptions, do not ask.

## Step 1 — Score (0-100)

Three blocks, one number.

### SEO block, 50 points

| Check | Points |
|---|---|
| Keyword in title, first 30 chars, title under 60 chars | 8 |
| Keyword density 1.5-2.5%, natural | 8 |
| Keyword in first 100 words | 6 |
| Keyword or variation in 2-3 H2/H3 headings | 6 |
| Heading hierarchy valid, no skipped levels | 3 |
| Meta description exists, 155-160 chars, keyword inside | 6 |
| URL slug, 3-5 words, keyword-first, no stop words | 3 |
| 3-5 internal links or placeholders with descriptive anchors | 7 |
| Readability, paragraphs under 150 words, grade 6-8 | 3 |

### AEO block, 30 points

AEO is what makes ChatGPT, Perplexity, and Claude quote the article instead of skipping it.

| Check | Points |
|---|---|
| At least 2 H2/H3 headings phrased as the actual questions people ask ("What is X", "How do you Y") | 8 |
| Each question heading followed by a 50-80 word answer capsule that stands alone | 10 |
| No links inside the answer capsules (links break extraction) | 4 |
| One-sentence direct definition of the core topic somewhere in the first screen | 4 |
| Facts and numbers stated in extractable sentences, not buried in narrative | 4 |

### Tone and quality block, 20 points

| Check | Points |
|---|---|
| Voice preserved, no generic "ranking article" paste | 8 |
| No filler added for length, every paragraph earns its place | 6 |
| Claims intact, no invented stats, no softened or removed author claims | 6 |

## Step 2 — Check the goal (this is the loop)

**Goal: total score 85 or higher, AND no single block below 60% of its max** (SEO 30+, AEO 18+, Tone 12+). The floor stops the loop from buying SEO points by wrecking the tone.

- **85+ with floors met →** Step 3. Ship.
- **Below →** rewrite ONLY the weakest failing checks, in order of points lost. Then rescore the whole article. **Round cap: 3.** Log each round's score in loop-log.md.
- **Cap hit below 85 →** move the article to /optimized anyway, but mark the report FAILED-AT-XX with the exact list of what still fails and why the loop could not fix it (e.g. "content length needs author input"). Never fake the score. Never loosen a rule to pass.

### Rewrite rules, never break these

- Fix only what the scorecard flags. Do not touch passing sections.
- Do not add filler for length. Do not add explanations the author did not write.
- Do not change section order or delete author content.
- Tone rules outrank score. If a rewrite gains SEO points but reads generic, revert it and take the lower score.
- Internal links go in as placeholders (`INTERNAL_LINK_1: topic`), never invented URLs.

## Step 3 — Ship

Write to /optimized:
- The final article
- A metadata block on top: SEO title, meta description, URL slug, target keyword

Write to /reports:

```
ARTICLE: [filename]
Keyword: [keyword] (provided / extracted)
Round 1: XX  →  Round 2: XX  →  Final: XX
  SEO XX/50 · AEO XX/30 · Tone XX/20
VERDICT: PASSED / FAILED-AT-XX
Changed: [one line per rewrite]
Still failing: [only if FAILED]
```

Append one line to loop-log.md: date, filename, rounds, before → after.

## The routine

When asked to automate, create a scheduled routine (07:00 daily or the owner's time) that:
1. Lists /finished. Empty folder, log "quiet morning" and stop. Do not invent work.
2. Runs Steps 0-3 on each article, oldest first.
3. Leaves everything in /optimized and /reports before the owner wakes up.

## Hard rules

- rules.md always overrides the defaults in this file. The owner tunes weights, thresholds, and the goal there.
- Never report a score that was not computed. Never pad. Never pass a failing article.
- Round cap 3, no exceptions.
- This skill does not build artifacts or dashboards. It scores, rewrites, rescores, and files the report. Nothing else.
- Do not promise rankings. Structure is checked, SERP positions are not.
