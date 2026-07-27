---
type: adr
status: accepted
date: 2026-07-27
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[brain_graph]]", "[[Graphify]]"]
tags:
  - adr
---

# ADR-0006 — Enforce vault invariants in CI, not just report them

## Context and Problem Statement

The vault had a health tool from the start: `vault_stats.py` reports orphans, stubs, and broken links, and a SessionStart hook prints its summary into every session. It always exits 0. Nothing in the repo could fail.

On 2026-07-27 two bugs surfaced within an hour of each other, both in that same machinery:

1. **`brain_graph.py`** — the inline-list regex excluded `[` and `]`, so a frontmatter list like `uses: ["[[A]]", "[[B]]", "[[C]]"]` produced an edge for the **first item only**. Every multi-value typed predicate in the vault was affected; the graph reported 249 edges when it had 270.
2. **`vault_stats.py`** — notes were keyed by filename stem, so all seven `_Index.md` files collapsed into one dict entry. Six were discarded, taking their outbound links with them, which is why links to `90-System/Templates/` had never actually been validated.

Neither threw an exception. Neither produced a broken link, an orphan, or any visible symptom. Both had survived a full `/vault-status` pass **whose output was read carefully and reasoned from**. The first was caught only because a `uses` list grew from five items to six and the edge count didn't move.

That is the shape of the problem: **a report that under-counts is indistinguishable from a vault with less in it.** More careful reading would not have caught either bug, because the output was internally consistent and entirely plausible.

## Decision Drivers

- Both bugs were silent under-reporters, and silence is exactly what a health report cannot flag.
- The vault is the system of record for a knowledge graph; an edge that silently doesn't exist is worse than one that visibly fails.
- Third-party code now lives in the repo (ADR-0005), which raises the cost of "nothing checks anything".
- A parts bin was already available: the abandoned [[Graphify]] branch had a working CI workflow, secret guard, and pre-commit hooks.

## Considered Options

- Keep reporting only, and read the reports more carefully
- Add tests, run them by hand
- Enforce in CI on every push and PR

## Decision Outcome

Chosen option: **enforce in CI**. `.github/workflows/vault-check.yml` runs on every PR and push to `main`: broken wikilinks → script regression tests → graph builds → secret guard → shellcheck.

The reporting tools stay exactly as they are. `vault_stats.py` remains a *report* that always exits 0 — it answers "what should I write next", which is a human question with no correct threshold. `check_links.py` is its enforcing counterpart and answers "is anything actually broken", which is binary. **Conflating the two would make the vault fail a build over two thin company notes**, which are correct by design.

### Consequences

- Good, because the two specific bugs are now pinned by 16 regression tests, verified to fail against the original code rather than assumed to.
- Good, because `check_links.py` and `vault_stats.py` are asserted to agree on broken links, so the two tools can't drift into contradicting each other.
- Good, because secrets are now mechanically blocked rather than only forbidden by a sentence in `Memory.md`.
- Bad, because a notes vault now has a build that can go red — a genuinely new failure mode for a repo whose point is writing things down. Mitigated by keeping the checks fast (~8 seconds) and few.
- Bad, because CI is a merge gate that didn't exist before, on a repo where the author is the only committer and often on a phone.
- Bad, because the checks only cover what someone thought to test. Neither bug would have been caught by a test written before it was found.

### Confirmation

The suite runs on every PR. Both regression suites were verified to *fail* against the pre-fix code — 3 failures for the parser, 3 failures and 3 errors for the keying — rather than merely passing against the fixed version.

## Pros and Cons of the Options

### Reporting only, read more carefully

- Good, because zero infrastructure, and nothing can block a merge.
- Bad, because it is precisely what was already in place when both bugs shipped and survived a review pass. The failure mode is invisible output, not inattentive reading.

### Tests run by hand

- Good, because it catches the bug class without a merge gate.
- Bad, because a test suite nobody is required to run degrades to a test suite nobody runs — the same drift ADR-0004 added hooks to prevent.

## More Information

Falsified if the build starts going red for reasons that don't matter, or if merging from a phone becomes painful enough to route around. The fix in that case is to drop checks, not to stop enforcing — a suite of five fast, high-signal checks is the whole design.

Ported from `claude/graphify-obsidian-integration-m15xef`; see [[Graphify]] for why only the hygiene was taken and the graph integration left dead.

## Amendments

<!-- Append only. -->
