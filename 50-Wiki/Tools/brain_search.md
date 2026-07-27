---
type: tool
summary: "This vault's semantic search engine - local, free, and inspectable, built in-house rather than bought."
related: ["[[Semantic Search]]", "[[Embeddings]]"]
uses: ["[[Local Embedding Models]]"]
alternative_to: ["[[Smart Connections]]"]
---

# brain_search

This vault's [[Semantic Search]] engine — `90-System/Scripts/brain_search.py`, invoked by `/recall`. Level 3, built in-house so it stays local, free, and inspectable.

## How it works

1. **Chunking**: splits each note on headings, sub-splits long sections at ~1600 chars (~400 tokens, where retrieval precision peaks), and prefixes every chunk with `Note title > Heading` for context.
2. **Embedding**: `sentence-transformers` with `BAAI/bge-small-en-v1.5` by default (small, ungated). Override with the `BRAIN_EMBED_MODEL` env var.
3. **Storage**: a plain numpy matrix — at a few thousand chunks, brute-force cosine is milliseconds, so a vector database would be pure overhead. Index is **incremental** (SHA-keyed per note: edit one note, re-embed only that note's chunks).
4. **Index location**: `90-System/Search Index/`, gitignored — each machine builds its own, so it never causes sync conflicts.

## Commands

```
python3 90-System/Scripts/brain_search.py index          # build/update
python3 90-System/Scripts/brain_search.py search "query" -k 10
python3 90-System/Scripts/brain_search.py chunks         # dry-run, no embeddings
```

Setup per machine: `pip install sentence-transformers`.

## Related

- [[brain_graph]] — the Level 4 sibling
