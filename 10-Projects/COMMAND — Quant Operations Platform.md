---
type: project
summary: "Self-hosted quant research and execution platform: a 16-gate governed order pipeline, nine local models, and eight strategy sidecars. Paper on Alpaca; Kalshi is the one live-money exception."
status: active
repo: "https://github.com/SoFloChris/openclaw-ui"
people: ["[[Chris Aguirre]]"]
companies: ["[[Alpaca Markets]]"]
uses: ["[[Alpaca]]", "[[Ollama]]", "[[Claude Code]]", "[[RAG]]"]
related: ["[[Governed Tool Execution]]", "[[Strategy Promotion Ladder]]"]
---

# COMMAND — Quant Operations Platform

> Self-hosted quant research and execution platform: governed order pipeline, multi-model local AI, a fleet of strategy sidecars, full-stack observability. **Alpaca path is paper-only — [[Kalshi Bot]] is the one live-money exception.**

**Repo:** `SoFloChris/openclaw-ui` (private) · **Build:** V112 · **Status:** Active

> [!warning] Two things to get right about this system
> 1. **"9 gates" is overloaded.** The [[Strategy Promotion Ladder]] has **9 gates**; order sealing in `execution-authority.ts` runs **16**. The README conflates them.
> 2. **It is not uniformly paper-only.** Everything on [[Alpaca]] is paper. `kalshi-bot` trades **real money**, deliberately micro-sized (max **$2**/trade, $8 daily loss, one loss trips the breaker). The `$3` you'll see in a trailing comment beside `maxTradeUsd` is a superseded value, not the enforced one.

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

## Two execution architectures (the key structural fact)

They coexist, and only one is governed:

| Path | Who | Flow |
|---|---|---|
| **Governed** | Backend ICT bot → `ict-signal-sidecar` | Signal → `execution-authority.ts` → **16 gates** → sealed packet → broker outbox → worker → Alpaca |
| **Sidecar** | donchian, vwma, options, crypto-agent | Signal → `risk-governor` check → **direct Alpaca REST call** |

The sidecars never write [[Order Intent]]s, so they technically honour the [[Single Writer Rule]] — but they bypass the 16-gate pipeline entirely. Their governance substitute is the [[Risk Governor]]. Worth knowing before assuming every order is gated. Full service-by-service breakdown: [[Sidecar Fleet]].

**Hard safety constants** (verified in `trading-safety.ts`, not the docs): paper-URL assertion before every broker call · stop-loss can never be disabled · **$20,000** max single order · 50 max daily orders · **$5,000** hard daily-loss cap that config cannot override. See [[Circuit Breaker]].

> Docs drift here: `TRADING-SYSTEM.md` and `BRAIN_MAP.md` still say $10,000. Source says $20,000. See [[Config Lies, Code Wins]].

## Core services worth knowing

- `execution-authority.ts` — **single writer** for `order_intents`; **16-gate** evaluation + state machine ([[Order Intent]], [[Single Writer Rule]])
- `trading-safety.ts` — paper-mode enforcement, caps, circuit breaker
- `reconciliation-worker.ts` — 60s broker/DB drift repair; its freshness is itself gate 14 ([[Reconciliation]])
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

Equity $99,646.81 from a $100,000 start · 12 strategies (6 paper-active, 1 validated, 3 draft, 2 backtested) · ~11,785 [[Ghost Trades\|ghost trades]] · 58 backtest runs · 35 scheduled jobs · 793 agent runs.

Backlog: 16 tasks, 14 done — the one open item is splitting `BotDashboard.tsx` (1109 LOC) per the file-structure rule.

## Open questions

- What concrete evidence promotes a strategy from paper-active to live-ready? (Gate 9 is operator-explicit by design — worth writing down the personal bar.)
- Are the 56 dormant tables worth pruning, or is "0 rows ≠ unused" still protecting them?

## Related

- [[Sidecar Fleet]] — the eight standalone services and how they wire together
- [[Strategy Promotion Ladder]] — the 9 gates a strategy climbs, versus the 16 an order passes
- [[Set Up ClaudeBrain]] — the vault documenting this
- [[Claude Code]] — the agent harness both projects are built around
