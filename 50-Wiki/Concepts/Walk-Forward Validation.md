---
type: concept
aliases: [walk-forward, WFA]
summary: "Rolling in-sample → out-of-sample backtest windows that expose curve-fitting; a hard promotion gate in COMMAND."
broader: "[[Strategy Promotion Ladder]]"
related: ["[[Ghost Trades]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Walk-Forward Validation

Instead of one backtest over all history — which invites curve-fitting — slice the timeline into rolling **in-sample → out-of-sample** windows. Optimize or measure on IS, then measure honestly on the OOS window that immediately follows, and step forward.

A strategy that only works in-sample is overfit. Walk-forward is what makes that visible.

## How [[COMMAND — Quant Operations Platform]] implements it

- Windows are generated so the **step size equals the OOS length** — OOS windows tile the timeline without overlapping, so no out-of-sample bar is ever counted twice.
- Each window runs two backtests (IS then OOS), recorded as experiment runs labelled profitable/unprofitable.
- **Robustness score = profitable OOS windows ÷ total OOS windows.** A plain hit rate, deliberately not return-weighted — one lucky window can't carry the score.
- It is a **hard gate**: step 4 of the [[Strategy Promotion Ladder]], and the subject of its own ADR in the repo.

## Why it matters to me

The design lesson generalises past trading: **the honest test is the one you run on data you didn't tune against, and it has to be structurally impossible to peek.** Non-overlapping OOS windows are that structure. The equivalent discipline in any evaluation is holding out a set you never look at until the decision is made.

The complementary metric COMMAND pairs with it — **PBO (Probability of Backtest Overfitting), gated below 0.5** — asks the same question from the other direction: given how many variants were tried, how likely is this result to be noise?

## Related

- [[Ghost Trades]] — the next rung: simulated fills against live prices
