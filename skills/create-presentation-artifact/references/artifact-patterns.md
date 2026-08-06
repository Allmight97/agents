# Artifact Patterns And Verification

Read this reference after choosing a durable presentation artifact. Select only
the shape, interaction, and proof needed for the reader's job.

## Artifact Shapes

- **Decision brief:** conclusion block, ranked options, tradeoff matrix, risks,
  next action.
- **Research synthesis:** TL;DR, source map, confidence labels, comparison cards,
  open questions.
- **Learning surface:** concept map, glossary, examples, gotchas, FAQ,
  progressive details.
- **Planning surface:** timeline, milestones, owners, decision log, risk table,
  handoff checklist.
- **Code understanding:** module map, call path, boundary labels, annotated
  findings, reviewer focus.
- **Review/report:** metric cards, finding list, severity chips, evidence links,
  action queue.
- **Interactive aid:** tabs, filters, toggles, checkboxes, sliders, copy/export
  actions.
- **Comparison workspace:** stable candidate controls, equal side-by-side frames,
  focused candidate views, and full-output access. Read
  [comparison-workspace.md](comparison-workspace.md) when complete outputs need
  repeated comparison.
- **Deck-like briefing:** full-width sections with navigation and keyboard flow
  when presentation is central.

## Build Rules

- Create one self-contained `.html` file unless the user asks otherwise.
- Put durable project-agnostic artifacts under
  `/Users/jstar/Library/Mobile Documents/iCloud~md~obsidian/Documents/Main Vault/Projects/Codex/Artifacts`
  unless the active project or user names a better home. Use a project subfolder
  for project-specific artifacts.
- Keep generated presentation layers outside repository canon, active specs, and
  agent guidance unless the user requests a repo-local artifact. Keep Markdown
  as the editable source when the repository needs one.
- Inline CSS and small JavaScript. Add dependencies only when they materially
  improve the result.
- Put the conclusion, recommendation, or key action at the top.
- Use semantic HTML, accessible controls, visible focus states, stable responsive
  layout, and horizontal overflow for wide tables.
- Include sources, evidence currency, and uncertainty boundaries for research.
- Expose meaningful data states such as verified, stale, blocked, risky, or
  pending review.

## Presentation Patterns

Use only patterns that clarify the material:

- **Top summary:** one-sentence conclusion plus two to four state chips.
- **Recommendation cards:** ranked options with why, why not, and status.
- **Comparison table:** stable columns for constraints, confidence, and fit.
- **Preset matrix:** practical modes, defaults, fallbacks, and selection rules.
- **Source panel:** what is known, inferred, unverified, or stale.
- **Action block:** next move, stop condition, and evidence that would change it.

For technical or research-heavy artifacts, distinguish **Known**, **Inferred**,
**Unverified**, and **Decision impact** when the distinction changes action.

## Interaction And Export

Add interaction only when it removes reader work:

- tabs for mutually exclusive sections;
- collapsibles for optional depth;
- filters or search for large lists;
- checkboxes for action tracking;
- sliders or toggles for tuning and comparison;
- copy/export controls when the user will reuse decisions, prompts, notes, or
  checklists.

When the reader can modify or select state, preserve it through an appropriate
copy-as-Markdown, JSON, prompt, checklist, or download path.

## Browser Verification

Verify substantial or interactive artifacts in the available browser. Use a
temporary local HTTP server when `file://` is blocked, and stop it afterward.

Check:

- the page renders and is not blank;
- desktop and relevant narrow layouts;
- core interactions;
- copy/export behavior when present;
- keyboard and focus behavior for interactive controls.

Tiny static one-pagers may skip browser verification when layout is not
decision-critical. Report that omission briefly.
