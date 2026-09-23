---
name: visual-brief
description: Create an HTML explanation when a diagram, comparison, or expandable evidence makes substantial material easier to understand.
---

# Visual Brief

Give the user an entry point they can absorb quickly and return to as the work
changes. Prefer this format for substantial communication across technical and
nontechnical subjects. Adapt the view to the question instead of filling a
standard report outline.

## Shape The Message

Identify the audience, the question the view must answer, the current state,
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
| Which option fits? | Comparison using the same decision criteria for each option |
| Where are we? | Actual status, remaining work and the choices that still need resolution |
| What is settled, and why? | Decision and brief rationale, linked to its owning record and supporting evidence |

A single diagram may be enough. For a substantial brief, use one focused HTML
file with a compact visible layer and native expandable details. Each collapsed
summary should name the subject and explain its significance; opening it reveals
outcomes, reasoning, proof or technical depth. The closed view must stand alone.

Link relevant issues, technical documents and source evidence where they answer
the reader's next question. Explain what a link provides instead of collecting
an undifferentiated bibliography. Show settled decisions and their implications
without copying an entire decision log into the entry point.

## Build The View

Use [assets/brief.html](assets/brief.html) as a preferred standalone starting
style when its current/target, flow and expandable-detail patterns fit. Read it
only when building the HTML. Replace its illustrative content and omit unused
sections. The subject, labels and section count are examples.

- Preserve the preferred visual character: readable system type, generous
  spacing, neutral surfaces, quiet blue accents, clear flow nodes and tidy
  disclosure rows. Adapt to an existing product's tokens when relevant.
- Support light and dark system themes with deliberate surface, text, border
  and accent colors. Verify both; a dark background alone is not a dark theme.
- Prefer semantic HTML, inline CSS and simple HTML/SVG diagrams. Native
  `details`/`summary` provides disclosure without an application framework.
  Add JavaScript only for an interaction that helps the reader reason or choose.
- Make the layout reflow for narrow screens. Keep diagrams readable in their
  stacked form, label status in words, and provide visible keyboard focus and
  sufficient contrast. Keep essential content usable without remote resources.
- Use physical cues only when they clarify interaction or relationships.
  Familiar disclosure markers and light surface separation can help; decorative
  textures and elaborate object metaphors should not compete with the content.
- Preserve distinctions between observed, proposed, completed and unverified
  states. Evidence supports completion; decorative percentages and editable
  checkboxes must not masquerade as tracked progress.

The starter is an aid to composition, not a required workflow. The artifact can
explain a personal decision, a system, a research result or a project without
inventing repository concepts, work slices or approval gates.

## Keep It Current

When another source owns the plan or data, link it and identify the HTML as a
dated snapshot. Update from that owner; do not create a second independently
editable tracker. If this artifact is itself the requested deliverable, it can
own the explanation without manufacturing an external source of truth.

On an update, rewrite around the new state instead of appending a history of
decisions. Preserve a useful existing artifact path. Keep detailed research in
one linked supporting location when it remains useful; clearly mark superseded
planning. Do not copy the entire brief back into chat or maintain redundant
Markdown and HTML plans merely for completeness.

## Verify And Deliver

Use the task's artifact location, or OS temp when none is specified and the
brief is ephemeral. Follow the host's supported preview and file-link tools.
Creating a local brief does not authorize external publication or tracker edits.

Inspect the rendered view at a normal and narrow width in light and dark themes
when the environment permits it. Check disclosure, clipping, diagram labels,
focus, contrast and links. Reconcile status and claims with the owning evidence.
If rendering is unavailable or blocked, perform structural checks and state the
limit; do not describe those checks as visual proof or work around a blocked
preview route.

Deliver the artifact with a short orientation and the decision or next action
that matters. Open it with a supported preview when possible and give its
usable link. The user should not need to read the chat history to understand it.
