---
type: project
status: active
repo: "https://github.com/SoFloChris/ClaudeBrain"
people: ["[[Chris Aguirre]]"]
uses: ["[[Obsidian]]", "[[Claude Code]]", "[[Obsidian Git]]", "[[brain_search]]", "[[brain_graph]]"]
related: ["[[Second Brain]]", "[[Every Level of a Claude Second Brain]]"]
---

# Set Up ClaudeBrain

> The master note for this vault — what it is, how it's built, and what's left. The vault documents itself.

**Repo:** `SoFloChris/ClaudeBrain` (public) · **Status:** Active · **Architecture:** Levels 1–4 of [[Second Brain Levels]]

## Outcome

A second brain that is genuinely usable from both machines, and that [[Claude Code]] agents actively **grow** rather than merely read.

## Architecture

| Level | What it is | Implementation |
|---|---|---|
| 1 — Router | `CLAUDE.md` as system prompt + folder map | Auto-loads every session |
| 2 — [[LLM Wiki]] | Entity notes + auto-loaded memory | `50-Wiki/`, `Memory.md` via `@import`, `/remember`, `/process-inbox` |
| 3 — [[Semantic Search]] | Search by meaning | [[brain_search]] + `/recall` |
| 4 — [[Knowledge Graph]] | Typed relationships, chain tracing | [[brain_graph]] + `/graph` + [[Graph Schema]] |
| 5 — Autonomous | Always-on, self-maintaining | **Deliberately skipped** — see build-triggers in [[Second Brain Levels]] |

**Structure:** [[PARA Method]] folders (`00-Inbox` → `40-Archive`) plus `50-Wiki/` for entities ([[Context vs Connections]] is the filter for what gets in) and `90-System/` for machinery.

**Sync:** plain git via [[Obsidian Git]] — 5-minute auto pull/push, laptop ↔ desktop. Derived artifacts (search index, graph JSON) are gitignored and rebuilt per machine, so they never conflict.

## Decisions

- (2026-07-24) **Agents must grow the vault, not just read it.** Router principle #5 plus a "Grow the vault" section; `/wrap` harvests conversations. *Why:* sessions were producing research and decisions that never became notes.
- (2026-07-24) **Levels 1–4 built, Level 5 skipped.** *Why:* [[Nate Herk]] stops at 4 himself; [[GBrain]]'s scale (146K pages) is the threshold that justifies always-on machinery, and this vault has ~50.
- (2026-07-24) **Typed frontmatter over inline fields** for relationships. *Why:* frontmatter is readable by Obsidian natively, Bases, [[Dataview]], and [[brain_graph]]; inline `key::` fields are Dataview-only.
- (2026-07-24) **Local embeddings, plain numpy storage.** *Why:* private and free; at a few thousand chunks brute-force cosine is milliseconds, so a vector DB would be pure overhead. `bge-small-en-v1.5` over EmbeddingGemma because Gemma is license-gated on Hugging Face and would break zero-config setup.
- (2026-07-24) **Semantic search is a fallback, not the default.** *Why:* the source video's own warning — grep and wikilinks first.

## Tasks

- [ ] Follow `SETUP.md` on the desktop
- [ ] Follow `SETUP.md` on the laptop
- [ ] Confirm a note edited on one machine appears on the other
- [ ] Fill in the "Who I am" section of `CLAUDE.md`
- [ ] `pip install sentence-transformers` on each machine (enables `/recall`)
- [ ] Capture 3 real notes into the Inbox and run `/process-inbox`
- [ ] Try `/graph "Nate Herk"` and `/recall what are the 5 levels?`

## Open questions

- Does the Stop-hook nudge earn its keep, or does it become noise to dismiss?
- At what note count does `/recall` start beating plain grep? (Currently grep wins — the vault is small.)

## Related

- [[Every Level of a Claude Second Brain]] — the source framework
- [[COMMAND — Quant Operations Platform]] — the other active build
