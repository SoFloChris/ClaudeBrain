#!/usr/bin/env python3
"""Regression tests for check_frontmatter's validation rules.

Stdlib only. Run directly:

    python3 90-System/Scripts/test_check_frontmatter.py

`check_frontmatter.py` was restored from the unmerged
`claude/obsidian-second-brain-setup-0c0jdy` branch (2026-07-24). It arrived
without tests, and it is an *enforcing* script — one that can block a merge —
so it gets them before being wired into CI. An over-eager validator that flags
correct frontmatter is worse than no validator at all, because the fix people
reach for is deleting the check.

The rule it enforces is subtle enough to be worth pinning precisely: an
unquoted `[[wikilink]]` in YAML parses as a nested list rather than a string,
so Obsidian's Properties UI, Bases, and every script silently drop the whole
frontmatter block. The note looks fine in the editor and is invisible to the
graph — the same species of silent failure as the two bugs found 2026-07-27.
"""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_frontmatter.py"
_spec = importlib.util.spec_from_file_location("check_frontmatter", SCRIPT)
check_frontmatter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_frontmatter)

BARE_LINK = check_frontmatter.BARE_LINK
SNAKE = check_frontmatter.SNAKE


class TestBareLinkDetection(unittest.TestCase):
    """Must flag unquoted links, and must NOT flag correctly quoted ones."""

    def test_flags_bare_scalar_link(self):
        self.assertTrue(BARE_LINK.search("works_at: [[Acme]]"))

    def test_flags_bare_list_link(self):
        self.assertTrue(BARE_LINK.search("related: [[[A]], [[B]]]"))

    def test_allows_quoted_scalar(self):
        self.assertFalse(BARE_LINK.search('works_at: "[[Acme]]"'))

    def test_allows_quoted_list(self):
        """The form the Graph Schema actually prescribes — must stay legal."""
        self.assertFalse(BARE_LINK.search('related: ["[[A]]", "[[B]]"]'))

    def test_ignores_frontmatter_without_links(self):
        self.assertFalse(BARE_LINK.search("type: concept\nstatus: active"))

    def test_finds_a_bare_link_on_a_later_line(self):
        """Multiline mode: the offending key is rarely the first one."""
        self.assertTrue(BARE_LINK.search('type: person\nworks_at: [[Acme]]\n'))


class TestSnakeCaseKeys(unittest.TestCase):
    def test_accepts_snake_case(self):
        for key in ("works_at", "type", "alternative_to", "superseded_by"):
            self.assertTrue(SNAKE.match(key), key)

    def test_rejects_other_cases(self):
        for key in ("worksAt", "works-at", "Works_At", "WorksAt"):
            self.assertFalse(SNAKE.match(key), key)


class TestSummaryExemptions(unittest.TestCase):
    """ADR-0007 requires a summary on content notes — and only those."""

    def test_structural_files_are_exempt(self):
        for stem in ("_Index", "Home", "SETUP", "README", "CLAUDE"):
            self.assertIn(stem, check_frontmatter.NO_SUMMARY_NEEDED, stem)

    def test_memory_is_exempt(self):
        """It's @-imported into CLAUDE.md, so it's always already in context."""
        self.assertIn("Memory", check_frontmatter.NO_SUMMARY_NEEDED)

    def test_daily_notes_are_exempt(self):
        """Transient scratch logs have no single claim to state."""
        for stem in ("2026-07-27", "2025-01-01"):
            self.assertTrue(check_frontmatter.DAILY_NOTE.match(stem), stem)

    def test_ordinary_notes_are_not_exempt(self):
        for stem in ("Knowledge Graph", "Nate Herk", "2026-07", "notes-2026-07-27"):
            exempt = (stem in check_frontmatter.NO_SUMMARY_NEEDED
                      or bool(check_frontmatter.DAILY_NOTE.match(stem)))
            self.assertFalse(exempt, stem)


class TestAgainstTheRealVault(unittest.TestCase):
    def test_vault_passes(self):
        """Guards against a rule so strict the vault can't satisfy it."""
        self.assertEqual(check_frontmatter.main(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
