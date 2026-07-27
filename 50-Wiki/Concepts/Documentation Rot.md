---
type: concept
summary: "Incorrect documentation is worse than missing documentation: missing docs send you elsewhere, wrong docs make you act confidently on a lie."
aliases: [doc rot, documentation decay]
related: ["[[Architecture Decision Record]]", "[[Diataxis]]", "[[Context vs Connections]]"]
tags:
  - concept
---

# Documentation Rot

Notes decay as the thing they describe moves on. The sharpest statement of the stakes, from Write the Docs: **incorrect documentation is worse than missing documentation** — missing docs make you look elsewhere, wrong docs make you act confidently on a lie.

## The named failure modes

Google's own account of GooWiki, their abandoned internal wiki, is the canonical case study. At one point it held **7 to 10 documents on setting up Borg**, most unmaintained. The causes they identified:

1. **No owner.** "Documents without owners become stale and difficult to maintain."
2. **Duplication with no canonical source.** The same fact in three places; two get updated.
3. **Flat namespace.** No hierarchy, so nobody could tell which document was authoritative.
4. **Documents serving more than one purpose** — links, concepts, and API reference in one page. "Such documents fail because they don't serve a single purpose." (This is [[Diataxis]] mode-mixing, arrived at independently.)
5. **Undated claims.** "We use SQLite" is unfalsifiable; "(2026-07-24) we use SQLite" tells a reader in 2028 exactly how much to trust it.

## What transfers to a personal vault

Team practices don't all port — I'm the only owner, so ownership metadata is dead weight. What does transfer:

| Team practice | Personal-vault version |
|---|---|
| Canonical doc per topic | **One note per concept**, not per book/project/meeting |
| Freshness dates + nag | `last_reviewed` in frontmatter + a Bases query for stale notes |
| Docs in the same PR as the code | Update the note in the same session you learn the thing |
| Link, don't duplicate | Wikilinks; link to a stub rather than restating |
| Deprecate, don't delete | Archive with a pointer to the successor |
| Scheduled review | **Backlink-driven re-reading** — see below |

## The mechanism that actually works here

Andy Matuschak's insight: **finding the right links requires reading old notes**, so dense linking is itself an organic review cycle — "evergreen note maintenance approximates spaced repetition." A vault that's genuinely linked gets re-read as a side effect of being extended. That's why the linking discipline in `CLAUDE.md` is a *maintenance* rule, not a tidiness rule.

The complementary defense: **prefer immutable records over living prose.** [[Architecture Decision Record]]s and changelog entries don't rot because they never claimed to be current. Keep the "current state" documents short and mostly links — they're the only part that needs upkeep.

## Related

- [[Context vs Connections]] — the intake filter; rot starts with hoarding
