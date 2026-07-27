---
type: adr
summary: "ADR-0007 (accepted): every content note carries a one-line summary stating its claim, enforced by a failing build rather than by instruction."
status: accepted
date: 2026-07-27
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[Progressive Disclosure]]", "[[Graph Schema]]", "[[Documentation Rot]]"]
tags:
  - adr
---

# ADR-0007 — Every content note carries a one-line `summary:`

Adapted from an ADR of the same name written 2026-07-24 on `claude/obsidian-second-brain-setup-0c0jdy` and never merged. The reasoning below is that author's; the enforcement mechanism is changed to match ADR-0006, and the numbers are restated against the vault as it actually is.

## Context and Problem Statement

An agent deciding whether a note is relevant has two options: read the filename, or open the note. Filenames are too coarse. Opening is expensive, and a wasted read costs **twice** — the wrong note's tokens, then the right note's afterwards.

When this was first written, 11 of ~100 notes carried any description field. When it was actually applied, **26 of 86 content notes** had one, all of them arriving in the same salvage that surfaced this decision. Everything written before that had nothing.

## Decision Drivers

- **The cost of adding it grows with the note count.** This is the one change that gets strictly more expensive to defer, and deferring it three days took it from 57 notes to 60.
- Obsidian Bases reads frontmatter exclusively, so one field serves the app, `.base` views, and scripts with no extra tooling.
- `grep -h '^summary:' -r 50-Wiki/` returns the entire wiki's contents for the price of one small read.
- Instructions in `CLAUDE.md` degrade over a long session; a mechanical check does not (ADR-0004).

## Considered Options

- **Nothing** — rely on filenames and `_Index.md` entries
- **A `summary:` field on every content note**
- **Richer metadata per note** — `description` + `status` + `date` + `tags` together

## Decision Outcome

Chosen option: **`summary:` on every content note**, phrased as the note's *claim* rather than its category, enforced in three places:

1. All 12 templates with frontmatter ship the field with type-specific guidance in a comment.
2. [[Graph Schema]] documents it as required and as reserved — it carries no edge.
3. `check_frontmatter.py` fails the build if a content note lacks one, or if what it has is too short to be a claim.

**Where this departs from the original:** that version enforced via `vault_stats.py --check` and the SessionStart brief. ADR-0006 keeps the reporting tool report-only, so the gate lives in the enforcing script instead. Same rule, different home.

The richer-metadata option was rejected as redundant: `status` already exists where it means something, and git holds the dates.

**Exempt:** structural files (`_Index`, `Home`, `README`, `SETUP`, `CLAUDE`); `Memory.md`, which is `@`-imported into `CLAUDE.md` and therefore always already in context; and daily notes, which are transient scratch logs with no single claim to state.

### Consequences

- Good, because choosing between sixty notes now costs one grep instead of sixty reads.
- Good, because the same field feeds `.base` dashboards, so the human view improves for free.
- Bad, because a summary can drift from the note it describes — a fresh [[Documentation Rot]] surface. Mitigated by keeping it to one sentence, cheap to re-read when editing the body.
- Bad, because **"state the claim, not the category" is a judgment a checker cannot make.** The build can only confirm the field exists and is long enough to be a sentence; whether it says anything true stays a review matter. A vault full of `summary: "A note about X"` would pass every check and deliver none of the benefit.
- Bad, because it is one more required field, and every required field is another way for an agent to produce a malformed note.

### Confirmation

`python3 90-System/Scripts/check_frontmatter.py` exits non-zero if any content note lacks a summary or carries one under 20 characters, and `.github/workflows/vault-check.yml` runs it on every pull request. Verified by deleting a summary and by replacing one with `"About RAG."` — both fail the build.

## Pros and Cons of the Options

### Do nothing

- Good, because no migration and no new rule to hold.
- Bad, because it forces a full read to answer "is this the right note?" — the exact cost [[Progressive Disclosure]] exists to remove.

### Richer per-note metadata

- Good, because it supports more `.base` view types out of the box.
- Bad, because fields nothing reads are fields that silently rot.

## More Information

The measurement that prompted the original (11/100 coverage) came from research into keeping agent context small over a large vault; the reasoning is in [[Progressive Disclosure]]. This application backfilled 60 notes, bringing coverage to 100% of content notes.

Falsified if summaries drift badly enough to mislead — at which point the answer is a staleness check, not abandoning the field.

## Amendments

<!-- Append only. -->
