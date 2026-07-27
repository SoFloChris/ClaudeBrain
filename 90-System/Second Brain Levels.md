---
summary: "The five-level maturity model this vault follows, whose point is to stop at the simplest level that solves the actual need."
---

# Second Brain Levels

The 5-level maturity model this vault follows, from [[Every Level of a Claude Second Brain]] by [[Nate Herk]]. The goal is **not** to reach Level 5 — it's the simplest architecture that solves the actual need. Notably, Nate himself stops at Level 4, and his own framing: "complexity climbs as you go up, not cost — most people land at 1–3."

Each level answers one question: L1 "find it by exact word/name" · L2 "pull everything on a topic together" · L3 "I searched different words than I wrote" · L4 "trace relationship chains across a cast" · L5 "consolidate on its own while I'm away".

## Level 1 — The Router ✅

`CLAUDE.md` acts as system prompt and router: who I am, how I work, where files live. Claude knows exactly where to look, and exact word/filename matching handles most retrieval.

## Level 2 — The Wiki ✅

The [[LLM Wiki]]: `50-Wiki/` holds one page per entity with `_Index.md` maps of content, `90-System/Memory.md` auto-loads into every session via CLAUDE.md's `@import`, and `/remember` + `/process-inbox` keep both fed. Claude Code's built-in `/memory` command edits the memory layer directly.

## Level 3 — Semantic Search ✅

Search by meaning via `90-System/Scripts/brain_search.py` (`/recall`): local sentence-transformers embeddings, heading-based chunks, incremental per-machine index. **Used surgically, per Nate's own caveat** — semantic search is often worse than just reading a full markdown file; it earns its keep on big piles (transcripts, reference dumps), while grep and wikilinks stay primary for a tidy vault. See [[Semantic Search]].

## Level 4 — Knowledge Graphs ✅

Typed relationships in frontmatter (`works_at: "[[Acme]]"` — vocabulary in `90-System/Graph Schema.md`) compiled by `90-System/Scripts/brain_graph.py` (`/graph`) into a queryable graph with hop-by-hop path tracing. Wikilinks alone aren't a graph — the types are what enable "how is X connected to Y?". See [[Knowledge Graph]].

## Level 5 — The Autonomous Brain ⏸ (deliberately not built)

Always-on syncing, autonomous memory updates, multiple agents sharing one brain. The archetype is [[Garry Tan]]'s GBrain (markdown-in-git → Postgres, auto-typed edges, hybrid search, overnight "dream cycle" maintenance, MCP server).

**Build it only when:** manual capture/processing is genuinely the bottleneck — e.g. multiple always-on agents need shared memory, or the vault grows past what session-based maintenance can keep clean. Until then, Level 4 is the ceiling on purpose.

## Key principles

- **Reverse engineer for recall:** design the file architecture around how you'll ask questions later.
- **Start with the lowest level:** different folders can run at different levels; don't chase complexity without a pain point.
- **Context vs. connections:** store evergreen context; don't fill the brain with noisy transient data.
- **Boring is beautiful:** a clean, well-organized folder of markdown files remains the foundation at every level.
