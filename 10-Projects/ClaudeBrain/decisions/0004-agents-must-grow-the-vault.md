---
type: adr
summary: "ADR-0004 (accepted): agents must write to the vault unprompted, not only read from it - with note-spam as the named counter-risk."
status: accepted
date: 2026-07-24
decision_makers: ["[[Chris Aguirre]]"]
project: "[[Set Up ClaudeBrain]]"
related: ["[[Context vs Connections]]", "[[Documentation Rot]]"]
tags:
  - adr
---

# ADR-0004 — Agents must write to the vault, not only read from it

## Context and Problem Statement

After several working sessions the vault had absorbed almost nothing: research was done, decisions were made, and entities were discussed, but the notes were never written. The router's rules all fired *reactively* — they described where to file input once handed over, and said nothing about producing notes unprompted. An agent optimising against those rules correctly concludes that reading and answering is the whole job.

## Decision Drivers

- A second brain that only gets written when its owner remembers to write is just a folder.
- The moment a question can't be answered from the vault is precisely the evidence that a note is missing ([[Reverse Engineer for Recall]]).
- Bulk-generating notes is *cheap* for an agent, so the guardrail against noise matters more here than in a hand-written vault.

## Considered Options

- Rely on explicit commands only (`/remember`, `/process-inbox`)
- Add proactive write-back rules to the router
- Add rules plus lifecycle hooks that make omission visible

## Decision Outcome

Chosen option: **rules plus hooks**. The router gains a top-priority principle ("a session that only reads has failed") and concrete triggers — entity mentioned, question the vault couldn't answer, decision made — while a `Stop` hook surfaces sessions that ended without writing anything. Rules set the intent; the hook catches the drift, because an instruction the model must remember is weaker than a mechanism that checks.

### Consequences

- Good, because knowledge compounds automatically instead of depending on the owner noticing.
- Good, because `/wrap` gives an explicit harvest for the end of a substantive conversation.
- Bad, because proactive writing risks note-spam — mitigated by [[Context vs Connections]] as an explicit quality bar and by an anti-gaming rule in `/wrap` ("don't invent notes to look productive").
- Bad, because a Stop hook that fires too eagerly becomes noise the user learns to dismiss. Mitigated by rate-limiting it and skipping it whenever notes actually changed.

### Confirmation

`vault_stats.py` reports orphans, stubs, and broken links — the observable signature of a vault being written badly. A session that adds notes without connecting them shows up there.

## Pros and Cons of the Options

### Explicit commands only

- Good, because zero risk of unwanted writes.
- Bad, because it puts the burden on the human to remember — the exact failure this ADR exists to fix.

### Rules without hooks

- Good, because simple, no shell scripts to maintain.
- Bad, because rules degrade over a long session as context fills; nothing detects the drift.

## More Information

Falsified if the hooks prove more annoying than useful — in which case keep the rules, drop the hook. Tracked as an open question in [[Set Up ClaudeBrain]].

## Amendments

<!-- Append only. -->
- **2026-07-24** — **The Stop hook false-positived on its first real run**, on a session that had written 60+ notes. It tested only `git status --porcelain` for uncommitted changes, so a session that wrote notes *and committed them* left a clean tree and looked idle. Fixed by also checking `git log --since='6 hours ago'` for committed note changes. The decision stands, but this is the exact failure mode the "Bad, because" bullet predicted — a nudge that fires wrongly is a nudge you learn to dismiss. Worth re-checking after a week of real use: if it misfires again, keep the rules and drop the hook.
