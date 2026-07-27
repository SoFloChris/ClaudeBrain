---
type: company
aliases: ["Cold IQ", "ColdLabs"]
relationship: reference
related: ["[[Claude Code]]", "[[Skills Are Verbs, Notes Are Nouns]]"]
---

# ColdIQ

**What they do:** A B2B outbound/GTM consultancy that publishes the largest public [[Claude Code]] skill library for sales — 100+ skills covering ICP definition, list building, cold email, LinkedIn, signal-based selling, and n8n automation. Given away free; the business is the services and their MCP/API marketplace behind it.

## Key facts (researched 2026-07)

- **Repo:** `Cold-IQ/ColdIQ-s-GTM-Skills` (~221 stars) — 6 master skills acting as orchestrators plus 43 sub-skills, alongside 31 standalone skills. Ships 137 sales triggers, 34 email templates, and 11 GTM plays as data.
- **Structure:** `master-skills/` (orchestrators) + `skills/` (standalone) + `COLDIQ-FIRST.md` (provider mapping). Master skills: Cold Email, LinkedIn Ads, LinkedIn Content, List Building, n8n Automation, Signal Sourcer.
- **The benchmark data is the moat:** campaign analysis is graded against real lemlist data — **244K+ campaigns and 249M+ emails**. That figure is what "244k campaign data" refers to on any skill tree you see screenshotted.
- **Install:** `npx skills add …`; MCP access via `COLDIQ_API_KEY=<key> npx -y @coldiq/mcp@latest`. Integrates with Apollo, Clay, Prospeo, Findymail, RB2B, lemlist, n8n, Salesforce, HubSpot, Slack.
- Their published workflow is a 7-step campaign build inside Claude Code: list building → ICP scoring of every account → tiering (Tier 1 gets manual outreach) → enrichment → copy → send → auto-improve. Claude Code handles 50k-row CSVs directly.
- **Open-source alternative:** `growthenginenowoslawski/coldoutboundskills` — 28 skills distilled from 1,000+ B2B campaigns, no vendor account required.

## Why it matters to me

Not for the outbound. Their workspace is the clearest public example of a **domain agent built on the same four-part shape as this vault** — router, memory, canonical brief, skills, data — which is the pattern worth stealing. See [[Skills Are Verbs, Notes Are Nouns]].

## Related

- [[Skills Are Verbs, Notes Are Nouns]] — the architecture their workspace demonstrates
- [[Claude Code]] — the harness all of their skills target
