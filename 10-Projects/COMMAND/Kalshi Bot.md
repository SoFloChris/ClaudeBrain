---
type: reference
project: "[[COMMAND — Quant Operations Platform]]"
aliases: [kalshi-bot, Kalshi]
summary: "The one COMMAND service that trades real money — a ~$278 account on Kalshi BTC binaries, hard-capped at $2 a trade, with the strictest risk config in the fleet."
related: ["[[Sidecar Fleet]]", "[[Reconciliation]]", "[[Circuit Breaker]]"]
tags:
  - reference
created: 2026-07-24
---

# Kalshi Bot

The odd one out in the [[Sidecar Fleet]], and the most interesting from a risk-culture standpoint.

> [!danger] This bot trades real money
> The platform-wide "paper only" rule covers the [[Alpaca]] equity and crypto path. `kalshi-bot` runs with `KALSHI_LIVE_TRADING=true` and `KALSHI_OBSERVATION_MODE=false` against a **~$278 live account**. It is a deliberate, deliberately tiny exception — not an oversight.

Market: Kalshi BTC binary event contracts (hourly and 15-minute). Fully self-contained — its own price feed, its own Kalshi WebSocket and REST client, RSA-signed API auth. The largest codebase of any bot: a 3,269-line engine, an 802-line API client, a 696-line risk module, and the fleet's only unit test file.

## Risk config — the tightest in the system

| Limit | Value |
|---|---|
| Max trade | **$2** (`// PASS1 strict: $2 hard // hard $3 — real money`) |
| Max daily loss | **$8** (*"~3% of $278"*) |
| Max daily notional | $25 |
| Max weekly loss | $15 |
| Concurrent positions | 2 (max 2 per market) |
| Rate limits | 36 orders/hour; 10 per market/hour; 10s cooldown |
| **Consecutive-loss halt** | **1** — *"PASS3: one loss trips CB"* |
| Reconciliation staleness | 45s |

A [[Circuit Breaker]] at **one loss** is the whole philosophy in a single constant: when the account is small and the strategies are unproven, the correct number of losses to tolerate before a human looks is one.

## Fee-aware edge floors

Binary contracts have wide fees relative to edge, so the thresholds are explicit: `minEdgePctTaker: 7.0`, `minEdgePctMaker: 3.0` (*"≥2% after maker fee"*), a 6¢ half-spread for market making, a fair-probability band of 0.38–0.62 for the core book with a separate wing band at 0.18–0.82 priced 8¢ wide for **adverse selection**, and a model-failure guard: if `|fair − marketMid| > 0.22`, skip the market entirely rather than assume the model is right and the market is wrong.

There's also a **markout halt** at an average −2¢ over 5 samples — a fill-quality check independent of P&L.

## The emergency rollback, and why it's the best comment in the repo

Seven strategies are implemented; the `LIVE_STRATEGIES` whitelist enables **only market making**. The comment explaining that is a first-rate postmortem:

> *"Wave 5 EMERGENCY ROLLBACK: ALL TAKERS DISABLED. MM-ONLY until fill-tracking bug is confirmed fixed. The takers were bleeding because (a) the 67.7% WR claim for streak_reversal was from 31 samples with wide Wilson CI, (b) our reconciliation loop was marking filled orders as 'cancelled', so circuit breaker + daily-loss cap never saw the losses."*

Two independent failures, both durable lessons:

- **(a) Small-sample overfitting.** A 67.7% win rate over 31 samples has a confidence interval wide enough to include "coin flip." The strategy was promoted on a number that never meant what it appeared to mean.
- **(b) Silent risk-control failure.** The breaker and the daily cap were configured correctly and did nothing, because [[Reconciliation]] was feeding them fiction. Every control downstream of broken accounting is decorative.

Note the response: not "fix the takers," but **disable everything unproven and run the one strategy whose accounting is trusted.** Retreat to the defensible position first.

## Operational details

- **Deep health check** — `/health` returns **503** when the bot is up but not cycling: *"zombie state. `restart:always` + healthcheck fail = auto-recycle."* Liveness that only proves the process exists is worthless; this proves it's *working*.
- **File-naming gotcha:** `binance-ws.ts` connects to **Coinbase**, not Binance. Its own header says so (*"Primary: Coinbase WS ticker — sub-second trades, free, no auth, reliable"*). A small live instance of [[Config Lies, Code Wins]] — even filenames drift.

## Related

- [[Sidecar Fleet]] — the other seven services, all of which are paper
- [[Reconciliation]] — the bug that made this bot's risk controls blind
- [[Circuit Breaker]] — set to one loss here, versus eight on the platform
