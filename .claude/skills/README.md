# Vendored skills

Checked in rather than linked so every machine and every agent session has them available
offline — the vault syncs by git, so a skill vendored here works on both the laptop and the
desktop with no per-machine install step.

## The kepano set — `obsidian-markdown/` · `obsidian-bases/` · `defuddle/` · `json-canvas/` · `obsidian-cli/`

All five vendored verbatim from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
— the official Obsidian skills by Steph Ango (@kepano), Obsidian's CEO. MIT licensed,
© 2026 Steph Ango; the full licence text is in `LICENSE-kepano-obsidian-skills`.

| Skill | What it gives Claude |
|---|---|
| `obsidian-markdown` | Exact syntax for callouts, embeds, block references, properties (+ three reference files) |
| `obsidian-bases` | `.base` files — filters, formulas, views, functions |
| `defuddle` | Clean markdown out of a web page, minus the navigation clutter — cheaper than WebFetch |
| `json-canvas` | Reading and writing `.canvas` files (see `90-System/Vault Architecture.canvas`) |
| `obsidian-cli` | Driving a vault from the command line; also plugin/theme debugging |

`defuddle` and `obsidian-cli` shell out to tools that must be installed separately — they
degrade to an error message rather than silently doing nothing, so an absent binary is
obvious on first use.

To update: re-download from
`https://raw.githubusercontent.com/kepano/obsidian-skills/main/skills/<name>/SKILL.md`.

## `watch/`

`/watch <url> [question]` — gives Claude a video input. Vendored verbatim from
[bradautomates/claude-video](https://github.com/bradautomates/claude-video) `skills/watch/`
at **v0.2.0**. MIT licensed, © 2026 Bradley Bonanno (`LICENSE` included).

Installed as a project skill rather than a plugin so it syncs with the vault. The plugin
repo's `hooks/` are deliberately **not** vendored — `SKILL.md` runs its own setup preflight
(`scripts/setup.py`), and the vault's own SessionStart/Stop hooks own `settings.json`.

**First run installs `ffmpeg` + `yt-dlp`** (auto via brew on macOS; prints exact commands on
Linux/Windows) and scaffolds `~/.config/watch/.env`. That config file lives outside the repo,
so a Whisper API key is never committed — captions are used first and most public videos need
no key at all. Output frames go to a temp dir, never into the vault.

To update: re-clone the repo and copy `skills/watch/` over this directory.
