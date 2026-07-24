---
type: tool
summary: "The markdown editor this vault lives in - plain files on disk, which is why it survives at every level."
built_by: "[[Dynalist Inc]]"
related: ["[[Second Brain]]", "[[PARA Method]]", "[[Bases]]"]
uses: ["[[Obsidian Git]]"]
---

# Obsidian

The markdown editor this vault lives in. Plain `.md` files in a folder on disk — no proprietary database, no lock-in, which is exactly why it survives as the foundation of a [[Second Brain]] at every level.

## Key facts

- **Properties** (frontmatter) since v1.4: types are Text, List, Number, Checkbox, Date, Date & time, Tags. Internal links in properties **must be quoted** (`works_at: "[[Acme]]"`) — unquoted brackets are invalid YAML. This is what powers our [[Knowledge Graph]].
- Frontmatter links are real links: they appear in graph view, backlinks, and outgoing links, with no plugin needed.
- **Bases** is now a core plugin (early access Obsidian 1.9.0, May 2025; public in 1.9.10, Aug 2025) — database-style table/card/list views that query frontmatter properties across the vault. Largely replaces [[Dataview]] for property-driven dashboards, but ignores Dataview's inline `key:: value` fields.
- Graph view colors nodes by configured color groups — ours are set per folder in `.obsidian/graph.json` (People green, Companies blue, Concepts orange, and so on).
- Vault config lives in `.obsidian/`; per-device state (`workspace.json`) is gitignored so the laptop and desktop don't fight.

## Related

- [[Smart Connections]] — plugin adding local semantic search inside Obsidian
- [[Obsidian Git]] — the sync engine for this vault
