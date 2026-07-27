---
type: resource
summary: "How to encode typed relationships so Obsidian, Bases, Dataview, and scripts all read the same edges - the reasoning behind this vault's Graph Schema."
topic: "[[Knowledge Graph]]"
related: ["[[Obsidian]]", "[[Graph Schema]]", "[[Dataview]]"]
---

# Obsidian Knowledge Graph Conventions

How to encode typed relationships in an Obsidian vault so both humans and scripts can use them. Researched 2026-07; this is the reasoning behind [[Graph Schema]].

## The core convention

**Every edge is a frontmatter key whose values are quoted wikilinks.** The key name is the relationship type.

```yaml
---
type: person
works_at: "[[Acme Corp]]"
knows:
  - "[[Jane Doe]]"
  - "[[John Smith]]"
---
```

Non-negotiable rules:

1. **Quote the links.** Unquoted `[[...]]` is invalid YAML — brackets parse as a nested list. Obsidian's Properties UI quotes automatically; scripts and templates must do it manually.
2. **`type` is a plain string, not a link.** It's node metadata, not an edge — and it lets Bases filter `type == "person"`.
3. **Store each fact once, on the subject's note.** Jane's note says `works_at`; Acme's note doesn't need a mirror. Reverse direction comes from backlinks and the graph.
4. **snake_case predicates from a fixed list**, documented in one place.

## Why frontmatter beats the alternatives

| Approach | Read by |
|---|---|
| **Frontmatter properties** | Obsidian natively (Properties UI, graph view, backlinks), Bases, [[Dataview]], Breadcrumbs, any script |
| Inline fields (`key:: value`) | [[Dataview]] only — Bases and the Properties UI ignore them |
| A "## Relations" body section | Humans only; nothing queries it |

Frontmatter links are **first-class graph edges** — they appear in graph view and backlinks with no plugin installed. That interoperability is the whole argument.

## The plugin layers (each optional, none required)

- **Bases** — core plugin since Obsidian 1.9.10 (Aug 2025). Table/card/list views over properties. `file.hasLink(this)` replicates a backlinks pane; `works_at.contains(this)` builds a company roster. Largely replaces Dataview for dashboards; ignores inline fields.
- **[[Dataview]]** — still the query standard; DQL can't do multi-hop traversal. Datacore (successor) is still 0.1.x and not in the plugin store — don't build on it.
- **Breadcrumbs** — actively maintained; the only in-app **multi-hop traversal** for typed links.
- **Graph Link Types** — renders the property name as a label on graph edges.
- **Juggl** — effectively unmaintained (last release Nov 2023). Avoid.

## Parsing it yourself

The entire extraction is a few lines: read YAML, skip reserved keys (`type`, `tags`, `aliases`, `created`), and for every remaining key run `re.findall(r"\[\[([^\]|#]+)", str(value))` → `(note, key, target)` triples. That's what [[brain_graph]] does.

For export to a real graph: **obsidiantools** (PyPI, actively maintained) parses a vault into a NetworkX graph plus frontmatter dataframes — from there GraphML, JSON, or Neo4j.

## Related

- [[Claude Code Memory and Commands]] — the agent side of the stack
