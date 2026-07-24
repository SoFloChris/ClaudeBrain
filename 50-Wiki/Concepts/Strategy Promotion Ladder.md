---
type: concept
aliases: [promotion ladder, 9-gate ladder, strategy lifecycle]
summary: "The 9-gate sequence a strategy must climb before it can risk real money in COMMAND — distinct from the 16 gates every individual order passes."
related: ["[[COMMAND — Quant Operations Platform]]", "[[Governed Tool Execution]]", "[[Walk-Forward Validation]]"]
tags:
  - concept
created: 2026-07-24
---

# Strategy Promotion Ladder

The 9-gate sequence a trading strategy must climb in [[COMMAND — Quant Operations Platform]] before it can touch real money. Each gate must pass explicitly — nothing advances by default. **Demotion, by contrast, is always allowed without gate checks.**

> [!warning] Two different "gate" counts, and they are not the same thing
> This ladder has **9 gates** and governs *a strategy's lifecycle*. Order sealing in `execution-authority.ts` runs **16 gates** on *every individual [[Order Intent]]*. The repo's README conflates them; `ARCHITECTURE.md` is explicit that they're distinct.

## The 9 gates

The lifecycle framing (`.claude/rules/trading.md`) and the checks framing (`SAFETY_GOVERNANCE_MATRIX.md`) describe the same 9:

| # | Stage | The check that must pass |
|---|---|---|
| 1 | Draft | Strategy exists and is enabled |
| 2 | Backtested | A completed backtest with **profit factor > 1.0** |
| 3 | Ghost-traded | Minimum **20 [[Ghost Trades]] at ≥40% win rate** |
| 4 | Walk-forward validated | [[Walk-Forward Validation]] — eval score **≥ 0.5** |
| 5 | Evaluated | No pending approvals outstanding |
| 6 | Evidence reviewed | Risk limits configured (`max_risk_pct > 0`, stop-loss required) |
| 7 | Admin approved | Idempotency check — no duplicate signal submissions |
| 8 | Paper-active | An [[Evidence Bundles\|evidence bundle]] exists |
| 9 | Live-ready | Logging tables available; **operator-explicit, never automated** |

Every transition logs to `strategy_lifecycle` with the full `gate_results` JSON and a `promoted_by`.

> [!note] A third framing exists
> `TRADING-SYSTEM.md` describes a 6-stage ladder — `draft → backtested → validated → paper_active → paper_verified → live` — gated on ≥1 backtest with Sharpe > 0, **PBO < 0.5**, a defined risk profile, **30+ paper trades with positive cumulative P&L**, and admin approval. Treat **"9-gate ladder" as the canonical vocabulary** and the 6-stage version as a companion description; the substantive gates (PBO, the 30-paper-trade requirement) are real either way. Three overlapping descriptions of one ladder is [[Documentation Rot]] caught in the act.

## Why it matters to me

It's the clearest expression of the design philosophy in COMMAND: **the burden of proof runs uphill.** A strategy is guilty until proven profitable, and the expensive gates — walk-forward, evidence review — sit *before* the ones that risk capital, not after.

The generalizable lesson beyond trading: when a system can act autonomously, safety comes from **staged promotion with irreversible-action gates at the end**, not from the agent being careful. Gate 9 being operator-explicit by design is the load-bearing part; everything above it is evidence-gathering that a machine can do unattended precisely *because* it can't self-promote past the last step.

The counterpart worth holding alongside it: a ladder needs a **descent** mechanism too. See [[Volume-Weighted Moving Average]] for a strategy retired with a compose profile rather than a promise.

## Related

- [[Governed Tool Execution]] — the same philosophy applied to individual tool calls
- [[Order Intent]] — the *other* gate sequence, per-order rather than per-strategy
- [[Walk-Forward Validation]] — gate 4, the hardest one to fake
