---
type: adr
status: accepted
date: 2026-07-24
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[Knowledge Graph]]", "[[Graph Schema]]", "[[Dataview]]"]
tags:
  - adr
---

# ADR-0002 — Encode typed relationships as quoted-wikilink frontmatter

## Context and Problem Statement

A [[Knowledge Graph]] needs typed edges — "works at", "built by" — not just undifferentiated links. Obsidian offers several places to put that data: YAML frontmatter properties, [[Dataview]] inline fields (`key:: value`), or a prose "Relations" section. Which becomes the canonical store?

## Decision Drivers

- The data must be readable by Obsidian natively, by plugins, and by our own Python scripts.
- One canonical location per fact — duplicated relationship data is the fastest route to contradictions.
- Whatever agents write must be mechanically parseable without heuristics.

## Considered Options

- YAML frontmatter properties, values as quoted wikilinks
- Dataview inline fields (`works_at:: [[Acme]]`)
- A prose `## Relations` section per note

## Decision Outcome

Chosen option: **frontmatter properties**, because it's the only option every consumer can read. Obsidian treats frontmatter links as first-class — they appear in graph view and backlinks with no plugin installed — and Bases, Dataview, Breadcrumbs, and [[brain_graph]] all parse the same bytes.

### Consequences

- Good, because one representation serves the Properties UI, the graph view, every query plugin, and our scripts.
- Good, because extraction is a five-line regex, so agents can't get it subtly wrong.
- Bad, because YAML is picky: unquoted `[[...]]` is invalid and silently breaks parsing, so every link must be quoted.
- Neutral, because relationships stated mid-sentence in prose stay untyped `mentions` edges — acceptable, since prose links are self-annotating by context.

### Confirmation

`python3 90-System/Scripts/brain_graph.py build` reports zero unresolved links, and `stats` shows typed edges (not just `mentions`) for entity notes.

## Pros and Cons of the Options

### Dataview inline fields

- Good, because metadata can sit inline in a sentence where it reads naturally.
- Bad, because **only Dataview reads them** — the Properties UI, Bases, and every script ignore them. That's a single-vendor dependency for the vault's core data.

### A prose `## Relations` section

- Good, because it's human-readable with zero syntax rules.
- Bad, because nothing queries it. It's documentation of relationships, not data.

## More Information

Vocabulary is fixed in [[Graph Schema]]; adding a predicate means adding a row there. Falsified if Obsidian ever drops frontmatter-link support (very unlikely — it's core to Properties).

## Amendments

<!-- Append only. -->
