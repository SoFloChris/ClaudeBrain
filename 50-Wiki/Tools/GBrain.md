---
type: tool
built_by: "[[Garry Tan]]"
related: ["[[Second Brain]]", "[[Knowledge Graph]]"]
uses: ["[[Embeddings]]"]
---

# GBrain

[[Garry Tan]]'s open-source "agent brain" (MIT, ~April 2026) — the archetypal **Level 5** autonomous second brain referenced in [[Every Level of a Claude Second Brain]].

## Key facts

- **Markdown in a git repo is the system of record**, synced into Postgres (local zero-config PGLite up to ~50K pages; Supabase/Postgres for teams).
- **Auto-linking with zero LLM calls**: `[[wikilink]]` syntax is converted into typed edges (`attended`, `works_at`, `invested_in`, `founded`, `advises`, `mentions`) via schema packs defining ~15 page types. Same core idea as our [[Graph Schema]], but automated at write time.
- **Hybrid retrieval**: pgvector HNSW embeddings + BM25 + reciprocal-rank fusion, benchmarked +31.4 points P@5 over vector-only [[RAG]].
- **The "dream cycle"**: an overnight cron that dedupes person pages, fixes citations, scores salience, and finds contradictions — the vault maintaining *itself*.
- MCP server with 30+ tools; a 43-skill pack for always-on agents. Garry's own instance: ~146K pages, 24K people, 5K companies.
- Companion project **GStack** is the slash-command skill pack whose agents share GBrain as memory.

## Why it matters to me

It's the reference design for where this vault would go at Level 5 — and the honest benchmark for how much scale justifies that complexity (146K pages, not 40). Two ideas are worth stealing early: **auto-typed edges at write time** and **a maintenance pass that runs without me**.

## Related

- [[Second Brain Levels]] — Level 5 and its build-triggers
