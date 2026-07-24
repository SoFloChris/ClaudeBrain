---
type: tool
summary: "Anthropic's agentic coding tool and the engine of this vault - it auto-loads CLAUDE.md, which is what makes Level 1 work at all."
built_by: "[[Anthropic]]"
related: ["[[Second Brain]]", "[[LLM Wiki]]"]
---

# Claude Code

Anthropic's agentic coding tool — and the engine of this vault. It reads `CLAUDE.md` automatically on every session, which is what makes Level 1 (the router) work at all.

## Key facts

- **`CLAUDE.md`** in the project root loads as the system prompt. Available in the terminal CLI, desktop app, web (claude.ai/code), and IDE extensions.
- **`@path/to/file.md` imports** pull other files into that context — how `90-System/Memory.md` auto-loads every session.
- **`/memory`** opens memory files for editing; memory lives at user level (`~/.claude/CLAUDE.md`) and project level.
- **Custom slash commands** are markdown files in `.claude/commands/`. Frontmatter takes `description`, `argument-hint`, `allowed-tools`, `model`; the body is the prompt, with `$ARGUMENTS` for input. Ours: `/recall`, `/graph`, `/remember`, `/process-inbox`, `/wrap`.
- **Hooks** in `.claude/settings.json` run shell commands on lifecycle events (SessionStart, Stop, UserPromptSubmit) — the mechanism that enforces vault-growth habits rather than relying on the model to remember.
- Skills, subagents, and MCP servers extend it further; the `memory` MCP server is an official knowledge-graph store if this vault ever outgrows [[brain_graph]].

## Related

- [[Obsidian]] — where the notes live; Claude Code is what edits them
- [[GBrain]] — a Level 5 system built on the same "agents share a markdown brain" idea
