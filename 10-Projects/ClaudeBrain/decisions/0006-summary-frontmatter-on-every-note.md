---
type: adr
summary: "ADR-0006 (accepted): every content note carries a one-line summary stating its claim, enforced by templates and vault_stats rather than by instruction alone."
status: accepted
date: 2026-07-24
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[Progressive Disclosure]]", "[[Graph Schema]]", "[[Agent Guide]]"]
tags:
  - adr
---

# ADR-0006 — Every content note carries a one-line `summary:`

## Context and Problem Statement

An agent deciding whether a note is relevant had only two options: read the filename, or open the note. Filenames are too coarse; opening is expensive and often wasted. At the time of this decision **11 of ~100 notes** carried any description field. This is the vault's tier-1 metadata layer under [[Progressive Disclosure]], and it was almost entirely absent.

## Decision Drivers

- The cost of adding it grows with the note count — it is the one change that gets strictly more expensive to defer.
- A wasted read costs *twice*: the wrong note's tokens plus the right note's afterwards.
- Obsidian Bases reads frontmatter exclusively, so a frontmatter field is usable by the app, by `.base` views, and by scripts with no extra tooling.
- Instructions in `CLAUDE.md` degrade over a long session; a mechanical check does not.

## Considered Options

- **Nothing** — rely on filenames and `_Index.md` entries
- **A `summary:` frontmatter field on every content note**
- **Richer metadata per note** — `description` + `status` + `date` + `tags`, per the obsidian-mind convention

## Decision Outcome

Chosen option: **`summary:` on every content note**, phrased as the note's *claim* rather than its category, and enforced in three places rather than one:

1. All 12 templates ship the field with type-specific guidance in a comment.
2. [[Graph Schema]] documents it as required, and as reserved — it carries no graph edge.
3. `vault_stats.py` reports any content note missing one, and the SessionStart hook surfaces that count.

The status/date fields of the richer option were rejected as redundant: `status` already exists where it means something (projects, ADRs), and git holds the dates.

`Memory.md` is exempt — it is `@`-imported into `CLAUDE.md`, so it is always already in context and never needs a summary to decide whether to open it.

### Consequences

- Good, because `grep -h '^summary:' -r 50-Wiki/` now returns the entire wiki's contents for the price of one small read — cheaper than opening three notes, and enough to choose correctly.
- Good, because summaries are also what `.base` dashboards display, so the same field serves the human view.
- Bad, because a summary can drift from the note it describes — a new [[Documentation Rot]] surface. Mitigated by keeping it to one sentence, which is cheap to re-read when editing the body.
- Bad, because "state the claim, not the category" is a judgment call a checker cannot verify. `vault_stats.py` can only confirm the field is non-empty; quality stays a review matter.

### Confirmation

`python3 90-System/Scripts/vault_stats.py` prints a **"Missing `summary:`"** section. Zero is the passing state, and the SessionStart brief reports it every session.

## Pros and Cons of the Options

### Do nothing

- Good, because no migration and no new rule to hold.
- Bad, because it forces a full read to answer "is this the right note?" — the exact cost [[Progressive Disclosure]] exists to remove.

### Richer per-note metadata

- Good, because it supports more `.base` view types out of the box.
- Bad, because fields nothing reads are fields that silently rot, and every extra required field is another way for an agent to produce a malformed note.

## More Information

The measurement that prompted this (11/100 coverage) came from research into keeping agent context small over a large vault; the reasoning is written up in [[Progressive Disclosure]]. Same-session backfill covered 57 notes, bringing coverage to 100%.
