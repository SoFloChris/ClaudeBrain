---
type: concept
summary: "Load a name and a one-line description always, the instructions when relevant, and the full content only when selected — the three-tier model behind Agent Skills, and the one this vault's indexes and summaries implement."
aliases: [progressive disclosure, three-tier loading, context budgeting]
related: ["[[Maps of Content]]", "[[Claude Code]]", "[[Retrieve to Enter, Navigate to Expand]]"]
tags:
  - concept
created: 2026-07-24
---

# Progressive Disclosure

Don't put knowledge in context. Put a **map** to knowledge in context, and let the agent walk it.

Anthropic's Agent Skills spec states the model in three tiers:

| Tier | Loaded | Cost | Content |
|---|---|---|---|
| **1 — Metadata** | Always, at startup | ~100 tokens per skill | `name` + `description` from frontmatter |
| **2 — Instructions** | When the skill triggers | Under 5k tokens | The SKILL.md body |
| **3 — Resources** | As needed | **Nothing until read** | Bundled files; scripts contribute only their *output* |

The mechanism is a filesystem, not a retrieval index — *"there's no context penalty for bundled content that isn't used."*

## The vault mapping

| Skills | This vault | Tier |
|---|---|---|
| `name` + `description` | A note's `summary:` frontmatter, and each `_Index.md` entry's em-dash clause | 1 |
| SKILL.md body | The folder's `_Index.md` | 2 |
| `reference/*.md` | The note itself | 3 |
| `scripts/*.py` | `.base` views, `grep`, [[brain_graph]] — output enters context, definitions never do | 3, free |

> [!warning] The difference that bites
> A skill's tier 1 is genuinely cheap because the runtime injects *only* the frontmatter. **A vault has no such runtime.** `CLAUDE.md` is loaded in full, every session, and so is every `@import` inside it. The vault's tier 1 is whatever is in the router — and it has to be hand-budgeted.

Anthropic's own guidance on that file is blunt: *"For each line, ask: would removing this cause Claude to make mistakes? If not, cut it. **Bloated CLAUDE.md files cause Claude to ignore your actual instructions.**"* And the diagnostic that follows from it — *"if Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."*

## The budgets, ported

Anthropic's numbers transfer directly to index files:

- **Under 500 lines** per tier-2 file. Stated twice in the skills best-practices doc.
- **A table of contents on anything over 100 lines** — so a partial read still reveals the full scope.
- **One level deep.** Links from a referenced file to *another* referenced file get read partially or not at all.
- Descriptions state **what it is and when to use it**, in the third person.

## Why it matters to me

The claim underneath all of it: **the expensive resource is attention, not storage.** A note that is never opened costs nothing; a note summarized badly costs a wasted read *plus* the read of the right note afterwards.

That reframes what a summary is for. It isn't a courtesy to a human skimmer — it's the mechanism by which the *next* read gets skipped. Which is why the rule here is that a `summary:` must state the note's **claim**, never its category: "a safety mechanism an agent can reset is not a safety mechanism" lets an agent decide; "a trading concept" forces it to open the file.

The same logic explains a rule this vault arrived at independently for backlink hygiene — *curate by hand, list in bulk with queries*. A hand-annotated link is tier-1 metadata. A `.base` query is a tier-3 script: it produces output without its forty results entering context.

## Related

- [[Maps of Content]] — what a tier-2 index is, in note-taking terms
- [[Retrieve to Enter, Navigate to Expand]] — how to *move* once the map is loaded
- [[Context vs Connections]] — the filter on what's worth a tier-3 file at all
