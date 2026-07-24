# Second Brain Levels

The 5-level maturity model this vault follows (from "Every Level of a Claude Second Brain Explained" by Nate Herk). The goal is **not** to reach Level 5 — it's the simplest architecture that solves the actual need. Only move up a level when you hit a specific pain point the current level cannot solve.

## Level 1 — The Router ✅ (we are here)

A `CLAUDE.md` file acts as system prompt and router: who you are, how you work, where files live. Claude knows exactly where to look for project data.

## Level 2 — The Wiki ✅ (we are here)

Structured wiki notes for entities (`50-Wiki/`), folder indexes as maps of content, and an automatic memory file (`Memory.md`) so knowledge compounds across sessions.

## Level 3 — Semantic Search

Search by meaning instead of exact keywords, via embeddings / a vector database.
**Level up when:** you regularly fail to find notes because you can't remember the words you used, and grep/wikilinks aren't cutting it.

## Level 4 — Knowledge Graphs

Explicit entity relationships ("Person X works at Company Y") that can be traversed as chains.
**Level up when:** you're asking multi-hop relationship questions the wiki's links can't answer.

## Level 5 — The Autonomous Brain

Always-on syncing, autonomous memory updates, multiple agents maintaining the vault.
**Level up when:** manual capture/processing is genuinely the bottleneck — not before.

## Key principles

- **Reverse engineer for recall:** design the file architecture around how you'll ask questions later.
- **Start with the lowest level:** don't chase complexity without a pain point.
- **Context vs. connections:** store evergreen business/life context; don't fill the brain with noisy transient data (Slack threads, raw emails).
- **Boring is beautiful:** a clean, well-organized folder of markdown files remains the foundation at every level.
