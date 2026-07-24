---
type: concept
summary: "The open JSON format behind Obsidian .canvas files - which is what lets an agent author a visual map as a file."
aliases: [Canvas, .canvas]
related: ["[[Obsidian]]", "[[C4 Model]]"]
tags:
  - concept
created: 2026-07-24
---

# JSON Canvas

The open file format behind Obsidian's `.canvas` files — an infinite visual board of nodes and edges, stored as plain JSON rather than a proprietary blob. Obsidian published it as an open spec, so the format outlives the app.

## Why it matters to me

**An agent can author a canvas.** That's the point. Because it's JSON, Claude can generate a visual map — an architecture diagram, a project overview, a concept map — as a file, and Obsidian renders it as a real, editable board.

That covers the gap [[C4 Model]] diagrams leave: Mermaid renders inside one note and can't link out, while a canvas *is* made of note references and can be rearranged by hand afterwards. For a system diagram of [[COMMAND — Quant Operations Platform]] where each box should open the actual note, a canvas beats a Mermaid block.

Node types the spec defines: text, file (embed a note), link (a URL), and group. Edges connect nodes by id, with optional sides and labels.

The `json-canvas` skill vendored in `.claude/skills/` carries the exact schema and worked examples.

## Related

- [[C4 Model]] — when to reach for a Mermaid diagram instead
