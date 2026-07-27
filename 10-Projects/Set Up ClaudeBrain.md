---
type: project
summary: "This vault documented by itself: Levels 1-4 built, Level 5 deliberately skipped, and the decision index explaining why."
status: active
repo: "https://github.com/SoFloChris/ClaudeBrain"
people: ["[[Chris Aguirre]]"]
uses: ["[[Obsidian]]", "[[Claude Code]]", "[[Obsidian Git]]", "[[brain_search]]", "[[brain_graph]]", "[[claude-video]]"]
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

**Quality gates:** three layers, weakest to strongest — templates *suggest* (every one ships a `summary:` field), `vault_stats.py` *reports* via the SessionStart hook, and `.github/workflows/vault-check.yml` *blocks* on every PR: frontmatter validity, quoted wikilinks, snake_case keys, a summary on every content note, broken links, the graph building, regression tests, secret shapes, and derived data in git. Only the third layer can't be forgotten — see [[0006-enforce-invariants-in-ci|ADR-0006]]. Local commands are in [[90-System/_Index|the System index]].

## Decisions

Index only — the reasoning lives in the [[Architecture Decision Record]]s themselves, which are immutable and dated.

| ADR | Decision | Status |
|---|---|---|
| [[0001-build-levels-1-4-skip-level-5\|ADR-0001]] | Build Levels 1–4, deliberately skip Level 5 | accepted |
| [[0002-typed-frontmatter-over-inline-fields\|ADR-0002]] | Typed relationships as quoted-wikilink frontmatter | accepted |
| [[0003-local-embeddings-numpy-storage\|ADR-0003]] | Local embeddings, plain numpy storage | accepted |
| [[0004-agents-must-grow-the-vault\|ADR-0004]] | Agents must write to the vault, not only read | accepted |
| [[0005-vendor-skills-not-plugins\|ADR-0005]] | Vendor third-party skills into the repo, don't plugin-install | accepted |
| [[0006-enforce-invariants-in-ci\|ADR-0006]] | Enforce vault invariants in CI, not just report them | accepted |
| [[0007-summary-frontmatter-on-every-note\|ADR-0007]] | Every content note carries a one-line `summary:` | accepted |
| [[0008-filesystem-and-cli-over-obsidian-mcp\|ADR-0008]] | Filesystem + Obsidian CLI, no Obsidian MCP server | accepted |

## Tasks

- [ ] Follow `SETUP.md` on the desktop
- [ ] Follow `SETUP.md` on the laptop
- [ ] Confirm a note edited on one machine appears on the other
- [ ] Fill in the "Who I am" section of `CLAUDE.md`
- [ ] `pip install sentence-transformers` on each machine (enables `/recall`)
- [ ] Capture 3 real notes into the Inbox and run `/process-inbox`
- [ ] Try `/graph "Nate Herk"` and `/recall what are the 5 levels?`
- [x] **Triage `claude/obsidian-second-brain-setup-0c0jdy`** — done 2026-07-27. It was a substantial extension of this vault, not a rival scaffold: it already had CI (rebuilt from scratch in #13 before anyone read it), 20 concepts, 3 COMMAND references, 3 more kepano skills, the [[Agent Guide]], the architecture Canvas, and the `summary:` convention. Salvaged across #17–#20; nothing of value left on it. **Confirmed 2026-07-27** by diffing it against `main`: the one file unique to it was a duplicate of [[0007-summary-frontmatter-on-every-note|ADR-0007]] still numbered 0006, which is where the numbering hazard in [[Architecture Decision Record]] comes from. The branch has been reset onto `main`.
- [ ] **Review the 60 summaries written on 2026-07-27** — they're tier-1 metadata an agent reads *instead of* opening a note, so one that misstates a note's claim misroutes future sessions. `grep -h '^summary:' -r 50-Wiki/` shows all of them in one read.
- [ ] **Fact-check the COMMAND reference notes** ([[Sidecar Fleet]], [[Risk Governor]], [[Kalshi Bot]]) against the running system — they carry position sizing and risk limits reproduced from an unmerged branch, never confirmed.
- [ ] **Verify `/watch` end-to-end on a local machine** — it has never actually watched a video. Web sessions can't (egress policy blocks YouTube), so this only proves out locally. Run it on the [[Every Level of a Claude Second Brain]] video, where a hand-written note already exists to compare the extraction against.

## Open questions

- Does the Stop-hook nudge earn its keep, or does it become noise to dismiss?
- At what note count does `/recall` start beating plain grep? (Currently grep wins — the vault is small.)

## Related

- [[Every Level of a Claude Second Brain]] — the source framework
- [[COMMAND — Quant Operations Platform]] — the other active build
