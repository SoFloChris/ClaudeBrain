---
type: project
summary: "Master note for this vault: what it is, how Levels 1-4 are built, and what is left to do. The vault documenting itself."
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

Index only — the reasoning lives in the [[Architecture Decision Record]]s themselves, which are immutable and dated.

| ADR | Decision | Status |
|---|---|---|
| [[0001-build-levels-1-4-skip-level-5\|ADR-0001]] | Build Levels 1–4, deliberately skip Level 5 | accepted |
| [[0002-typed-frontmatter-over-inline-fields\|ADR-0002]] | Typed relationships as quoted-wikilink frontmatter | accepted |
| [[0003-local-embeddings-numpy-storage\|ADR-0003]] | Local embeddings, plain numpy storage | accepted |
| [[0004-agents-must-grow-the-vault\|ADR-0004]] | Agents must write to the vault, not only read | accepted |
| [[0005-filesystem-and-cli-over-obsidian-mcp\|ADR-0005]] | Filesystem + CLI, no Obsidian MCP server | accepted |
| [[0006-summary-frontmatter-on-every-note\|ADR-0006]] | A one-line `summary:` on every content note | accepted |

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
