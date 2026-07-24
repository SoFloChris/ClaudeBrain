---
type: concept
aliases: [evergreen note, permanent notes]
broader: "[[Second Brain]]"
inspired_by: "[[Andrej Karpathy]]"
related: ["[[Documentation Rot]]", "[[Context vs Connections]]"]
tags:
  - concept
created: 2026-07-24
---

# Evergreen Notes

Andy Matuschak's practice: notes "written and organized to evolve, contribute, and accumulate over time, across projects." The distinguishing claim is that this isn't about note-taking at all — *"'Better note-taking' misses the point; what matters is better thinking."*

## The five principles

1. **Atomic** — one idea per note, but the *whole* of that idea. Too broad and you won't notice new material about a notion buried inside; too fragmented and you shatter the link network. Matuschak is explicit that there's "no clear litmus test — just a bunch of tradeoffs."
2. **Concept-oriented** — factor notes by *concept*, not by book, author, project, or meeting. This is the one that changes filing behaviour most.
3. **Densely linked** — and this is also the maintenance mechanism (below).
4. **Prefer associative ontologies to hierarchical taxonomies** — links cut across fields; the temptation to navigate by hierarchy is a trap.
5. **Write for yourself by default**, disregarding audience.

## Why concept-orientation is the load-bearing one

Note-per-book or note-per-meeting feels natural and quietly fails: *"there's no accumulation."* Your new thoughts on a concept don't combine with the old ones — you end up with scattered notes about the same idea under different names, each buried in a larger document. Worse, there's *"no pressure to synthesize."*

This is the personal-vault version of the duplicate-docs problem in [[Documentation Rot]]: Google's "7 to 10 documents on setting up Borg" is the same failure at team scale.

## Linking as maintenance

The subtle payoff: *"finding the right links requires reading old notes, so it's also an organic mechanism for intermittently reviewing the notes we've written."* Matuschak calls this *evergreen note maintenance approximates spaced repetition* — a genuinely linked vault gets re-read as a side effect of being extended, which is why the linking discipline here is a maintenance rule rather than a tidiness one.

## Titles are APIs

Because `[[Title]]` is the call site, the title is the interface. The rules that follow: separation of concerns (atomicity), sharp titles as **complete declarative phrases**, positive framings. `Notes Should Be Atomic` over `Atomicity`. Bare nouns are reserved for defining core terms.

*"If you struggle to summarize a note in a sharp title, that's often a sign that your thinking is muddy or that the note is about several topics."*

## The exception this vault relies on

Person, company, and tool notes are **"weakly evergreen"** in Matuschak's own taxonomy — they aren't concept-oriented, so they aren't as useful to build on. Their job is different: *"targets for backlinks."* That's why `50-Wiki/People/` notes here are deliberately thin and nobody should try to fix that.

## Related

- [[Maps of Content]] — the navigation layer over a densely linked set of these
