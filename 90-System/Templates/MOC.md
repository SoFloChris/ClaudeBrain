---
type: moc
# What this map collects, and the thread connecting them.
summary: ""
aliases: []
related: []
tags:
  - moc
created: {{date}}
updated: {{date}}
---

# {{title}} MOC

> [!abstract] What this map is for
> One or two lines: what question this map answers, and when to come back to it.

> **Build a MOC only at a "mental squeeze point"** — when scattered notes on a topic have
> become genuinely overwhelming. Don't create them preemptively. A MOC is *curated*
> (omission is a feature); an `_Index.md` is *exhaustive* (every file listed). They are
> different species — keep both.

The through-line: state the idea that organizes everything below.

## Decided

- [[ ]] — why it's settled

## Working theories

- [[ ]] — what I currently believe and what would change my mind

## Open questions

- [[ ]] — what's unresolved

## Everything else on this topic

<!-- Bulk listing goes in a query, not hand-written links — queries create no backlink noise. -->

```dataview
LIST
FROM #topic-tag
WHERE !contains(file.name, "MOC") AND !contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```
