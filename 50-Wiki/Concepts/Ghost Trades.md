---
type: concept
aliases: [ghost trading, shadow trades]
summary: "Fully simulated fills tracked against real live prices — a rung below paper trading, used to build a sample before risking even fake capital."
broader: "[[Strategy Promotion Ladder]]"
related: ["[[Walk-Forward Validation]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Ghost Trades

Paper trading *below* paper trading: fully simulated fills tracked against **real live market prices**, with no broker involved at all. The purpose is to accumulate a statistically meaningful sample of how a strategy behaves in live conditions before risking even fake capital.

## How [[COMMAND — Quant Operations Platform]] uses them

- A ghost strategy can be created **from natural language** — a local model converts a prose description into structured entry/exit criteria.
- An evaluator runs every 15 minutes and walks each trade through `planned → open → closed` using real prices. Its header is emphatic: *"Uses honest price checks — no fake fills or fake closures."*
- Outcomes feed back into per-indicator win-rate stats, and into the crypto bot's **loss quarantine** — a symbol with a bad recent record gets blocked from new entries.
- **Promotion gate:** minimum **20 ghost trades at ≥40% win rate** before a strategy advances. Roughly 11,785 ghost trades exist in the system.

## Why it matters to me

The honest-simulation rule is the whole point. A simulator that invents fills tells you what you want to hear; one that only closes a position when the real price actually traded there tells you something. **The cheapest tier of a promotion ladder is worthless if it's optimistic.**

The generalisable pattern: before something touches production, run it against *live inputs* with *inert outputs*, and require a minimum sample — not a minimum success rate on three trials.

## Related

- [[Strategy Promotion Ladder]] — where this sits in the sequence
