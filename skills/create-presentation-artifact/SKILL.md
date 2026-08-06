---
name: create-presentation-artifact
description: Create durable human-facing presentation artifacts when a decision, review, comparison, plan, research synthesis, or operational model would be hard to reconstruct from prose. Use for self-contained HTML, comparison workspaces, and interactive action aids; route ordinary summaries, repo canon, production UI, teaching workspaces, and agent guidance to their owners.
---

# Create Presentation Artifact

Create polished user-facing artifacts for decisions, reviews, plans, research,
learning, and handoff surfaces. The usual output is a single-file HTML artifact.

## Outcome Standard

Minimize the cognitive work required to form an accurate operational model.
Transfer reconstruction, comparison, sequencing, state tracking, ownership,
and completion proof from the reader into the artifact. Preserve necessary
complexity, but embody it in visible structure instead of narrative. Prefer
recognition over recall: expose active state, scope, relationships, and
completion. Let visuals replace redundant prose rather than decorate it.

Lead with the useful answer, then make supporting detail easy to scan. Keep the
primary path and current state visible. A reader should not have to join facts
from distant paragraphs, remember earlier definitions, or decode a metaphor to
understand the next section.

## Reader And Editorial Contract

Before drafting, identify:

- **audience:** who will use the artifact;
- **job:** decide, orient, compare, learn, review, plan, act, or hand off;
- **current state:** what is true now;
- **reader familiarity:** new, working knowledge, or expert;
- **next action:** what the reader should be able to do after the first layer;
- **durability:** one-time aid, active work surface, or durable reference.

Write for that reader, not an imaginary general audience. Put state before
story and literal orientation before voice, metaphor, or framing. The first
screen should normally contain one title, one plain-language answer, and no
more than three material state or scope facts. Keep visible introductory prose
under roughly 60 words unless comprehension genuinely requires more.

Use the subject's actual name or decision as the primary title. Put a literal
one-sentence identity directly beneath it: what the subject is, what it does,
and any prerequisite or boundary whose omission could change the reader's
interpretation. Treat a tagline as optional secondary voice after orientation,
never as a substitute for it. Read the opening literally; if a compact phrase
supports a materially wrong interpretation, rewrite it instead of expecting
the reader to infer the intended scope.

Across the artifact, narrative prose should be the minority. For a technical
onboarding or research briefing, default to no more than about 1,000 visible
words, excluding code tokens and a compact source index. Put necessary evidence
depth in collapsed details. A paragraph must earn its place over a label,
annotation, table, diagram, or state marker and should rarely exceed three
sentences. Exceed the budget only when the reader's job cannot be completed
accurately within it.

After factual synthesis and before visual styling, edit the copy:

- Keep text that helps the reader decide, act, navigate, or understand a
  consequential boundary.
- Convert repeated fields, sequence, ownership, state, and comparison into
  visible structure.
- Move useful depth behind progressive disclosure.
- Delete reader-direction, scene-setting, process narration, repeated
  qualifications, consultant language, and prose that narrates a visible
  relationship.
- Separate fact, inference, uncertainty, and recommendation when the
  distinction changes action or confidence.

A self-contained artifact does not need every true fact on its first screen.
The first layer must stand alone; later layers carry evidence, history, and
reference detail.

Before building, verify the representation:

- **Scan:** without reading full paragraphs, the reader can identify the
  subject, current state, primary relationship, consequential boundary, and
  next action.
- **Reconstruction:** facts that must be combined are adjacent or visibly
  connected; the reader does not perform the join mentally.
- **Resume:** headings, labels, and visible state let the reader look away and
  return without rebuilding context.
- **Subtraction:** prose repeated by a visual, label, table, or state marker is
  removed.
- **Literal reading:** the title and first sentence remain accurate when read
  without charitable interpretation, domain familiarity, or marketing context.

If a check fails, change the representation before adding explanation. Minimal
cognitive friction does not mean deleting necessary information or hiding the
primary path behind interaction.

Choose the visual posture from audience, domain, and reuse context. Default to restrained presentation design unless the material calls for a stronger register:

- high contrast, readable type, stable spacing, and 8px-or-less radii;
- structured information, not decorative noise;
- color used to encode status, priority, confidence, risk, or category;
- cards only for real units of information, not nested decoration;
- responsive layout that remains useful on narrow screens.

Before styling, read
[`references/visual-taste.md`](references/visual-taste.md). Choose its five art
direction decisions and apply its Taste Check. Restrained presentation is an
explicit visual-system choice, not a bypass. Use the examples as mechanics,
not templates to copy.

## Boundaries

Use a different owner when the task is not a presentation artifact:

- `teach` owns stateful learning workspaces, missions, lessons, references, and learning records.
- `impeccable` owns production frontend/UI implementation and design critique.
- `writing-great-skills` owns skill architecture, invocation, no-ops, and skill text quality.
- `agents-md-steward` owns AGENTS.md, CLAUDE.md, CODEX.md, and repo instruction networks.
- An available inline-visualization surface owns one compact relationship that
  does not need durable reuse.
- Plain Markdown is better for source-of-truth repo docs, issue bodies, specs, policies, and small answers.

## Format Decision

Create a presentation artifact when at least one is true:

- the output is primarily for human consumption, decision, learning, review, or action;
- Markdown would become a wall of text or lose important relationships;
- the user needs side-by-side comparison, visual hierarchy, progressive disclosure, or spatial structure;
- the artifact benefits from tabs, cards, filters, collapsibles, diagrams, timelines, checklists, charts, preset matrices, or copy/export controls;
- the work synthesizes research, options, tradeoffs, evidence, or next actions;
- the user needs a durable surface to revisit later.

Use an available inline visual instead when one compact relationship is enough
and the result does not need to be revisited. Do not create a durable file merely
because a diagram could exist.

Keep Markdown when:

- the artifact is a source-of-truth repo doc, issue body, policy, spec, or agent-facing context file;
- the user needs easy line-level editing or reviewable diffs;
- the user asked for an ordinary summary, answer, or explanation rather than a durable artifact;
- a short answer or simple table is enough;
- HTML generation and verification would add more friction than value.

If both are useful, keep Markdown as the editable source and create HTML as the presentation/action surface.

## Externalize the Operational Model

Before choosing components or styling, extract only the structure the reader
would otherwise have to hold mentally:

- **sources:** inputs, actors, prerequisites, files, facts, or resources;
- **operations:** actions and the exact sources or states they affect;
- **states:** meaningful intermediate and final conditions;
- **edges:** order, dependency, flow, ownership, or containment;
- **control:** choices, conditions, loops, joins, and stopping rules;
- **proof:** the observable result or verification.

Choose one primary visual form based on the hardest relationship:

| Relationship | Primary form |
|---|---|
| Exact mappings or repeated-field comparison | Table |
| Inputs transformed separately and later combined | Merge lanes or converging flow |
| Conditions leading to different outcomes | Decision tree |
| State changing across events | State diagram or timeline |
| Parallel work divided by owner | Swimlanes with an explicit join |
| Ownership, nesting, or containment | Tree or nested map |
| Components with several dependencies | Dependency graph |
| Physical or interface placement | Wireframe |

Place sources where they enter. Make each operation's scope visible. Name
intermediate states when later work depends on them. Show branches, convergence,
parallel work, loops, and exit conditions directly. Replace or define unfamiliar
action labels at their point of use. End with a concrete result and observable
completion checks.

Delete prose that merely narrates the geometry, decorative nodes, obvious
legends, and duplicate visuals. Combine forms only when each answers a distinct
question.

When topology is the hard part, read
[`references/spatial-grammar.md`](references/spatial-grammar.md). Inspect its
companion SVG when the current harness can read local images; the text
descriptions are the portable fallback.

## Build And Verification

After choosing the artifact's primary relationship, read
[`references/artifact-patterns.md`](references/artifact-patterns.md) for the
smallest matching shape, build rules, interaction/export patterns, and browser
proof. For repeated full-output comparison, read
[`references/comparison-workspace.md`](references/comparison-workspace.md)
directly.

## Delivery

Return:

- a link to the generated artifact file;
- one sentence describing what it is for;
- verification performed or skipped;
- the source Markdown/context file if one was also created or updated.

Keep the final answer short. Do not make the final answer a second copy of the artifact.
