---
type: tool
aliases: ["graphify", "graphifyy"]
alternative_to: ["[[brain_graph]]"]
related: ["[[Knowledge Graph]]", "[[Graph Engineering]]", "[[LightRAG]]"]
repo: "https://github.com/safishamsi/graphify"
---

# Graphify

A knowledge-graph tool for AI coding assistants: point it at a folder, it extracts entities and relations with an LLM, and serves the resulting graph to the agent over MCP (`query_graph`, `get_node`, `get_neighbors`, `shortest_path`). Same family as [[LightRAG]] — extraction-first rather than authored-first.

## Why it's in this vault as a *rejected* option

**This vault was very nearly built on it.** The branch `claude/graphify-obsidian-integration-m15xef` (2026-07-07, four commits, never merged) scaffolded a PARA vault wired to Graphify: `.mcp.json` pointing at a `graphify-mcp.sh` launcher, a `graphify-sync.sh` rebuild step, `.graphifyignore`, and a `CLAUDE.md` instructing the agent to **prefer graph queries over reading notes**.

The current vault, built three weeks later, went the other way — and the reasons are already written down:

- **ADR-0002** — relationships are authored as typed frontmatter, not extracted. If you write them yourself, no model has to guess, and the graph stays inspectable in plain markdown.
- **[[LightRAG]]'s note** makes the same call about the same category of tool.
- The router says grep and wikilinks first; the abandoned `CLAUDE.md` said the opposite.

It also carried real costs the authored approach doesn't: an LLM extraction pass on every rebuild, API keys in a `.env`, and a `graphify-out/` artifact that must never be committed.

## What was worth taking from that branch anyway

The graph integration is obsolete; the engineering hygiene around it was better than the vault it was scaffolding. Its CI workflow, secret guard, and pre-commit hooks were ported in 2026-07-27 — see ADR-0006. Worth remembering as a general lesson: **a dead branch can still be a parts bin.**

## When it would become interesting again

If the vault ever accumulates a large corpus of documents *someone else wrote* — imported papers, meeting transcripts, scraped research — hand-typing relations stops scaling and extraction starts earning its cost. That's the same trigger recorded for [[LightRAG]], and the vault is nowhere near it at 59 notes.

## Related

- [[brain_graph]] — what this vault built instead; authored edges, zero dependencies, no API key
- [[Graph Engineering]] — the discipline both tools implement, at very different levels of automation
- [[LightRAG]] — the same trade-off, evaluated and declined on the same grounds
