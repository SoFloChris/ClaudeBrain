---
type: adr
summary: "ADR-0005 (accepted): third-party skills are vendored into the repo rather than plugin-installed, so they ride the git sync to both machines with no per-device setup."
status: accepted
date: 2026-07-27
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[Claude Code]]", "[[claude-video]]"]
tags:
  - adr
---

# ADR-0005 — Vendor third-party skills into the repo instead of installing them as plugins

## Context and Problem Statement

Installing [[claude-video]]'s `/watch` skill forced the question for the first time: a third-party [[Claude Code]] skill can be installed as a **plugin** (via the marketplace, landing in `~/.claude/`) or **vendored** into the project at `.claude/skills/`. The two look equivalent from inside a single session and are not equivalent across machines.

This vault syncs laptop ↔ desktop by git. Anything that lives outside the repo — a plugin install, a config file, a globally installed binary — is invisible to that sync and has to be repeated per device. The failure is silent: a command works where you set it up and is simply absent everywhere else, which is the worst shape of bug for a tool you reach for occasionally.

## Decision Drivers

- The vault's whole sync model is "if it matters, it's in the repo."
- Two machines, and per-device setup steps get skipped or forgotten.
- Skills are **executable code**, not notes — what runs should be reviewable and pinned, not fetched on demand.
- Skill packs rot faster than notes do: every one has a dependency on a vendor API or export format that can change without warning.
- Precedent already existed — `obsidian-markdown` and `obsidian-bases` were vendored from `kepano/obsidian-skills` for exactly this reason.

## Considered Options

- Install as a plugin on each machine
- Vendor the skill directory into `.claude/skills/`
- Add the upstream repo as a git submodule

## Decision Outcome

Chosen option: **vendor verbatim into `.claude/skills/`**, recording source, version, and license in `.claude/skills/README.md`.

The deciding argument is that the repo is the only thing guaranteed to be identical on both machines. A vendored skill is available the moment `git pull` finishes, with no install step to forget — and because it arrives as a diff, the code that will execute is reviewable *before* it lands rather than after it misbehaves.

### Consequences

- Good, because a skill works on both machines after one pull, with zero per-device setup beyond binaries the skill installs itself.
- Good, because the exact version is pinned and visible in git history; there is no "which version is the desktop on?"
- Good, because vendoring forces a read of the code first. `/watch` got an audit — outbound hosts, credential handling, where it writes — which a marketplace install would have skipped.
- Bad, because **updates are manual**. There is no `/plugin update`; a vendored skill stays at its pinned version until someone re-copies it, and upstream fixes are invisible. Mitigated by recording the version in `.claude/skills/README.md` so staleness is at least legible.
- Bad, because third-party code now lives in a notes repo — `/watch` alone is ~2,600 lines of Python. The vault is no longer purely prose.
- Bad, because the security burden shifts entirely onto review-before-vendor. Nothing re-checks a skill after it's checked in.

### Confirmation

`.claude/skills/README.md` names the source, version, and license of every vendored skill. The decision is working if a freshly cloned vault has every skill available with no extra install; it has failed if a skill works on one machine and not the other.

## Pros and Cons of the Options

### Plugin install per machine

- Good, because updates are one command and upstream fixes arrive without effort.
- Good, because the notes repo stays prose-only.
- Bad, because it must be repeated on every machine, and its absence is silent.
- Bad, because the installed version is invisible to the repo — two machines can silently diverge.

### Git submodule

- Good, because it pins a version *and* makes updating a tracked operation.
- Bad, because submodules are a well-known footgun in a repo synced by a background auto-commit plugin like [[Obsidian Git]] — a detached submodule pointer is far harder to recover from than a stale file copy.
- Bad, because it pulls the upstream repo's entire tree (tests, CI, packaging) to get one skill directory.

## More Information

Falsified if the manual update burden grows past the per-device setup it avoids — realistically, once more than a handful of skills are vendored and upstream is moving fast. At that point the answer is probably a small script that re-copies each skill from its pinned upstream ref, not a return to per-machine installs.

## Amendments

<!-- Append only. -->
