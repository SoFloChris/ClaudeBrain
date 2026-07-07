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
```

### Build / refresh the graph

```bash
./scripts/graphify-sync.sh    # wraps: graphify extract . --update
```

Run this after any batch of note edits. `--update` re-extracts only changed files, so it's cheap to
run often. Output lands in `graphify-out/` (gitignored — regenerate locally, don't commit it).

### Query it

```bash
graphify query "what have I written about X?"
graphify explain "<note or concept title>"
graphify path "<note A>" "<note B>"
```

### Live agent access (MCP)

`.mcp.json` in this repo registers a `graphify` MCP server for Claude Code:

```json
{
  "mcpServers": {
    "graphify": {
      "command": "python",
      "args": ["-m", "graphify.serve", "graphify-out/graph.json"]
    }
  }
}
```

Once `graphify-out/graph.json` exists (run the sync script first), any Claude Code session opened in
this repo gets `query_graph`, `get_node`, `get_neighbors`, and `shortest_path` tools scoped to this
vault — no need to dump whole notes into context.

## Workflow

1. Capture into `00-Inbox/`.
2. Weekly review: move notes into `01-Projects/`, `02-Areas/`, `03-Resources/`, or `04-Archive/`, and
   link related notes with `[[wikilinks]]` — links are what make the graph useful.
3. Run `./scripts/graphify-sync.sh` to refresh the graph.
4. Query via `graphify query`/`graphify explain`/`graphify path`, or let an agent use the MCP tools.
