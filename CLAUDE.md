# ClaudeBrain — Router

This file is the system prompt and router for my second brain. Read it first in every session. It tells you who I am, how I work, and where everything lives.

## Who I am

- Name: Chris Aguirre — my hub note is [[Chris Aguirre]]; link new people/employers to it so the graph maps my world
- Email: chris.aguirre333@gmail.com
- Fill in: role, current focus, and anything an assistant should always know about you.

## How this vault works

This is an Obsidian vault of plain markdown files, synced between my laptop and desktop with git. You (Claude) are expected to read, search, create, and update notes here.

Design principles (in priority order):

1. **Reverse engineer for recall.** Files are organized around how I will ask for them later. Before filing anything, ask: "what question would retrieve this?"
2. **Context vs. connections.** Store evergreen context (people, projects, decisions, reference material). Do NOT hoard transient noise (chat threads, one-off emails, raw logs). Summarize what matters, discard the rest.
3. **Boring is beautiful.** A clean folder of markdown files is the foundation. Do not invent new top-level folders, databases, or clever schemes. Work within the map below.
4. **Start at the lowest level.** This vault runs at Levels 1–4 (router, wiki, semantic search, knowledge graph). Only add Level 5 complexity (always-on automation) when a concrete pain point demands it. See `90-System/Second Brain Levels.md`.
5. **A session that only reads has failed.** You are a co-author of this vault, not a search engine over it. Every substantive session should leave the vault richer — see "Grow the vault" below.

## Where files live

| Folder | Purpose |
|---|---|
| `00-Inbox/` | Capture zone. Unprocessed notes and daily notes land here. Empty it regularly into the folders below. |
| `10-Projects/` | Active efforts with an outcome and an end date. One folder or note per project. |
| `20-Areas/` | Ongoing responsibilities with no end date (health, finances, home, work areas). |
| `30-Resources/` | Reference material by topic — things I might use someday. |
| `40-Archive/` | Completed projects and inactive notes. Move things here instead of deleting. |
| `50-Wiki/` | Evergreen entities: `People/`, `Companies/`, `Tools/`, `Concepts/`. One note per entity, linked with `[[wikilinks]]`. |
| `90-System/` | The machinery: `Memory.md`, `Templates/`, and system docs. Rarely touched during normal capture. |

Each folder has an `_Index.md` — a map of content listing what's inside. Keep indexes current when adding or moving notes.

## The craft

`90-System/Agent Guide.md` is the working manual — which tool answers which question, the note-type conventions, the failure modes, and the vendored Obsidian skills. Read it when doing substantive work in the vault.

## Memory (auto-loaded)

My durable facts and preferences load with this file every session:

@90-System/Memory.md

## Grow the vault (do this without being asked)

Reading is half the job. The other half is writing, in the flow of normal conversation:

- **Entity trigger.** The moment a person, company, tool, or concept comes up as more than a passing mention — in my messages, in research you do, in work we discuss — create its wiki note from the template, with typed frontmatter per the Graph Schema. Don't queue it, don't ask permission. A one-line note with two good links beats no note.
- **Answer capture.** If I ask something the vault can't answer and you answer from general knowledge or research, save the distilled answer (to `30-Resources/` or `50-Wiki/Concepts/`) before finishing the turn. The fact that I asked proves it's worth retrieving later — that's "reverse engineer for recall."
- **Decision capture.** When we decide something (approach, tool choice, plan), record it in the relevant project note's Decisions section, or create the project note if none exists.
- **Connect while writing.** Every note you create or touch: link related notes with `[[wikilinks]]` (only where the connection is real), add typed frontmatter edges where a Graph Schema predicate fits, and update the folder's `_Index.md`.
- **End-of-session sweep.** Before ending any substantive session, do a 30-second pass: any entity, fact, decision, or answer from this conversation not yet in the vault? Write it now. `/wrap` runs this explicitly.
- **The guardrail** is still context vs. connections: capture distilled, evergreen knowledge — never raw transcripts, logs, or play-by-play. If it wouldn't matter in a month, it doesn't go in.

## Linking discipline

Backlinks are only valuable if every one of them was deliberate. Two rules keep them that way:

- **Never write a bare wikilink in a "Related" section.** Every curated link carries an em-dash clause saying *how* the notes relate: `- [[Graph Schema]] — defines which of these links become typed edges.` **If you can't state the relationship, don't add the link.** A forced link is worse than a missing one.
- **Curate by hand, list in bulk with queries.** A hand-written `[[link]]` creates a backlink; a Bases/Dataview query does not. So hand-link the handful you can annotate, and use a `.base` view for "everything tagged X". Never hand-list 40 notes — that buries the signal in the target's backlink pane.

Note-type conventions (from Andy Matuschak's evergreen-note practice):

- **Concept notes carry the thinking.** Prefer declarative claim titles that make an argument (`Notes Should Be Atomic`) over bare nouns (`Atomicity`); bare nouns are for defining core terms. If a note runs past ~300 words, look for a second claim hiding inside it.
- **Entity notes (People/Companies/Tools) are deliberately thin.** They're link infrastructure and backlink targets, not essays. Don't over-invest in them.
- **Use `aliases`** on entities and concepts — it feeds Obsidian's unlinked-mentions pane, which is the cheapest way to find connections you missed.

## Rules for Claude

- **Filing:** New raw input goes to `00-Inbox/` unless I say where it belongs. When processing the inbox, move notes to the correct folder and update that folder's `_Index.md`.
- **Memory:** When you learn a durable fact about me, my projects, or my preferences, append it to `90-System/Memory.md` under the right heading with today's date (the `/remember` command does this too). Never store secrets or credentials there.
- **Linking:** Prefer `[[wikilinks]]` to people, companies, and concepts in `50-Wiki/`. Create the wiki note (from the matching template in `90-System/Templates/`) if it doesn't exist.
- **Typed relationships:** Record facts like "works at" as frontmatter (`works_at: "[[Acme]]"`, quoted, snake_case) using only the predicates in `90-System/Graph Schema.md`. That's what powers `/graph`.
- **Recall tools:** `/recall <question>` for semantic + keyword search across the vault; `/graph <entity>` for relationship questions; plain Grep/Read for everything else (often best — this vault is small).
- **Naming:** Descriptive Title Case filenames, no dates in titles except daily notes (`YYYY-MM-DD`).
- **Templates:** Use `90-System/Templates/` when creating projects, people, companies, concepts, meetings, or resources.
- **Deleting:** Don't. Archive to `40-Archive/` instead, and note the move in the relevant `_Index.md`.
