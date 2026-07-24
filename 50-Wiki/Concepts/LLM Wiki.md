---
type: concept
related: ["[[Second Brain]]"]
---

# LLM Wiki

A wiki written *for* an AI assistant to read and maintain: raw material (video transcripts, meeting recordings, research) gets processed into interconnected concept pages with an index, so the model can navigate to exactly the pages it needs instead of loading everything. Popularized by Andrej Karpathy; the basis of [[Nate Herk]]'s Level 2.

## Why it matters to me

`50-Wiki/` is this vault's LLM wiki: one page per entity, `_Index.md` maps of content for navigation, `[[wikilinks]]` for connections, and templates so every page has a predictable shape. The `/process-inbox` command is the ingestion pipeline — raw captures in, distilled wiki pages out.

## Related

- [[Every Level of a Claude Second Brain]] — Level 2 section
- [[Knowledge Graph]] — what the wiki becomes when links get types
