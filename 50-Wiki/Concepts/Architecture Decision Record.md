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

## The two formats

**Nygard (2011)** — the original, five sections: Title, Status, Context, Decision, Consequences. Minimal enough that there's no excuse not to write one.

**MADR 4.0** — adds what Nygard omits: `Decision Drivers`, `Considered Options`, and per-option pros/cons, plus a **Confirmation** section asking how you'd verify the decision is actually being followed. That last one is the sharpest question in the template — most decisions have no enforcement, and writing "none" is itself informative. This vault's `ADR.md` template follows MADR.

## Conventions worth keeping

- **Filename:** `NNNN-title-with-dashes.md`, zero-padded, in a `decisions/` folder beside the project note.
- **When to write one:** when future-you would ask "why on earth is it like this?" Not for tiny, reversible, or temporary choices.
- **Superseding is bidirectional:** the new ADR gets `supersedes`, the old gets `superseded_by` and a status change. Never delete a superseded ADR — the wrong turn is part of the record.
- **Context and Decision are immutable once accepted.** Later learning goes in an appended, dated `## Amendments` section. In practice most teams allow this pragmatic mutability rather than pure immutability.

## Related

- [[Documentation Rot]] — ADRs are the antidote, because they never claim to be current
- [[Diataxis]] — an ADR is *explanation*; keeping it out of reference docs is the whole discipline
