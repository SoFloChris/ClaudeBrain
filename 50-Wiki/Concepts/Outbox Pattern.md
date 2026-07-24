---
type: concept
aliases: [transactional outbox, broker outbox]
summary: "Commit the intent to act into your own database in the same transaction as the decision, and let a separate worker perform the external call — so a crash mid-flight loses nothing and duplicates nothing."
related: ["[[Order Intent]]", "[[Reconciliation]]", "[[COMMAND — Quant Operations Platform]]"]
tags:
  - concept
created: 2026-07-24
---

# Outbox Pattern

A decision and its external side effect can't be made atomic — your database and someone else's API don't share a transaction. The outbox pattern accepts that and moves the boundary: **write the intent to act into your own DB in the same transaction as the decision**, then let a separate worker drain that queue and make the network call.

The atomic guarantee you get is "the decision and the promise to act are committed together." The network call becomes retryable rather than lost.

## How [[COMMAND — Quant Operations Platform]] runs it

When an [[Order Intent]] seals, it is enqueued to `broker_outbox` **in the same transaction as the seal**. A worker then:

- drains every 5 seconds with **row-level locking**, so two workers can't send the same order;
- retries with **exponential backoff**, `max_attempts` default 3;
- **dead-letters** what still fails, rather than retrying forever.

The `client_order_id` assigned at seal time is what makes the retry safe — the broker treats a resend as the same order.

## Why it matters to me

**The failure this prevents is the one you can't detect: a process that dies between "I decided" and "I sent."** Without an outbox, that gap produces either a lost order or — worse, if you retry naively — a duplicate one. With it, the decision is durable and the send is idempotent, so recovery is just "drain the queue again."

Two design notes that generalise:

- **Dead-letter, don't retry forever.** Infinite retry converts a transient outage into an unbounded backlog that eventually fires all at once, at prices that no longer make sense.
- **Idempotency key at commit time, not send time.** Generating it when the decision is frozen is what lets *any* future attempt be recognised as the same attempt.

An outbox handles the crash. It does not handle "the broker accepted it and I never learned" — that's [[Reconciliation]]'s job. The two are complements, not alternatives.

## Related

- [[Order Intent]] — the sealed decision that gets enqueued
- [[Reconciliation]] — covers the gap an outbox structurally cannot
