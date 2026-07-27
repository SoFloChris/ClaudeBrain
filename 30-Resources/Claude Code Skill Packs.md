---
type: resource
topic: "[[Claude Code]]"
related: ["[[claude-video]]", "[[ColdIQ]]", "[[Skills Are Verbs, Notes Are Nouns]]"]
---

# Claude Code Skill Packs

Public skill packs worth knowing, with install commands. Researched 2026-07 — star counts and versions rot fast; the repos are the source of truth.

## The packs

| Pack | What it gives Claude | Size | License |
|---|---|---|---|
| `bradautomates/claude-video` | `/watch` — download, frame-extract, and transcribe any video → [[claude-video]] | 10.8k ★ | MIT |
| `Cold-IQ/ColdIQ-s-GTM-Skills` | Outbound/GTM: 6 orchestrators + 43 sub-skills, 137 triggers, 34 templates → [[ColdIQ]] | 221 ★ | unstated |
| `growthenginenowoslawski/coldoutboundskills` | Cold outbound, vendor-free: campaign grading, Prospeo exports, Maps scraping | 28 skills | open source |
| `codejunkie99/graph-engineering` | 9-stage knowledge-graph pipeline + task-graph orchestration patterns → [[Graph Engineering]] | 144 ★ | MIT |
| `Newuxtreme/watch-video-skill` | Alternative video-watching skill (visual feedback framing) | — | — |
| `mathiaschu/watch` | Fork of claude-video using local `mlx-whisper` — fully offline transcription | — | — |

## Install patterns

```bash
# Claude Code plugin marketplace (preferred where supported)
/plugin marketplace add <owner>/<repo>
/plugin install <skill>@<repo>

# Cross-tool (Codex, Cursor, Copilot) — installs globally
npx skills add <owner>/<repo> -g

# Manual — clone and drop into the skills directory
git clone https://github.com/<owner>/<repo>.git
cp -r <repo>/<skill-dir> ~/.claude/skills/
```

Project-scoped skills live in `.claude/skills/` (this vault vendors `obsidian-markdown` and `obsidian-bases` that way); user-scoped in `~/.claude/skills/`.

## What to actually install here

Only [[claude-video]] cleared the bar — it feeds the capture pipeline this vault already runs by hand. **Installed 2026-07-27** at `.claude/skills/watch/`, vendored verbatim so it syncs to both machines rather than being a per-machine plugin install; see `.claude/skills/README.md`.

The rest are architecture references, not dependencies: read the tree, steal the naming, skip the install. Forty skills nobody maintains is worse than six that get used ([[Skills Are Verbs, Notes Are Nouns]]).

## Related

- [[Claude Code Memory and Commands]] — the sibling reference: memory, imports, slash commands, hooks
- [[Skills Are Verbs, Notes Are Nouns]] — how to judge whether a pack is worth adopting
