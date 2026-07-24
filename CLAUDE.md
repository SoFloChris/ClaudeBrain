# ClaudeBrain — Router

This file is the system prompt and router for my second brain. Read it first in every session. It tells you who I am, how I work, and where everything lives.

## Who I am

- Name: Chris Aguirre
- Email: chris.aguirre333@gmail.com
- Fill in: role, current focus, and anything an assistant should always know about you.

## How this vault works

This is an Obsidian vault of plain markdown files, synced between my laptop and desktop with git. You (Claude) are expected to read, search, create, and update notes here.

Design principles (in priority order):

1. **Reverse engineer for recall.** Files are organized around how I will ask for them later. Before filing anything, ask: "what question would retrieve this?"
2. **Context vs. connections.** Store evergreen context (people, projects, decisions, reference material). Do NOT hoard transient noise (chat threads, one-off emails, raw logs). Summarize what matters, discard the rest.
3. **Boring is beautiful.** A clean folder of markdown files is the foundation. Do not invent new top-level folders, databases, or clever schemes. Work within the map below.
4. **Start at the lowest level.** This vault is a Level 1–2 brain (router + wiki). Only add complexity (semantic search, knowledge graphs, automation) when a concrete pain point demands it. See `90-System/Second Brain Levels.md`.

## Where files live

| Folder | Purpose |
|---|---|
| `00-Inbox/` | Capture zone. Unprocessed notes and daily notes land here. Empty it regularly into the folders below. |
| `10-Projects/` | Active efforts with an outcome and an end date. One folder or note per project. |
| `20-Areas/` | Ongoing responsibilities with no end date (health, finances, home, work areas). |
| `30-Resources/` | Reference material by topic — things I might use someday. |
| `40-Archive/` | Completed projects and inactive notes. Move things here instead of deleting. |
| `50-Wiki/` | Evergreen entities: `People/`, `Companies/`, `Concepts/`. One note per entity, linked with `[[wikilinks]]`. |
| `90-System/` | The machinery: `Memory.md`, `Templates/`, and system docs. Rarely touched during normal capture. |

Each folder has an `_Index.md` — a map of content listing what's inside. Keep indexes current when adding or moving notes.

## Memory (auto-loaded)

My durable facts and preferences load with this file every session:

@90-System/Memory.md

## Rules for Claude

- **Filing:** New raw input goes to `00-Inbox/` unless I say where it belongs. When processing the inbox, move notes to the correct folder and update that folder's `_Index.md`.
- **Memory:** When you learn a durable fact about me, my projects, or my preferences, append it to `90-System/Memory.md` under the right heading with today's date (the `/remember` command does this too). Never store secrets or credentials there.
- **Linking:** Prefer `[[wikilinks]]` to people, companies, and concepts in `50-Wiki/`. Create the wiki note (from the matching template in `90-System/Templates/`) if it doesn't exist.
- **Typed relationships:** Record facts like "works at" as frontmatter (`works_at: "[[Acme]]"`, quoted, snake_case) using only the predicates in `90-System/Graph Schema.md`. That's what powers `/graph`.
- **Recall tools:** `/recall <question>` for semantic + keyword search across the vault; `/graph <entity>` for relationship questions; plain Grep/Read for everything else (often best — this vault is small).
- **Naming:** Descriptive Title Case filenames, no dates in titles except daily notes (`YYYY-MM-DD`).
- **Templates:** Use `90-System/Templates/` when creating projects, people, companies, concepts, meetings, or resources.
- **Deleting:** Don't. Archive to `40-Archive/` instead, and note the move in the relevant `_Index.md`.
