---
type: concept
aliases: [circuit breakers, kill switch]
summary: "An automatic halt that trips on cumulative damage rather than any single failure — and, critically, cannot reset itself."
related: ["[[Governed Tool Execution]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Circuit Breaker

An automatic halt that trips on **cumulative** damage rather than on any single bad event — and whose defining property is that **it does not reset itself**.

## How [[COMMAND — Quant Operations Platform]] configures it

| Trigger | Action |
|---|---|
| 8 consecutive losses | Pause new entries |
| 15% per-strategy drawdown | Halt that strategy |
| VIX > 35 | **Reduce size to 25%** — graduated, not a halt |
| Daily loss (soft % + hard $5,000 cap) | Block all trades until manual reset |

Two details worth stealing:

- **The VIX response is graduated.** Most breakers are binary; scaling to 25% keeps the system participating in the regime it was built for while cutting the blast radius.
- **Existing positions are not auto-closed** when it trips. Halting *new* risk is a different decision from liquidating existing risk, and conflating them turns a safety mechanism into a forced seller at the worst moment.

The invariant repeated across every governance doc: **"cannot be auto-reset by any AI/agent path."** Reset is admin-only, and the risk governor's reset requires a literal confirmation phrase in the request body.

Each component carries its own independent breaker, tuned to its own risk: the risk governor halts at 3–5 consecutive losses, the backend ICT bot at 3 or a 2% daily loss, and the live-money Kalshi bot at **one loss**.

## Why it matters to me

**A safety mechanism an agent can reset is not a safety mechanism.** That single rule is the difference between a circuit breaker and a suggestion — and it's the same principle as [[Governed Tool Execution]]: put the authority to un-block outside the system that got blocked.

The second lesson is from a real incident in the repo: a reconciliation bug was marking filled orders as cancelled, so **the breaker never saw the losses**. A breaker is only as good as the accounting feeding it — which is why [[Reconciliation]] is itself a gate.

## Related

- [[Reconciliation]] — the accounting a breaker depends on
