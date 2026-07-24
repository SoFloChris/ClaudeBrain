---
type: tool
summary: "The community plugin that is this vault's entire sync engine between laptop and desktop."
related: ["[[Obsidian]]"]
---

# Obsidian Git

The community plugin that syncs this vault between laptop and desktop. It is the entire sync engine — there is no proprietary sync service in the loop.

## Key facts

- Settings that matter: **auto pull interval 5 min**, **auto commit-and-push interval 5 min**, **pull on startup**.
- The loop: edit anywhere → auto commit + push → the other machine auto-pulls.
- Conflicts are ordinary git conflicts. Markdown merges cleanly unless the *same line* of the *same note* is edited on both machines while offline — then open the file, keep the right version, delete the `<<<<<<<` markers, and commit.
- Manual escape hatches live in the command palette: "Git: Pull", "Git: Commit-and-push".

## Related

- [[Set Up ClaudeBrain]] — the install steps for each machine
