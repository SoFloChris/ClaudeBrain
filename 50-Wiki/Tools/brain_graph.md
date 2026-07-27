---
type: tool
summary: "This vault's knowledge graph engine, whose hand-rolled frontmatter parser is the fragile part to check first."
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

## The frontmatter parser is hand-rolled — check it first

`parse_frontmatter()` is a deliberate minimal-YAML subset (zero dependencies), which means **list properties are the fragile part**. It bit once already: the inline-list regex excluded `[` and `]` from unquoted items, so `uses: ["[[A]]", "[[B]]", "[[C]]"]` yielded only the *first* edge and silently dropped the rest — fixed 2026-07-27.

The failure mode is nasty because it's invisible: no error, no broken link, no orphan. The graph just quietly under-reports, and `stats` looks plausible. **When edge counts feel low, test the parser on a real line before trusting the numbers:**

```bash
python3 -c "import importlib.util; s=importlib.util.spec_from_file_location('bg','90-System/Scripts/brain_graph.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.parse_frontmatter(['related: [\"[[A]]\", \"[[B]]\"]']))"
```

Anything other than two intact `[[wikilinks]]` back means the parser is eating edges again.

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
