# Vendored skills

All five skills from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) — the official
Obsidian skills by [[Steph Ango]] (@kepano), Obsidian's CEO. MIT licensed, © 2026 Steph Ango;
full licence in `LICENSE-kepano-obsidian-skills`. Vendored at upstream `a1dc48e` (2026-06-08).

They're checked in rather than linked so every machine and every agent session has authoritative
Obsidian knowledge offline.

| Skill | What it gives an agent |
|---|---|
| `obsidian-markdown` | Exact syntax for wikilinks, embeds, callouts, block references, properties. References: `CALLOUTS.md`, `EMBEDS.md`, `PROPERTIES.md`. |
| `obsidian-bases` | `.base` file authoring — filters, formulas, views, plus the full `FUNCTIONS_REFERENCE.md`. |
| `obsidian-cli` | Drive a vault from the command line: read, create, search notes, manage properties and tasks. |
| `json-canvas` | Author `.canvas` files programmatically — visual maps, flowcharts, architecture diagrams. Includes `EXAMPLES.md`. |
| `defuddle` | Extract clean markdown from a web page, stripping nav and clutter. **Prefer this over WebFetch** when capturing an article into the vault — fewer tokens, better text. |

## Updating

```bash
git clone --depth 1 https://github.com/kepano/obsidian-skills.git /tmp/obsidian-skills
cp -r /tmp/obsidian-skills/skills/* .claude/skills/
```

Keep this table and the vendored commit hash in sync when you do.
