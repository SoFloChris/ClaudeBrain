---
type: tool
related: ["[[Semantic Search]]"]
alternative_to: ["[[brain_search]]"]
uses: ["[[Embeddings]]", "[[Obsidian]]"]
---

# Smart Connections

The main Obsidian community plugin for [[Semantic Search]] — the no-code alternative to this vault's [[brain_search]] script.

## Key facts

- **Local by default**: embeds notes on your machine with `TaylorAI/bge-micro-v2` (384-dim) via transformers.js. No API key, no setup, nothing leaves the machine. Can point at Ollama (e.g. `nomic-embed-text`) for better quality.
- Surfaces a "related notes" pane plus semantic search; **v4** slimmed the free core (chat split into a separate Smart Chat plugin, advanced features moved to paid tiers).
- **Licensing caveat**: the v3→v4 transition changed the license from open source to a source-available "Smart Plugins License" with a non-compete clause, without prior announcement — it caused community backlash. It still works and still stays local; it's just no longer open source.
- Pairs well with **Omnisearch**, which is keyword-only (MiniSearch/BM25, no embeddings) — the two complement rather than compete.

## Why it matters to me

The zero-effort path to Level 3 inside Obsidian. Our `/recall` script covers the same ground with full control and no license questions, but Smart Connections is worth installing if I want related-note suggestions while writing.

## Related

- [[Local Embedding Models]] — what to run under the hood
