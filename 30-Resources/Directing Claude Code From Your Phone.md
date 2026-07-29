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

## Dispatch — a chat on the phone that spawns a session on the desktop

Remote Control's weakness is that *something has to already be running* before the phone is useful. Dispatch removes that precondition, which makes it the right answer to "open a chat on my phone and have it start up on my desktop."

Dispatch is a persistent conversation living in the **Cowork** tab of the Claude Desktop app. Message it a task and it decides how to handle it. A task becomes a Code session either because you asked outright ("open a Claude Code session and fix the login bug") or because Dispatch judged it to be development work. Bug fixes, dependency updates, test runs, and PRs route to Code; research, documents, and spreadsheets stay in Cowork.

The spawned session appears in the Desktop app's **Code** tab sidebar with a **Dispatch** badge — so it's controllable from the desktop *and* the phone, and a push notification hits the phone when it finishes or needs approval.

Requirements worth checking before committing to this path:

- **Pro or Max plan.** Dispatch is explicitly unavailable on Team and Enterprise.
- **Desktop app installed and running** on the target machine — this is what hosts the session, so the machine has to be awake.
- **On Windows, [Git for Windows](https://git-scm.com/downloads/win) must be installed** or the Code tab won't work at all; restart the app after installing.
- Each session gets its own [git worktree](https://code.claude.com/docs/en/worktrees) under `<project-root>/.claude/worktrees/`, so parallel sessions don't collide.
- With computer use enabled, Dispatch sessions can drive apps too — but approvals expire every 30 minutes and re-prompt, unlike the session-long approvals in ordinary Code sessions.

## Choosing between them

| If you want to… | Use |
|---|---|
| Start work from the phone with nothing running yet | **Dispatch** |
| Take over a session already in progress at the desk | **Remote Control** |
| Work a repo you don't have cloned, or run many tasks in parallel | **Cloud** |

## Out-of-band access is a different job

Everything above assumes the machine is healthy and signed in. When it isn't — locked out, service down, mid-boot — none of it helps, because all of it runs *inside* a working session. That's a separate need, and SSH is the right tool for it.

**The obstacle is NAT, not SSH.** Home machines have no public address. Forwarding port 22 on the router solves reachability by exposing SSH to the entire internet, which invites continuous brute-force traffic against a machine holding trading credentials. Not worth it.

**Tailscale is the answer instead.** Free for personal use, runs on Windows and both phone platforms, and puts every device on a private WireGuard mesh with a stable `100.x.x.x` address — no port forwarding, no dynamic DNS, nothing publicly exposed. Pair it with a phone terminal (Termius, Blink, JuiceSSH) for access from anywhere.

> **Check before building.** On 2026-07-29 this was recommended as new setup when Tailscale had in fact been running on both of Chris's machines for weeks. `~/.ssh/config` already pointed at `100.x` addresses. **Read `~/.ssh/config` and run `tailscale status` first** — the mesh may already exist, and the only missing piece may be the phone.

**A laptop can serve as a jump host when the target is locked out.** Phone → laptop over Tailscale → desktop over whatever SSH key the laptop already holds. Only the laptop needs to be reachable, which makes this work even when the desktop can't be signed into at all.

**The client-side failure mode to recognize.** A phone SSH client reporting *"connection timed out — no more addresses to try"* against a `100.x` address almost always means the VPN is off, not that the host is down: without Tailscale running, that address is unroutable. On iOS the tell is the **`VPN` badge in the status bar** — absent badge, absent route. Check that before touching the host, port, or key, all of which are innocent.

**Private keys are the single point of failure.** `~/.ssh` is not inside OneDrive or any sync folder by default, so the keys die with the machine holding them. Copy the folder into cloud storage — it is a few KB, and it is what lets a phone pick up the connection after a laptop is gone.

**Keep the two jobs separate.** SSH is a recovery channel; a phone keyboard driving a Windows command prompt is a miserable place to write code. Dispatch is the work surface. Wanting SSH was never the mistake — changing a machine's login password to get it was, and so was expecting it to double as the way to do real work.

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
