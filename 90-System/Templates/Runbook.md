---
type: runbook
# What this procedure accomplishes, and when to reach for it.
summary: ""
project: 
owner: "[[Chris Aguirre]]"
risk: medium
reversible: true
last_reviewed: {{date}}
last_tested: 
related: []
tags:
  - runbook
---

# Runbook — {imperative goal, e.g. "Restore COMMAND from a cold backup"}

> **Purpose:** {one sentence — what this achieves and when you'd run it}
> **Risk:** {what could go wrong} · **Reversible:** {yes/no}

## When to run this

**Triggers / symptoms**
- {the alert, error string, or condition that brings you here}

**Do NOT run this if**
- {conditions that make this the wrong procedure — link to the right one}

## Prerequisites

- [ ] Access: {credentials, keys, admin role}
- [ ] State: {what must be true before starting}
- [ ] Tools: {CLI versions, binaries}

## Procedure

### 1. {step}

```bash
{exact copy-pasteable command}
```

*Expected:* `{exact expected output — never "it should work"}`
*If this fails:* → Troubleshooting below

## Verification

Proves the whole thing worked, independently of the steps above.

```bash
```

- [ ] {observable condition, with the exact value or threshold}

## Rollback

**Trigger:** {when to abandon and roll back}

```bash
```

*Expected:* ``

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
|  |  |  |

## Change history

- **YYYY-MM-DD** — {what changed in this runbook and why}
