#!/usr/bin/env python3
"""Regression tests for brain_graph's hand-rolled frontmatter parser.

Stdlib only, matching brain_graph's zero-dependency rule. Run directly:

    python3 90-System/Scripts/test_brain_graph.py

These exist because of a real bug, found 2026-07-27: the inline-list regex
excluded `[` and `]`, so `uses: ["[[A]]", "[[B]]", "[[C]]"]` produced an edge
for the FIRST item only and silently shredded the rest into bare text that
matched no wikilink. Every multi-value typed predicate in the vault was
affected — the graph reported 249 edges when it had 270.

It survived because the failure is invisible: no exception, no broken link, no
orphan, and a `stats` table that looks entirely plausible. A graph that
under-reports is indistinguishable from a graph with fewer relationships. So
the parser gets tests even though nothing else in this vault does.
"""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "brain_graph.py"
_spec = importlib.util.spec_from_file_location("brain_graph", SCRIPT)
brain_graph = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(brain_graph)

parse = brain_graph.parse_frontmatter


class TestInlineLists(unittest.TestCase):
    def test_quoted_wikilink_list_keeps_every_item(self):
        """The 2026-07-27 bug: only the first item survived."""
        got = parse(['uses: ["[[Obsidian]]", "[[Claude Code]]", "[[brain_search]]"]'])
        self.assertEqual(got["uses"],
                         ["[[Obsidian]]", "[[Claude Code]]", "[[brain_search]]"])

    def test_single_item_list(self):
        got = parse(['related: ["[[Second Brain]]"]'])
        self.assertEqual(got["related"], ["[[Second Brain]]"])

    def test_comma_inside_a_wikilink_is_not_a_separator(self):
        """Quoted items must match whole, or a note titled `A, B` splits in two."""
        got = parse(['related: ["[[A, B]]", "[[C]]"]'])
        self.assertEqual(got["related"], ["[[A, B]]", "[[C]]"])

    def test_bare_unquoted_list(self):
        got = parse(["aliases: [Chris, me]"])
        self.assertEqual(got["aliases"], ["Chris", "me"])

    def test_empty_list(self):
        self.assertEqual(parse(["related: []"])["related"], [])


class TestScalarsAndBlocks(unittest.TestCase):
    def test_quoted_scalar_wikilink(self):
        self.assertEqual(parse(['topic: "[[Embeddings]]"'])["topic"], "[[Embeddings]]")

    def test_plain_scalar(self):
        self.assertEqual(parse(["type: concept"])["type"], "concept")

    def test_block_list(self):
        got = parse(["tags:", "  - concept", "  - vault"])
        self.assertEqual(got["tags"], ["concept", "vault"])


class TestEdgesFromLists(unittest.TestCase):
    """The parser feeding the graph is the point; assert the edges themselves."""

    def test_every_list_item_becomes_an_edge(self):
        fm = parse(['uses: ["[[A]]", "[[B]]", "[[C]]"]'])
        targets = [t for v in fm["uses"] for t in brain_graph.WIKILINK.findall(str(v))]
        self.assertEqual(targets, ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
