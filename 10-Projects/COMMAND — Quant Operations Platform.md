---
type: project
summary: "An autonomous quant trading lab where no strategy reaches real money without clearing nine explicit governance gates — paper-live on Alpaca."
status: active
repo: "https://github.com/SoFloChris/openclaw-ui"
people: ["[[Chris Aguirre]]"]
companies: ["[[Alpaca Markets]]"]
uses: ["[[Alpaca]]", "[[Ollama]]", "[[Claude Code]]", "[[RAG]]"]
related: ["[[Governed Tool Execution]]", "[[Strategy Promotion Ladder]]"]
---

# COMMAND — Quant Operations Platform

> Institutional-grade autonomous quantitative trading lab: 9-gate governance, multi-model AI, full-stack observability. **Paper trading live on [[Alpaca]].**

**Repo:** `SoFloChris/openclaw-ui` (private) · **Build:** V112 · **Status:** Active, paper-live

## Outcome

A trading platform where no strategy reaches real money without passing an explicit, auditable gate sequence — and where AI agents can extend the system without ever bypassing that governance.

## Architecture at a glance

| Layer | Stack |
|---|---|
| Backend | Node.js 22 + Fastify + TypeScript |
| Frontend | React 19 + Vite + Zustand + Tailwind (51 lazy-loaded panels) |
| Database | SQLite WAL — single file, 217 tables (161 active, 56 dormant) |
| AI/LLM | [[Ollama]] (9 local models), [[Anthropic]], OpenAI, Google, xAI |
| Containers | 7 Docker services via docker-compose |
| GPU | NVIDIA RTX PRO 6000 (96 GB VRAM) |
| Broker | [[Alpaca]] paper; IBKR Gateway architecture-ready (port 4002) |
| Markets | BTC/USD, ETH/USD, US equities |

Monorepo: `packages/{server,client,shared,tests}` (pnpm workspaces), plus standalone `services/` bots — donchian, vwma, options, crypto, kalshi, risk-governor, ict-signal-sidecar, market-data-bus.

## The trading pipeline

```
ICT signal detection (4-layer)
  → bot signal pipeline (validation + scoring)
  → 9-gate promotion ladder  ← see [[Strategy Promotion Ladder]]
  → execution authority (single writer, state machine)
  → Alpaca paper trading
  → reconciliation worker (60s state sync)
```

**Safety controls:** paper-mode assertion, stop-loss required, $20K max single order, 50 max daily orders, circuit breaker on drawdown.

## Core services worth knowing

- `execution-authority.ts` — **single writer** for `order_intents`; 9-gate evaluation + state machine
- `trading-safety.ts` — paper-mode enforcement, caps, circuit breaker
- `policy-engine.ts` — tiered evaluation (info / read / write / admin / dangerous) — see [[Governed Tool Execution]]
- `dispatcher.ts` — the 9-step governed tool pipeline (131 governed tools, 17 categories)
- `model-router.ts` / `model-exchange.ts` — local-first, cost-aware LLM routing across 5 providers
- `walk-forward.ts` — walk-forward validation; a **hard gate** for paper promotion
- `memory-store.ts` / `rag-pipeline.ts` — AI memory with embedding search and decay ([[RAG]])

## Invariants (never weaken)

These are the standing constraints from the repo's session contract — the rules an agent must not "helpfully" refactor away:

1. **Paper trading only** unless the operator explicitly enables live.
2. **No path bypasses governance** — self-improvement and schema evolution stay approval-gated. The safety core (`execution-authority`, `policy-engine`, `trading-safety`) is off-limits.
3. **Single writer per canonical table** — check the table-ownership matrix before adding writes; migrations only in `db.ts` / `v*-migrations.ts`.
4. **Real state only** — never invent routes, tables, services, UI tabs, or broker behavior.
5. **Batch, don't one-shot** — extend rather than rebuild; update `claude-progress.txt` before every commit.

## Documentation map (in-repo)

The repo practices progressive disclosure — `CLAUDE.md` is the contract, `docs/INDEX.md` the map:

- **Generated truth** (never hand-edit): `docs/system/` — `ARCHITECTURE.md`, `SERVICE-MAP.md`, `ROUTE-MAP.md`, `TABLE_OWNERSHIP_MATRIX.md`, `TOOL_CATALOG.md`
- **Decisions**: `docs/decisions/` (ADR-001 ECharts as primary charts; ADR-005 VPS 24/7 overnight operation)
- **Runbooks**: `docs/runbooks/TOOLBOX_RUNBOOK.md`, `docs/system/RUNBOOKS.md`
- **Rules**: core rules auto-load from `.claude/rules/`; reference rules in `docs/rules/` load on demand

## Operations

```bash
docker compose up -d --build      # launch all 7 containers
curl -s localhost:3001/api/health # verify
pnpm typecheck && pnpm verify     # typecheck + test + health + screenshot
```

Ports: frontend 8080 · backend 3001 · Ollama 11434 · docker proxy 2375 · IBKR 4002.

## Current state (last snapshot)

Equity $99,646.81 from a $100,000 start · 12 strategies (6 paper-active, 1 validated, 3 draft, 2 backtested) · 6,063 ghost trades · 58 backtest runs · 35 scheduled jobs · 793 agent runs.

Backlog: 16 tasks, 14 done — the one open item is splitting `BotDashboard.tsx` (1109 LOC) per the file-structure rule.

## Open questions

- What concrete evidence promotes a strategy from paper-active to live-ready? (Gate 9 is operator-explicit by design — worth writing down the personal bar.)
- Are the 56 dormant tables worth pruning, or is "0 rows ≠ unused" still protecting them?

## Related

- [[Set Up ClaudeBrain]] — the vault documenting this
- [[Claude Code]] — the agent harness both projects are built around
