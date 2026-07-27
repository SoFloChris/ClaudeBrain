---
type: adr
# The decision and its because, in one line:
# "ADR-000N (accepted): X, because Y."
summary: ""
status: proposed
date: {{date}}
decision_makers: ["[[Chris Aguirre]]"]
project: 
supersedes: 
superseded_by: 
related: []
tags:
  - adr
---

# ADR-NNNN — {short title: the problem and the chosen solution}

<!-- Pick NNNN from `decisions/` on the DEFAULT branch, not on yours. Two sessions
     on separate branches will each read their own folder, each conclude the next
     number is the same one, and git will merge both without a conflict because
     each only added a file. This has already happened once here — see the
     numbering section of [[Architecture Decision Record]]. -->


## Context and Problem Statement

{Two or three sentences. State the problem as a question if you can, and name the
components it touches. This section is the historical record — once accepted, don't
rewrite it.}

## Decision Drivers

- {a force or constraint that actually shaped this}

## Considered Options

- {option 1}
- {option 2}

## Decision Outcome

Chosen option: "{option}", because {the deciding reason}.

### Consequences

- Good, because {…}
- Bad, because {…}
- Neutral, because {…}

### Confirmation

{How would you know this decision is actually being followed? A test, a startup
assertion, a lint rule. If you can't name one, say so honestly.}

## Pros and Cons of the Options

### {option 1}

- Good, because {…}
- Bad, because {…}

## More Information

{What would falsify this? When should it be revisited?}

## Amendments

<!-- Append only. Never rewrite Context or Decision Outcome — those are the record. -->
- **YYYY-MM-DD** — {what was learned later, and whether the decision still stands}
