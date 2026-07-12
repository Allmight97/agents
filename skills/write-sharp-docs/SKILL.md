---
name: write-sharp-docs
description: Write, rewrite, critique, and manage high-taste technical program and engineering documents. Use when asked for better docs, specs, RFCs, decision memos, launch or readiness docs, completion records, Google Docs-ready drafts, less LLM-y writing, senior TPM or staff-engineer polish, document pruning, audience fit, decision clarity, or durable knowledge management.
---

# Write Sharp Docs

## First Move

Identify five facts before drafting or editing:

- **Audience**: exec, director, staff engineer, TPM, implementation team, review group, partner team, or future maintainer.
- **Document job**: decide, align, brief, launch, hand off, unblock, record, audit, or maintain.
- **Current state**: proposed, approved, in progress, completed, blocked, deferred, rejected, or mixed.
- **Durability**: one-time work state, active project doc, durable canon, or decision record.
- **Surface**: chat answer, Markdown, Google Doc, Google Sheet, Google Slides, issue, PR description, or repo doc.

If the user points at Google Drive, Docs, Sheets, or Slides, use the relevant Google connector skill when available for live file state, edits, comments, export, import, or file organization. Do not rely on web search or model memory for live enterprise document state.

If the job is packaging the current session for a fresh task, `handoff` owns the
artifact and its structure. Use this skill only to improve handoff prose when
the user explicitly asks for that editorial pass.

## State Before Story

Establish what is true now before explaining how it happened. A reader should
never have to infer whether a statement is proposed, approved, in progress,
completed, blocked, deferred, or rejected.

For mixed-status work, lead with the smallest useful state ledger:

- **Completed**: the outcome and its durable location or proof
- **Remaining**: unfinished work, owner, and next action
- **Decision needed**: the exact unresolved choice and recommendation
- **Deferred or rejected**: what is intentionally not happening and why

Use only the categories that contain material information. Do not force a
status table onto a one-state document.

Separate a finding from its disposition. For an audit that led to action, make
the chain explicit: **finding → decision → change → proof**. A finding without
its disposition reads like an open proposal even after the work is complete.

When work advances from proposal to implementation, rewrite the document around
the new current state. Remove obsolete future tense, stale decision prompts,
and recommendations that were already accepted or rejected. Do not append a
completion note to an otherwise proposal-shaped document.

## Structure Selector

Choose the smallest structure that does the job:

- **Small or reversible change**: answer, owner, next action, risk if ignored.
- **RFC or design doc**: decision needed, recommendation, context, constraints, options, tradeoffs, rollout, risks, open questions.
- **Decision memo**: decision, recommendation, evidence, options considered, impact, owners, date, revisit trigger.
- **Launch or readiness doc**: current status, launch criteria, risks, owners, verification, rollback, communications, unresolved decisions.
- **Audit or completion record**: current-state ledger, material findings and dispositions, completed changes with proof, remaining work, deferred decisions.

For a long document, disclose progressively:

1. current state, recommendation, and next action;
2. decision or implementation detail;
3. evidence, history, and reference material.

The first layer must stand alone. Do not make the reader hunt through detail to
discover whether the work happened or what remains.

## Taste Rules

Lead with the decision surface: status, recommendation, action, owner, or needed decision. Put background after the reader knows why it matters.

Keep:

- Decision pressure, tradeoffs, constraints, dates, owners, and unresolved questions.
- A compact implementation record when exact completed work, publication state, or durable location prevents ambiguity.
- Evidence that changes the decision, scope, risk, or confidence.
- Alternatives only when they prevent re-litigation or expose a real tradeoff.
- Context that a new but competent reader needs to act without a meeting.

Delete or compress:

- Provenance narration, chronological process narration, compliance theater, and activity logs that do not change current state.
- Generic best-practice filler, obvious non-goals, template cargo cult, and self-justifying caveats.
- Risks without owner, trigger, impact, or mitigation.
- Status hidden inside paragraphs when a table or lead sentence would scan faster.
- Long histories that belong in a linked artifact or decision record.

Distinguish an implementation record from process narration. “Published commit
X; plugin Y is enabled; restart remains” orients the reader. A chronological
account of commands, retries, and intermediate thoughts usually does not.

Use plain company-document language. Avoid consultant polish, marketing tone, bureaucratic ceremony, and LLM-shaped transitions.

## Google Enterprise Defaults

Use Google Docs for narrative decisions, RFCs, handoffs, and reviewable drafts. Prefer heading hierarchy, short tables for status and ownership, comments for unresolved reviewer input, and links to canonical sources rather than copied context.

Use Google Sheets for trackers, launch checklists, risk registers, workback plans, stakeholder maps, and anything that needs filtering, assignment, status, or repeated updates.

Use Google Slides for exec readouts, decision reviews, launch readiness summaries, incident updates, and cross-functional alignment where sequencing and visual hierarchy matter more than full prose.

When managing docs, separate durable canon from temporary work state. Promote only enduring decisions, contracts, and operating rules into canon. Archive or close stale working docs instead of letting them become false authority.

## Output Modes

Match the user's request:

- **Rewrite**: return the improved doc or section directly.
- **Taste diff**: list what to cut, keep, reorder, and strengthen.
- **Structure proposal**: give the doc outline and explain only the choices that change reader action.
- **Google Docs plan**: name the target Google surface, section shape, comment strategy, and source links needed.
- **Canon routing**: say what belongs in a durable doc, what stays temporary, and what should be deleted or archived.

## Completion Check

Before finishing, verify:

- the first screen says what is true now and what remains;
- every material finding has an explicit disposition;
- settled proposals and questions have been rewritten or removed;
- completed claims name durable proof or location when it matters;
- fact, inference, recommendation, and open question are not blurred;
- the reader's next action is obvious;
- context stays proportional to risk, process filler is gone, and durable
  knowledge is routed to the right home.
