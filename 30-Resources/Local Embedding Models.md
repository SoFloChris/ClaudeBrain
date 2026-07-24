---
type: resource
summary: "Comparison of small local embedding models for personal-vault semantic search, and why bge-small-en-v1.5 won on being ungated rather than on benchmark rank."
topic: "[[Embeddings]]"
related: ["[[Semantic Search]]", "[[brain_search]]", "[[Voyage AI]]"]
---

# Local Embedding Models

Which model to run for [[Semantic Search]] over personal notes. Researched 2026-07.

## The candidates

| Model | Params | Dims | Context | Verdict |
|---|---|---|---|---|
| `all-MiniLM-L6-v2` | 22M | 384 | ~256 tok | 2021-era; outclassed but still works |
| **`bge-small-en-v1.5`** | ~33M | 384 | 512 | **This vault's default** — tiny, ungated, good |
| `gte-small` | ~33M | 384 | 512 | Comparable to bge-small |
| `nomic-embed-text-v1.5` | 137M | 768 (truncatable) | 8192 | Long-time local-RAG default; beats ada-002 |
| `google/embeddinggemma-300m` | 308M | 768 → 512/256/128 | 2048 | Highest-ranked MTEB model under 500M — but **license-gated** on Hugging Face (needs login), which breaks zero-config |
| `Qwen3-Embedding-0.6B` | 0.6B | 1024 | 32K | Strongest small option; heavier |

**Why bge-small won here:** ungated (no HF login), ~130MB download, and at this vault's size the bottleneck is chunking quality, not model quality. EmbeddingGemma is the documented upgrade for anyone willing to accept the Gemma license — override with `BRAIN_EMBED_MODEL`.

**Quirk:** BGE models want queries prefixed with `"Represent this sentence for searching relevant passages: "`. [[brain_search]] applies this automatically; forgetting it measurably degrades results.

## Via [[Ollama]]

`embeddinggemma` (622MB) · `nomic-embed-text` (274MB) · `mxbai-embed-large` (670MB) · `qwen3-embedding:0.6b` (639MB) · `bge-m3` (1.2GB, hybrid dense+sparse). Worth using if Ollama is already running; otherwise `sentence-transformers` avoids a second daemon.

## Hosted, if local ever isn't enough

[[Anthropic]] ships no embeddings API and points to [[Voyage AI]] (`voyage-4-lite` ≈ $0.02/M tokens). OpenAI `text-embedding-3-small` is also $0.02/M (1536 dims). A whole vault is 1–5M tokens — pennies either way. Local still wins on privacy and zero setup friction.

## Storage: don't over-engineer

At a few thousand chunks, a plain numpy matrix + brute-force cosine is **milliseconds**. sqlite-vec is still pre-1.0 alpha; LanceDB and Chroma are real databases solving a problem this vault doesn't have. Revisit only past ~100K chunks.

## Chunking (matters more than the model)

Split on markdown headings first, keeping the heading path as context. Sub-split long sections to ~400 tokens with 10–20% overlap — retrieval precision peaks in the 256–512 token range. For short notes, one chunk per section is plenty.

## Related

- [[brain_search]] — the implementation of all of the above
