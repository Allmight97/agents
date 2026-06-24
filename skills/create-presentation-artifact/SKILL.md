---
name: create-presentation-artifact
description: Create durable user-facing presentation artifacts, usually self-contained HTML, for research synthesis, decision support, planning, code understanding, reviews, dashboards, and briefing surfaces. Use when the user asks for an artifact, dashboard, visual synthesis, decision aid, interactive checklist, or a revisitable surface where Markdown would lose important relationships. Do not use for ordinary summaries, repo source-of-truth docs, production UI implementation, stateful teaching workspaces, skill edits, or agent guidance.
---

# Create Presentation Artifact

Create polished user-facing artifacts for decisions, reviews, plans, research,
learning, and handoff surfaces. The usual output is a single-file HTML artifact.

## Outcome Standard

Build artifacts that reduce decision friction.

Lead with the useful answer, then make the supporting detail easy to scan. A strong artifact should feel like a compact briefing surface: recommendation first, tradeoffs visible, uncertainty labeled, sources/currency included, and the next action obvious.

Choose the visual posture from audience, domain, and reuse context. Default to restrained presentation design unless the material calls for a stronger register:

- high contrast, readable type, stable spacing, and 8px-or-less radii;
- structured information, not decorative noise;
- color used to encode status, priority, confidence, risk, or category;
- cards only for real units of information, not nested decoration;
- responsive layout that remains useful on narrow screens.

## Boundaries

Use a different owner when the task is not a presentation artifact:

- `teach` owns stateful learning workspaces, missions, lessons, references, and learning records.
- `impeccable` owns production frontend/UI implementation and design critique.
- `writing-great-skills` owns skill architecture, invocation, no-ops, and skill text quality.
- `agents-md-steward` owns AGENTS.md, CLAUDE.md, CODEX.md, and repo instruction networks.
- Plain Markdown is better for source-of-truth repo docs, issue bodies, specs, policies, and small answers.

## Format Decision

Create a presentation artifact when at least one is true:

- the output is primarily for human consumption, decision, learning, review, or action;
- Markdown would become a wall of text or lose important relationships;
- the user needs side-by-side comparison, visual hierarchy, progressive disclosure, or spatial structure;
- the artifact benefits from tabs, cards, filters, collapsibles, diagrams, timelines, checklists, charts, preset matrices, or copy/export controls;
- the work synthesizes research, options, tradeoffs, evidence, or next actions;
- the user needs a durable surface to revisit later.

Keep Markdown when:

- the artifact is a source-of-truth repo doc, issue body, policy, spec, or agent-facing context file;
- the user needs easy line-level editing or reviewable diffs;
- the user asked for an ordinary summary, answer, or explanation rather than a durable artifact;
- a short answer or simple table is enough;
- HTML generation and verification would add more friction than value.

If both are useful, keep Markdown as the editable source and create HTML as the presentation/action surface.

## Artifact Shapes

Choose the smallest shape that fits the job:

- **Decision brief:** conclusion block, ranked options, tradeoff matrix, risks, next action.
- **Research synthesis:** TL;DR, source map, confidence labels, comparison cards, open questions.
- **Learning surface:** concept map, glossary, examples, gotchas, FAQ, progressive details.
- **Planning surface:** timeline, milestones, owners, decision log, risk table, handoff checklist.
- **Code understanding:** module map, call path, boundary labels, annotated findings, reviewer focus.
- **Review/report:** metric cards, finding list, severity chips, evidence links, action queue.
- **Interactive aid:** tabs, filters, toggles, checkboxes, sliders, copy/export actions.
- **Deck-like briefing:** full-width sections with navigation and keyboard-friendly flow when presentation is central.

## Build Rules

- Create one self-contained `.html` file unless the user asks otherwise.
- Put durable project-agnostic artifacts under `/Users/jstar/Library/Mobile Documents/iCloud~md~obsidian/Documents/Main Vault/Projects/Codex/Artifacts` unless the active project or user names a better artifact home.
- For project-specific artifacts, prefer a project subfolder under that artifact
  root, such as `/Users/jstar/Library/Mobile Documents/iCloud~md~obsidian/Documents/Main Vault/Projects/Codex/Artifacts/audiobook-boss` for
  Audiobook Boss.
- Do not place generated HTML companions in repo canon docs, active specs, or
  agent guidance unless the user explicitly asks for that repo-local
  artifact. Keep repository Markdown as the editable source when a repo doc is
  needed, and keep the presentation layer external by default.
- Inline CSS and small JavaScript. Avoid build steps and external dependencies unless clearly useful.
- Put the conclusion, recommendation, or key action at the top.
- Design for scanning first, detail second.
- Use progressive disclosure for dense material: tabs, details/summary, side nav, filters, or compact matrices.
- Use semantic HTML and accessible controls: real buttons, labels, headings, focus states, keyboard-friendly interactions.
- Use stable responsive layout: grids, tables with horizontal overflow, sticky nav where useful, mobile-friendly breakpoints.
- Include source links, evidence/currency notes, and explicit uncertainty boundaries when research is involved.
- Make data states visible: recommended, watchlist, blocked, risky, unknown, verified, stale, or pending review.
- Avoid repeating the artifact contents in the final response; let the artifact carry the detail.

## Presentation Patterns

Prefer patterns that clarify relationships:

- **Top summary:** one-sentence conclusion plus 2-4 key chips.
- **Recommendation cards:** ranked options with why/why not/status.
- **Comparison table:** stable columns for specs, costs, constraints, confidence, and fit.
- **Preset matrix:** practical modes, defaults, fallback modes, and when to use each.
- **Source/currency panel:** what is known, inferred, unverified, or awaiting review.
- **Action block:** next move, stop condition, and what evidence would change the decision.

For technical or research-heavy artifacts, separate:

- **Known:** directly sourced or verified.
- **Inferred:** reasoned from specs, tests, or system behavior.
- **Unverified:** needs review, hands-on testing, or current data.
- **Decision impact:** what changes if the uncertainty resolves one way or the other.

## Interaction and Export

Add interaction only when it reduces user friction.

Use:

- tabs for mutually exclusive sections;
- collapsibles for optional depth;
- filters/search for large lists;
- checkboxes for action tracking;
- sliders/toggles for tuning or comparison;
- copy/export buttons when the user may reuse decisions, prompts, notes, or checklists.

If the user can modify, select, triage, tune, or annotate inside the artifact, include an export path such as:

- `copy as markdown`;
- `copy JSON`;
- `copy prompt`;
- `copy checklist`;
- `download` only when useful.

The export should preserve the user's decisions so they can paste them back into an agent chat, an issue, a doc, or a repo.

## Browser Verification

Use browser verification for substantial or interactive artifacts.

Verify when any of these are true:

- JavaScript interaction is present;
- the artifact is more than a tiny static one-pager;
- it has tabs, filters, collapsibles, drag/drop, charts, diagrams, copy/export buttons, or responsive layout that affects usability;
- it is user-facing for an important decision, interview, presentation, or handoff;
- the user explicitly asks for verification.

Verification should include:

- open the artifact locally in the available browser tool when possible;
- if `file://` is blocked, use a temporary local HTTP server rooted at the artifact folder;
- check that the page is not blank;
- inspect desktop layout;
- exercise core interactions;
- check copy/export behavior if present;
- check mobile/narrow layout when responsiveness matters;
- stop any temporary server before final delivery.

For tiny static one-pagers with no interaction or visual sensitivity, browser verification may be skipped. If skipped, say so briefly.

## Delivery

Return:

- a link to the generated artifact file;
- one sentence describing what it is for;
- verification performed or skipped;
- the source Markdown/context file if one was also created or updated.

Keep the final answer short. Do not make the final answer a second copy of the artifact.
