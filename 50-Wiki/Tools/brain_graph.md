---
type: tool
related: ["[[Knowledge Graph]]", "[[Graph Schema]]"]
alternative_to: ["[[LightRAG]]"]
---

# brain_graph

This vault's [[Knowledge Graph]] engine — `90-System/Scripts/brain_graph.py`, invoked by `/graph`. Level 4, pure standard library, zero dependencies.

## How it works

- **Typed edges** come from frontmatter: any property whose value contains a `[[wikilink]]` becomes an edge whose *type is the property name* (`works_at: "[[Acme]]"` → `-[works_at]->`). Vocabulary is fixed by [[Graph Schema]].
- **Untyped edges** come from body wikilinks, recorded as `mentions`. Links inside code spans and code blocks are ignored (they're examples, not relationships).
- Node types come from `type:` frontmatter, falling back to the folder.
- Output is `90-System/Graph/graph.json` — gitignored and rebuilt on demand.

## Commands

```
python3 90-System/Scripts/brain_graph.py build            # compile the graph
python3 90-System/Scripts/brain_graph.py query "Entity"   # everything connected
python3 90-System/Scripts/brain_graph.py path "A" "B"     # shortest chain A → B
python3 90-System/Scripts/brain_graph.py stats            # counts by type
```

`path` is the payoff — the relationship-chain tracing that no backlink pane or vector search can do.

## Related

- [[brain_search]] — the Level 3 sibling
