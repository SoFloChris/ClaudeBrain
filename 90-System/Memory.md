# Memory

Durable facts Claude has learned, appended over time. Each entry gets a date. Edit or prune freely — this file is context, not a log. Never store secrets or credentials here.

## About Chris

- (2026-07-24) Vault created; syncing between laptop and desktop via git. GitHub handle `SoFloChris`.
- (2026-07-24) Wants professional-grade notes: fully linked and backlinked, every curated link annotated with *how* the notes relate. Thin or unlinked notes are a defect, not a placeholder.
- (2026-07-24) Prefers verified facts over plausible ones. When a doc and the source disagree, cite the source — see [[Config Lies, Code Wins]].

## Preferences

- (2026-07-24) Vault runs at Levels 1–4 (router, wiki, semantic search, knowledge graph); Level 5 deliberately skipped until a concrete pain point demands it.
- Semantic search is a fallback, not the default — grep and wikilinks first (per the source video's advice).
- (2026-07-24) Chris wants Claude to actively GROW the vault — create entity notes, capture answers and decisions, add connections — not just read from it. A session that only reads has failed.
- (2026-07-27) Chris sends screenshots of X/Twitter posts and GitHub trees with "research this" — the expected output is verification (is the claim true?) plus extraction (what's the reusable architecture?), not a summary of the screenshot. See [[Verify the Claim, Steal the Architecture]].
- (2026-07-27) Standing filter for skill packs and tools: install only what feeds a workflow already run by hand; read the rest as architecture references. Six maintained commands beat forty unmaintained ones.
- (2026-07-27) Third-party skills get **vendored into `.claude/skills/`**, not installed as plugins — the vault syncs by git, so checking the skill in makes it work on both machines with no per-device setup. Document source, version, and license in `.claude/skills/README.md`.
- (2026-07-27) `/watch` ([[claude-video]]) is installed vault-wide for turning videos into notes. Needs `ffmpeg` + `yt-dlp` on first run per machine.
- (2026-07-27) **Reading `/vault-status` output:** stub detection is note-type aware — only types that carry thinking (concept, project, resource, reference, adr, runbook, moc, area) can be flagged, because People/Companies/Tools are *meant* to be thin link infrastructure. An empty `knows` predicate is likewise not a defect: the vault's cast is public figures Chris learns from, not contacts, so there's no truthful edge to add. Don't re-litigate either.

## Environment

- (2026-07-27) **Web sessions cannot delete remote git branches.** The session's git proxy returns HTTP 403 on any delete refspec (`git push origin --delete`, `:branch`, `:refs/heads/branch` all fail), and the GitHub MCP toolset has `create_branch` but no delete-branch tool. Ordinary pushes work fine — it's deletion specifically. So merged branches have to be cleaned up from the PR page's "Delete branch" button or from a local clone. Don't spend turns retrying it.
- (2026-07-27) **Claude Code web sessions run behind an egress proxy** that denies most non-allowlisted hosts (YouTube is blocked — verified 403 on CONNECT). So `/watch` and anything else that fetches from the open web only works in a **local** session on the laptop or desktop. Don't retry or route around a proxy 403 — it's an org policy denial, not a transient failure. The allowlist is governed by the environment's network policy, changeable in the Claude Code on the web settings.

## Projects

- (2026-07-24) **[[COMMAND — Quant Operations Platform]]** (`SoFloChris/openclaw-ui`, private) — self-hosted quant research and execution platform, build V112. Two facts to never get wrong: the [[Strategy Promotion Ladder]] has **9** gates while order sealing runs **16**; and the platform is paper-only *on [[Alpaca]]* — [[Kalshi Bot]] trades real money on a ~$278 account, capped at $2–3 per trade. **Unverified against the running system as of 2026-07-27** — these came from vault notes, not from Chris confirming them.
- (2026-07-24) **[[Set Up ClaudeBrain]]** (`SoFloChris/ClaudeBrain`, public) — this vault. Levels 1–4 built; eight ADRs recorded.
- (2026-07-24) **[[Helper-Agents]]** (`SoFloChris/Helper-Agents`, public) — empty repo, no commits. Needs a scope decision or archival.

## Vault decisions worth not relitigating

- **No Obsidian MCP server** — filesystem tools plus the [[Obsidian CLI]] cover it without standing context cost (ADR-0008).
- **Every content note carries a one-line `summary:`** stating its claim, enforced by templates and `check_frontmatter.py` (ADR-0007).
- **Never `mv` or `git mv` a note.** Obsidian only rewrites inbound links when the rename happens in-app, and it isn't running in an agent session. Prefer `aliases:`.
- **No embeddings upgrade planned.** At this vault's size the whole corpus fits in context several times over; see [[Retrieve to Enter, Navigate to Expand]] for the thresholds that would change this.
- **Third-party skills are vendored, never plugin-installed** (ADR-0005), and **vault invariants are enforced by CI, not just reported** (ADR-0006).

## People & Relationships

- (2026-07-24) Still unknown: Chris's employer and colleagues. [[Chris Aguirre]] has no `works_at` or `knows` edges — ask before inventing any.
