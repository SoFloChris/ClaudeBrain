---
type: concept
aliases: ["graph engineering", "agentic knowledge graph", "GraphRAG"]
broader: "[[Knowledge Graph]]"
related: ["[[RAG]]", "[[LightRAG]]"]
---

# Graph Engineering

Designing an AI system around an **explicit graph** — knowledge as nodes and typed edges the agent traverses — instead of flat documents retrieved by similarity. The term went viral on X in July 2026; the discipline underneath it ([[Knowledge Graph]]s, GraphRAG, graph-based agent memory) predates the name by years.

## Why it matters to me

This is the vocabulary that grew up around what this vault already does at Level 4. When someone says "graph engineering" they may mean my [[Graph Schema]] — or two unrelated things. Worth knowing which.

Within 48 hours of going viral the term meant three different things:

| Meaning | What it actually is |
|---|---|
| **Graph-structured knowledge/memory** | Typed nodes and edges the agent traverses — this vault's Level 4 |
| **Orchestration graphs** | Multi-agent systems as explicit DAGs with typed nodes and transitions |
| **Graphs of loops** | Networks of self-improvement cycles watching each other |

Only the first is about recall. The other two borrow the word for control flow.

## The real pipeline

Every credible version runs some ordering of the same stages. The most rigorous public one is `codejunkie99/graph-engineering` (MIT, ~144 stars) — a Claude skill adapted from **Southeast University's graduate Knowledge Graph course** (taught in Chinese since 2019 by Prof. Peng Wang):

**Scope → Representation → Ontology → Entities → Relations → Events → Quality Gate → Fusion → Serve to LLMs**

The two stages the viral versions always skip are the two that decide whether it works:

- **Ontology first.** A small controlled edge vocabulary, fixed before extraction. Let an LLM invent predicates freely and you get `works_at`, `employed_by`, and `is_employee_of` as three unrelated edges. (Same reason this vault's [[Graph Schema]] is a closed list.)
- **Quality gate + fusion.** Entity resolution ("Edwin Aldrin" → "Buzz Aldrin", zero string overlap) and provenance on every fact. Without it the graph accumulates duplicate nodes faster than it accumulates answers.

The 2026 trend line across the field: lazy indexing, agentic traversal (the agent picks hops live rather than following a fixed query plan), small edge vocabularies, and honest routing — send a question to the graph only when it's actually a multi-hop question.

## When it breaks

- **Extraction cost scales with the corpus, and re-extraction is the real bill.** Change the ontology and you re-run the whole pipeline.
- **Vector [[RAG]] still wins for "what did I say about X"** — single-hop lookups don't need edges. The graph earns its keep on relationship chains and on questions whose answer lives in no single document.
- **At this vault's size (~50 notes) the whole apparatus is overkill.** Hand-typed frontmatter is a graph; it just doesn't need extraction. Automated graph engineering becomes interesting somewhere north of a few thousand documents I didn't write myself.
- **The name is currently a hype magnet** — see [[Verify the Claim, Steal the Architecture]].

## Related

- [[Knowledge Graph]] — the concept; graph engineering is the practice of building one at scale
- [[LightRAG]] — one implementation of the extract-then-traverse pipeline
- [[Graph Schema]] — this vault's ontology, hand-maintained instead of LLM-extracted
