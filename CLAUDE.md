# ClaudeBrain — Session Contract

This repo **is** an Obsidian vault (PARA structure) doubling as a knowledge graph via
[Graphify](https://github.com/safishamsi/graphify). See [`README.md`](README.md) for setup and
[`Welcome.md`](Welcome.md) for the note map.

## Working in this repo

- Prefer the `graphify` MCP tools (`query_graph`, `get_node`, `get_neighbors`, `shortest_path`) over
  reading whole notes when looking something up — that's the point of the graph.
- After adding/editing notes, the graph is stale until `./scripts/graphify-sync.sh` runs. Run it
  before relying on query results for anything just written.
- Keep notes in the right PARA bucket (`00-Inbox` → triage → `01-Projects`/`02-Areas`/`03-Resources`/`04-Archive`).
  Link related notes with `[[wikilinks]]` — unlinked notes are graph dead ends.
- Never commit `graphify-out/` (regenerable), `.obsidian/workspace*.json` (machine-local UI state), or
  a `.env` file (use `.env.example` as the template) — CI (`.github/workflows/vault-check.yml`) blocks
  all three, plus obvious API-key-shaped strings.
- Run `./scripts/install-hooks.sh` once per clone — it wires up a pre-commit hook (`.githooks/pre-commit`)
  that runs `check-links.py` and `guard-secrets.sh` locally, so violations are caught before a commit
  exists rather than after it's pushed. CI (`vault-check.yml`) runs the same two checks as a backstop.
- Don't delete notes to "clean up" — move stale ones to `04-Archive/` so the graph keeps their history.
- If you run `graphify install --project`, diff the resulting changes to this file before accepting —
  it may try to rewrite sections that are hand-maintained here.
