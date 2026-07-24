# 🌐 Wiki

Evergreen entities — the "nouns" of my life and work. One page per entity, always linked with `[[wikilinks]]`. This is what makes recall work: ask about a person or tool and everything connected is one hop away.

| Subfolder | Contains | Template |
|---|---|---|
| `People/` | Anyone I interact with or learn from | [[90-System/Templates/Person\|Person]] |
| `Companies/` | Organizations, clients, vendors | [[90-System/Templates/Company\|Company]] |
| `Tools/` | Software, libraries, and scripts I use or evaluate | [[90-System/Templates/Tool\|Tool]] |
| `Concepts/` | Ideas, methods, principles, recurring topics | [[90-System/Templates/Concept\|Concept]] |

**Rule:** wiki notes hold *evergreen* facts. Meeting-by-meeting detail belongs in project or inbox notes that *link here*. Typed relationships go in frontmatter per [[Graph Schema]].

## People

- [[Chris Aguirre]] — me; the hub every other note connects back to
- [[Nate Herk]] — creator of the second-brain framework this vault follows
- [[Garry Tan]] — YC CEO; built [[GBrain]], the Level 5 archetype
- [[Andrej Karpathy]] — originated the [[LLM Wiki]] idea behind Level 2
- [[Steph Ango]] — Obsidian's CEO; wrote the skills vendored in this vault

## Companies

- [[Anthropic]] — makers of [[Claude Code]]; no first-party embeddings API
- [[Dynalist Inc]] — makers of [[Obsidian]]
- [[Voyage AI]] — embeddings vendor Anthropic points to
- [[Alpaca Markets]] — the broker behind [[COMMAND — Quant Operations Platform]]
- [[AI Automation Society]] — Nate Herk's community
- [[Y Combinator]] — Garry Tan's company

## Tools

- [[Obsidian]] — where the notes live · [[Obsidian Git]] — how they sync
- [[Claude Code]] — the agent harness
- [[brain_search]] — Level 3 semantic search · [[brain_graph]] — Level 4 knowledge graph
- [[Bases]] — core database plugin, powers the dashboards · [[Dataview]] — the query plugin it largely replaces
- [[Smart Connections]] — no-code semantic search plugin
- [[LightRAG]] — graph RAG system · [[GBrain]] — Level 5 reference design
- [[Alpaca]] — broker API · [[Ollama]] — local LLM runtime

## Concepts

**How this vault works**

- [[Second Brain]] — what this vault is · [[PARA Method]] — the folder skeleton
- [[Context vs Connections]] — what gets in · [[Reverse Engineer for Recall]] — where it goes
- [[LLM Wiki]] — Level 2 · [[Semantic Search]] — Level 3 · [[Knowledge Graph]] — Level 4
- [[Embeddings]] · [[RAG]] — the retrieval machinery

**Feeding an agent without drowning it**

- [[Progressive Disclosure]] — load a map, not the territory; the three-tier budget behind indexes and summaries
- [[Retrieve to Enter, Navigate to Expand]] — which retriever earns its keep at which vault size, and why curation outlasts all of them

**Writing that survives**

- [[Evergreen Notes]] · [[Maps of Content]] — how notes are written and navigated here
- [[Architecture Decision Record]] · [[Diataxis]] · [[C4 Model]] — the documentation forms
- [[Documentation Rot]] — the decay all of the above defend against · [[Config Lies, Code Wins]] — its sharpest instance
- [[Shape Up]] — appetite and non-goals, for scoping work
- [[JSON Canvas]] — visual maps an agent can author

**Governing systems that act on their own** — patterns from [[COMMAND — Quant Operations Platform]]

- [[Governed Tool Execution]] — allow / deny / ask, applied to every tool call
- [[Strategy Promotion Ladder]] — the 9 gates a strategy climbs before it risks money
- [[Order Intent]] — freezing the decision · [[Evidence Bundles]] — the work it must show
- [[Single Writer Rule]] — one service per table · [[Outbox Pattern]] — surviving the crash between decision and send
- [[Reconciliation]] — repairing drift from broker truth · [[Circuit Breaker]] — the halt that can't reset itself
- [[Safety Checks Should Fail Closed]] — what a guard does when it can't run

**Markets** — the domain vocabulary behind COMMAND

- [[ICT Smart Money Concepts]] — the price-action vocabulary and its 4-layer filter
- [[Donchian Channels]] · [[Volume-Weighted Moving Average]] — the two breakout primitives
- [[Walk-Forward Validation]] — the honest backtest · [[Ghost Trades]] — the rung below paper
- [[Loss Quarantine]] — per-symbol memory beneath the portfolio breaker

A full, always-current list lives in [[90-System/Bases/Entity|the Entity base]] — this index is the curated view.
