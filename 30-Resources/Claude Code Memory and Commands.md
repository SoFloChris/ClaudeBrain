---
type: resource
topic: "[[Claude Code]]"
related: ["[[Second Brain]]", "[[LLM Wiki]]"]
---

# Claude Code Memory and Commands

Reference for the [[Claude Code]] features this vault is built on. Verified against official docs (2026-07).

## Memory hierarchy

Loaded automatically, in precedence order:

| Scope | Location |
|---|---|
| Enterprise | managed policy path (org-wide) |
| Project | `./CLAUDE.md` — checked into the repo, shared |
| User | `~/.claude/CLAUDE.md` — personal, all projects |

`CLAUDE.local.md` is deprecated; use imports instead.

## Imports

```markdown
@90-System/Memory.md
```

- Relative and absolute paths both work; `~/` works for home-relative.
- Recursive up to **5 levels** deep.
- **Not evaluated inside code spans or code blocks** — so documenting the syntax doesn't trigger it.
- This is how `Memory.md` reaches every session without being pasted.

## The `/memory` command

Opens memory files in your editor for direct editing. Note: there is **no `#` quick-add shortcut** — that's a common misconception. Our `/remember` command fills that gap by appending dated facts under the right heading.

## Custom slash commands

Markdown files in `.claude/commands/` (project) or `~/.claude/commands/` (personal). Filename becomes the command name; subdirectories namespace it.

```markdown
---
description: One-line summary shown in the command list
argument-hint: [what to pass]
allowed-tools: Bash(python3 *), Read, Grep
model: claude-opus-4-8
---

Prompt body. Use $ARGUMENTS for all args, or $1 $2 for positional.
Prefix a line with ! to run it as bash; use @path to inline a file.
```

Ours: `/recall`, `/graph`, `/remember`, `/process-inbox`, `/wrap`.

## Hooks

Shell commands wired to lifecycle events in `.claude/settings.json` — the mechanism for enforcing habits the model would otherwise have to remember.

- **`SessionStart`** — matchers `startup` / `resume` / `clear` / `compact` / `fork`. **stdout is injected into context.** Ideal for briefing an agent on vault state.
- **`Stop`** — fires when Claude finishes responding. Can return `{"decision": "block", "reason": "..."}` on stdout with **exit 0** to send feedback and keep going. The stdin payload includes **`stop_hook_active`** — check it and exit 0 immediately when true, or you create an infinite loop.
- **`UserPromptSubmit`** — can inject context via `{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "..."}}`. The nesting is required; top-level `additionalContext` is silently ignored.

**Exit codes:** `0` = success (stdout JSON honored) · `2` = blocking error (**stdout ignored**, stderr used) · other = non-blocking error. Don't combine exit 2 with JSON output — pick one channel.

`$CLAUDE_PROJECT_DIR` resolves to the repo root in hook commands. `.claude/settings.json` is picked up automatically when a repo is cloned.

## Related

- [[Obsidian Knowledge Graph Conventions]] — the other half of the stack
