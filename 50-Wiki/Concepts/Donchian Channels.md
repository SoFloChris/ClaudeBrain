---
type: concept
aliases: [Donchian, Donchian channel, 20/10 breakout, Turtle breakout]
summary: "Bands at the highest high and lowest low of the last N bars; the classic asymmetric 20/10 exits faster than it enters, and the exit band doubles as the stop."
related: ["[[Volume-Weighted Moving Average]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Donchian Channels

Bands drawn at the **highest high** and **lowest low** of the last *N* bars. A close above the upper band is a breakout — a trend-following entry — and the opposite band trails behind as the exit.

## The asymmetry is the design

[[COMMAND — Quant Operations Platform]]'s `donchian-bot` uses **20/10**: enter on a break of the 20-bar high, exit on the 10-bar low. That's the classic Turtle-trader configuration, and the asymmetry is deliberate — **exit faster than you enter.** A 20-bar high is a high bar for conviction; a 10-bar low is a low bar for doubt.

The second consequence is quieter and more useful: because the 10-bar low is also the initial stop, **position size becomes a direct function of recent range**. Risk 0.5% of equity, divide by the distance from entry to the 10-bar low, and a volatile instrument automatically gets a smaller position. No separate volatility model required — the channel *is* the volatility measure.

COMMAND floors that stop distance at 0.8% of price, so a compressed range can't manufacture an enormous position out of a tiny denominator.

## What it's paired with

A raw breakout takes every false break, so the bot requires confluence — at least one of a bullish fair value gap, a break of structure, or price above session VWAP ([[ICT Smart Money Concepts]]) — plus a **regime gate**: no equity entries unless SPY is above its 200-day moving average.

Exits are trailed rather than targeted: breakeven at +1R, lock +0.5R at +1.5R, a Chandelier-style trail at `peak − 1.5R`, 50% scaled out at +1.5R, and **no hard take-profit** — the comment in the source is *"trail runner."*

## Why it matters to me

Two transferable ideas, neither about trading:

- **Asymmetric thresholds for entering versus exiting a state.** Requiring more evidence to commit than to withdraw is the right default whenever being wrong is more expensive than being late. It's the same shape as a Schmitt trigger, or a retry policy that backs off fast and ramps up slowly.
- **Derive the tolerance from the data, not from a constant.** The stop isn't "2%"; it's "where recent price action says the thesis is broken." Any threshold I hardcode is a guess about a distribution I could have measured — with a floor to keep the measurement from degenerating.

## Related

- [[Volume-Weighted Moving Average]] — the fleet's other breakout primitive, filtered on participation rather than range
- [[ICT Smart Money Concepts]] — the confluence filter layered on top of the raw breakout
