---
type: concept
aliases: [fail closed, fail-closed, fail safe]
summary: "When a safety check can't run, the answer is no. A check that returns 'allow' on its own failure is not a check — it is an outage away from being absent."
related: ["[[Circuit Breaker]]", "[[Governed Tool Execution]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Safety Checks Should Fail Closed

**When a safety check cannot run, its answer is "no."**

The alternative — returning "allow" when the check is unavailable — quietly converts every dependency of that check into a bypass. The database is slow, so the risk query times out, so the trade goes through. Nobody wrote that rule; it emerged from an exception handler.

## The pattern in [[COMMAND — Quant Operations Platform]]

Three independent implementations, which is what makes it a convention rather than an accident:

| Mechanism | Failure | Behaviour |
|---|---|---|
| **Risk governor** auth | `RISK_GOVERNOR_TOKEN` not configured | Returns **503** on every risk endpoint — an unconfigured risk service refuses to approve anything |
| **Loss quarantine** | DB error reading trade history | Returns `blocked: true`, reason `loss_quarantine_unavailable` |
| **Order sealing** gate 14 | Last [[Reconciliation]] run >5 min ago | Refuses to seal — no trading on stale accounting |
| **Order sealing** gate 13 | Broker health check times out (5s) | Gate fails; intent is `gated_rejected` |

Each one costs availability to buy correctness. That's the trade, and it's the right way round for anything touching money.

## The counter-example in the same system

`/health` is the **only unauthenticated route** on the risk governor. Fail-closed applied to health checks would be self-defeating: an unreachable health endpoint makes the orchestrator unable to distinguish "down" from "locked", and `restart: always` never fires.

So the rule isn't "fail closed everywhere." It's **fail closed on the paths that authorize action, fail open on the paths that observe it.**

## Why it matters to me

This is the same claim as [[Circuit Breaker]]'s "a breaker an agent can reset is not a breaker," seen from the other side. There, the failure was the system *clearing* its own block; here, it's the system *never applying* one because the check errored.

The practical test to run on any guard I write: **assume the check throws. What happens?** If the answer is "the action proceeds," it isn't a guard — it's a suggestion with an exception handler.

## Related

- [[Circuit Breaker]] — the same principle applied to resetting rather than evaluating
- [[Governed Tool Execution]] — where the allow/deny/ask decision is made for agents
