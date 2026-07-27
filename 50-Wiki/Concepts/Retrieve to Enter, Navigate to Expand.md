---
type: concept
summary: "Use whatever finds the right neighbourhood — grep at 100 notes, BM25 at 1,000, embeddings at 10,000 — then follow curated links outward. Retrieval picks the entry point; structure does the expansion."
aliases: [retrieve then navigate, hybrid retrieval, similarity is not relevance]
related: ["[[Semantic Search]]", "[[Knowledge Graph]]", "[[Progressive Disclosure]]", "[[Agent Guide]]"]
tags:
  - concept
created: 2026-07-24
---

# Retrieve to Enter, Navigate to Expand

The grep-versus-embeddings argument is the wrong argument. They do different jobs: **retrieval gets you to the right neighbourhood; curated links expand from there.** Use whichever retriever the corpus size justifies, then stop retrieving and start following links.

## Why the debate looks unresolvable

Both sides have real evidence, because they measured different regimes.

**For grep.** Anthropic tried RAG in early Claude Code and dropped it: *"we landed on just agentic search… it outperformed everything. By a lot."* No index to keep in sync, no chunking, no staleness. And for a *personal* vault there's a sharper argument still — **you are both the author and the querier, so your query vocabulary and your document vocabulary are the same vocabulary.** Vocabulary mismatch is exactly what embeddings exist to fix, and it's largely absent at personal scale.

**For embeddings.** Cursor's internal benchmark puts semantic search at **+12.5% accuracy on average** (range +6.5% to +23.5%) over grep-and-CLI alone — and their production system runs **both**. A vendor benchmark reports hybrid BM25 + dense retrieval cutting Claude Code's token use ~39% by replacing iterative grep loops with one lookup.

Both are consistent with one model: **grep's cost is the number of round trips needed to disambiguate, and round trips grow with corpus size.** At 100 notes it's one grep. At 10,000 it's five greps and forty file reads.

## The honest routing table

| Situation | Reach for |
|---|---|
| You know the term, name, tag, or filename | **grep / glob** — exact, no staleness, ~50 tokens |
| You know the entity but not the note | **backlinks and `[[wikilinks]]`** — structure you already curated |
| The corpus is small enough to list | **read the `_Index.md`** — no retrieval at all |
| Conceptual query in words you didn't write with | **embeddings** — the vocabulary-mismatch case |
| "What have I written about X" — recall over precision | **embeddings + grep** |
| Grep returns 200 hits | **rank, don't scan** — this is BM25's case, not grep's |

**BM25 is the most underrated option in the whole debate.** It's an index, so it's cheap at query time; lexical, so it never invents a match; and it solves grep's actual failure mode, which is *over*-retrieval rather than under-retrieval — all without an embedding model.

## Similarity is not relevance

The strongest statement of the navigate side is PageIndex: build a table-of-contents-shaped tree with a `summary` on every node, and retrieve by **reasoning over the tree** — no vectors, no chunking. Reported 98.7% on FinanceBench.

Its node schema is `{title, id, location, summary, children}` — which is *exactly* an `_Index.md` entry. **An Obsidian vault with indexes and annotated wikilinks is a hand-built PageIndex tree**, and the links were built by the person who will query them, which makes them better than any extracted graph.

That reframes this vault's linking rule in retrieval terms: **the em-dash clause after a link is the node's `summary` field.** It's what lets an agent decide whether to traverse an edge *without opening the target*. A bare wikilink forces the read that the annotation would have avoided.

The honest limits, from PageIndex's own docs: every traversal hop is another LLM call, so it's slower and costlier than one vector lookup, and it *"does not provide an advantage over vector retrieval for short or unstructured content."* Navigation costs calls; retrieval costs tokens.

## What the graph literature actually found

GraphRAG-Bench (ICLR 2026) is blunt: *"GraphRAG is not a universal upgrade over vanilla RAG. Graph structures provide measurable benefits specifically when the answer depends on relationships among entities, documents, or events, not merely on term matching."* Its methodological jab lands too — many questions labelled "multi-hop" are just sequential lookups a dense retriever handles alone.

That is precisely the split this vault already encodes: `/graph` for relationship questions, `/recall` for semantic ones, grep for everything else. The benchmark data supports the routing; it does not support using the graph as a general search tool.

## Why it matters to me

Three things I want to keep:

1. **At this vault's size, the entire corpus fits in context several times over.** That makes "read the index and pick" a *one-hop* operation that beats every retriever. Adding machinery now would be solving a problem I don't have — the same reasoning as ADR-0001's Level 5 deferral.
2. **Curation is the compounding asset.** The retriever gets swapped as the corpus grows; the annotated links keep working at every scale, and they're the one thing an off-the-shelf system can't supply.
3. **Know which failure mode you have.** Grep fails by returning too much; embeddings fail by returning plausible-but-wrong. Reaching for the wrong fix makes both worse.

## Related

- [[Progressive Disclosure]] — what gets loaded at each stage of this
- [[Semantic Search]] — the retriever this vault built, and why it stays a fallback
- [[Knowledge Graph]] — the navigate half, and the questions that actually need it
