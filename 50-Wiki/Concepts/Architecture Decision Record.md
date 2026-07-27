---
type: concept
summary: "The value of an ADR is the context, not the decision - you will remember what you chose and forget what forced it."
aliases: [ADR, ADRs]
related: ["[[Documentation Rot]]", "[[Diataxis]]"]
tags:
  - concept
---

# Architecture Decision Record

A short document capturing one significant decision, the context that forced it, and the consequences accepted. The point isn't the decision — you'll remember *what* you chose. The point is the **context**, which you will absolutely forget, and without which future-you can't tell whether the decision still holds.

## Why it matters to me

ADRs are the one documentation form that **doesn't rot**, because they're explicitly historical. A "current architecture" page goes stale the moment the architecture moves; an ADR dated 2026-07-24 stays true forever — it's a record of what was decided *then*, with what was known *then*.

That's why project master notes here carry an *index* of decisions rather than the decisions themselves: the volatile summary and the durable record have different lifecycles and shouldn't share a file.

### The numbering hazard, learned the hard way

Sequential numbers are the one part of the format that doesn't survive parallel work. Two agent sessions on separate branches will each read the `decisions/` folder *as their branch sees it*, each conclude the next number is 0005, and each be right locally and wrong globally.

That happened in this vault. Three ADRs written on `claude/obsidian-second-brain-setup-0c0jdy` as 0005 and 0006 landed on `main` as **0007** and **0008**, because a different 0005 and 0006 had been merged meanwhile. The branch's copy survived as a duplicate sitting at a number that by then meant something else entirely — the kind of conflict git cannot detect, since both sides only ever *added* files.

Two things follow. **Check the default branch before claiming a number**, and when adopting an unmerged ADR, **restate its numbers against the vault as it actually is** rather than preserving the ones it was born with — which is what `ADR-0007` does explicitly in its opening line.

## The two formats

**Nygard (2011)** — the original, five sections: Title, Status, Context, Decision, Consequences. Minimal enough that there's no excuse not to write one.

**MADR 4.0** — adds what Nygard omits: `Decision Drivers`, `Considered Options`, and per-option pros/cons, plus a **Confirmation** section asking how you'd verify the decision is actually being followed. That last one is the sharpest question in the template — most decisions have no enforcement, and writing "none" is itself informative. This vault's `ADR.md` template follows MADR.

## Conventions worth keeping

- **Filename:** `NNNN-title-with-dashes.md`, zero-padded, in a `decisions/` folder beside the project note.
- **Take the number from the default branch, not from your own.** A sequential number is a *claim on a shared namespace*, and a branch is the one place you can't see who else has claimed it.
- **When to write one:** when future-you would ask "why on earth is it like this?" Not for tiny, reversible, or temporary choices.
- **Superseding is bidirectional:** the new ADR gets `supersedes`, the old gets `superseded_by` and a status change. Never delete a superseded ADR — the wrong turn is part of the record.
- **Context and Decision are immutable once accepted.** Later learning goes in an appended, dated `## Amendments` section. In practice most teams allow this pragmatic mutability rather than pure immutability.

## Related

- [[Documentation Rot]] — ADRs are the antidote, because they never claim to be current
- [[Diataxis]] — an ADR is *explanation*; keeping it out of reference docs is the whole discipline
