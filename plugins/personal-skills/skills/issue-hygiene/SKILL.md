---
name: issue-hygiene
description: Draft, publish, label, refresh, or close a GitHub issue so its body is resume-ready and every write is authorized. Use when an issue is written, edited, labeled, or closed, or when a PR an issue references merges.
---

# Issue Hygiene

An issue is a durable work surface another session resumes without this chat.
Its body states what is true now and the one next action. Everything else is
noise that a later reader pays for.

## Authorization

Draft in chat first. Create, edit, comment on, label, or close an issue only
when the user authorized that specific write. Agreement on the content is not
authorization to publish it. A request that names the publication (for example
"open the issues", "close it", "rewrite it in place") is, and so is one that
names the outcome ("update the tracker so I don't have to remember anything")
for the writes that outcome needs.

## Body

- Lead with current state and the next action. State what is true on the
  default branch, with a file path only where it is load-bearing for
  verification. Then the single next action or decision.
- Evidence may be long: measurements, tables, verified file facts. Options
  and checklists may not. One open fork per issue, with a default. A decision
  for the owner is one question in the next-action line, never a checklist of
  boxes.
- Evidence lives in the repository or in the issue. Not on an agent's machine,
  not in a git-ignored folder, not in this chat.
- No agent or model names in a body or comment. A recommendation an agent
  wrote is a recommendation, never a decision.
- Plan, verification, and the open fork follow when the work is substantial.
  Verification names commands and the manual checks static proof cannot
  cover.
- Process history stays out. After a decision, rewrite around the new state
  rather than appending.
- A parent issue earns its place only when it sequences three or more pieces
  or holds a decision that spans them. Two pieces blocked by the same PR stand
  alone.

## Labels

Read the repository's label meanings before applying any (`gh label list`).
Apply a "ready for an agent" label only when a fresh agent can act without chat
context: current truth and the affected owner are explicit, scope and ordered
dependencies are stated, proof is located, and no human decision remains; any
open fork has a default and an escalation trigger. Never pair it with a label
that says a human answer or more information is still needed.

## Freshness

- When a PR an issue references merges, or the owning code changes, re-check
  the issue's current-state claims before acting on it. An open issue keeps no
  next action that already happened.
- Prefer native tracking over memory: a PR that resolves an issue says
  `Closes #n` in its body, and a PR that unblocks issues says which.
- Closing: one or two sentences with the proof and where any leftovers went.
  A closed issue with a stale body is not a safe plan; a reopen starts with a
  rewrite.
