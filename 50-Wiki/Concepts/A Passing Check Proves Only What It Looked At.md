---
type: concept
summary: "A check that answers a narrower question than the one you asked returns the same clean output as one that answers it properly — so a green result is evidence of scope, not of correctness."
aliases: ["silent under-reporting", "false clean", "check scope", "verify the verifier"]
related: ["[[Config Lies, Code Wins]]", "[[Documentation Rot]]"]
---

# A Passing Check Proves Only What It Looked At

Every check answers some question. When it answers a **narrower** one than you intended, the output is indistinguishable from success: no error, no anomaly, just a clean result that means less than you think it does.

This is not carelessness. All four instances below came from checks that were correctly written for the question their author had in mind, run by someone asking a slightly larger one.

## The evidence

Four instances in a single day (2026-07-27), all in this vault or its tooling:

| The check | The question it answered | The question being asked |
|---|---|---|
| `brain_graph`'s frontmatter regex | "what's the first item in this list?" | "what are the items in this list?" |
| `vault_stats` note keying | "what notes exist, keyed by filename?" | "what notes exist?" — seven `_Index.md` collapsed to one |
| Salvage completeness diff | "which file *paths* exist only on that branch?" | "what content exists only on that branch?" |
| A grep for `check(N, 'name'` | "which gates are declared on one line?" | "which gates exist?" — five were multi-line |

Three of the four were caught only because **a number failed to move when it should have**: an edge count that didn't rise when a link was added, a `uses` list that grew without the graph growing. The fourth was caught because its answer was too strange to accept — "gates 7 through 10 don't exist" is not a shape real code takes.

Note what didn't catch any of them: reading the output carefully. It was internally consistent and entirely plausible every time.

## Why it matters

It's the whole argument for [[0006-enforce-invariants-in-ci|ADR-0006]]. A health report cannot flag what it never examined, so the answer isn't a better report — it's a check that **fails**, plus a test that pins the check itself. `test_brain_graph.py` and `test_vault_stats.py` exist because the tools were wrong in ways their own output couldn't show.

## The countermeasures that actually worked

- **Watch for numbers that don't move.** Add a sixth item and confirm the count goes to six. A silent under-reporter is invisible in absolute terms and obvious in deltas.
- **Distrust a suspiciously clean result on a messy question.** "Nothing left to salvage" from a 109-file branch deserved a second look; it got one, and was wrong.
- **Distrust a suspiciously strange result too.** The gate-count grep was wrong in the *alarming* direction, which is what made it survivable — a false alarm gets investigated, a false all-clear does not.
- **Verify the verifier against a known-bad input.** Every regression test written this day was confirmed to fail against the pre-fix code, not merely to pass against the fixed one.

## When it breaks

Taken too far this is paralysis — you cannot verify every verifier, and most checks are fine. The trigger is narrower: **be suspicious when a check's answer would look the same whether or not it did its job.** A test that fails loudly on a narrow reading needs none of this; a grep, a count, or a path comparison earns the scrutiny because its failure mode is silence.

## Related

- [[Config Lies, Code Wins]] — the sibling failure: there the *documentation* is narrower than the truth, here the *tool* is
- [[0006-enforce-invariants-in-ci|ADR-0006]] — the decision this pattern forced, after two instances in one hour
- [[brain_graph]] — where the first instance lived, and where its test now guards the parser
