---
type: reference
project: "[[COMMAND — Quant Operations Platform]]"
aliases: [risk-governor, portfolio risk service]
summary: "COMMAND's shared cross-bot risk service: every strategy container must ask it before placing an order, and it answers from broker truth rather than its own bookkeeping."
related: ["[[Sidecar Fleet]]", "[[Safety Checks Should Fail Closed]]", "[[Circuit Breaker]]"]
tags:
  - reference
created: 2026-07-24
---

# Risk Governor

The shared portfolio-risk service in [[COMMAND — Quant Operations Platform]] (port 8093). Its header states the contract: *"Every strategy container must call this BEFORE placing any order."*

It is the governance substitute for the four sidecar bots that bypass the [[Order Intent]] pipeline — see [[Sidecar Fleet]]. Deliberately standalone: *"does NOT import from `packages/server/`."*

## API

| Endpoint | Purpose |
|---|---|
| `POST /can-open` | Atomically **check and reserve** a slot |
| `POST /release` | Undo the reservation when the order fails |
| `POST /record-close` | Report realized P&L |
| `GET /state`, `GET /health` | Inspection |
| `POST /reset` | Clear a halt — requires body `{"confirm":"RESET_RISK_GOVERNOR"}` |

**Check-and-reserve in one call** is the important design choice. A separate "may I?" and "I did" would race: two bots could both be told yes before either took the slot.

Auth is a bearer token, and the service returns **503 on every risk endpoint if the token isn't configured** — [[Safety Checks Should Fail Closed]] in one line. `/health` is the sole unauthenticated route, so an orchestrator can still tell "down" from "locked."

## Checks, in order

halted → max positions → daily loss → weekly loss → consecutive losses → input validation → direct-crypto toggle → vol-scaled notional cap → gross exposure → correlation cluster. Only then does it increment `openPositions` and record the symbol.

## Configuration — and its clamps

| Setting | Default | Hard clamp |
|---|---|---|
| `maxPositions` | 6 | 1–8 |
| `maxDailyLoss` | $930 | — |
| `maxWeeklyLoss` | $2,325 | — |
| `maxConsecutiveLosses` | 3 | 1–5 |
| `maxNotionalPct` | 0.12 | 0.01–0.20 |
| `maxGrossExposure` | 0.55 | 0.01–0.70 |
| `targetAnnualVol` | 0.10 | 0.01–0.20 |
| `volScaleCap` | 1.25 | 0.1–1.25 |
| `maxCorrelation` | 0.75 | 0.1–0.75 |

> [!warning] The compose file asks for more than the code allows
> `docker-compose.yml` sets `RISK_MAX_POSITIONS=10` and `RISK_MAX_CORRELATION=0.85`. Both are **silently clamped** to 8 and 0.75. The running configuration is not the stated one — see [[Config Lies, Code Wins]].

## Two mechanics worth understanding

**Volatility targeting.** `getVolScaler()` annualizes the standard deviation of the last 20 daily returns (× √252) and scales notional by `targetAnnualVol / annualVol`, capped at `volScaleCap`. It needs ≥5 daily returns before it does anything — so a fresh deployment sizes normally until it has a volatility estimate, rather than guessing.

**Correlation clusters.** A hardcoded map — `semiconductor`, `crypto_proxy`, `crypto`, `mega_tech`, `ev_energy`, `speculative`, `index_etf`, `industrial` — with a default of **one open position per cluster** (crypto excepted, up to 3). Crude compared with a live correlation matrix, and considerably harder to fool: six "different" semiconductor names are one bet, and a hardcoded map knows that on day one.

## Operational details

- **Broker truth sync every 60s** from Alpaca's positions and account endpoints, with a **$10 dust filter** so uncloseable residual positions don't consume risk slots.
- **Persistence to `state.json`**, so a halt survives a restart. A [[Circuit Breaker]] that a container restart clears isn't one.
- Daily reset on ET calendar rollover, pushing the day's P&L onto a 60-entry ring of daily returns.
- Auto-halts at the consecutive-loss cap; clears **only** via the authenticated reset with its confirm phrase.

## Related

- [[Sidecar Fleet]] — the bots required to call this before every order
- [[Safety Checks Should Fail Closed]] — the 503-without-token behaviour, stated as a principle
- [[Config Lies, Code Wins]] — the clamp gotcha above, generalised
