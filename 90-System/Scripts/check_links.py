#!/usr/bin/env python3
"""Fail if any [[wikilink]] in the vault points at a note that doesn't exist.

`vault_stats.py` reports broken links as part of a health summary and always
exits 0. This is the enforcing version: it exits non-zero so CI can block a
merge, and it reports file:line so the fix is one click away.

Two deliberate differences from vault_stats:

1. **Notes are keyed by relative path, not filename stem.** vault_stats keys by
   stem, so all six `_Index.md` files collapse into one entry and five of them
   are never checked at all. Every file gets scanned here.
2. **Anything under the vault is a valid link target**, including
   `90-System/Templates/` and `90-System/Scripts/`, which vault_stats excludes
   from its note set. `50-Wiki/_Index.md` legitimately links to the templates;
   those links are real and must resolve.
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".obsidian", ".git", ".trash", "node_modules", ".claude"}
# Scanned for outbound links. Templates hold empty `[[ ]]` placeholders and
# Scripts/Graph hold generated or example text — all still valid link targets.
SKIP_SCAN_PREFIXES = ("90-System/Templates/", "90-System/Scripts/",
                      "90-System/Graph/", "90-System/Search Index/")
# Matches vault_stats.py / brain_graph.py: inside markdown tables the alias pipe
# is escaped (`[[note\|Alias]]`), so the trailing backslash must come off.
WIKILINK = re.compile(r"\[\[([^\]|#]+?)\\?(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def markdown_files():
    for path in sorted(VAULT.rglob("*.md")):
        if not any(part in SKIP_DIRS for part in path.parts):
            yield path


def strip_code(text):
    """Links inside code blocks and spans are documentation examples, not links.
    Fenced blocks are replaced with their newlines so line numbers stay honest."""
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text,
                  flags=re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


def main():
    files = list(markdown_files())
    by_stem, by_relpath = set(), set()
    for path in files:
        rel = path.relative_to(VAULT).with_suffix("").as_posix()
        by_stem.add(path.stem.lower())
        by_relpath.add(rel.lower())

    broken = []
    for path in files:
        rel = path.relative_to(VAULT).as_posix()
        if rel.startswith(SKIP_SCAN_PREFIXES):
            continue
        text = strip_code(path.read_text(encoding="utf-8", errors="replace"))
        for lineno, line in enumerate(text.splitlines(), start=1):
            for match in WIKILINK.finditer(line):
                target = match.group(1).strip()
                # Empty template placeholders and embedded Bases views aren't links.
                if not target or target.endswith(".base"):
                    continue
                key = target.lower()
                if key in by_relpath or key.rsplit("/", 1)[-1] in by_stem:
                    continue
                broken.append((rel, lineno, target))

    if broken:
        print(f"Found {len(broken)} broken wikilink(s):", file=sys.stderr)
        for rel, lineno, target in broken:
            print(f"  {rel}:{lineno}: [[{target}]]", file=sys.stderr)
        return 1

    print(f"OK — {len(files)} markdown files, no broken wikilinks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
