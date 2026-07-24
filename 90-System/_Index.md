# ⚙️ System

The machinery of the vault. Rarely touched during day-to-day capture.

- [[Memory]] — durable facts Claude has learned (auto-loaded into every session, human-editable)
- [[Second Brain Levels]] — the 5-level roadmap; Levels 1–4 are built, Level 5 deliberately isn't
- [[Graph Schema]] — the controlled vocabulary for typed relationships
- `Templates/` — note templates (wired to Obsidian's Templates core plugin)
- `Scripts/` — `brain_search.py` (Level 3 semantic search) and `brain_graph.py` (Level 4 knowledge graph)

Slash commands (in `.claude/commands/`, available in any Claude Code session here): `/remember`, `/process-inbox`, `/recall`, `/graph`, `/wrap` (harvest a conversation into notes).

Vault-level files (in the root, outside this folder):

- `CLAUDE.md` — the router; Claude reads it first every session
- `Home.md` — human dashboard
- `SETUP.md` — how to install and sync on each machine
