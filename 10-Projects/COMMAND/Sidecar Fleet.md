---
type: reference
project: "[[COMMAND — Quant Operations Platform]]"
aliases: [COMMAND sidecars, services topology, strategy containers]
summary: "Reference map of COMMAND's eight standalone service containers — what each one does, what it talks to, and which of the two execution paths it takes."
related: ["[[Risk Governor]]", "[[Kalshi Bot]]"]
tags:
  - reference
created: 2026-07-24
---

# COMMAND — Sidecar Fleet

Reference for the eight standalone containers under `services/` in [[COMMAND — Quant Operations Platform]]. Each has its own Dockerfile, `package.json`, and `src`; none of them import from `packages/server/`.

Shared conventions: Node 22 + `tsx` (one Python exception), `ws` for WebSockets, `better-sqlite3` against the shared DB file, plain `node:http` servers with no framework, `/health` + `/status` endpoints, `network_mode: host`, and a `TRADING_EXECUTION_ENABLED` kill switch that degrades any bot to signal-only logging.

## Topology

```
Alpaca stock WS (IEX) ─┐
Alpaca crypto WS ──────┴─→ market-data-bus :8092 ──(WS fan-out)──┐
                                                                  ├→ donchian-bot :8094  (equities)
                                                                  ├→ crypto-agent  :8095  (crypto)
                                                                  └→ vwma-bot      :8097  (OFF)
options-bot :8096 ──(REST polling, no bus)───────────────────────┘
        │
        └─ all four ─→ risk-governor :8093 ─→ Alpaca (broker truth)
        │
        └─ all four ─→ write `position_stops` ─→ platform Exit Manager

kalshi-bot        :8091 — fully self-contained; shares only the SQLite file
ict-signal-sidecar:8090 — pure compute, called by the *backend*, not by the bots
```

## The fleet

| Service | Port | Job | Execution path |
|---|---|---|---|
| `market-data-bus` | 8092 | Single Alpaca WS per feed, fanned out locally | none (infrastructure) |
| [[Risk Governor\|risk-governor]] | 8093 | Cross-bot portfolio risk; every bot calls before ordering | none (gatekeeper) |
| `donchian-bot` | 8094 | [[Donchian Channels]] 20/10 breakout on equities, long-only | sidecar (direct REST) |
| `crypto-agent` | 8095 | 3-signal crypto ensemble; [[Loss Quarantine]] lives here | sidecar (direct REST) |
| `options-bot` | 8096 | Cash-secured puts on an RSI(2) oversold trigger | sidecar (direct REST) |
| `vwma-bot` | 8097 | [[Volume-Weighted Moving Average]](10) crypto breakout — **profiled off** | sidecar (disabled) |
| [[Kalshi Bot\|kalshi-bot]] | 8091 | Kalshi BTC binary contracts — **the live-money exception** | own venue, own risk |
| `ict-signal-sidecar` | 8090 | Python; pure [[ICT Smart Money Concepts]] signal computation | none (compute only) |

## Two facts that surprise people

**1. Only one path is gated.** The backend ICT bot goes through `execution-authority.ts` and its 16 gates. The four sidecar bots call the risk governor and then hit Alpaca's REST API **directly**. They honour the [[Single Writer Rule]] in the narrow sense — they never write `order_intents` — while bypassing the [[Order Intent]] pipeline entirely.

**2. `market-data-bus` exists for a quota, not an abstraction.** Its header says so: *"Solves: Alpaca connection limit (1 connection per feed per API key)."* Without it every strategy container needs its own broker socket and they collide. It normalises ticks to `{T:'t', S, p, s}`, rewrites `BTC/USD` → `BTC-USD`, reconnects with backoff capped at 60s, and runs a watchdog that force-reconnects if no tick arrives for 300 seconds.

## Notable per-service details

- **`donchian-bot`** — 3-day post-loss cooldown; regime gate requires SPY above its 200-day MA; `closePosition` is explicitly 3-phase (close at broker accepting 200 *or* 404 → clear local state *immediately* → best-effort DB cleanup), so a DB failure can't strand a phantom position.
- **`crypto-agent`** — universe narrows from 36 liquid majors to 5 core names to, in production, **two symbols** (`BTC-USD, ETH-USD`). Its `profit-engine.ts` records every exit-parameter change with the reason: breakeven moved to +1.5R *"(was 0.8R — too early, killed runners in chop)"*, partials to 30% at +2.5R *"(was 50% @ 1.2R — cut profit runs short)"*, risk distance floored at 1.5% *"so noise does not invent tiny R."*
- **`options-bot`** — 12 tickers with individually tuned RSI thresholds (XBI at 18, AAPL at 22, TLT at 30); takes profit at 50% of credit captured; time-exits at 5 DTE to dodge gamma and assignment; trades only 10:00–15:30 ET, *"avoid open/close chaos."*
- **`ict-signal-sidecar`** — the only Python service, and deliberately so. Its header: *"This is an EXACT copy of the proven `live_signals.py` logic. Do NOT simplify, change thresholds, or port to TypeScript."* A polyglot boundary drawn purely to protect backtest/live fidelity.

## Related

- [[COMMAND — Quant Operations Platform]] — the platform these services hang off
- [[Risk Governor]] — the one component every sidecar must call
- [[Kalshi Bot]] — the fleet member that trades real money
