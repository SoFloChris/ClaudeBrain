#!/usr/bin/env python3
"""Fail if any [[wikilink]] in the vault points at a note that doesn't exist."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".obsidian", "graphify-out"}
WIKILINK = re.compile(r"\[\[([^\]|#]+)")
FENCED_CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(text):
    """Drop fenced/inline code so literal `[[example]]` snippets in docs aren't
    flagged as broken links."""
    text = FENCED_CODE_BLOCK.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return INLINE_CODE.sub("", text)


def vault_markdown_files():
    for path in ROOT.rglob("*.md"):
        if not any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            yield path


def main():
    md_files = list(vault_markdown_files())
    by_basename = {}
    by_relpath = {}
    for path in md_files:
        rel = path.relative_to(ROOT).with_suffix("")
        by_basename.setdefault(path.stem.lower(), path)
        by_relpath[str(rel).lower()] = path

    broken = []
    for path in md_files:
        text = strip_code(path.read_text(encoding="utf-8", errors="replace"))
        for lineno, line in enumerate(text.splitlines(), start=1):
            for match in WIKILINK.finditer(line):
                target = match.group(1).strip().lower()
                if target and target not in by_basename and target not in by_relpath:
                    broken.append((path.relative_to(ROOT), lineno, match.group(1).strip()))

    if broken:
        print(f"Found {len(broken)} broken wikilink(s):", file=sys.stderr)
        for path, lineno, target in broken:
            print(f"  {path}:{lineno}: [[{target}]]", file=sys.stderr)
        return 1

    print(f"OK — {len(md_files)} notes, no broken wikilinks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
