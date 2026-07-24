---
type: concept
broader: "[[Second Brain]]"
related: ["[[Second Brain]]", "[[Knowledge Graph]]"]
---

# Semantic Search

Search by meaning instead of exact keywords: text is chunked, converted to embedding vectors, and queries return the nearest neighbors by cosine similarity — so "feedback" can surface notes about "evaluations" and "test results" that never use the word.

## Why it matters to me

Level 3 of this vault. Implemented locally and privately in `90-System/Scripts/brain_search.py` (sentence-transformers + `bge-small-en-v1.5`, heading-based ~400-token chunks, incremental numpy index), used via `/recall`.

## Key facts (researched 2026-07)

- **Use it surgically.** Per [[Nate Herk]]: semantic search "is not magic, and is often worse than simply reading a full markdown file." It earns its keep on large piles (transcripts, reference dumps) — not on a small tidy vault.
- **Local model options:** `bge-small-en-v1.5` (tiny, ungated — this vault's default), `nomic-embed-text` (Ollama classic), `google/embeddinggemma-300m` (best small model on MTEB as of 2025-09, but license-gated on Hugging Face), `Qwen3-Embedding-0.6B` (strongest small, heavier).
- **Hosted options:** Anthropic has no first-party embeddings API — they officially point to Voyage AI (Voyage 4 family, Jan 2026; `voyage-4-lite` ≈ $0.02/M tokens). OpenAI `text-embedding-3-small` is $0.02/M.
- **In Obsidian without code:** the Smart Connections plugin (v4) embeds locally by default with zero config — note it moved from open source to a source-available license in the v3→v4 transition. Omnisearch is great but keyword-only (BM25, no vectors).
- **Storage at this scale:** a few thousand chunks fits comfortably in a plain numpy matrix — brute-force cosine is milliseconds; vector databases (sqlite-vec, LanceDB, Chroma, Pinecone, Supabase Vector) only pay off much larger.

## Related

- [[Every Level of a Claude Second Brain]] — Level 3 section
