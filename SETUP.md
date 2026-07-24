# Setup — Laptop & Desktop

Do these steps on **each machine** (desktop first, then laptop — the steps are identical). At the end, both machines share one vault that syncs through this GitHub repo, and Claude can work inside it.

## 1. Install the apps

- [Obsidian](https://obsidian.md/download) (free)
- [Git](https://git-scm.com/downloads) — on Mac, running `git` once in Terminal offers to install it; on Windows use the installer defaults
- Optional but recommended: [GitHub Desktop](https://desktop.github.com/) if you prefer clicking to typing

## 2. Clone the vault

Pick a permanent home for it (examples: `~/ClaudeBrain` on Mac, `C:\Users\you\ClaudeBrain` on Windows), then:

```
git clone https://github.com/SoFloChris/ClaudeBrain.git
```

(or in GitHub Desktop: **File → Clone Repository → ClaudeBrain**)

## 3. Open it in Obsidian

1. Open Obsidian → **Open folder as vault** → choose the cloned `ClaudeBrain` folder.
2. When asked whether to trust the vault and enable its settings, say yes — the vault ships its own config (templates folder, daily notes, new-note location already wired up).
3. Open `Home.md` — that's the dashboard.

## 4. Install Obsidian Git (auto-sync)

This is what keeps laptop and desktop in sync without you thinking about it.

1. **Settings → Community plugins → Turn on community plugins → Browse**
2. Search **"Git"** (by Vinzent / Denis Olehov), install, **enable**.
3. In the plugin's settings, set:
   - **Auto pull interval:** 5 minutes
   - **Auto commit-and-push interval:** 5 minutes
   - **Pull on startup:** on
   - **Commit message:** leave default
4. First time only, git may ask for GitHub credentials — sign in via GitHub Desktop or follow the prompt (it uses your normal GitHub login).

The sync loop is just git: edit anywhere → auto commit+push → other machine auto-pulls. If you ever edit the *same line* of the *same note* on both machines while offline, git will flag a conflict — open the file, keep the version you want, delete the conflict markers.

## 5. Hook up Claude

Any of these work — they all read `CLAUDE.md` automatically because it's in the vault root:

- **Claude Code (terminal):** `cd` into the vault folder and run `claude`.
- **Claude Desktop / Cowork:** point it at the `ClaudeBrain` folder.
- **Claude Code on the web:** this repo is already connected — just start a session on it.

First session, try: *"Read my router and tell me how this vault works. Then add a note to my inbox that says hello."*

## 6. Make it yours

- Fill in the **Who I am** section of `CLAUDE.md` (role, current focus).
- Add your real areas to `20-Areas/_Index.md`.
- Check off the tasks in `10-Projects/Set Up ClaudeBrain.md` as you go.

## Troubleshooting

- **Changes not showing up on the other machine:** open the command palette (`Cmd/Ctrl+P`) → "Git: Pull". If that errors, "Git: Commit-and-push" on the machine you edited first.
- **Obsidian shows a "Merge conflict" notice:** open the affected file, pick the right lines, remove the `<<<<<<<`/`>>>>>>>` markers, then commit-and-push.
- **Don't edit on both machines at the same time** while offline and you'll basically never see a conflict — markdown files merge cleanly otherwise.
