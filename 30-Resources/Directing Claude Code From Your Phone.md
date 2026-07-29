---
type: resource
summary: "Reaching Claude Code from a phone is a choice about where the work executes, and the two options that run on your own hardware need no inbound access — which is why SSH is the wrong tool for it."
aliases: ["Remote Control", "Claude Code Dispatch", "Work on my desktop from my phone", "Phone to desktop Claude"]
topic: "[[Claude Code]]"
related: ["[[Claude Code Memory and Commands]]"]
tags:
  - resource
---

# Directing Claude Code From Your Phone

Reference for the five ways to reach a Claude Code session while away from the machine. Verified against the official docs (2026-07).

The question this answers: *"My desktop is always on — how do I make it do the work while I direct from my phone?"*

## The real axis is where execution happens

Not "how do I connect." Every option below is reached from the same phone and the same claude.ai/code interface. They differ in **whose CPU and filesystem** are involved.

| Option | Trigger | Runs on | Setup |
|---|---|---|---|
| **Dispatch** | Message a task from the mobile app | **Your machine** (Desktop app) | Pair mobile app with Desktop |
| **Remote Control** | Steer a live session from phone/web | **Your machine** (CLI or VS Code) | `claude remote-control` |
| **Claude Code on the web** | Start a session at claude.ai/code | Anthropic cloud VM | None |
| **Channels** | Push events from Telegram/Discord | **Your machine** (CLI) | Install a channel plugin |
| **Scheduled tasks** | A cron schedule | CLI, Desktop, *or* cloud | Pick a frequency |

**Dispatch and Remote Control are the only ones that touch your own files.** Everything else clones from GitHub into a throwaway container.

## Why SSH is the wrong frame

The instinct — "just SSH into the desktop" — solves a problem that doesn't exist, and creates two that do (an inbound port, and NAT traversal to a home network).

Remote Control inverts it:

> Your local Claude Code session makes **outbound HTTPS requests only and never opens inbound ports on your machine.**

The desktop dials out to Anthropic and polls for work; the phone talks to Anthropic. Neither ever connects *to* the desktop. No port forwarding, no tunnel, no static IP, no key management. This is strictly better than SSH for the purpose, not a workaround for lacking it.

## Remote Control — steering a live session

Run on the machine that should do the work, from inside the project directory:

```bash
claude remote-control          # server mode, prints a URL + QR code
claude --remote-control        # ordinary interactive session, also reachable remotely
/remote-control                # from inside a running session, keeps its history
```

Then open the URL, scan the QR, or find the session at claude.ai/code — it shows a computer icon with a green dot when online.

What survives the trip: the local filesystem, local MCP servers, project config, and `@` file-path autocomplete. Messages can be sent from terminal, browser, and phone interchangeably; all stay in sync.

Worth knowing before relying on it:

- **The local process must stay alive.** Close the terminal and the session dies. On an always-on machine, start it inside `tmux` or `screen` so it outlives a disconnect.
- **~10 minutes of network loss kills it.** The machine being awake isn't enough; it has to reach the network.
- Auto-connect for every session: `/config` → **Enable Remote Control for all sessions**.
- Requires a claude.ai login. API keys, `setup-token` tokens, and a non-Anthropic `ANTHROPIC_BASE_URL` all disqualify it.
- `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, and `DISABLE_GROWTHBOOK` each silently disable the feature-flag check it depends on.

## Dispatch — delegating without a running session

Remote Control's weakness is that *something has to already be running*. Dispatch removes that: pair the mobile app with the Desktop app once, then message a task from the phone and it spawns a Desktop session on demand. The docs rate it "minimal setup," and it's the better fit for delegating work while genuinely away rather than steering work already in progress.

## The GitHub access rule people get wrong

For **cloud** sessions specifically:

> A cloud session can access any repository the connecting GitHub account can see, **not just the repositories the Claude GitHub App is installed on.** App installation enables PR webhooks for Auto-fix; it is not a session-level access control.

So a repo that a cloud session can't reach is an account-visibility problem, not an app-installation problem. Two fixes:

- **`/web-setup`** in a local terminal syncs that machine's `gh` CLI token to your Claude account — the path when the repo lives under a *different* GitHub account you're logged into locally.
- **`claude --cloud`** from a repo with no GitHub remote bundles the local repository and uploads it directly. `CCR_FORCE_BUNDLE=1` forces this even when GitHub is connected. Bundles must be under 100 MB and exclude untracked files.

None of this applies to Remote Control or Dispatch — they read the disk directly, so a repo that never left the machine is still fully workable.

## Related

- [[Claude Code]] — the tool all five of these options are surfaces onto
- [[Claude Code Memory and Commands]] — what loads into a session once one is running, wherever it runs
