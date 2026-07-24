---
type: tool
summary: "Obsidian's core database plugin: table, card, and list views built from frontmatter properties, no community plugin needed."
aliases: [Obsidian Bases]
built_by: "[[Dynalist Inc]]"
alternative_to: ["[[Dataview]]"]
related: ["[[Obsidian]]", "[[Knowledge Graph]]"]
tags:
  - tool
created: 2026-07-24
---

# Bases

[[Obsidian]]'s **core** database plugin — table, card, list, and map views built from frontmatter properties. No community plugin required.

## Key facts

- Shipped in early access with Obsidian 1.9.0 (May 2025); **generally available in 1.9.10 (Aug 2025)**.
- Views live in `.base` files (YAML) or embedded in a note with `![[Name.base#View]]`.
- Queries **frontmatter properties only** — it does not read [[Dataview]]'s inline `key:: value` fields. Another reason this vault stores relationships in frontmatter.
- The `this` keyword resolves to the *embedding* file, so one `.base` can act as a per-entity dashboard on every note that embeds it.
- Values are **editable in place** — changing a cell writes back to the note's frontmatter. Dataview output is read-only.

## Why it matters to me

Three `.base` files in `90-System/Bases/` run on it: `Projects` (active work), `Orphans` (link hygiene), and `Entity` (the "Mentioned in" panel embedded on every wiki note). Being core means these work on both machines with nothing to install.

Gotchas worth remembering: date subtraction returns a Duration, so reach for `.days` before `.round()`; wrap formulas containing double quotes in single quotes; guard null properties with `if()` or the formula crashes.

## Related

- [[Dataview]] — what it replaces for dashboards, and what it can't do (no JS, no inline fields)
- [[Steph Ango]] — his `obsidian-bases` skill is the syntax reference vendored here
