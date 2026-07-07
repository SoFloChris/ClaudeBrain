# ClaudeBrain

A PARA-method Obsidian vault wired to [Graphify](https://github.com/safishamsi/graphify) as a
persistent, queryable knowledge graph — the "second brain" agents can read from and reason over.

## Structure

```
00-Inbox/      unsorted captures — process into a PARA bucket during weekly review
01-Projects/   active, time-bound efforts with a defined outcome
02-Areas/      ongoing responsibilities with no end date
03-Resources/  reference material and topics of interest
04-Archive/    completed projects / inactive areas, kept for the graph's history
```

Start at [[Welcome]] for the vault map. Open this folder as a vault in the Obsidian app to browse
and edit notes normally — Graphify only reads the Markdown, it doesn't require any Obsidian plugin.

## Graphify integration

Graphify turns the vault's Markdown + `[[wikilinks]]` into a queryable knowledge graph
(`graphify-out/graph.json`) that an agent can query instead of re-reading every note.

### One-time setup

```bash
pipx install graphifyy        # or: uv tool install graphifyy
graphify install --project    # registers the skill for this repo (writes CLAUDE.md/AGENTS.md hints)
cp .env.example .env          # only needed for standalone `graphify extract`/`query` outside an assistant session
```

`graphify install --project` may rewrite `CLAUDE.md`/`AGENTS.md` — diff before accepting, since this
repo's `CLAUDE.md` is also hand-maintained (see below).

### Build / refresh the graph

```bash
./scripts/graphify-sync.sh
```

Run this after any batch of note edits. The script checks for broken `[[wikilinks]]` first (via
`scripts/check-links.py`) and fails fast rather than feeding a broken vault into extraction; it does
a full `graphify extract .` on first run and an incremental `--update` afterward. Output lands in
`graphify-out/` (gitignored — regenerate locally, don't commit it).

### Query it

```bash
graphify query "what have I written about X?"
graphify explain "<note or concept title>"
graphify path "<note A>" "<note B>"
```

### Live agent access (MCP)

`.mcp.json` registers a `graphify` MCP server for Claude Code, pointed at `scripts/graphify-mcp.sh`
rather than invoking `python`/`python3` directly — the wrapper picks whichever interpreter exists and
fails with a clear message (instead of a Python traceback) if `graphify-out/graph.json` hasn't been
built yet.

Once the graph exists (run the sync script first), any Claude Code session opened in this repo gets
`query_graph`, `get_node`, `get_neighbors`, and `shortest_path` tools scoped to this vault — no need
to dump whole notes into context.

`.mcp.json` uses `graphify.serve`'s stdio transport (local-process only, no network exposure). Graphify
also supports `--transport http --host 0.0.0.0 --port ... --api-key ...` for team-wide access — if you
ever switch to that, **always set `--api-key`**; without it, the graph (personal notes included) is
served unauthenticated to anything that can reach that host/port.

### Hardening / CI

```bash
./scripts/install-hooks.sh   # one-time: run the checks below on every local commit, not just in CI
```

- `.github/workflows/vault-check.yml`'s actions are pinned to commit SHAs (not floating `@v4`/`@v5`
  tags) and the workflow's `GITHUB_TOKEN` is scoped to `permissions: contents: read` — standard
  supply-chain hardening for Actions. `shellcheck` lints every script on each run.
- `scripts/graphify-mcp.sh` checks that the `graphify` Python module actually imports before serving,
  so a missing install fails with an install hint instead of a bare traceback.
- `scripts/check-links.py` — fails if any `[[wikilink]]` points at a note that doesn't exist. Run by
  `graphify-sync.sh`, the pre-commit hook, and CI.
- `scripts/guard-secrets.sh` — blocks `graphify-out/`, a `.env` file, a `*.pem`/`*.key` file, or an
  API-key/private-key-shaped string from being committed (covers Anthropic, OpenAI, Google, AWS,
  GitHub, and Slack token formats). Run by the pre-commit hook and CI — the hook catches it before the
  commit exists, CI is the backstop if the hook was never installed or was bypassed.

## Workflow

1. Capture into `00-Inbox/`.
2. Weekly review: move notes into `01-Projects/`, `02-Areas/`, `03-Resources/`, or `04-Archive/`, and
   link related notes with `[[wikilinks]]` — links are what make the graph useful.
3. Run `./scripts/graphify-sync.sh` to refresh the graph.
4. Query via `graphify query`/`graphify explain`/`graphify path`, or let an agent use the MCP tools.
