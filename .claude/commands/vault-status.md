---
description: Vault health — orphans, stubs, broken links, and what needs writing
allowed-tools: Bash(python3 *), Read, Grep
---

Report on the health of the vault and turn it into a work list.

1. Run `python3 "90-System/Scripts/vault_stats.py"`
2. Run `python3 "90-System/Scripts/brain_graph.py" build` then `stats` for the graph shape.
3. Read the output and tell me, in priority order:
   - **Broken links** — notes that are linked but don't exist. Each one is a note someone already decided was worth referencing; offer to write them.
   - **Orphans** — notes with no links in or out. Either they need connecting, or they were noise and belong in `40-Archive/`.
   - **Stubs** — notes too thin to be useful. Say which deserve expanding and which are fine as thin entity notes (People/Companies/Tools are *meant* to be thin).
   - **Shape** — is the graph mostly `mentions` edges? That means relationships aren't typed; suggest which frontmatter predicates from `90-System/Graph Schema.md` would add real structure.
4. Offer to fix the top few right now. Don't fix anything without saying what you're about to do.
