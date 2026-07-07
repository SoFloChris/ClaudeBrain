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
- Never commit `graphify-out/` (regenerable) or `.obsidian/workspace*.json` (machine-local UI state).
- Don't delete notes to "clean up" — move stale ones to `04-Archive/` so the graph keeps their history.
