---
type: concept
summary: "Four kinds of documentation - tutorial, how-to, reference, explanation - and the claim that mixing them is the dominant documentation failure."
aliases: [Diátaxis]
related: ["[[Documentation Rot]]", "[[Architecture Decision Record]]"]
tags:
  - concept
---

# Diataxis

Daniele Procida's claim that there are exactly **four** kinds of documentation, because there are exactly two axes and they define the whole territory:

- **Action vs. cognition** — what the user *does* vs. what the user *knows*
- **Acquisition vs. application** — the user at *study* vs. the user at *work*

| | informs action | informs cognition |
|---|---|---|
| **acquisition** (study) | **Tutorial** — a lesson | **Explanation** — why it's like this |
| **application** (work) | **How-to guide** — a recipe | **Reference** — the machinery, described |

The compass is two questions: *action or cognition? acquisition or application?* — and it yields the answer.

## Why it matters to me

**Mixing the modes is the dominant documentation failure**, and I do it constantly. The specific version I keep committing: letting *rationale leak into reference*. An architecture table starts explaining why SQLite was chosen — that's explanation wearing a reference costume, and it makes the table harder to scan while burying the reasoning where nobody looks for it.

The fix in this vault:

- **Reference** → the architecture tables in a project master note. Facts. No opinions.
- **How-to** → runbooks. Competent reader, real goal, no teaching.
- **Explanation** → [[Architecture Decision Record]]s and concept notes. This is where *why* lives.
- **Tutorial** → rare here, but real: "get this running from a cold clone."

## The tutorial/how-to confusion

The most common conflation, and the distinction is **study vs. work — not beginner vs. advanced**. A how-to guide can cover something basic; a tutorial can cover something advanced. A driving lesson is a tutorial; a route is a how-to. Procida's stakes argument: a clinical manual that tried to teach while guiding a real procedure "would kill people."

## The workflow advice

Explicitly anti-big-bang, and worth quoting because it contradicts the instinct: *"It certainly does not mean that you should create empty structures for tutorials/how-to guides/reference/explanation with nothing in them. Don't do that. It's horrible."* The method is to pick one document, ask what need it serves, make one improvement, and repeat.

## Related

- [[Documentation Rot]] — mode separation is itself a rot-prevention measure: the volatile parts stop dragging down the durable ones
