---
type: tool
summary: "The heavyweight extraction-based alternative to this vault's authored graph, worth revisiting only past the scale hand-typed relations can cover."
related: ["[[Knowledge Graph]]", "[[RAG]]"]
alternative_to: ["[[brain_graph]]"]
---

# LightRAG

Open-source retrieval system that builds a knowledge graph out of your documents using LLM-driven entity and relationship extraction, then answers questions by traversing it. [[Nate Herk]] uses it to demo Level 4 in [[Every Level of a Claude Second Brain]] — the colorful node-ball on screen is LightRAG's web UI, **not** Obsidian's graph view.

## Key facts

- Extracts entities and typed relations automatically from unstructured documents — no manual tagging required.
- Ships its own storage layer (file-based by default; Neo4j and others optional).
- Combines graph traversal with vector retrieval, so it answers both "what is X" and "how does X connect to Y".

## Why it matters to me

It's the heavyweight alternative to this vault's approach. We chose explicit typed frontmatter + [[brain_graph]] instead: if you write the relationships yourself, you don't need a model to guess them, and the graph stays inspectable in plain markdown. LightRAG becomes worth revisiting only if the vault grows past what hand-typed relationships can cover.

## Related

- [[Knowledge Graph]] — the concept LightRAG implements
