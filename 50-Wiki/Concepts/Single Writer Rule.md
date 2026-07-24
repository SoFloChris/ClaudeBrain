---
type: concept
aliases: [single writer, table ownership, one writer per table]
summary: "Exactly one service may write a given canonical table; everyone else reads or calls that service — an application-level contract that buys state-machine integrity, not just lock avoidance."
related: ["[[Order Intent]]", "[[Governed Tool Execution]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Single Writer Rule

**Exactly one service is allowed to `INSERT`/`UPDATE` a given canonical table.** Everyone else reads it, or calls that service. It is an *application-level ownership contract*, not a database constraint — which is why it needs enforcement machinery to survive.

## Three reasons, only one of which is about locks

[[COMMAND — Quant Operations Platform]] states all three:

1. **Write contention.** SQLite WAL mode allows concurrent readers but a single writer; multiple write paths produce `SQLITE_BUSY`. The repo's known-error catalog literally maps that error to *"Check single-writer rule in `TABLE_OWNERSHIP_MATRIX`."*
2. **State-machine integrity.** If only `execution-authority.ts` can transition [[Order Intent]] rows, illegal transitions become impossible *by construction* — no route, scanner, or UI handler can shortcut a gate.
3. **Auditability.** One writer means one place to log, one place to emit events, one place to enforce invariants.

Reason 2 is the one worth carrying to systems that have no lock problem at all.

## Making it stick

A rule agents can't check is a rule agents will break. COMMAND enforces it with:

- a **generated** `TABLE_OWNERSHIP_MATRIX.md` (deterministic, no LLM) that agents must consult before adding any DB write;
- a CI script, `scripts/check-table-ownership.sh`;
- an always-on rule file loaded into every agent session.

Sample ownerships: `order_intents` → execution-authority · `positions_live` → reconciliation · `ai_memory` → memory-store · `approvals` → approval-manager (**many requesters, single resolver**).

## Where it bends — and that's the honest part

The sidecar bots each open the same SQLite file and write `position_stops` directly; `options-bot` even creates its own table at boot. They set `busy_timeout = 5000` to cope. A real deviation, mitigated by each bot owning **distinct rows**.

Worth recording rather than hiding: a stated invariant with a known, bounded exception is more useful than one everybody quietly violates.

## Why it matters to me

The generalizable claim: **the cheapest way to make an invalid state unreachable is to reduce the number of places that can produce it to one.** Validation scattered across five writers is five chances to forget; one writer is one place to be correct.

The corollary is about agents specifically — the same reason [[Governed Tool Execution]] funnels every tool call through one dispatcher. A single choke point is the only kind of rule an autonomous system can't route around.

## Related

- [[Order Intent]] — the canonical example: one writer, one state machine
- [[Governed Tool Execution]] — the same choke-point argument applied to tool calls
