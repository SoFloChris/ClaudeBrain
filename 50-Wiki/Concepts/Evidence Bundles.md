---
type: concept
aliases: [evidence bundle, show your work]
summary: "A structured, mandatory record of the inputs behind a high-stakes AI decision — attached to the decision itself and checked as a gate, not filed as a log."
related: ["[[Order Intent]]", "[[RAG]]", "[[Governed Tool Execution]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Evidence Bundles

"Show your work" made **mandatory and machine-checked**. No high-stakes AI decision reaches execution without a structured record of the market state, signal, agent analysis, and risk at decision time.

The distinction from logging: a log is written *after*, read *never*, and blocks *nothing*. An evidence bundle is attached to the decision before it executes, and its existence and completeness are **gates 8 and 9** of order sealing in [[COMMAND — Quant Operations Platform]].

## Shape

- **Required for:** trade decisions (ghost and live), [[RAG]]-grounded responses, backtest summaries, multi-agent syntheses, AI analysis reports.
- **Lifecycle:** `building → complete → archived`, with `failed` as the off-ramp. Transitions run through an assertion — an invalid transition throws rather than silently corrupting the record.
- **Items** carry a typed `source_type` (`chart_snapshot`, `memory`, `news_item`, `scanner_hit`, `document_chunk`, `indicator`, `price_data`), the content, a ≤300-char excerpt, a weight, a confidence, and provenance JSON.

The typed source and the provenance field are what make a bundle auditable rather than decorative: you can ask *"which of these decisions leaned on retrieved memory versus live price data?"* and get an answer.

> [!warning] The bypass is the interesting part
> When `auto_execute_enabled` is on and no approval is pending, gates 8 and 9 are **waived** with the reason `"OK (auto-execute bypass)"`. The evidence requirement is exactly as strong as the config flag above it — worth knowing before trusting that every executed order has a bundle behind it.

## Why it matters to me

**Evidence you can't gate on is documentation, not governance.** The design move here isn't collecting provenance — everyone collects provenance. It's making bundle completeness a *precondition of execution*, so an incomplete record stops the trade instead of producing an unexplainable one.

The transferable version for any agent system: if an agent must produce a citation-bearing record before its action commits, hallucinated justification becomes a *blocking failure* rather than a plausible paragraph nobody reads.

And the caveat transfers too — a mandatory gate with a config-flag bypass is a **default**, not an invariant. Know which one you have.

## Related

- [[Order Intent]] — what a bundle attaches to, and what refuses to seal without one
- [[Governed Tool Execution]] — the gate framework bundles plug into
