---
type: concept
aliases: [order intents, decision packet, frozen packet]
summary: "The durable record of a decision to trade, created before any broker contact and hash-sealed once it passes every gate — so what was decided survives what the market did next."
related: ["[[Evidence Bundles]]", "[[Single Writer Rule]]", "[[Outbox Pattern]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Order Intent

An **order intent** is the durable record of a *decision to trade* — written before any broker is contacted, carried through a strict state machine, and made immutable once every gate passes.

The point is separating **what was decided** from **what happened**. A broker order tells you a fill price. An order intent tells you the reasoning, the market state, the risk snapshot, and the strategy version that produced it — permanently, whether the trade won or lost.

## The state machine

[[COMMAND — Quant Operations Platform]]'s `execution-authority.ts` runs it:

```
draft → building_evidence → {waiting_approval | ready_for_gating}
      → {sealed | gated_rejected} → queued_for_submission → submitting
      → submitted → acknowledged → filled → position_open → position_closed → completed
```

Terminal states: `completed, failed, cancelled, rejected, replaced, gated_rejected, reconciled_error`. Any state can fall to `failed`; `reconciled_error` is reachable from anywhere — which is [[Reconciliation]] declaring the record untrustworthy.

## Sealing

At the moment all 16 gates pass, the intent is **sealed**:

- A **SHA-256 `packet_hash`** is computed over symbol, side, quantity, prices, strategy version, evidence bundle ID, and risk snapshot.
- A `client_order_id` is assigned for idempotent submission — resubmitting can't double-fill.
- After sealing, **only lifecycle timestamps and `terminal_reason` may change.** The decision itself is frozen and tamper-evident.

Sealed intents are enqueued to `broker_outbox` **in the same transaction** as the seal — see [[Outbox Pattern]].

## Why it matters to me

Three ideas here transfer well beyond trading:

1. **Record the decision, not just the action.** Most systems log what they did. Logging *what they knew and why they chose* is what makes a postmortem possible.
2. **Freeze at the commit point.** A hash over the inputs turns "we think this is what the strategy saw" into proof. Anything mutable after the decision is a place for the story to drift.
3. **One writer, one state machine.** Because only `execution-authority.ts` may transition an intent, illegal transitions are impossible *by construction* rather than by discipline — see [[Single Writer Rule]].

## Related

- [[Evidence Bundles]] — the "show your work" attached to an intent before it can seal
- [[Single Writer Rule]] — why exactly one service transitions these rows
- [[Outbox Pattern]] — how a sealed intent survives a crash on its way to the broker
