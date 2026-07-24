---
description: Save a durable fact to the vault's memory file
argument-hint: [the fact to remember]
---

Append this fact to `90-System/Memory.md`: $ARGUMENTS

Rules:
- File it under the most fitting existing heading (About Chris / Preferences / Projects / People & Relationships); create a new `##` heading only if none fits.
- Format: `- (YYYY-MM-DD) fact`, using today's date.
- If it contradicts an existing entry, update the old entry instead of duplicating — note the change.
- Never store secrets, credentials, or API keys. If the fact contains one, refuse and say why.
- If the fact mentions a person, company, or concept, link it with `[[wikilinks]]` and create the wiki note in `50-Wiki/` (from the matching template) if it doesn't exist.
