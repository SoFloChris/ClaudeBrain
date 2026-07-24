---
type: concept
summary: "Basecamp's method; the two portable ideas are fixed appetite instead of estimates, and explicit non-goals."
aliases: [appetite, no-gos]
related: ["[[Architecture Decision Record]]"]
tags:
  - concept
created: 2026-07-24
---

# Shape Up

Basecamp's product method. Two of its ideas are worth stealing even if you never adopt the rest, and both are about **constraining scope before design starts**.

## Appetite, not estimate

*"Appetites start with a number and end with a design. Estimates start with a design and end with a number."*

You decide how much time a problem is **worth** — small batch ≈ 1–2 weeks, big batch ≈ 6 weeks — and then design something that fits. It inverts the usual failure where a design is produced first and the schedule is negotiated against it afterwards.

For solo projects this is the single most useful idea in the method: with no manager, nothing else stops scope creep.

## The five ingredients of a pitch

1. **Problem** — the raw idea, ideally *"a single specific story that shows why the status quo doesn't work."*
2. **Appetite** — how much time it's worth.
3. **Solution** — the core elements, in a form people grasp immediately.
4. **Rabbit holes** — details called out specifically to avoid trouble.
5. **No-gos** — what's *explicitly excluded* to fit the appetite.

*"It's critical to always present both a problem and a solution together... Diving straight into 'what to build' is dangerous."*

## No-gos, and why they generalise

**Non-goals appear in every serious engineering template** — Google design docs, Kubernetes KEPs, Rust RFCs — and are almost always missing from personal project notes. Google's definition is the sharp one: non-goals *"aren't negated goals like 'the system shouldn't crash', but rather things that could reasonably be goals, but are explicitly chosen not to be."*

That's why the Project Master template here has an explicit **"not in scope"** section, and why [[Architecture Decision Record]]s record considered-and-rejected options rather than only the winner.

## One idea deliberately not adopted

Shape Up rejects backlogs outright — *"backlogs are a big weight we don't need to carry"* — with unbet pitches simply let go. Defensible for a company with a betting table; for a personal vault, `40-Archive/` is the gentler version of the same instinct.

## Related

- [[Set Up ClaudeBrain]] — where appetite and non-goals actually get applied
