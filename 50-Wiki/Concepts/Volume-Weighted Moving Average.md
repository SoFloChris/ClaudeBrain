---
type: concept
aliases: [VWMA, volume weighted moving average]
summary: "A moving average weighting each close by that bar's volume — so a break above it implies participation, not just drift."
related: ["[[Donchian Channels]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Volume-Weighted Moving Average

A moving average where each close is weighted by that bar's volume:

$$\text{VWMA}_n = \frac{\sum (\text{close}_i \times \text{vol}_i)}{\sum \text{vol}_i}$$

Unlike a simple moving average, it reflects **where the volume actually traded**. A break above VWMA therefore implies participation rather than drift — price moved *and* size went with it.

## The weaknesses, and the filters that address them

VWMA's failure modes are direct consequences of its definition, and [[COMMAND — Quant Operations Platform]]'s `vwma-bot` filters for exactly those:

| Weakness | Filter |
|---|---|
| Thin prints move it easily — a "break" on no volume is noise | Current volume ≥ **1.2×** the 20-bar average |
| In a dead range everything crosses it constantly | ATR(14) ≥ **0.5×** the 20-bar average ATR |

There's a nice implementation detail: the volume filter is *skipped* when average volume ≤ 10, because tick-level WebSocket messages often report `size=1`. A filter applied to data that can't support it produces confident nonsense.

## Why this bot is switched off — and why that's the useful part

`vwma-bot` self-reports PF 1.55 and Sharpe 2.39 on 57 trades a year, and is nonetheless **profiled off**: `restart: "no"`, execution disabled, behind a `legacy-vwma` compose profile. The runbook is blunt — *"do not start without proof"* — and the incident log records the reason as *"VWMA spray."*

That's the most instructive thing in the file. A strategy with acceptable backtest numbers was **retired for live behaviour**, and the retirement was made structural (a compose profile) rather than social (a note saying don't run it). Compare the [[Strategy Promotion Ladder]], which is entirely about climbing — this is the descent, and it's implemented with equal seriousness.

Also worth noting: long-only, because *"Alpaca crypto does NOT support short selling"* — a constraint from the venue, recorded in a code comment at the point where someone would otherwise try.

## Why it matters to me

**Weighting by participation instead of time is a general move.** Any average over events where the events have different magnitudes is quietly lying if it treats them equally — request latency weighted by request count, sentiment weighted by reach, error rates weighted by traffic.

And the retirement lesson: **a decommission needs a mechanism, not a decision.** "We agreed not to run it" degrades; `profiles: ["legacy-vwma"]` doesn't.

## Related

- [[Donchian Channels]] — the range-based breakout primitive this one complements
- [[Strategy Promotion Ladder]] — the climb; this note documents the fall
