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


def collect():
    notes, links_out, mentioned = {}, {}, Counter()
    for path in iter_notes():
        rel = path.relative_to(VAULT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        targets = real_targets(text)
        targets.discard(path.stem)
        notes[path.stem] = {
            "path": rel,
            "folder": rel.split("/")[0] if "/" in rel else "(root)",
            "words": len(body_of(text).split()),
            "structural": path.stem in STRUCTURAL,
        }
        links_out[path.stem] = targets
        for t in targets:
            mentioned[t] += 1
    return notes, links_out, mentioned


def report(brief=False):
    notes, links_out, mentioned = collect()
    content = {n: i for n, i in notes.items() if not i["structural"]}

    orphans = sorted(
        n for n, i in content.items()
        if not links_out.get(n) and mentioned.get(n, 0) == 0
    )
    stubs = sorted(
        (i["words"], n) for n, i in content.items() if i["words"] < STUB_WORDS
    )
    unresolved = sorted({t for tgts in links_out.values() for t in tgts if t not in notes})
    inbox = [n for n, i in content.items() if i["folder"] == "00-Inbox"]
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
            srcs = [n for n, t in links_out.items() if target in t][:3]
            print(f"  {target}  ← from {', '.join(srcs)}")
    else:
        print("  none 🎉")

    if unresolved or orphans or stubs:
        print("\nEach line above is a note worth writing or connecting.")


if __name__ == "__main__":
    report(brief="--brief" in sys.argv)
