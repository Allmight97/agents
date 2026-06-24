---
name: write-sharp-docs
description: Write, rewrite, critique, and manage high-taste technical program and engineering documents. Use when Codex is asked for better docs, specs, RFCs, decision memos, launch or readiness docs, handoffs, Google Docs-ready drafts, less LLM-y writing, senior TPM or staff-engineer polish, document pruning, audience fit, decision clarity, or durable knowledge management.
---

# Write Sharp Docs

## First Move

Identify four facts before drafting or editing:

- **Audience**: exec, director, staff engineer, TPM, implementation team, review group, partner team, or future maintainer.
- **Document job**: decide, align, brief, launch, hand off, unblock, record, audit, or maintain.
- **Durability**: one-time work state, active project doc, durable canon, or decision record.
- **Surface**: chat answer, Markdown, Google Doc, Google Sheet, Google Slides, issue, PR description, or repo doc.

If the user points at Google Drive, Docs, Sheets, or Slides, use the relevant Google connector skill when available for live file state, edits, comments, export, import, or file organization. Do not rely on web search or model memory for live enterprise document state.

## Structure Selector

Choose the smallest structure that does the job:

- **Small or reversible change**: answer, owner, next action, risk if ignored.
- **RFC or design doc**: decision needed, recommendation, context, constraints, options, tradeoffs, rollout, risks, open questions.
- **Decision memo**: decision, recommendation, evidence, options considered, impact, owners, date, revisit trigger.
- **Launch or readiness doc**: current status, launch criteria, risks, owners, verification, rollback, communications, unresolved decisions.
- **Handoff**: current state, intended outcome, changed files or docs, commands or links, next actions, known risks.

## Taste Rules

Lead with the decision surface: status, recommendation, action, owner, or needed decision. Put background after the reader knows why it matters.

Keep:

- Decision pressure, tradeoffs, constraints, dates, owners, and unresolved questions.
- Evidence that changes the decision, scope, risk, or confidence.
- Alternatives only when they prevent re-litigation or expose a real tradeoff.
- Context that a new but competent reader needs to act without a meeting.

Delete or compress:

- Provenance narration, process narration, compliance theater, and "what I did" recaps.
- Generic best-practice filler, obvious non-goals, template cargo cult, and self-justifying caveats.
- Risks without owner, trigger, impact, or mitigation.
- Status hidden inside paragraphs when a table or lead sentence would scan faster.
- Long histories that belong in a linked artifact or decision record.

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

Before finishing, verify the document makes the reader's next action obvious, keeps context proportional to risk, removes provenance/process filler, and routes durable knowledge to the right home.
