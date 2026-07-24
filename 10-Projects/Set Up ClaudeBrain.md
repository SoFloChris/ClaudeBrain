---
type: project
status: active
related: ["[[Second Brain]]"]
---

# Set Up ClaudeBrain

**Outcome:** Vault cloned, syncing, and usable with Claude on both machines.

## Tasks

- [ ] Follow `SETUP.md` on the desktop
- [ ] Follow `SETUP.md` on the laptop
- [ ] Confirm a note edited on one machine appears on the other
- [ ] Fill in the "Who I am" section of `CLAUDE.md`
- [ ] `pip install sentence-transformers` on each machine (enables `/recall`)
- [ ] Capture 3 real notes into the Inbox and run `/process-inbox`
- [ ] Try `/graph "Nate Herk"` and `/recall what are the 5 levels?`

## Decisions

- (2026-07-24) Agents must grow the vault, not just read it: entity notes, answer capture, and decision capture happen proactively in every session; `/wrap` harvests a conversation explicitly. Added as a top-level router rule.

## Notes

This vault follows the "5 Levels of a Claude Second Brain" approach (see [[90-System/Second Brain Levels]]). It starts at Level 1–2 on purpose.
