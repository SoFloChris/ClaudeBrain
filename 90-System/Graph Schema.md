# Graph Schema

The controlled vocabulary for this vault's knowledge graph. Every typed relationship is a frontmatter key whose value is a quoted `"[[wikilink]]"` (or a list of them). The key name **is** the relationship type. Stick to this list — invent a new predicate only when none fits, and add it here when you do.

## Node types (`type:` — plain string, never a link)

`person` · `company` · `tool` · `concept` · `project` · `area` · `resource` · `reference` · `adr` · `runbook` · `moc` · `meeting` · `changelog`

`resource` vs `reference`: a **resource** is external material filed by topic in `30-Resources/` (an article, a video, a researched answer). A **reference** documents a system I own — a service, a component, an architecture — and lives beside its project under `10-Projects/<Project>/`, carrying `project:` back to the master note.

Wiki subfolders: `50-Wiki/People/`, `Companies/`, `Tools/`, `Concepts/`.
Per-project documentation: `10-Projects/<Project>/decisions/NNNN-title-with-dashes.md` (ADRs, per MADR convention).

## Predicates (frontmatter keys → typed edges)

| Predicate | Used on | Meaning |
|---|---|---|
| `works_at` | person | Employment/affiliation: person → company |
| `knows` | person | Person → person connection |
| `people` | company, project | Members/contacts: entity → people |
| `companies` | project | Organizations involved |
| `related` | any | Generic "meaningfully connected" when nothing sharper fits |
| `author` | resource | Who made it |
| `topic` | resource | What it's about |
| `broader` | concept | Parent concept (hierarchy) |
| `built_by` | tool | Who makes it: tool → person/company |
| `uses` | project, tool | Depends on / is built with |
| `alternative_to` | tool | Competing or substitutable option |
| `inspired_by` | concept, tool | Where the idea came from |
| `project` | adr, runbook, changelog, reference | Which project this document belongs to |
| `decision_makers` | adr | Who made the call |
| `owner` | runbook | Who maintains it |
| `supersedes` | adr | This ADR replaces an older one |
| `superseded_by` | adr | This ADR was replaced — set on **both** notes when superseding |

Body `[[wikilinks]]` become untyped `mentions` edges automatically — use them freely in prose; reserve frontmatter for facts worth typing.

## Rules

1. **Quote every link in YAML**: `works_at: "[[Acme]]"` — unquoted brackets are invalid YAML and break parsing.
2. **Store each fact once, on the subject's note.** Jane's note says `works_at: "[[Acme]]"`; Acme's note doesn't need a mirror entry (the graph and backlinks derive the reverse direction).
3. **Reserved keys carry no edges**: `type`, `summary`, `tags`, `aliases`, `status`, `created`, `updated`, `date`, `last_reviewed`, `last_tested`, plus plain-string fields like `role`, `relationship`, `source`, `due`, `repo`, `build`, `risk`, `reversible`, `versioning`.
   - **`summary:`** is one quoted sentence stating what a note *claims*, not what category it belongs to. It exists so an agent can decide whether to open a note without paying to read it. Currently **optional and unevenly present** — the notes salvaged from `claude/obsidian-second-brain-setup-0c0jdy` carry it, most others don't. Making it required vault-wide is a live proposal with its own ADR on that branch, not yet adopted.
4. snake_case predicate names, always.

## Consumers

- `90-System/Scripts/brain_graph.py` (`/graph`) — builds and queries the graph
- Obsidian natively: Properties UI, graph view, backlinks all understand frontmatter links
- Optional plugins that read the same data unchanged: **Bases** (core plugin since Obsidian 1.9.10 — per-entity dashboards, e.g. filter `type == "person"` and `works_at.contains(this)`), **Dataview** (ad-hoc queries), **Breadcrumbs** (multi-hop traversal in-app), **Graph Link Types** (labels edges in graph view)
