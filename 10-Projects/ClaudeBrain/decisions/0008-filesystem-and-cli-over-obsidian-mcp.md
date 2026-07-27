---
type: adr
summary: "ADR-0008 (accepted): drive the vault through Claude Code's filesystem tools and the Obsidian CLI, not an Obsidian MCP server."
status: accepted
date: 2026-07-27
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[Obsidian CLI]]", "[[Claude Code]]", "[[Progressive Disclosure]]"]
tags:
  - adr
---

# ADR-0008 — Drive the vault from the filesystem and CLI, not an Obsidian MCP server

Written 2026-07-24 on `claude/obsidian-second-brain-setup-0c0jdy` as ADR-0005 and never merged; renumbered here because 0005 was taken in the meantime. The reasoning is that author's, restated against the vault as it now is.

## Context and Problem Statement

Several Obsidian MCP servers exist and are actively maintained. Adopting one is the obvious-looking move for "let an agent operate my vault." Should this vault run one?

## Decision Drivers

- Every MCP tool schema occupies context in **every** window, whether used or not — a standing tier-1 cost under [[Progressive Disclosure]].
- Setup friction compounds across two machines; anything needing a key, a plugin, or a running app gets skipped on the second one.
- A few operations genuinely cannot be done from the filesystem, and they matter — link-preserving renames above all.
- Agent sessions run when Obsidian is closed.

## Considered Options

- **Local REST API** (coddingtonbear) — a plugin with a built-in MCP server; requires Obsidian running plus an API key
- **A wrapper over Local REST API** — `cyanheads/obsidian-mcp-server` (14 tools, BM25 search) or `MarkusPfundstein/mcp-obsidian` (7 tools)
- **`bitbonsai/mcpvault`** — direct filesystem, no plugin, works with Obsidian closed
- **No MCP server** — Claude Code's native tools, plus the [[Obsidian CLI]] where it uniquely helps

## Decision Outcome

Chosen option: **no MCP server.** Claude Code already has Read/Write/Edit/Glob/Grep against the filesystem, and this vault is plain markdown with no database and no sync layer — an MCP server would add a process, a key, a running-app dependency, and permanent schema tokens in exchange for capabilities the filesystem already provides.

The genuine filesystem gaps are named rather than papered over: **link-preserving renames**, Obsidian's **live metadata cache** (resolved links, backlinks, unresolved links), **command-palette execution**, and **Bases evaluation**. These are covered by installing the [[Obsidian CLI]] on whichever machine is running Obsidian, and by `brain_graph.py` / `check_links.py` for the link-integrity half.

### Consequences

- Good, because zero standing context cost and nothing to keep running.
- Good, because it works identically on both machines and inside a headless agent session.
- Bad, because **renaming a note in an agent session breaks inbound links silently** — Obsidian only rewrites them when the rename happens in-app. Mitigated by a hard rule in `CLAUDE.md`: never `mv` a note; prefer `aliases:`; if a rename is unavoidable, rewrite every inbound link in the same commit and confirm zero unresolved links.
- Bad, because there's no BM25 tier. Accepted: at 88 notes grep does not over-retrieve, and [[Retrieve to Enter, Navigate to Expand]] puts BM25's crossover around 1,000 notes.
- Neutral: `mcpvault` is the only option that works with Obsidian closed, and it remains the one to revisit if this decision is ever reversed.

### Confirmation

Stronger now than when this was written. `check_links.py` fails the build on any unresolved wikilink, and `vault_stats.py` reports the same number every session via the SessionStart hook. If filesystem-only operation is corrupting the link graph, that number stops being zero — which is the observable signature this decision would be wrong. It is currently zero across 112 markdown files.

## Pros and Cons of the Options

### Local REST API or a wrapper over it

- Good, because it exposes Obsidian's real metadata cache and command palette — things nothing else can reach.
- Bad, because it requires Obsidian to be running, which agent sessions cannot assume.
- Bad, because of an **[unverified]** reported data-loss issue where a POST can overwrite file contents on a metadata-cache miss. Not confirmed first-hand; enough to warrant caution before enabling writes.

### mcpvault (direct filesystem)

- Good, because no plugin, no key, works with Obsidian closed.
- Bad, because its tools largely restate Read/Write/Edit/Grep — paying schema tokens for capability already present.

## More Information

Revisit if the vault passes ~1,000 notes (BM25 ranking starts to earn its keep) or if link-preserving renames become routine rather than exceptional. Research summarised in [[Obsidian Knowledge Graph Conventions]] and [[Retrieve to Enter, Navigate to Expand]].

## Amendments

<!-- Append only. -->
