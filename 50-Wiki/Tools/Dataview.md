---
type: tool
alternative_to: ["[[Bases]]"]
uses: ["[[Obsidian]]"]
related: ["[[Knowledge Graph]]"]
---

# Dataview

The long-standing Obsidian plugin for querying notes like a database. Still the de facto query standard in 2026, though [[Obsidian]]'s core **Bases** plugin now covers most property-driven dashboards without any plugin at all.

## Key facts

- Actively maintained; stewardship passed from the original author (blacksmithgu) to community maintainer @holroy.
- **Datacore**, the intended successor, is still 0.1.x and *not* in the community plugin store — don't build on it yet.
- Queries our typed frontmatter directly:

  ```
  TABLE works_at AS "Company", role
  FROM "50-Wiki/People"
  WHERE works_at = [[Acme Corp]]
  ```
- **Inline fields (`key:: value`) are a Dataview-only invention** — the Properties UI, Bases, and most modern tooling ignore them. This vault deliberately uses frontmatter instead, so the same data is readable by Obsidian natively, Bases, Dataview, and [[brain_graph]] alike.
- Cannot do multi-hop traversal in DQL — that needs DataviewJS, the Breadcrumbs plugin, or our `/graph path` command.

## Related

- [[Obsidian Knowledge Graph Conventions]] — why frontmatter beat inline fields here
