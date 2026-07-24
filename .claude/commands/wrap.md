---
description: Harvest this conversation into the vault — notes, links, memory
---

Sweep everything durable from this conversation into the vault. Work through the checklist, then report.

1. **Entities.** List every person, company, tool, and concept that came up as more than a passing mention. For each: create its `50-Wiki/` note from the matching template (or enrich the existing one) — typed frontmatter per `90-System/Graph Schema.md`, at least two honest `[[wikilinks]]`, one or two Key facts.
2. **Facts about me.** Anything durable I revealed (preferences, situation, relationships, current focus) → `90-System/Memory.md` under the right heading, dated. No secrets or credentials.
3. **Decisions.** Anything we decided → the relevant project note's Decisions section (create the project from the template if it doesn't exist).
4. **Answers & research.** Any question I asked that the vault couldn't answer, which you answered from knowledge or research → distill into a note in `30-Resources/` or `50-Wiki/Concepts/`. Distilled means: what I'd want to re-read in a month, not a transcript.
5. **Open loops.** Tasks or follow-ups mentioned but not tracked → check them into the relevant project note, or drop a note in `00-Inbox/` if homeless.
6. **Housekeeping.** Update every `_Index.md` you touched, then rebuild the graph: `python3 "90-System/Scripts/brain_graph.py" build`
7. **Report.** List what you added or changed as `[[wikilinks]]`, one line each. If the honest answer for a step was "nothing", say so — don't invent notes to look productive. Quality bar: context vs. connections; if it wouldn't matter in a month, skip it.
