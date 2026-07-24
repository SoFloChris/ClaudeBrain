---
type: tool
summary: "The brokerage API COMMAND executes through - paper only, with a reconciliation worker syncing broker truth every 60s."
built_by: "[[Alpaca Markets]]"
related: ["[[COMMAND — Quant Operations Platform]]"]
---

# Alpaca

Commission-free brokerage API used by [[COMMAND — Quant Operations Platform]] for order execution. Currently **paper trading only** (`paper-api.alpaca.markets`).

## Key facts

- Integration lives in `alpaca.ts`; orders flow through `broker-worker.ts` (5s outbox processing, 30s order polling, fill tracking).
- A reconciliation worker syncs Alpaca state every 60s so local state can't silently drift from the broker's.
- `ALPACA_BASE_URL` **must contain `paper-api`** — this is an enforced safety assertion, not a convention.
- Also serves market data quotes alongside Yahoo Finance.
- IBKR Gateway is architecture-ready as an alternative broker (port 4002) but not active.

## Related

- [[Strategy Promotion Ladder]] — what a strategy must pass before Alpaca ever sees an order
