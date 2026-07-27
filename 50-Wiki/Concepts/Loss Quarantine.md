---
type: concept
aliases: [symbol quarantine, loss quarantining]
summary: "Blocking new entries in a specific symbol-and-direction whose recent record is bad — a per-instrument memory that sits below the portfolio-level circuit breaker."
broader: "[[Circuit Breaker]]"
related: ["[[Ghost Trades]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Loss Quarantine

A [[Circuit Breaker]] asks "is the *system* losing?" Loss quarantine asks a narrower and more useful question: **"is this *particular thing* losing?"** — and blocks new entries in that symbol-and-direction while the answer is yes.

The unit matters. Halting all trading because BTC shorts have been bad is an overreaction; continuing to take BTC shorts because the portfolio is fine is the actual mistake.

## How [[COMMAND — Quant Operations Platform]] implements it

`crypto-agent`'s `loss-quarantine.ts` queries combined real and [[Ghost Trades]] history for the symbol+direction before every entry, over **two windows**:

| Window | Minimum sample | Blocks when |
|---|---|---|
| **Recent** — 14 days | ≥2 trades | ≤ −$25 total P&L with ≤50% win rate, **or** ≥3 trades at ≤ −$10 with ≤50% WR |
| **Structural** — 180 days | ≥5 trades | ≤ −$25 with ≤50% WR |

Three design details worth keeping:

- **It fails closed.** A DB error returns `blocked: true`, reason `loss_quarantine_unavailable` — see [[Safety Checks Should Fail Closed]].
- **It reads simulated history too.** Ghost trades count toward the record, so a symbol can be quarantined before it ever costs real money.
- **Symbol variants are normalised** (`BTC-USD` / `BTC/USD` / `BTC-USDT`) — otherwise the quarantine is trivially evaded by a naming difference, which is the sort of bug that looks like it's working.

A block also sets a 20-minute cooldown, so a quarantined symbol isn't re-queried on every tick.

## Why it matters to me

The generalisable shape is **a feedback loop scoped to the unit that actually varies**. Portfolio-level controls average away the signal; per-instrument memory keeps it.

Two conditions make it honest rather than superstitious: a **minimum sample** before the rule can fire (two trades isn't evidence — hence the escalating thresholds), and **two time horizons**, so a recent bad run and a structurally bad pairing are caught by different tests. Without those it's just recency bias with a config file.

The equivalent I'd want in an agent system: not "the agent failed, stop the agent," but "this tool, on this kind of input, has a bad record — route around it."

## Related

- [[Circuit Breaker]] — the portfolio-level control this sits beneath
- [[Ghost Trades]] — simulated history that feeds the quarantine decision
