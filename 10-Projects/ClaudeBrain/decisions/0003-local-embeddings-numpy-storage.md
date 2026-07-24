---
type: adr
summary: "ADR-0003 (accepted): run bge-small-en-v1.5 locally with a flat numpy index rather than a hosted embeddings API and vector database."
status: accepted
date: 2026-07-24
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[Semantic Search]]", "[[brain_search]]", "[[Local Embedding Models]]", "[[Voyage AI]]"]
tags:
  - adr
---

# ADR-0003 — Local embeddings with plain numpy storage for semantic search

## Context and Problem Statement

Level 3 ([[Semantic Search]]) needs an embedding model and somewhere to put the vectors. Options span from a hosted API plus a managed vector database to a local model plus a flat file. What's the right size for a personal vault of a few thousand chunks?

## Decision Drivers

- Notes are personal; sending them to a third party by default is a real cost, not a hypothetical one.
- Setup friction is compounding — anything requiring an account, key, or login gets skipped on the second machine.
- At this scale, retrieval quality is dominated by chunking, not by model size.

## Considered Options

- `sentence-transformers` locally + numpy array
- `sentence-transformers` locally + sqlite-vec / LanceDB / Chroma
- Hosted embeddings ([[Voyage AI]] or OpenAI) + managed vector DB
- `google/embeddinggemma-300m` as the local model

## Decision Outcome

Chosen option: **local `sentence-transformers` with `BAAI/bge-small-en-v1.5`, stored in a plain numpy array**, because at a few thousand chunks a brute-force cosine scan is milliseconds — a vector database would add a dependency to solve a problem that doesn't exist — and a local, ungated model keeps both privacy and zero-config setup intact.

### Consequences

- Good, because nothing leaves the machine and there are no keys to manage.
- Good, because the whole search engine is one readable file with one dependency.
- Good, because the index is per-machine and gitignored, so it can never cause a sync conflict.
- Bad, because each machine pays a one-time `pip install` and model download.
- Bad, because this won't scale past ~100K chunks — at which point it should be revisited, not patched.

### Confirmation

`brain_search.py index` builds, reports "index up to date" on an unchanged second run, and re-embeds only the changed note's chunks after a single-file edit. All three were verified at build time.

## Pros and Cons of the Options

### EmbeddingGemma-300m as the model

- Good, because it's the highest-ranked MTEB model under 500M parameters.
- Bad, because it's **license-gated on Hugging Face** — it needs an account and `huggingface-cli login`, which breaks the zero-config property on a second machine. Documented as an opt-in upgrade via `BRAIN_EMBED_MODEL` instead.

### Hosted embeddings + managed vector DB

- Good, because higher quality and no local compute.
- Bad, because personal notes would leave the machine by default, and a vault of a few thousand notes costs pennies to embed — the spend isn't the objection, the exposure is.

### A local vector database

- Good, because it scales and keeps vectors beside metadata.
- Bad, because sqlite-vec is still pre-1.0, and Chroma/LanceDB are real infrastructure for a workload that fits in RAM twice over.

## More Information

Revisit past roughly 100K chunks, or if retrieval quality becomes the limiting factor rather than chunking. [[Local Embedding Models]] holds the model comparison for that day.

## Amendments

<!-- Append only. -->
