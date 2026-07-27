# ⚙️ System

The machinery of the vault. Rarely touched during day-to-day capture.

## Docs

- [[Agent Guide]] — the craft, where `CLAUDE.md` is the rules: what to reach for, in what order, and the failure modes
- [[Memory]] — durable facts Claude has learned (auto-loaded into every session, human-editable)
- [[Second Brain Levels]] — the 5-level roadmap; Levels 1–4 built, Level 5 deliberately skipped
- [[Graph Schema]] — the controlled vocabulary for typed relationships

## Templates (`Templates/`)

Entity: `Person` · `Company` · `Tool` · `Concept`
Work: `Project` (light) · `Project Master` (builds) · `ADR` · `Runbook` · `Changelog`
Other: `Daily Note` · `Meeting Note` · `Resource` · `MOC`

## Scripts (`Scripts/`)

| Script | Purpose |
|---|---|
| [[brain_search]] | Level 3 semantic search — `index`, `search`, `chunks` |
| [[brain_graph]] | Level 4 knowledge graph — `build`, `query`, `path`, `stats` |
| `vault_stats.py` | Vault health — orphans, stubs, broken links (`--brief` for hooks). **Reports; always exits 0.** |
| `check_links.py` | Broken wikilinks with `file:line`, **exits non-zero** — the enforcing version, run by CI |
| `check_frontmatter.py` | Frontmatter parses as YAML, links are quoted, keys are snake_case (needs PyYAML) |
| `test_brain_graph.py` | Regression tests for [[brain_graph]]'s frontmatter parser (stdlib `unittest`) |
| `test_vault_stats.py` | Regression tests for `vault_stats.py`'s note keying and link resolution |
| `guard-secrets.sh` | Fails if anything secret-shaped is tracked; scans `git ls-files`, not the working tree |

## Canvas

`Vault Architecture.canvas` — the vault's own structure as a JSON Canvas: folders, scripts, and the four levels, with 11 live links into the notes they describe. Open it in Obsidian; edit it with the vendored `json-canvas` skill.

## Bases (`Bases/`)

Live dashboards, queried by Obsidian's core Bases plugin. Embed with `![[Name.base#View]]`.

- `Projects.base` — active work, with a staleness marker
- `Orphans.base` — notes with no links in or out
- `Entity.base` — "mentioned in" panel; embedded on every entity note via `this`

## Slash commands (`.claude/commands/`)

`/remember` · `/process-inbox` · `/recall` · `/graph` · `/wrap` · `/vault-status`

## Hooks (`.claude/hooks/`)

- `vault-brief.sh` — **SessionStart**: injects vault stats and the growth mandate into context
- `capture-nudge.sh` — **Stop**: if a session ends with nothing written, says so once (rate-limited to 90 min, silent whenever notes changed)

## Vendored skills (`.claude/skills/`)

`obsidian-markdown` and `obsidian-bases` from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) (MIT, by Obsidian's CEO) — authoritative syntax, available offline. `watch` from [bradautomates/claude-video](https://github.com/bradautomates/claude-video) (MIT) — see [[claude-video]] and ADR-0005 for why these are vendored rather than plugin-installed.

## CI (`.github/workflows/vault-check.yml`)

Runs on every PR and push to `main`: frontmatter validity → broken wikilinks → regression tests → graph builds → secret guard → derived-data guard → shellcheck.

Assembled from two abandoned branches, each of which had better engineering hygiene than the vault it belonged to: the workflow skeleton and secret guard from `claude/graphify-obsidian-integration-m15xef`, the frontmatter and derived-data checks from `claude/obsidian-second-brain-setup-0c0jdy`.

The reason it exists: `brain_graph`'s parser silently dropped every multi-value typed edge for weeks, and nothing could see it — a graph that under-reports looks exactly like a graph with fewer relationships. Health *reports* can't catch that; a failing build can. Reasoning in [[0006-enforce-invariants-in-ci|ADR-0006]].

Every step runs locally, so a push never has to be the first test:

```bash
python3 "90-System/Scripts/check_frontmatter.py"       # pip install pyyaml
python3 "90-System/Scripts/check_links.py"
python3 -m unittest discover -s "90-System/Scripts" -p "test_*.py"
python3 "90-System/Scripts/brain_graph.py" build
./90-System/Scripts/guard-secrets.sh
git ls-files '90-System/Graph/*' '90-System/Search Index/*'   # must print nothing
shellcheck 90-System/Scripts/*.sh .claude/hooks/*.sh   # pip install shellcheck-py
```
