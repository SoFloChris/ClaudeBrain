---
type: concept
aliases: [C4]
related: ["[[Diataxis]]", "[[Architecture Decision Record]]"]
tags:
  - concept
---

# C4 Model

Simon Brown's four levels of architecture diagram, each a zoom level on the one above:

1. **System Context** — the system as one box, its users, and the systems it talks to. Audience: everybody.
2. **Container** — the separately runnable things inside it (apps, data stores) and how they communicate. Audience: technical people.
3. **Component** — what's inside one container. *Not recommended by default.*
4. **Code** — classes and functions. *Not recommended*; generate from an IDE if ever needed.

**Draw levels 1 and 2 and stop.** That's Brown's own guidance — "sufficient for most software development teams" — and it's the maintenance argument too: context and container diagrams change slowly, component diagrams change every refactor, code diagrams are stale within days.

## "Container" does not mean Docker

Brown's own disclaimer leads the page: a container is **an application or a data store** — anything that must be *running* for the system to work. A Spring app, an Angular SPA, a database schema, a serverless function, even a shell script. A JAR or DLL is **not** a container; those organize code *inside* one. The test is the runtime boundary, not the deployment tooling.

## Notation is free — and that matters here

C4 is deliberately notation-independent, and in Aug 2025 Brown *removed* the prescriptive box-style examples from the site in favour of plain requirements. What's actually required:

- Every element states its **type** and, for containers/components, its **technology**.
- Every diagram has a **title** and a **key/legend**.
- Every relationship is unidirectional, labelled, and — between containers — names the **protocol**. Explicitly: avoid bare labels like "Uses".

## Why this vault draws C4 with `flowchart`, not Mermaid's `C4Context`

Tested against the Mermaid versions Obsidian actually bundles (11.4.1 and 11.13.0). Mermaid's dedicated C4 syntax renders, but three things disqualify it for a linked vault:

1. **It can't link to notes.** `class node internal-link` — Obsidian's mechanism for clickable diagram nodes — is a *parse error* inside a C4 block. A C4-syntax diagram is a dead image; a flowchart one is a navigation surface.
2. **It hardcodes colours.** The docs say so outright: "C4 diagram is fixed style... different css is not provided under different skins." Titles and relationship labels render `#444444` — nearly invisible on a dark theme, and relationship labels are where the protocols live.
3. **It's officially experimental** with a renderer rewrite (`c4-beta`) actively landing, so existing diagrams will change appearance.

Flowchart syntax has been stable for years, honours the theme, renders a legend, and supports `internal-link`. Since notation is free, **a flowchart with proper C4 labels *is* a compliant C4 diagram**.

## Practical rules

- **Quote every node label.** Unquoted parentheses break the parser.
- **Never put `[[wikilinks]]` inside a Mermaid block** — they break parsing raw, render as inert text when quoted, and Obsidian's graph and backlinks can't see inside the block anyway. Put the links in prose *underneath* the diagram.
- Pin both `fill` and `color` in `classDef` so boxes survive light and dark themes.
- Obsidian 1.13.0 added a one-time per-vault consent banner before it renders Mermaid at all — if diagrams look broken, check that first.

## Related

- [[Diataxis]] — architecture diagrams are *reference*; the reasoning behind them belongs in an [[Architecture Decision Record]]
