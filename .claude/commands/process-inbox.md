---
description: File everything in 00-Inbox into the right folders
---

Process the inbox:

1. List every note in `00-Inbox/` (including `Daily/`) except `_Index.md`.
2. For each note, decide (context vs. connections — keep evergreen context, drop transient noise):
   - Actionable with an end date → `10-Projects/` (create the project note from the template if new)
   - Ongoing responsibility → `20-Areas/`
   - Reference material worth keeping → `30-Resources/` (summarize; don't hoard raw dumps)
   - About a person/company/concept → merge the durable facts into the entity's note in `50-Wiki/` (create from template if missing)
   - Durable fact about me → append to `90-System/Memory.md` with today's date
   - Pure noise → tell me and ask before archiving it to `40-Archive/`
3. Daily notes older than 7 days: extract anything durable per the rules above, then move the daily note to `40-Archive/`.
4. Update every `_Index.md` you touched, and link entities with `[[wikilinks]]` as you go.
5. Rebuild the knowledge graph: `python3 "90-System/Scripts/brain_graph.py" build`
6. Finish with a short summary: what was filed where, and anything you need me to decide.
