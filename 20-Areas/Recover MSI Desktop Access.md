---
type: runbook
summary: "The laptop already holds working SSH access to the locked-out MSI desktop, so recovery runs from a Claude Code session on the laptop — not from a web session, which can never reach either machine."
project: 
owner: "[[Chris Aguirre]]"
risk: medium
reversible: true
last_reviewed: 2026-07-29
last_tested: 
related: ["[[Directing Claude Code From Your Phone]]"]
tags:
  - runbook
---

# Runbook — Recover MSI Desktop Access and Set Up Phone Control

> **Purpose:** Get back into the locked-out MSI desktop using the SSH access the laptop already has, then replace the SSH arrangement with Dispatch so the phone can drive the desktop properly.
> **Risk:** A wrong turn can trigger a BitLocker prompt · **Reversible:** yes, provided the recovery key is in hand first

## When to run this

**Triggers / symptoms**
- Locked out of the MSI desktop after its Windows password was changed to enable SSH (2026-07-29)
- Want phone-directed work that executes on the desktop

**Do NOT run this from a web or mobile Claude session.** Those run in throwaway Anthropic cloud containers with no `ssh` binary, no keys, and no network route to either machine. Verified repeatedly — see `Memory.md`. **This runbook only works from a Claude Code session running on the laptop**, because that is where the SSH key physically lives.

## Prerequisites

- [ ] **BitLocker recovery key saved** from [account.microsoft.com/devices/recoverykey](https://account.microsoft.com/devices/recoverykey) — screenshot every entry, both machines. Do this first; it is the only guard against the one unrecoverable outcome.
- [ ] Laptop powered on and on the same network as the desktop
- [ ] Claude Code installed on the laptop

## Procedure

### 1. Start a session on the laptop, in the vault

```bash
cd /path/to/ClaudeBrain
git pull
claude
```

Pulling first loads `Memory.md` and this runbook, so the session starts with the full history rather than rediscovering it.

### 2. Find the SSH target

```bash
cat ~/.ssh/config
ls -la ~/.ssh/
```

*Expected:* a `Host` entry for the desktop with `HostName`, `User`, and `IdentityFile`, plus a private key file.
*If empty:* the setup lives somewhere else on the laptop — search shell history with `grep -i ssh ~/.bash_history ~/.zsh_history`, and check past Claude Code session transcripts under `~/.claude/projects/`.

### 3. Confirm the key still works

```bash
ssh <host-alias-from-config>
```

*Expected:* a shell on the desktop **without a password prompt**. Key-based auth is unaffected by the Windows password change, which is why this route survives the lockout.
*If it asks for a password:* auth is password-based, not key-based, and this route is dead — fall back to Verification below.

### 4. Reset the Windows password over SSH

From the desktop shell, as an administrator:

```cmd
net user <username> <new-password>
```

To list accounts first if the username is uncertain:

```cmd
net user
```

*Expected:* `The command completed successfully.`
*If access denied:* the SSH user is not elevated. Open an elevated shell or use an admin account.

### 5. Log in at the desktop

Use the new password at the lock screen.

*If a blue BitLocker screen appears instead:* it displays a **Key ID** — match that against the saved list and enter the corresponding 48-digit key.

### 6. Replace SSH with Dispatch

Once inside, do this before anything else — it is what SSH was meant to accomplish and it works without inbound access:

1. Install the Claude Desktop app ([Windows x64](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect))
2. Install [Git for Windows](https://git-scm.com/downloads/win), restart the app — the Code tab will not work without it
3. Sign in, open the **Cowork** tab, pair the phone from Dispatch settings
4. Turn off the OpenSSH server and revert any firewall or port-forwarding rules added for it

See [[Directing Claude Code From Your Phone]] for the full comparison.

## Verification

Proves recovery worked independently of the steps above:

- [ ] Desktop logs in at the lock screen with the new password
- [ ] A task messaged to Dispatch from the phone spawns a session badged **Dispatch** in the Desktop app's Code tab
- [ ] `ssh` to the desktop from the laptop now **fails**, confirming the SSH exposure is closed

## Rollback

**Trigger:** step 3 fails, meaning there is no working key.

Fall back to ordinary Windows recovery, which needs someone physically at the desktop:

1. Lock screen → **Sign-in options** → try the **PIN**; it is stored separately and survives a password change
2. Microsoft account (lock screen shows an email) → reset at [account.live.com/password/reset](https://account.live.com/password/reset) from the phone; the desktop picks it up once online
3. Local account (lock screen shows a plain username) → enter a wrong password once, click **Reset password**, answer the security questions
4. Second admin account on the machine → reset from **Settings → Accounts → Family & other users**

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| `ssh: connect to host ... port 22: Connection refused` | OpenSSH server not running, or desktop asleep | Wake the desktop; the service may be manual-start |
| `Permission denied (publickey)` | Wrong key or wrong user | Check `IdentityFile` and `User` in `~/.ssh/config` |
| `net user` → access denied | SSH session not elevated | Use an admin account or an elevated shell |
| Blue screen asking for 48 digits | BitLocker recovery triggered | Match the on-screen **Key ID** to the saved keys |
| Microsoft password reset doesn't take | Desktop offline, so the old cached password still applies | Get it on Ethernet or Wi-Fi, then retry |

## Change history

- **2026-07-29** — Created after the SSH setup changed the desktop's Windows password and locked it out. Written to be run from the laptop, since that is the only machine holding the key.

## Related

- [[Directing Claude Code From Your Phone]] — what step 6 replaces the SSH arrangement with, and why it needs no inbound access
