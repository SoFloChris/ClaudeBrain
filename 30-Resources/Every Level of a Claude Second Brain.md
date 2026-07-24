---
type: resource
source: "https://www.youtube.com/watch?v=DTCyvo6cC54"
author: "[[Nate Herk]]"
topic: "[[Second Brain]]"
---

# Every Level of a Claude Second Brain

**Source:** YouTube, Nate Herk | AI Automation, published 2026-06-17. This vault is built on this video's model — his demo vault is called "Herk2".

## Summary (in my own words)

Five levels of AI second brain, from a simple markdown router to an always-on autonomous system. The central advice is anti-hype: pick the **lowest** level that solves your actual pain, and different folders of the same vault can run at different levels.

## The 5 levels

1. **Router** — one `CLAUDE.md` auto-loads as system prompt + routing layer over a clean folder tree. Retrieval is exact word/filename matching.
2. **The Wiki** — an "[[LLM Wiki]]" (inspired by Andrej Karpathy): raw material (transcripts, meetings, research) gets processed into interconnected concept pages. The router now points to three things: the wiki, references, and a memory file kept fresh by Claude Code's `/memory` auto-memory.
3. **[[Semantic Search]]** — chunk → embed → vector store (he names Pinecone and Supabase Vector). His demo: keyword search for "feedback" finds only that word; semantic search also surfaces "live test results" and "evaluations". **His caveat: semantic search is often worse than just reading a full markdown file — apply it surgically** (big transcript piles, rules databases), not everywhere.
4. **[[Knowledge Graph]]s** — wikilinks alone are NOT a knowledge graph; you need **typed relationships** ("Jordan *works at* Acme") so you can trace relationship chains hop-by-hop. He demos with LightRAG (open-source, LLM-extracted entities/relations).
5. **Autonomous Brain** — continuously syncing, self-updating, multi-agent. The archetype is **GBrain** by [[Garry Tan]]: markdown in git synced to Postgres, wikilinks auto-typed into edges, hybrid search (pgvector + BM25 + rank fusion), an overnight "dream cycle" cron that dedupes and fixes the vault, and an MCP server for always-on agents. **Nate himself does not run Level 5** — the overhead isn't justified by his workflow.

## Key takeaways

- Reverse engineer for recall: design the file architecture around how you'll ask questions later.
- Context vs. connections: store evergreen context; don't fill the brain with noisy transient data.
- Boring is beautiful: a clean folder of markdown stays the foundation at every level.
- Only move up a level when you hit a concrete pain the current level can't solve.

## How this vault implements it

- Levels 1–2: `CLAUDE.md` router + `50-Wiki/` + auto-loaded `90-System/Memory.md` + `/remember` & `/process-inbox`
- Level 3: `90-System/Scripts/brain_search.py` (local embeddings) + `/recall` — used surgically, per his advice
- Level 4: typed frontmatter relations + `90-System/Scripts/brain_graph.py` + `/graph`
- Level 5: deliberately not built. See [[90-System/Second Brain Levels]] for the trigger conditions.

## Related

- Earlier companion video (the Herk2 build): "I Turned Claude Into the Ultimate Second Brain" — youtube.com/watch?v=8QQ_INxAhRs
- GBrain: github.com/garrytan/gbrain · GStack: github.com/garrytan/gstack
