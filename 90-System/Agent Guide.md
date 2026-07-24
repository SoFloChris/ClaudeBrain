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

## Which tool for which question

Reach for the cheapest thing that answers it. Ordered by cost:

1. **Grep / Read** — you know roughly what it's called or what words it uses. In a vault this size this is *usually the right answer*, and the source framework says so explicitly.
2. **Backlinks / `[[wikilink]] `following** — you have one note and want its neighbourhood.
3. **`/graph <entity>`** — you want a *typed* relationship or a chain: "who works where", "how do these two connect".
4. **`/recall <question>`** — keyword search failed because the note uses different vocabulary. Semantic search is a **fallback, not a default**.
5. **`/vault-status`** — you want to know what's missing rather than what exists.

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
