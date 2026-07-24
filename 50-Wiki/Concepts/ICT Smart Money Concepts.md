---
type: concept
aliases: [ICT, Smart Money Concepts, SMC]
summary: "Price-action vocabulary (FVG, order blocks, liquidity sweeps) built on the idea that institutions engineer liquidity before moving price — and the 4-layer filter COMMAND derives from it."
related: ["[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# ICT Smart Money Concepts

A price-action vocabulary built on one premise: large institutions have to *engineer* liquidity before they can move size, and that engineering leaves readable footprints.

## The vocabulary

| Term | What it actually is |
|---|---|
| **Fair Value Gap (FVG)** | A three-candle pattern where the middle candle's move leaves a gap between the outer candles' wicks — an imbalance price tends to revisit |
| **Order Block (OB)** | The last opposing candle before a strong directional move — the institutional footprint |
| **Breaker Block** | A failed order block that flips to support/resistance once broken |
| **Liquidity Sweep / Inducement** | Price pushes past an obvious high or low to take out stops, then reverses — stops *are* the liquidity |
| **Market Structure Shift (MSS) / BOS / CHoCH** | A break of a significant swing high or low, signalling trend change |
| **Premium / Discount** | Price above / below the midpoint of the recent swing range — buy in discount, sell in premium |
| **Kill Zones** | Time windows when institutional activity concentrates |

## The 4-layer filter

[[COMMAND — Quant Operations Platform]]'s `ict-signal-sidecar` turns that vocabulary into a rejection cascade — a signal must survive all four:

1. **Bias** — directional bias from the BOS/CHoCH series (prefer H4, fall back to D1). Neutral → reject.
2. **Premium/Discount** — on H1, price must be in *discount* for a bullish bias (or premium for bearish).
3. **Inducement** — a liquidity sweep in the last 5 bars with the right sign. **Scored, not required** — absence only costs confidence points.
4. **Entry trigger** — on M30, an active FVG or OB matching bias, within 0.3% (crypto) / 0.5% (stocks) of price. None → reject.

Two cross-cutting gates: volatility (H4 ATR% ≥ 0.5%) and BOS recency (within 30 bars). **Hard kill: stale BOS *and* low volatility → reject outright.**

**Confidence scoring** starts at 50, capped at 100: +15 both FVG and OB · +10 inducement · +10 BOS confirmed · +10 D1 agrees with H4 · +5 high vol · +10 tight proximity. **Threshold to trade: 80.** Confidence then sets risk: 80–84 → 1.5× base, 85–89 → 2.0×, 90+ → 2.5×, with an "OB Mega" case at 3.5%.

## Why it matters to me

The transferable idea isn't the trading vocabulary — it's the **rejection cascade with one scored (not required) layer**. Three hard gates give determinism; the soft layer contributes to a confidence number that then scales position size. That's a cleaner design than either "all filters required" (too few signals) or "score everything" (no floor on quality).

> Watch out: kill-zone times are defined **four different ways** across COMMAND's repo (ET in one doc, UTC in another, different hours in the config and the backtester). A live example of [[Documentation Rot]].

## Related

- [[Strategy Promotion Ladder]] — what a signal must survive *after* passing this filter
