---
type: concept
aliases: ["agent workspace pattern", "skill pack architecture", "domain agent workspace"]
broader: "[[Second Brain]]"
inspired_by: "[[ColdIQ]]"
related: ["[[Claude Code]]", "[[Second Brain]]"]
---

# Skills Are Verbs, Notes Are Nouns

A working agent workspace splits into two halves that must not be merged: **notes hold the nouns** (what is true — entities, decisions, reference material) and **skills hold the verbs** (how to do a repeatable job). Confusing them produces either a vault full of procedures nobody executes, or skills that hard-code facts that change.

## Why

Every mature [[Claude Code]] workspace I've seen converges on the same four-part shape, regardless of domain:

| Part | This vault | An outbound-sales workspace |
|---|---|---|
| **Router** | `CLAUDE.md` — who I am, where things live | `CLAUDE.md` — operating rules |
| **Memory** | `90-System/Memory.md` (auto-loaded) | `memory.md` — session memory |
| **Canonical brief** | `Home.md` + project notes | `outreach-brief.md` — the one true campaign brief |
| **Skills** | `/recall`, `/graph`, `/wrap` — 6 commands | 40 skills in 7 folders |
| **Data** | the notes themselves | `data/connections.md` + `raw/` CSV cache |

The outbound example is worth studying because it's the same architecture pointed at revenue instead of recall. Its 40 skills group into a **pipeline, in execution order** — strategy (`icp-definer`, `persona-definer`, `pain-identifier`, `offer-definer`) → list-building → copywriting → outreach channel → campaign assembly → replies → automation. The folder names *are* the workflow. Someone reading the tree learns the process.

**What that teaches this vault:**

1. **Name skills as verbs on a noun.** `icp-definer`, `reply-handler`, `n8n-debugger`. Mine already follow it — `process-inbox`, `remember`, `recall`. A skill named for a topic instead of an action is a note in the wrong folder.
2. **One canonical brief, referenced by every skill.** Their `outreach-brief.md` is the single source of campaign truth so 40 skills can't drift apart. This vault's equivalent is `CLAUDE.md` + `Memory.md` — which is exactly why durable facts belong there and not restated inside commands.
3. **Separate the cache from the knowledge.** `data/raw/` holds cached CSV outputs; `data/connections.md` holds the distilled integration map. Same distinction as [[Context vs Connections]] — and the reason scraped output never becomes a note.
4. **Skills encode benchmarks, notes don't.** Their `copywriting-analyzer` and `outbound-analyst` both carry the same 244k-campaign benchmark data. Reference data that a *procedure* needs lives with the procedure.

## When it breaks

Forty skills is a lot of surface for one person to maintain, and skill packs rot faster than notes do — every one of those outbound skills has a dependency on a vendor's API or export format that can change without warning. Notes about a person stay true; a skill that scrapes a site is true until Tuesday.

The honest read: **borrow the shape, not the volume.** This vault needs six good commands, not forty. Add the seventh when a job is repeated three times by hand — the same trigger rule as [[Second Brain Levels]].

## Related

- [[Claude Code]] — the harness that defines skills, commands, and the router
- [[Context vs Connections]] — the same cache-vs-knowledge line, drawn at the vault door
- [[ColdIQ]] — the outbound skill pack this pattern was reverse-engineered from
