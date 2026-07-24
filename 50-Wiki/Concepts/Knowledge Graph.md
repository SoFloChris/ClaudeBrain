---
type: concept
related: ["[[Second Brain]]", "[[Semantic Search]]"]
---

# Knowledge Graph

Entities (people, companies, concepts) connected by **typed relationships** — not just "these notes link to each other" but *how* they relate: "Jordan *works at* Acme", "Product X *competitor of* Product Y". The payoff is relationship-chain tracing: follow edges hop-by-hop to answer questions no keyword or vector search can.

## Why it matters to me

Level 4 of this vault. Wikilinks alone are **not** a knowledge graph (per [[Nate Herk]]) — they say two notes are related without saying how. This vault adds the "how" via frontmatter properties on wiki notes:

```yaml
type: person
works_at: "[[Acme]]"
knows: ["[[Jordan Lee]]"]
```

`90-System/Scripts/brain_graph.py` compiles those properties (typed edges) plus body wikilinks (untyped "mentions" edges) into a queryable graph — `/graph` answers "how is X connected to Y?" with an actual path.

## Key facts (researched 2026-07)

- The property name **is** the relationship type: `works_at: "[[Acme]]"` → `(note) -[works_at]-> (Acme)`. Link values in YAML must be quoted.
- Obsidian renders frontmatter links in the Properties UI and counts them as real links (graph view, backlinks) — so the same data serves humans and scripts.
- Heavier alternatives if this ever outgrows the script: LightRAG (what Nate demos — LLM-extracted entities/relations), the official `@modelcontextprotocol/server-memory` MCP server (entities/relations/observations knowledge graph Claude can edit), or GBrain's approach (auto-typing wikilink edges via schema packs, zero LLM calls).

## Related

- [[Every Level of a Claude Second Brain]] — Level 4 section
