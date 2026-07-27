---
type: tool
summary: "Command-line access to a vault; the one job it does that the filesystem cannot is renaming a note without breaking inbound links."
aliases: [obsidian-cli]
built_by: "[[Dynalist Inc]]"
related: ["[[Obsidian]]", "[[Claude Code]]"]
tags:
  - tool
created: 2026-07-24
---

# Obsidian CLI

Command-line access to an [[Obsidian]] vault — read, create, and search notes, manage properties and tasks, without opening the app. Documented by the official `obsidian-cli` skill vendored in `.claude/skills/`.

## Why it matters to me

It's the difference between an agent that *edits files that happen to be in a vault* and one that *operates the vault*. Plain filesystem writes (what [[brain_search]] and [[brain_graph]] do) can't ask Obsidian anything — they can't resolve a link the way Obsidian would, or trigger a re-index. The CLI can.

It also covers plugin/theme development — reload plugins, run JavaScript in the app, capture errors, take screenshots, inspect the DOM — which is the path if this vault ever needs a custom plugin rather than another Python script.

## Related

- [[Claude Code]] — the agent that would drive it
- [[JSON Canvas]] — the other programmatic surface into a vault
