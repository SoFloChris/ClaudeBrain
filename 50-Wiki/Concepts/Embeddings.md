---
type: concept
broader: "[[Semantic Search]]"
related: ["[[Semantic Search]]", "[[RAG]]"]
---

# Embeddings

Text converted into a vector of numbers, positioned so that similar *meanings* land near each other in space. Compare two vectors with cosine similarity and you get "how related are these?" without either text sharing a single word.

## Why it matters to me

The engine under [[Semantic Search]] and therefore under `/recall`. Practical facts worth remembering:

- **Dimensions** are the vector length (384, 768, 1024…). More isn't automatically better; it costs storage and compute.
- **Matryoshka models** (EmbeddingGemma, Voyage 4, OpenAI v3) can be truncated to fewer dimensions with graceful quality loss — a free speed knob.
- **Normalize, then dot product** = cosine similarity. That's the whole search step; the rest is bookkeeping.
- **Query prefixes matter** for some models: BGE models expect queries prefixed with "Represent this sentence for searching relevant passages:" — [[brain_search]] does this automatically.
- **Chunking beats model choice** for note search. Splitting on headings at ~400 tokens matters more than which small model you pick.
- [[Anthropic]] ships no embedding model; they point to [[Voyage AI]].

## Related

- [[Local Embedding Models]] — the specific models and how they compare
