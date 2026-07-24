# ⚙️ System

The machinery of the vault. Rarely touched during day-to-day capture.

## Docs

- [[Agent Guide]] — the working manual: which tool answers which question, note-type conventions, failure modes
- [[Memory]] — durable facts Claude has learned (auto-loaded into every session, human-editable)
- [[Second Brain Levels]] — the 5-level roadmap; Levels 1–4 built, Level 5 deliberately skipped
- [[Graph Schema]] — the controlled vocabulary for typed relationships
- `Vault Architecture.canvas` — visual map of the four levels; every box opens the real note

## Templates (`Templates/`)

Entity: `Person` · `Company` · `Tool` · `Concept`
Work: `Project` (light) · `Project Master` (builds) · `ADR` · `Runbook` · `Changelog`
Other: `Daily Note` · `Meeting Note` · `Resource` · `MOC`

## Scripts (`Scripts/`)

| Script | Purpose |
|---|---|
| [[brain_search]] | Level 3 semantic search — `index`, `search`, `chunks` |
| [[brain_graph]] | Level 4 knowledge graph — `build`, `query`, `path`, `stats` |
| `vault_stats.py` | Vault health — orphans, stubs, broken links (`--brief` for hooks) |

## Bases (`Bases/`)

Live dashboards, queried by Obsidian's core Bases plugin. Embed with `![[Name.base#View]]`.

- `Projects.base` — active work, with a staleness marker
- `Orphans.base` — notes with no links in or out
- `Entity.base` — "mentioned in" panel; embedded on every entity note via `this`

## Slash commands (`.claude/commands/`)

`/remember` · `/process-inbox` · `/recall` · `/graph` · `/wrap` · `/vault-status`

## Hooks (`.claude/hooks/`)

- `vault-brief.sh` — **SessionStart**: injects vault stats and the growth mandate into context
- `capture-nudge.sh` — **Stop**: if a session ends with nothing written, says so once (rate-limited to 90 min, silent whenever notes changed)

## Vendored skills (`.claude/skills/`)

`obsidian-markdown` and `obsidian-bases` from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) (MIT, by Obsidian's CEO) — authoritative syntax, available offline.
