---
type: concept
summary: "Every tool an agent can call passes a policy engine that classifies it by blast radius, and the dangerous tiers require an approval record before they run."
related: ["[[COMMAND — Quant Operations Platform]]", "[[Strategy Promotion Ladder]]"]
---

# Governed Tool Execution

The pattern from [[COMMAND — Quant Operations Platform]]: every tool an AI agent can call passes through a policy engine that classifies it by blast radius, and dangerous tiers require approval records before executing.

**Tiers:** `info` → `read` → `write` → `admin` → `dangerous`

- `policy-engine.ts` evaluates the tier
- `dispatcher.ts` runs a 9-step pipeline around every governed call (131 tools across 17 categories)
- `approval-manager.ts` records approvals for anything in the "ask" tier

## Why it matters to me

This is the answer to "how do you let agents act without letting them wreck things." Not prompt-level pleading ("please be careful") but a **structural chokepoint**: the agent cannot reach a dangerous capability except through code that checks authorization and writes an audit record.

The key property is that governance is **unbypassable by design** — including by the agent improving itself. Self-improvement and schema evolution stay approval-gated, which is what stops a capable agent from quietly widening its own permissions.

Worth stealing for any agent system: classify tools by reversibility, gate the irreversible ones, and log every decision.

## Related

- [[Claude Code]] — hooks are the lightweight version of this idea
