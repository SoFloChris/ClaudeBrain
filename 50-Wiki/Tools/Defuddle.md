---
type: tool
summary: "Strips a web page down to the actual article and returns clean markdown - the capture pipeline's front door, and cheaper than WebFetch."
built_by: "[[Dynalist Inc]]"
alternative_to: []
related: ["[[Context vs Connections]]"]
tags:
  - tool
created: 2026-07-24
---

# Defuddle

Extracts the actual article out of a web page — stripping navigation, sidebars, cookie banners, and related-post clutter — and returns clean markdown. It's the engine behind Obsidian Web Clipper, documented by the `defuddle` skill vendored in `.claude/skills/`.

## Why it matters to me

**This is the capture pipeline's front door.** When something on the web is worth keeping, the failure mode is pasting the whole page — nav junk included — into `00-Inbox/` and calling it captured. That's exactly the hoarding [[Context vs Connections]] warns against, and it poisons [[Semantic Search]] with boilerplate.

Defuddle gets clean text in, so the only remaining work is the part that actually matters: distilling it and linking it.

Practical rule from the skill: **prefer it over WebFetch for ordinary web pages** (fewer tokens, better text), but not for URLs already ending in `.md` — those are already markdown.

## Related

- [[Semantic Search]] — clean input is what keeps the index signal-dense
