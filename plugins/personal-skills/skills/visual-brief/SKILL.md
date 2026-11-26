---
name: visual-brief
description: "Explain substantial material as one HTML brief with a diagram, comparison, or expandable evidence. Use when the user asks for a brief or visual summary, or when a plan, comparison, or status is too large for a chat reply."
---

# Visual Brief

Give the user a brief they can absorb quickly and return to as the work
changes. Adapt the brief to the question instead of filling a standard report
outline.

## Shape The Message

Identify the audience, the question the brief must answer, the current state,
and the evidence or working document that owns the facts. Use available
research; presentation alone does not call for a new audit or implementation.

The first layer should establish the answer or recommendation, what matters
now, and any next action or consequential choice. Make it usable for someone
arriving without the conversation. Put the explanation beside the visual that
supports it. Keep decision-changing uncertainty visible; supporting mechanics
and evidence can expand on demand.

Choose only the views that earn their space:

| Reader's question | Useful shape |
| --- | --- |
| What changes? | Current → intended state, with the important difference named |
| How do the pieces fit? | Short flow or relationship diagram; label each part's role and the connections that matter |
| Which option fits? | Comparison: name the decision first, align the same criteria across options, show each option's cost as plainly as its benefit, and recommend only when the evidence supports it |
| Where are we? | Plan or status: goal, current state, and intended behavior first, then the approach, remaining work, and risks and open questions as options; remove a question once it is decided |
| What is settled, and why? | Decision and brief rationale, linked to its owning record and supporting evidence |
| Rows that share the same fields | Table with one line above it that says what the rows show; columns ordered identity, evidence, status, action; status in words, not by color alone |

A single diagram may be enough. For a substantial brief, use one focused HTML
file with a compact visible layer and native expandable details. Each collapsed
summary should name the subject and explain its significance; opening it reveals
outcomes, reasoning, proof or technical depth. The closed view must stand alone.

Link relevant issues, technical documents and source evidence where they answer
the reader's next question. Explain what a link provides instead of collecting
an undifferentiated bibliography. Show settled decisions and their implications
without copying an entire decision log into the brief.

Done when you can state the first layer's answer in one sentence and name each
view the brief uses.

## Build The View

Use the starter, [assets/brief.html](assets/brief.html), when its
current/target, flow and expandable-detail patterns fit. Read it only when
building the HTML. Replace its illustrative content and omit unused sections.
The subject, labels and section count are examples.

- Keep the starter's visual character when not adapting to an existing
  product's tokens.
- Support light and dark system themes with deliberate surface, text, border
  and accent colors. Verify both; a dark background alone is not a dark theme.
- Prefer semantic HTML, inline CSS and simple HTML/SVG diagrams. Add
  JavaScript only for an interaction that helps the reader reason or choose.
- Make the layout reflow for narrow screens. Keep diagrams readable in their
  stacked form, label status in words, and provide visible keyboard focus and
  sufficient contrast. Keep essential content usable without remote resources.
- Preserve distinctions between observed, proposed, completed and unverified
  states. Evidence supports completion; decorative percentages and editable
  checkboxes must not masquerade as tracked progress.

Done when every section left from the starter carries real content.

## Keep It Current

When another source owns the plan or data, link it and identify the brief as a
dated snapshot. Update from that owner; do not create a second independently
editable tracker. If the brief is itself the requested deliverable, it can own
the explanation without manufacturing an external source of truth.

On an update, rewrite around the new state; delete superseded planning from the
brief, and keep detailed research in one linked supporting location when it
remains useful. Preserve a useful existing brief path. Do not copy the entire
brief back into chat or maintain redundant Markdown and HTML plans merely for
completeness.

## Verify And Deliver

Use the location the task names; otherwise use the host's preview or
publishing tool, or the OS temp directory when the host has none. Creating a
local brief does not authorize external publication or tracker edits.

Inspect the rendered brief at a normal and narrow width in light and dark
themes when the environment permits it. Check disclosure, diagram labels,
focus, contrast and links. At the narrow width, check that nothing overflows
its layout: no sideways page scroll, no text cut off by a container that clips,
and long paths, code and URLs wrap inside their box. Reconcile status and
claims with the owning evidence. If rendering is unavailable or blocked,
perform structural checks and state the limit; do not describe those checks as
visual proof or work around a blocked preview route.

Deliver the brief with a short orientation and the decision or next action
that matters. Open it with a supported preview when possible and give its
usable link. The user should not need to read the chat history to understand it.
