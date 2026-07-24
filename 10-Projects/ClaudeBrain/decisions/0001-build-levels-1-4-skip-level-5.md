---
type: adr
summary: "ADR-0001 (accepted): build Levels 1-4 and deliberately skip Level 5 automation until a named build-trigger fires."
status: accepted
date: 2026-07-24
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[Second Brain Levels]]", "[[GBrain]]"]
tags:
  - adr
---

# ADR-0001 — Build Levels 1–4 and deliberately skip Level 5

## Context and Problem Statement

[[Every Level of a Claude Second Brain]] defines five levels of second-brain maturity, from a plain router file to an always-on autonomous system. Which level should this vault target? The temptation is to build the most sophisticated thing available; the framework's own advice is the opposite.

## Decision Drivers

- The vault holds ~50 notes, maintained by one person on two machines.
- Level 5 machinery (Postgres sync, overnight maintenance crons, multi-agent state sharing) has real operational cost and can fail silently.
- The source framework's author stops at Level 4 himself.
- Complexity that isn't exercised rots faster than complexity that is.

## Considered Options

- Levels 1–2 only (router + wiki)
- Levels 1–4 (add semantic search and a knowledge graph)
- Levels 1–5 (add always-on autonomy, [[GBrain]]-style)

## Decision Outcome

Chosen option: **Levels 1–4**, because each of those levels answers a question this vault will actually be asked ("find it by name", "pull the topic together", "I searched different words than I wrote", "trace the relationship chain"), while Level 5 answers a question — "consolidate on its own while I'm away" — that only becomes real at a scale this vault is nowhere near.

### Consequences

- Good, because every layer built is a layer used; nothing is speculative scaffolding.
- Good, because Levels 3–4 are ~600 lines of dependency-light Python that a single person can read and repair.
- Bad, because vault maintenance stays manual — orphans, stubs, and stale notes are found only when something looks for them.
- Neutral, because Level 5 remains available later; nothing built here forecloses it.

### Confirmation

`Second Brain Levels.md` records the explicit build-triggers for Level 5. The decision is being followed as long as no always-on process is added to the vault without one of those triggers firing.

## Pros and Cons of the Options

### Levels 1–2 only

- Good, because it's the least machinery to maintain.
- Bad, because relationship questions ("how do I know this person?") have no answer beyond manual link-following.

### Levels 1–5

- Good, because the vault would maintain itself.
- Bad, because [[GBrain]]'s reference instance is ~146,000 pages; the machinery is sized for a problem this vault doesn't have.
- Bad, because always-on background writes are the hardest kind of system to debug when they go wrong.

## More Information

Revisit if: manual capture becomes the bottleneck; multiple always-on agents need shared memory; or the vault passes a few thousand notes and hand-maintenance visibly fails.

## Amendments

<!-- Append only. -->
