# Memory

Durable facts Claude has learned, appended over time. Each entry gets a date. Edit or prune freely — this file is context, not a log. Never store secrets or credentials here.

## About Chris

- (2026-07-24) Vault created; syncing between laptop and desktop via git. GitHub handle `SoFloChris`.

## Preferences

- (2026-07-24) Vault runs at Levels 1–4 (router, wiki, semantic search, knowledge graph); Level 5 deliberately skipped until a concrete pain point demands it.
- Semantic search is a fallback, not the default — grep and wikilinks first (per the source video's advice).
- (2026-07-24) Chris wants Claude to actively GROW the vault — create entity notes, capture answers and decisions, add connections — not just read from it. A session that only reads has failed.
- (2026-07-24) Wants professional-grade notes: fully linked and backlinked, every curated link annotated with *how* the notes relate. Thin or unlinked notes are treated as a defect, not a placeholder.
- (2026-07-24) Prefers verified facts over plausible ones. When a doc and the source disagree, cite the source — see [[Config Lies, Code Wins]].

## Projects

- (2026-07-24) **[[COMMAND — Quant Operations Platform]]** (`SoFloChris/openclaw-ui`, private) — self-hosted quant research and execution platform, build V112. Two facts to never get wrong: the [[Strategy Promotion Ladder]] has **9** gates while order sealing runs **16**; and the platform is paper-only *on [[Alpaca]]* — [[Kalshi Bot]] trades real money on a ~$278 account, capped at $2–3 per trade.
- (2026-07-24) **[[Set Up ClaudeBrain]]** (`SoFloChris/ClaudeBrain`, public) — this vault. Levels 1–4 built; six ADRs recorded.
- (2026-07-24) **[[Helper-Agents]]** (`SoFloChris/Helper-Agents`, public) — empty repo, no commits. Needs a scope decision or archival.

## Vault decisions worth not relitigating

- (2026-07-24) **No Obsidian MCP server** — filesystem tools plus the [[Obsidian CLI]] cover it without standing context cost (ADR-0005).
- (2026-07-24) **Every content note carries a one-line `summary:`** stating its claim, enforced by templates and `vault_stats.py` (ADR-0006).
- (2026-07-24) **Never `mv` or `git mv` a note.** Obsidian only rewrites inbound links when the rename happens in-app, and it isn't running in an agent session. Prefer `aliases:`.
- (2026-07-24) **No embeddings upgrade planned.** At this vault's size the whole corpus fits in context several times over; see [[Retrieve to Enter, Navigate to Expand]] for the size thresholds that would change this.

## People & Relationships

- (2026-07-24) Still unknown: Chris's employer and colleagues. `[[Chris Aguirre]]` has no `works_at` or `knows` edges — ask before inventing any.
