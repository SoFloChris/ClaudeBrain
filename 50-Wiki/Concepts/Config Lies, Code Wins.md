---
type: concept
aliases: [config drift, code is the source of truth, verify against source]
summary: "Documentation and config files describe intent; only the source describes behaviour. When they disagree — and at scale they always do — the code is the fact."
related: ["[[Documentation Rot]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Config Lies, Code Wins

Documentation states intent. Config states *requested* intent. Only the source states behaviour. At any real scale these three diverge — so **when writing something down as a fact, read the code.**

This is [[Documentation Rot]] narrowed to a specific, checkable rule: for any constant, threshold, or limit, cite the file it's enforced in — not the doc that describes it.

## Three live examples from [[COMMAND — Quant Operations Platform]]

Each is a different *mechanism* of divergence, which is why all three are worth keeping:

**1. Config asks, code clamps.** `docker-compose.yml` sets `RISK_MAX_POSITIONS=10` and `RISK_MAX_CORRELATION=0.85`. The risk governor silently clamps them to its own bounds — **8** and **0.75**. The operator's stated configuration is not the running configuration, and nothing warns.

**2. Docs lag source.** Two documents state a $10,000 max single order. `trading-safety.ts` enforces **$20,000**. Four other documents say $20,000 correctly — so a majority vote among docs would have got it right, and reading any single doc would have got it wrong.

**3. The same constant, defined four ways.** Kill-zone session times appear in ET in one doc, UTC in another, with different hours again in the config and in the backtester. There is no "correct" doc to find; the backtester and the live path are simply testing different things.

## The failure mode this creates

Divergence 1 is the dangerous one, because it inverts trust. Reading the compose file feels like reading the source — it's in the repo, it's version-controlled, it's specific. But it records what somebody *asked for*, and the clamp that overrode it lives elsewhere. **A config value is an input to behaviour, not a statement of it.**

## Why it matters to me

The rule I want out of this, for note-taking as much as for engineering: **a fact worth recording is worth tracing to its enforcement point.** When I write "the cap is $20,000" into a note, the note should be able to say *where* — because in a year the docs will have drifted again and the citation is the only thing that lets me re-check.

Corollary, and the reason COMMAND generates its architecture docs mechanically: **the doc that can't drift is the one nobody writes by hand.**

## Related

- [[Documentation Rot]] — the general decay this is one mechanism of
- [[COMMAND — Quant Operations Platform]] — where all three examples live
