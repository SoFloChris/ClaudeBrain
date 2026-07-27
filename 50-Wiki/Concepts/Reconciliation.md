---
type: concept
aliases: [reconciling, broker reconciliation, state drift repair]
summary: "Periodically comparing your record of the world against the authoritative external record and repairing the drift — because every risk control downstream is only as honest as this."
related: ["[[Order Intent]]", "[[Circuit Breaker]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Reconciliation

Periodically compare **your** record of orders and positions against the **broker's** record, and repair the difference. A missed fill webhook silently desynchronizes your risk model from reality, and nothing downstream will notice.

## The authority boundary is the whole design

[[COMMAND — Quant Operations Platform]]'s `reconciliation-worker.ts` runs every 60 seconds, and its docblock states exactly what it may do:

> *"CANNOT create new order intents, bypass approvals, or alter sealed packet content. CAN only repair state and escalate via Execution Authority."*

That sentence is the pattern. A repair process is powerful — it edits records that gates already approved — so it gets **narrow, explicit** authority: fix state, escalate everything else. It may not become a second path to trading.

Reconciliation health is itself **gate 14** of order sealing: if the last run was more than 5 minutes ago, the pipeline refuses to seal new orders. The system would rather stop trading than trade on stale accounting.

## Engineering details worth stealing

- **In-flight guard.** A `reconRunning` flag, because *"a slow cycle (>60s) must not overlap the next tick. Overlap was leaving `reconciliation_runs` rows stuck in 'running' and double-processing intents."*
- **Crash recovery at startup** — orphaned `running` rows are retired on boot: *"No sweep can be in-flight at startup."*
- A companion `reconciliation-prefill.ts` handles intents stranded before a fill.

## Why it matters to me

**Every safety mechanism is downstream of its accounting.** The [[Circuit Breaker]] counts consecutive losses; the daily-loss cap sums realized P&L. Both read the same ledger reconciliation maintains — so a reconciliation bug doesn't degrade safety gracefully, it *silently deletes* it.

That's not hypothetical. In COMMAND's `kalshi-bot`, the reconciliation loop was marking **filled orders as cancelled**, so the circuit breaker and daily-loss cap never saw the losses. The takers bled until an emergency rollback disabled them. The breaker wasn't broken; it was blind.

The general rule: **when you build a control that reads state, ask who guarantees that state is true — and make that guarantee a gate, not an assumption.**

## Related

- [[Order Intent]] — the records reconciliation repairs, and the `reconciled_error` terminal state
- [[Circuit Breaker]] — the control that fails silently when reconciliation lies
