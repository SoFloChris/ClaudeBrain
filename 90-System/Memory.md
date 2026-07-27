# Memory

Durable facts Claude has learned, appended over time. Each entry gets a date. Edit or prune freely — this file is context, not a log. Never store secrets or credentials here.

## About Chris

- (2026-07-24) Vault created; syncing between laptop and desktop via git.

## Preferences

- (2026-07-24) Vault runs at Levels 1–4 (router, wiki, semantic search, knowledge graph); Level 5 deliberately skipped until a concrete pain point demands it.
- Semantic search is a fallback, not the default — grep and wikilinks first (per the source video's advice).
- (2026-07-24) Chris wants Claude to actively GROW the vault — create entity notes, capture answers and decisions, add connections — not just read from it. A session that only reads has failed.
- (2026-07-27) Chris sends screenshots of X/Twitter posts and GitHub trees with "research this" — the expected output is verification (is the claim true?) plus extraction (what's the reusable architecture?), not a summary of the screenshot. See [[Verify the Claim, Steal the Architecture]].
- (2026-07-27) Standing filter for skill packs and tools: install only what feeds a workflow already run by hand; read the rest as architecture references. Six maintained commands beat forty unmaintained ones.
- (2026-07-27) Third-party skills get **vendored into `.claude/skills/`**, not installed as plugins — the vault syncs by git, so checking the skill in makes it work on both machines with no per-device setup. Document source, version, and license in `.claude/skills/README.md`.
- (2026-07-27) `/watch` ([[claude-video]]) is installed vault-wide for turning videos into notes. Needs `ffmpeg` + `yt-dlp` on first run per machine.
- (2026-07-27) **Reading `/vault-status` output:** the 40-word stub threshold does not apply to People/Companies/Tools — those are meant to be thin link infrastructure, so leave them. An empty `knows` predicate is likewise not a defect: the vault's cast is public figures Chris learns from, not contacts, so there's no truthful edge to add. Don't re-litigate either every run.

## Environment

- (2026-07-27) **Web sessions cannot delete remote git branches.** The session's git proxy returns HTTP 403 on any delete refspec (`git push origin --delete`, `:branch`, `:refs/heads/branch` all fail), and the GitHub MCP toolset has `create_branch` but no delete-branch tool. Ordinary pushes work fine — it's deletion specifically. So merged branches have to be cleaned up from the PR page's "Delete branch" button or from a local clone. Don't spend turns retrying it.
- (2026-07-27) **Claude Code web sessions run behind an egress proxy** that denies most non-allowlisted hosts (YouTube is blocked — verified 403 on CONNECT). So `/watch` and anything else that fetches from the open web only works in a **local** session on the laptop or desktop. Don't retry or route around a proxy 403 — it's an org policy denial, not a transient failure. The allowlist is governed by the environment's network policy, changeable in the Claude Code on the web settings.

## Projects

- (nothing yet)

## People & Relationships

- (nothing yet)
