---
summary: "How an agent operates this vault at a professional standard - the retrieval cost ladder, note-type conventions, and the failure modes to watch for."
---

# Agent Guide

How an agent operates this vault at a professional standard. `CLAUDE.md` is the router — the *rules*. This is the *craft*: what to reach for, in what order, and what the failure modes look like.

## The four levels, as Obsidian features

Each level answers one question, and each is implemented with specific machinery.

| Level | The question | Obsidian feature | This vault |
|---|---|---|---|
| **1 — Router** | "Find it by exact name" | Filenames, folders, quick switcher, `[[wikilinks]]` | `CLAUDE.md` auto-loads; [[PARA Method]] folders; `_Index.md` per folder |
| **2 — Wiki** | "Pull everything on a topic together" | Backlinks pane, unlinked mentions, `aliases`, Properties | `50-Wiki/` entities; `Memory.md` via `@import`; `/remember`, `/process-inbox` |
| **3 — Semantic search** | "I searched different words than I wrote" | (not native — Smart Connections, or a script) | [[brain_search]] + `/recall`; local embeddings, gitignored index |
| **4 — Knowledge graph** | "Trace a relationship chain" | Frontmatter link properties, graph view, **Bases** | Typed predicates in [[Graph Schema]]; [[brain_graph]] + `/graph`; `.base` dashboards |

**Level 5 is deliberately not built** — see ADR-0001. Don't add always-on automation without one of its build-triggers firing.

## The retrieval cost ladder

**Escalate only when the cheaper primitive can't answer the question.** A 300-line note opened to read 15 lines is 285 lines of wasted context.

| Need | Reach for | Cost |
|---|---|---|
| Does a note exist? What's it called? | `_Index.md`, or `ls 50-Wiki/**` | **Cheapest** |
| What's this note about? | Its `summary:` frontmatter | Cheap |
| What's this note about, across 60 notes? | `grep -h '^summary:' -r 50-Wiki/` | Cheap, and answers "which one?" |
| A specific claim inside it | `Grep -C 3 "<term>"` | Medium |
| The whole argument | `Read` the note | **Expensive — last resort** |

Then, by question type:

1. **Grep / Read** — you know roughly what it's called or what words it use. In a vault this size this is *usually the right answer*.
2. **Backlinks / following `[[wikilinks]]`** — you have one note and want its neighbourhood. On a well-linked vault, traversing hand-made links often beats vector search: those links encode judgments about relevance that embeddings only approximate.
3. **`/graph <entity>`** — a *typed* relationship or a chain: "who works where", "how do these connect".
4. **`/recall <question>`** — keyword search failed because the note uses different vocabulary. A **fallback, not a default**.
5. **`/vault-status`** — what's *missing* rather than what exists.

**Never claim the vault has nothing until both the index and a full-text search come back empty — and say that you searched.**

**Every note carries a one-line `summary:`, and that is not decoration.** `grep -h '^summary:' -r 50-Wiki/` returns the whole wiki's contents for the price of one small read — cheaper than opening three notes, and enough to pick the right one. Write the summary as the note's *claim*, never its category: "a safety mechanism an agent can reset is not a safety mechanism" tells the next agent whether to open the file; "a trading concept" does not.

## Renaming is dangerous — read this before moving anything

Obsidian rewrites inbound `[[wikilinks]]` **only when the rename happens inside the app.** In an agent session Obsidian isn't running, so `mv` / `git mv` / write-then-delete renames the file at the OS level and every link pointing at it breaks silently.

If a rename is genuinely needed: grep the vault for the old name, rewrite every inbound link in the same commit, rebuild the graph, and confirm zero unresolved links. On a machine where Obsidian *is* running, `obsidian move` does this correctly — that's the one job the CLI does that the filesystem can't.

**Prefer `aliases:` over renaming.** An alias preserves every existing link, feeds unlinked-mentions, and costs nothing.

## Writing notes: the professional bar

**Note types are not interchangeable** — this is the single most common quality failure:

- **Entity notes** (People / Companies / Tools) are deliberately **thin**. Link infrastructure and backlink targets. Don't write essays here.
- **Concept notes** carry the thinking. Prefer a **declarative claim** title you can defend over a bare noun. If one runs past ~300 words, look for a second claim hiding inside.
- **Project master notes** are *reference*: facts, architecture, status. The moment you catch yourself writing "we chose X because…", stop — that's an **ADR**.
- **ADRs** are immutable once accepted. Later learning goes in a dated `## Amendments` section, never by rewriting Context.

Per [[Diataxis]]: mixing these modes is the dominant documentation failure, and it damages both halves.

## Linking: earn every backlink

- **Never a bare wikilink in a Related section.** Every curated link carries an em-dash clause saying *how* the notes relate. **If you can't state it, don't add the link.**
- **Curate by hand, list in bulk with queries.** A hand-written link creates a backlink; a `.base` query creates none. So annotate the handful that matter and let a Bases view carry "everything of type X". Hand-listing forty notes buries the signal in the target's backlink pane.
- **Store each fact once, on the subject's note.** Jane's note says `works_at`; Acme's doesn't mirror it. The reverse direction comes free from backlinks and the graph.
- **Quote every link in frontmatter** — `works_at: "[[Acme]]"`. Unquoted brackets are invalid YAML and break parsing silently.

## Growing the vault

A session that only reads has failed. Write as you go:

- **Entity trigger** — a person, company, tool, or concept comes up as more than a passing mention → its wiki note exists before the turn ends.
- **Answer capture** — the vault couldn't answer, and you answered from knowledge or research → save the distilled answer. The question is the proof it was worth keeping.
- **Decision capture** — a real choice with alternatives → an ADR, not a bullet.
- **`/wrap`** harvests a whole conversation at the end.

**The guardrail is [[Context vs Connections]]**: distilled evergreen knowledge only, never transcripts or logs. An agent can generate notes cheaply, which makes note-spam the characteristic agent failure. If it wouldn't matter in a month, it doesn't go in.

**Before creating a note, check whether it already exists** under a different name — search first, and prefer adding an `alias` or enriching the existing note over creating a near-duplicate. Duplicates with no canonical source are the number-one cause of [[Documentation Rot]].

## Capabilities beyond plain file edits

Five official Obsidian skills are vendored in `.claude/skills/` and load automatically:

| Reach for | When |
|---|---|
| `obsidian-markdown` | Exact callout, embed, block-reference, or property syntax |
| `obsidian-bases` | Authoring or fixing a `.base` dashboard |
| [[Obsidian CLI]] | Driving the vault from the shell rather than editing files blind |
| [[JSON Canvas]] | A visual map where boxes should open real notes — see `Vault Architecture.canvas` |
| [[Defuddle]] | **Capturing a web page** — prefer it over WebFetch; clean markdown, fewer tokens |

## Failure modes to watch for

- **Reading without writing.** The default failure. The Stop hook catches it; don't wait for the hook.
- **Note-spam to look productive.** The opposite failure. `/wrap` explicitly forbids inventing notes.
- **Bare links.** A Related section of unannotated wikilinks is noise wearing the costume of structure.
- **Rationale leaking into reference.** Architecture tables that explain *why*. Move it to an ADR.
- **Untyped relationships.** If everything is `related`, the graph can't answer anything a backlink pane couldn't.
- **Derived files in git.** `90-System/Graph/` and `Search Index/` are gitignored on purpose — they're per-machine and would conflict endlessly.

## Related

- [[Second Brain Levels]] — the roadmap and the Level 5 build-triggers
- [[Graph Schema]] — the relationship vocabulary
- [[Documentation Rot]] — why these rules exist
