---
type: concept
summary: "Retrieve the relevant documents first and put them in context, rather than trusting what the model memorized."
broader: "[[Semantic Search]]"
related: ["[[Semantic Search]]", "[[Embeddings]]", "[[Knowledge Graph]]"]
---

# RAG

Retrieval-Augmented Generation: instead of relying on what a model memorized, retrieve the relevant documents first and put them in its context. Retrieve → augment the prompt → generate.

## Why it matters to me

Every `/recall` is a small RAG pipeline: [[brain_search]] retrieves chunks, Claude reads them, then answers **with citations to the source notes**. The citation habit is the point — an answer I can trace back to a note is one I can trust and correct.

## Key facts

- **Retrieval quality dominates.** A better model can't rescue bad retrieval; chunking and indexing decide the ceiling.
- **Hybrid beats pure vector.** Combining semantic search with keyword/BM25 scoring consistently outperforms either alone — [[GBrain]] measured +31.4 points P@5 for hybrid + rank fusion over vector-only. This is exactly why `/recall` runs semantic search *and* a keyword grep.
- **Graph RAG** ([[LightRAG]], [[Knowledge Graph]]) adds relationship traversal, answering "how does X connect to Y" instead of just "what mentions X".
- For a small vault, plain reading beats retrieval — [[Nate Herk]]'s warning that semantic search is "often worse than simply reading a full markdown file" is really a warning about premature RAG.

## Related

- [[Every Level of a Claude Second Brain]] — Levels 3 and 4 are RAG variants
