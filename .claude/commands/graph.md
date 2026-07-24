---
description: Query the vault's knowledge graph (relationships between people, companies, concepts)
argument-hint: [entity, or "A -> B" for a connection path]
allowed-tools: Bash(python3 *)
---

Answer this relationship question using the vault's knowledge graph: $ARGUMENTS

1. Rebuild the graph first (it's instant): `python3 "90-System/Scripts/brain_graph.py" build`
2. Then:
   - For a single entity: `python3 "90-System/Scripts/brain_graph.py" query "<entity>"`
   - For how two things connect: `python3 "90-System/Scripts/brain_graph.py" path "<A>" "<B>"`
   - For an overview: `python3 "90-System/Scripts/brain_graph.py" stats`
3. The graph gives you the skeleton — open the actual notes in `50-Wiki/` to flesh out the answer with facts before responding.
4. If the graph is missing a relationship you can see in the notes, fix the source note's frontmatter (e.g. `works_at: "[[Company]]"`) so it's captured next time.
