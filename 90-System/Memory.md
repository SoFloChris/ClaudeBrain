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

- (2026-07-27) **Web sessions cannot delete remote git branches — don't offer, just hand over the link.** The git proxy returns HTTP 403 on every delete refspec form (`git push origin --delete`, `:branch`, `:refs/heads/branch`), and the GitHub MCP has `create_branch` but no delete counterpart. Ordinary pushes work fine; deletion specifically does not. This was confirmed four separate ways in one session — treat it as settled, never retry it, and never say "I'll clean that up" about a branch.

  The reply that actually helps: **[github.com/SoFloChris/ClaudeBrain/branches](https://github.com/SoFloChris/ClaudeBrain/branches)** (trash icon), or the **Delete branch** button on the merged PR's page, or `git push origin --delete <branch>` from the laptop.

  Worth stating whether the branch is a true ancestor of `main` (`git merge-base --is-ancestor`) — if it isn't, deleting discards commit history that content-level salvage doesn't preserve.
- (2026-07-27) **`openclaw-ui` can be pulled into a session on demand** via `add_repo` (`SoFloChris/openclaw-ui`, private) — so COMMAND claims can be checked against source rather than taken from vault notes. Clone once, inline, with a generous timeout; the proxy caps concurrent git ops. Last verified at `ebda240`.
- (2026-07-27) **Claude Code web sessions run behind an egress proxy** that denies most non-allowlisted hosts (YouTube is blocked — verified 403 on CONNECT). So `/watch` and anything else that fetches from the open web only works in a **local** session on the laptop or desktop. Don't retry or route around a proxy 403 — it's an org policy denial, not a transient failure. The allowlist is governed by the environment's network policy, changeable in the Claude Code on the web settings.
- (2026-07-29) **A web/mobile session does NOT run on Chris's MSI desktop — it runs in an Anthropic-hosted throwaway cloud container.** Verified: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, hostname `vm`, `/home/user/` holding only the one freshly-cloned repo. Consequence, and the reason this keeps coming up: **local-only work on the desktop is unreachable from the phone.** Anything Claude touches from mobile must already be pushed to GitHub *and* granted to the Claude GitHub App. Directing from the phone is fine — the desktop being on or off is irrelevant, because it was never the thing doing the work. Verified 2026-07-29: `list_environments` returns exactly one environment — `env_01C6K3z75NeistDnDwQuQBkb` "Default", kind `anthropic_cloud`. **Corrected same day:** the "always-on desktop as the worker" model does *not* require a self-hosted runner (an earlier note guessed `ccpool_`; the docs describe no such user-configurable option). It's [[Directing Claude Code From Your Phone|Remote Control or Dispatch]] — both of which run on Chris's own machine.

- (2026-07-29) **A session is pinned to ONE GitHub owner — `add_repo` refuses cross-owner adds outright.** Verified: asking this ClaudeBrain session (owner `soflochris`) for a repo under a different owner returns `cross-tier adds are not supported in v1 … Start a new session with the requested repo as the initial source`. The pin fails *before* any permission or existence check, so a wrong-owner add tells you nothing about whether the repo exists — don't go debugging GitHub App grants first. The only path to a repo under a different account is a **new session created with that repo as its initial source** (claude.ai/code → new session → pick the repo). Corollary: **one session can never span the vault and an unrelated work repo.**
- (2026-07-29) **Chris's actual goal — "direct from my phone, work happens on my MSI desktop" — is a supported feature, and it is NOT SSH.** It's **Remote Control** (`claude remote-control` on the desktop, steer from phone/web) or **Dispatch** (pair mobile app with the Desktop app, message a task, it spawns a Desktop session). Both execute on Chris's own hardware with his own filesystem; the phone is just a window. Key insight that makes SSH unnecessary rather than merely blocked: **the desktop makes outbound HTTPS only and never opens an inbound port.** Full comparison and setup in [[Directing Claude Code From Your Phone]]. When Chris asks for this again, don't re-explain why SSH fails — go straight to `claude remote-control` in `tmux`.
- (2026-07-29) **Claude cannot SSH out of a web session — including into Chris's MSI desktop.** Verified: no `ssh` binary in the container, `~/.ssh` empty, and the agent proxy's own README lists non-443 ports and raw TCP under *"Not supported through the proxy (report, do not work around)"*. A home desktop behind NAT would additionally need a public endpoint or tunnel. Treat "just SSH into my desktop" as settled-impossible rather than a config gap. The productive redirect: **the desktop isn't needed at all** — if the code is on GitHub, a session sourced from that repo does the work, and no machine of Chris's has to be powered on.

## Projects

- (2026-07-24) **[[COMMAND — Quant Operations Platform]]** (`SoFloChris/openclaw-ui`, private) — self-hosted quant research and execution platform, build V112. Two facts to never get wrong: the [[Strategy Promotion Ladder]] has **9** gates while order sealing runs **16**; and the platform is paper-only *on [[Alpaca]]* — [[Kalshi Bot]] trades real money on a ~$278 account, hard-capped at **$2** per trade. **Verified against `openclaw-ui` @ `ebda240` on 2026-07-27** — the money constants, gate counts, and promotion thresholds all check out against source; one error was found and fixed (the per-trade cap is $2, not $3).
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
