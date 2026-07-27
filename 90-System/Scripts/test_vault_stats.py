#!/usr/bin/env python3
"""Regression tests for vault_stats' note keying.

Stdlib only. Run directly:

    python3 90-System/Scripts/test_vault_stats.py

These exist because of a real bug, found 2026-07-27: `collect()` keyed notes by
filename *stem*, so all seven of this vault's `_Index.md` files collapsed into a
single dict entry. Six were silently discarded — their outbound links never
counted toward `mentioned` (inflating orphan counts) and their dangling links
never surfaced as broken (hiding real breakage). Any two notes sharing a
filename collide the same way.

Second bug in the same function: links were resolved against the *report's* note
set, which excludes `90-System/Templates/`. Since `50-Wiki/_Index.md` links to
every template, those links were only ever "clean" because the stem collision
had already thrown them away. Fixing one without the other turns them into false
positives, so both are pinned here.

The assertions are structural rather than content-based, so they stay valid as
the vault grows.
"""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "vault_stats.py"
_spec = importlib.util.spec_from_file_location("vault_stats", SCRIPT)
vault_stats = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vault_stats)


class TestNoteKeying(unittest.TestCase):
    def test_every_scanned_file_survives_collection(self):
        """The 2026-07-27 bug: same-stem files overwrote each other."""
        scanned = list(vault_stats.iter_notes())
        notes, _, _ = vault_stats.collect()
        self.assertEqual(len(notes), len(scanned),
                         "collect() lost notes — keys are colliding again")

    def test_every_index_file_is_its_own_entry(self):
        """_Index.md is the collision this vault actually has: one per folder."""
        indexes = [p for p in vault_stats.iter_notes() if p.stem == "_Index"]
        notes, _, _ = vault_stats.collect()
        keyed = [rel for rel in notes if rel.endswith("_Index.md")]
        self.assertEqual(len(keyed), len(indexes))
        self.assertGreater(len(indexes), 1, "fixture assumption: several indexes")

    def test_keys_are_paths_not_stems(self):
        notes, links_out, _ = vault_stats.collect()
        self.assertTrue(all(k.endswith(".md") for k in notes),
                        "note keys should be relative paths")
        self.assertEqual(set(notes), set(links_out),
                         "links_out must be keyed the same way as notes")

    def test_outbound_links_counted_from_every_index(self):
        """Links from a non-last index must reach `mentioned`."""
        _, links_out, mentioned = vault_stats.collect()
        for rel, targets in links_out.items():
            if rel.endswith("_Index.md"):
                for target in targets:
                    self.assertGreaterEqual(
                        mentioned.get(target, 0), 1,
                        f"{rel} links to [[{target}]] but it went uncounted")


class TestLinkResolution(unittest.TestCase):
    def test_templates_are_valid_link_targets(self):
        """Excluded from the report, but notes legitimately link to them."""
        resolvable = vault_stats.link_targets()
        templates = [p.stem for p in
                     (vault_stats.VAULT / "90-System" / "Templates").glob("*.md")]
        self.assertTrue(templates, "fixture assumption: templates exist")
        for stem in templates:
            self.assertIn(stem, resolvable)

    def test_resolution_set_is_a_superset_of_scanned_notes(self):
        resolvable = vault_stats.link_targets()
        for path in vault_stats.iter_notes():
            self.assertIn(path.stem, resolvable)

    def test_agrees_with_check_links(self):
        """The two tools must not contradict each other on broken links."""
        spec = importlib.util.spec_from_file_location(
            "check_links", SCRIPT.parent / "check_links.py")
        check_links = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(check_links)

        _, links_out, _ = vault_stats.collect()
        resolvable = vault_stats.link_targets()
        stats_broken = {t for tgts in links_out.values() for t in tgts
                        if t not in resolvable}
        self.assertEqual(check_links.main() == 0, not stats_broken,
                         "vault_stats and check_links disagree on broken links")


if __name__ == "__main__":
    unittest.main(verbosity=2)
