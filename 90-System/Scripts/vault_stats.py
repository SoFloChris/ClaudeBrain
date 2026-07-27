#!/usr/bin/env python3
"""ClaudeBrain vault health — what exists, and what needs writing.

Pure standard library. Used by the SessionStart hook to brief agents, and by
`/vault-status` on demand.

Usage:
    python3 vault_stats.py            # full report
    python3 vault_stats.py --brief    # one-paragraph summary (for hooks)
"""

import re
import sys
from collections import Counter
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".obsidian", ".git", ".trash", "node_modules", ".claude"}
SKIP_PREFIXES = ("90-System/Templates/", "90-System/Scripts/", "90-System/Graph/",
                 "90-System/Search Index/")
STRUCTURAL = {"_Index", "Home", "SETUP", "README", "CLAUDE"}
# Inside markdown tables the alias pipe must be escaped (`[[note\|Alias]]`), so the
# trailing backslash has to be stripped off the captured target.
WIKILINK = re.compile(r"\[\[([^\]|#]+?)\\?(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
STUB_WORDS = 40


def iter_notes():
    for path in sorted(VAULT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.relative_to(VAULT).as_posix().startswith(SKIP_PREFIXES):
            continue
        yield path


def body_of(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def strip_code(text):
    """Links inside code blocks and spans are documentation examples, not real links."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


def real_targets(text):
    targets = set()
    for raw in WIKILINK.findall(strip_code(text)):
        target = raw.strip().rsplit("/", 1)[-1]
        # skip embedded Bases views and empty template placeholders
        if not target or target.endswith(".base"):
            continue
        targets.add(target)
    return targets


def link_targets():
    """Every note a [[wikilink]] may legitimately point at, by basename.

    Deliberately wider than iter_notes(): `90-System/Templates/` and `Scripts/`
    are excluded from the health report but are real files that notes link to —
    `50-Wiki/_Index.md` links to every template. Resolving against the narrower
    set would report those links as broken.
    """
    return {path.stem for path in VAULT.rglob("*.md")
            if not any(part in SKIP_DIRS for part in path.parts)}


def collect():
    """Notes are keyed by RELATIVE PATH, not filename stem.

    Keying by stem silently dropped six of this vault's seven `_Index.md` files
    — each overwrote the last in the dict, so their outbound links never counted
    toward `mentioned` and their dangling links never surfaced as broken. Any two
    notes sharing a filename collide the same way. The bug was invisible because
    a report that under-counts looks exactly like a vault with fewer links.
    """
    notes, links_out, mentioned = {}, {}, Counter()
    for path in iter_notes():
        rel = path.relative_to(VAULT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        targets = real_targets(text)
        targets.discard(path.stem)
        notes[rel] = {
            "name": path.stem,
            "path": rel,
            "folder": rel.split("/")[0] if "/" in rel else "(root)",
            "words": len(body_of(text).split()),
            "structural": path.stem in STRUCTURAL,
        }
        links_out[rel] = targets
        for t in targets:
            mentioned[t] += 1
    return notes, links_out, mentioned


def report(brief=False):
    notes, links_out, mentioned = collect()
    content = {rel: i for rel, i in notes.items() if not i["structural"]}
    resolvable = link_targets()

    orphans = sorted(
        i["name"] for rel, i in content.items()
        if not links_out.get(rel) and mentioned.get(i["name"], 0) == 0
    )
    stubs = sorted(
        (i["words"], i["name"]) for i in content.values() if i["words"] < STUB_WORDS
    )
    unresolved = sorted({t for tgts in links_out.values() for t in tgts
                         if t not in resolvable})
    inbox = [i["name"] for i in content.values() if i["folder"] == "00-Inbox"]
    by_folder = Counter(i["folder"] for i in content.values())

    if brief:
        bits = [f"{len(content)} notes"]
        if inbox:
            bits.append(f"{len(inbox)} unprocessed in Inbox")
        if orphans:
            bits.append(f"{len(orphans)} orphaned")
        if stubs:
            bits.append(f"{len(stubs)} stubs")
        if unresolved:
            bits.append(f"{len(unresolved)} broken links")
        print("Vault: " + ", ".join(bits) + ".")
        if orphans[:3]:
            print("Orphans (no links in or out): " + ", ".join(orphans[:3])
                  + (" …" if len(orphans) > 3 else ""))
        if unresolved[:3]:
            print("Links pointing at notes that don't exist yet: "
                  + ", ".join(unresolved[:3]) + (" …" if len(unresolved) > 3 else ""))
        return

    print(f"# Vault health — {len(content)} content notes\n")
    print("## By folder")
    for folder, count in sorted(by_folder.items()):
        print(f"  {folder:16} {count}")

    print(f"\n## Orphans — no links in or out ({len(orphans)})")
    print("  " + ("\n  ".join(orphans) if orphans else "none 🎉"))

    print(f"\n## Stubs — under {STUB_WORDS} words ({len(stubs)})")
    if stubs:
        for words, name in stubs:
            print(f"  {words:4}w  {name}")
    else:
        print("  none 🎉")

    print(f"\n## Broken links — pointed at, but no such note ({len(unresolved)})")
    if unresolved:
        for target in unresolved:
            # Paths, not stems — "50-Wiki/_Index" is actionable, "_Index" isn't.
            srcs = [rel[:-3] for rel, t in links_out.items() if target in t][:3]
            print(f"  {target}  ← from {', '.join(srcs)}")
    else:
        print("  none 🎉")

    if unresolved or orphans or stubs:
        print("\nEach line above is a note worth writing or connecting.")


if __name__ == "__main__":
    report(brief="--brief" in sys.argv)
