#!/usr/bin/env python3
"""ClaudeBrain knowledge graph — Level 4.

Builds a graph of entities and relationships from the vault's markdown files,
then answers relationship queries over it. Pure standard library; no installs.

Sources of graph data:
  - Frontmatter properties whose values contain [[wikilinks]] become TYPED edges
    (property name = relationship), e.g. `works_at: "[[Acme]]"` -> (note)-[works_at]->(Acme).
  - [[wikilinks]] in note bodies become untyped `mentions` edges.
  - `type:` frontmatter (person/company/concept/project/...) labels each node,
    falling back to the note's folder.

Usage:
  python3 brain_graph.py build                 # writes 90-System/Graph/graph.json
  python3 brain_graph.py query "Some Entity"   # everything connected to an entity
  python3 brain_graph.py path "A" "B"          # shortest relationship chain A -> B
  python3 brain_graph.py stats                 # node/edge counts by type
"""

import json
import re
import sys
from collections import deque
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
GRAPH_PATH = VAULT / "90-System" / "Graph" / "graph.json"
SKIP_DIRS = {".obsidian", ".git", ".trash", "node_modules", "90-System"}
SKIP_REL_KEYS = {"type", "tags", "aliases", "status", "created", "cssclasses"}

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

FOLDER_TYPES = {
    "50-Wiki/People": "person",
    "50-Wiki/Companies": "company",
    "50-Wiki/Concepts": "concept",
    "10-Projects": "project",
    "20-Areas": "area",
    "30-Resources": "resource",
}


def iter_notes():
    for path in VAULT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def split_frontmatter(text):
    """Return (frontmatter_lines, body). Tolerates missing frontmatter."""
    if not text.startswith("---"):
        return [], text
    lines = text.splitlines()
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() in ("---", "..."):
            return lines[1:i], "\n".join(lines[i + 1:])
    return [], text


def parse_frontmatter(lines):
    """Minimal YAML subset: `key: value`, quoted strings, [a, b] inline lists,
    and `- item` block lists. Enough for Obsidian properties; not full YAML."""
    data = {}
    key = None
    for raw in lines:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        if re.match(r"^\s*-\s+", raw) and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(_scalar(re.sub(r"^\s*-\s+", "", raw)))
            continue
        m = re.match(r"^([A-Za-z0-9_ -]+):\s*(.*)$", raw)
        if not m:
            continue
        key, value = m.group(1).strip(), m.group(2).strip()
        if value == "":
            data[key] = []  # may be filled by following `- item` lines
        elif value.startswith("[") and value.endswith("]"):
            items = re.findall(r'"[^"]*"|\'[^\']*\'|[^,\[\]]+', value[1:-1])
            data[key] = [_scalar(i) for i in items if _scalar(i)]
        else:
            data[key] = _scalar(value)
    return data


def _scalar(value):
    return value.strip().strip("\"'").strip()


def build():
    nodes, edges = {}, []

    def ensure_node(name, ntype="unknown", path=None):
        node = nodes.setdefault(name, {"type": ntype, "path": path})
        if node["type"] == "unknown" and ntype != "unknown":
            node["type"] = ntype
        if node["path"] is None and path:
            node["path"] = path
        return node

    for path in iter_notes():
        name = path.stem
        if name in ("_Index", "Home", "SETUP", "README", "CLAUDE"):
            continue
        rel = path.relative_to(VAULT).as_posix()
        fm_lines, body = split_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        fm = parse_frontmatter(fm_lines)

        ntype = str(fm.get("type") or "") or next(
            (t for prefix, t in FOLDER_TYPES.items() if rel.startswith(prefix)), "note"
        )
        ensure_node(name, ntype, rel)

        for prop, value in fm.items():
            if prop.lower() in SKIP_REL_KEYS:
                continue
            values = value if isinstance(value, list) else [value]
            for v in values:
                for target in WIKILINK.findall(str(v)):
                    target = target.strip()
                    if target and target != name:
                        ensure_node(target)
                        edges.append({"from": name, "rel": prop, "to": target})

        typed = {(e["from"], e["to"]) for e in edges}
        for target in WIKILINK.findall(body):
            target = target.strip()
            if "/" in target:
                target = target.rsplit("/", 1)[-1]
            if target and target != name and (name, target) not in typed:
                ensure_node(target)
                edges.append({"from": name, "rel": "mentions", "to": target})

    # de-duplicate edges
    seen, unique = set(), []
    for e in edges:
        k = (e["from"], e["rel"], e["to"])
        if k not in seen:
            seen.add(k)
            unique.append(e)

    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_PATH.write_text(
        json.dumps({"nodes": nodes, "edges": unique}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"graph: {len(nodes)} nodes, {len(unique)} edges -> {GRAPH_PATH.relative_to(VAULT)}")


def load():
    if not GRAPH_PATH.exists():
        sys.exit("No graph yet — run: python3 brain_graph.py build")
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def find_node(nodes, query):
    if query in nodes:
        return query
    low = query.lower()
    matches = [n for n in nodes if low in n.lower()]
    if not matches:
        sys.exit(f"No entity matching '{query}'")
    if len(matches) > 1:
        print(f"(matched '{matches[0]}'; other candidates: {', '.join(matches[1:5])})")
    return matches[0]


def query(name):
    g = load()
    node = find_node(g["nodes"], name)
    info = g["nodes"][node]
    print(f"{node}  [{info['type']}]  {info.get('path') or ''}".rstrip())
    out = [e for e in g["edges"] if e["from"] == node]
    inc = [e for e in g["edges"] if e["to"] == node]
    for e in sorted(out, key=lambda e: (e["rel"] == "mentions", e["rel"])):
        print(f"  -[{e['rel']}]-> {e['to']}")
    for e in sorted(inc, key=lambda e: (e["rel"] == "mentions", e["rel"])):
        print(f"  <-[{e['rel']}]- {e['from']}")
    if not out and not inc:
        print("  (no connections)")


def path_between(a, b):
    g = load()
    start, goal = find_node(g["nodes"], a), find_node(g["nodes"], b)
    adj = {}
    for e in g["edges"]:
        adj.setdefault(e["from"], []).append((e["to"], e["rel"], "->"))
        adj.setdefault(e["to"], []).append((e["from"], e["rel"], "<-"))
    prev, queue, seen = {}, deque([start]), {start}
    while queue:
        cur = queue.popleft()
        if cur == goal:
            break
        for nxt, rel, direction in adj.get(cur, []):
            if nxt not in seen:
                seen.add(nxt)
                prev[nxt] = (cur, rel, direction)
                queue.append(nxt)
    if goal not in prev and start != goal:
        sys.exit(f"No path between '{start}' and '{goal}'")
    steps, cur = [], goal
    while cur != start:
        parent, rel, direction = prev[cur]
        arrow = f"-[{rel}]->" if direction == "->" else f"<-[{rel}]-"
        steps.append(f"{arrow} {cur}")
        cur = parent
    print(start, " ".join(reversed(steps)))


def stats():
    g = load()
    by_type, by_rel = {}, {}
    for info in g["nodes"].values():
        by_type[info["type"]] = by_type.get(info["type"], 0) + 1
    for e in g["edges"]:
        by_rel[e["rel"]] = by_rel.get(e["rel"], 0) + 1
    print(f"nodes: {len(g['nodes'])}")
    for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    print(f"edges: {len(g['edges'])}")
    for r, c in sorted(by_rel.items(), key=lambda x: -x[1]):
        print(f"  {r}: {c}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        build()
    elif cmd == "query" and len(sys.argv) > 2:
        query(sys.argv[2])
    elif cmd == "path" and len(sys.argv) > 3:
        path_between(sys.argv[2], sys.argv[3])
    elif cmd == "stats":
        stats()
    else:
        print(__doc__)
