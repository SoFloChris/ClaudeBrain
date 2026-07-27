#!/usr/bin/env python3
"""Validate every note's YAML frontmatter, and the conventions the graph depends on.

The failure this catches is silent: an unquoted `[[wikilink]]` in frontmatter is
invalid YAML, so Obsidian's Properties UI, Bases, and every script drop the whole
block without complaining. The note looks fine in the editor and is invisible to
the graph.

Usage:
    python3 check_frontmatter.py        # report and exit 1 on any error
"""

import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".obsidian", ".git", ".trash", "node_modules", ".claude"}
# Templates carry `{{date}}` placeholders that are deliberately not valid YAML.
SKIP_PREFIXES = ("90-System/Templates/", "90-System/Scripts/", "90-System/Graph/",
                 "90-System/Search Index/")
BARE_LINK = re.compile(r"^\s*[\w_]+\s*:\s*(?:\[\s*)?\[\[", re.M)
KEY = re.compile(r"^([A-Za-z_][\w_]*)\s*:", re.M)
SNAKE = re.compile(r"^[a-z][a-z0-9_]*$")


def iter_notes():
    for path in sorted(VAULT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.relative_to(VAULT).as_posix().startswith(SKIP_PREFIXES):
            continue
        yield path


def frontmatter(text):
    """Returns the raw frontmatter block, or None if the note has none."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return None if end == -1 else text[3:end]


def main():
    try:
        import yaml
    except ImportError:
        print("PyYAML not installed — run: pip install pyyaml", file=sys.stderr)
        return 2

    errors = []
    for path in iter_notes():
        rel = path.relative_to(VAULT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        if fm is None:
            continue

        try:
            data = yaml.safe_load(fm)
        except Exception as exc:  # noqa: BLE001 — any parse failure is a failure
            first = str(exc).splitlines()[0]
            errors.append(f"{rel}: invalid YAML — {first}")
            continue

        if data is not None and not isinstance(data, dict):
            errors.append(f"{rel}: frontmatter is not a mapping")
            continue

        # An unquoted wikilink parses as a nested list, not a string. It is the
        # single most common way to silently drop a note out of the graph.
        if BARE_LINK.search(fm):
            errors.append(f"{rel}: unquoted [[wikilink]] in frontmatter — "
                          'write works_at: "[[Acme]]"')

        for key in KEY.findall(fm):
            if not SNAKE.match(key):
                errors.append(f"{rel}: frontmatter key '{key}' is not snake_case")

    if errors:
        print(f"FAIL — {len(errors)} frontmatter problem(s):\n")
        for err in errors:
            print(f"  {err}")
        return 1

    print("PASS — frontmatter parses everywhere, links quoted, keys snake_case.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
