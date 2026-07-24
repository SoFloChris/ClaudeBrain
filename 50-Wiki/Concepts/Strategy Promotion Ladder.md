---
type: concept
related: ["[[COMMAND — Quant Operations Platform]]", "[[Governed Tool Execution]]"]
---

# Strategy Promotion Ladder

The 9-gate sequence a trading strategy must climb in [[COMMAND — Quant Operations Platform]] before it can touch real money. Each gate is a checkpoint that must pass explicitly — nothing advances by default.

1. **Draft** — strategy exists
2. **Backtested** — historical performance measured
3. **Ghost-traded** — simulated live positions tracked
4. **Walk-forward** — validated out-of-sample (a hard gate, not advisory)
5. **Evaluated** — scored across domains
6. **Evidence reviewed** — a human looks at the artifacts
7. **Admin approved** — explicit authorization
8. **Paper-active** — trading with real market data, fake money
9. **Live-ready** — operator-explicit only; never automated

## Why it matters to me

It's the clearest expression of the design philosophy in COMMAND: **the burden of proof runs uphill.** A strategy is guilty until proven profitable, and the expensive gates (walk-forward, evidence review) sit before the ones that risk capital.

The generalizable lesson beyond trading: when a system can act autonomously, the safety comes from staged promotion with irreversible-action gates at the end — not from the agent being careful.

## Related

- [[Governed Tool Execution]] — the same philosophy applied to tool calls
