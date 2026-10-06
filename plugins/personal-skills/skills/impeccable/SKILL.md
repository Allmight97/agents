---
name: impeccable
description: "Design, build, critique, or refine frontend interfaces. Use for UI layout, typography, color, accessibility, interaction, motion, and browser-based visual iteration; backend-only work is outside scope."
---

Design and iterate real frontend interfaces with explicit UX choices, implementation, and browser proof where visual behavior matters.

`<impeccable-skill-dir>` means the absolute directory containing the exact copy
of this `SKILL.md` loaded for the current invocation. Resolve it from the skill
location supplied by the harness; if the harness supplies the `SKILL.md` path,
use its parent directory. Resolve it once, then replace the placeholder inside
each quoted script path below and in the command references. If the loaded skill
location is unavailable, report bundled scripts as unavailable and continue any
work that does not depend on them; do not substitute an arbitrary copy.

## Route And Gather Context

Resolve the requested command before running setup. For `pin`/`unpin`, go
straight to their section. For a bare invocation, use the menu routing below.
For design work:

1. Load the matching command reference. Keep its scope aligned with the request;
   an audit-and-fix request includes authorized remediation.
2. Run `node "<impeccable-skill-dir>/scripts/context.mjs"` when project context has
   not been read for this project. Treat its output as project evidence. Missing
   PRODUCT.md does not block a task supported by the brief and existing code;
   `init` owns explicitly requested context setup.
3. Inspect the relevant design tokens, components, and surface. Preserve stated
   brand choices, including user-provided colors and references.
4. For broad visual design, read `reference/brand.md` for marketing/editorial
   surfaces or `reference/product.md` for app/tool interfaces. For a narrow copy
   or spacing change, load only guidance that affects it.
5. For visual judgment, read `reference/quality-gates.md`. Use
   `scripts/palette.mjs` only when choosing a new palette and a generated seed
   would help; it does not override supplied identity or a chosen palette.

## Design guidance

Make the interface coherent with the product, audience, and existing design system. Prefer working implementation over mockup prose. Verify the result with the browser when layout, interaction, responsiveness, animation, or visual polish is part of the task.

For a bounded fix, use the smallest intervention that resolves the user-visible problem: copy, spacing, hierarchy, color, state handling, or interaction before broader redesign. For build, redesign, or exploration commands, the requested scope sets the size of the change. When the change is a critique rather than an edit, lead with ranked findings and concrete next actions.

Detailed visual quality checks live in `reference/quality-gates.md`; load it when
judging layout, styling, interaction, or motion.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `craft [feature]` | Build | Shape, then build a feature end-to-end | [reference/craft.md](reference/craft.md) |
| `shape [feature]` | Build | Plan UX/UI before writing code | [reference/shape.md](reference/shape.md) |
| `init` | Build | Set up project context: PRODUCT.md, DESIGN.md, live config, next steps | [reference/init.md](reference/init.md) |
| `document` | Build | Generate DESIGN.md from existing project code | [reference/document.md](reference/document.md) |
| `extract [target]` | Build | Pull reusable tokens and components into design system | [reference/extract.md](reference/extract.md) |
| `critique [target]` | Evaluate | UX design review with heuristic scoring | [reference/critique.md](reference/critique.md) |
| `audit [target]` | Evaluate | Technical quality checks (a11y, perf, responsive) | [reference/audit.md](reference/audit.md) |
| `polish [target]` | Refine | Final quality pass before shipping | [reference/polish.md](reference/polish.md) |
| `bolder [target]` | Refine | Amplify safe or bland designs | [reference/bolder.md](reference/bolder.md) |
| `quieter [target]` | Refine | Tone down aggressive or overstimulating designs | [reference/quieter.md](reference/quieter.md) |
| `distill [target]` | Refine | Strip to essence, remove complexity | [reference/distill.md](reference/distill.md) |
| `harden [target]` | Refine | Production-ready: errors, i18n, edge cases | [reference/harden.md](reference/harden.md) |
| `onboard [target]` | Refine | Design first-run flows, empty states, activation | [reference/onboard.md](reference/onboard.md) |
| `animate [target]` | Enhance | Add purposeful animations and motion | [reference/animate.md](reference/animate.md) |
| `colorize [target]` | Enhance | Add strategic color to monochromatic UIs | [reference/colorize.md](reference/colorize.md) |
| `typeset [target]` | Enhance | Improve typography hierarchy and fonts | [reference/typeset.md](reference/typeset.md) |
| `layout [target]` | Enhance | Fix spacing, rhythm, and visual hierarchy | [reference/layout.md](reference/layout.md) |
| `delight [target]` | Enhance | Add personality and memorable touches | [reference/delight.md](reference/delight.md) |
| `overdrive [target]` | Enhance | Push past conventional limits | [reference/overdrive.md](reference/overdrive.md) |
| `clarify [target]` | Fix | Improve UX copy, labels, and error messages | [reference/clarify.md](reference/clarify.md) |
| `adapt [target]` | Fix | Adapt for different devices and screen sizes | [reference/adapt.md](reference/adapt.md) |
| `optimize [target]` | Fix | Diagnose and fix UI performance | [reference/optimize.md](reference/optimize.md) |
| `live` | Iterate | Visual variant mode: pick elements in the browser, generate alternatives | [reference/live.md](reference/live.md) |

Plus two management commands: `pin <command>` and `unpin <command>`, detailed below.

### Routing rules

1. **No argument**: offer 2-3 commands relevant to the current task or project,
   with a short reason. If repository context is needed, run `context.mjs` and
   `context-signals.mjs` once. Use a narrow `detect.mjs --json <target>` scan only
   when it could change the recommendation. Show the full menu when requested.
   A bare invocation does not authorize running a suggested design command.
2. **First word matches a command**: load its reference file and follow its instructions. Everything after the command name is the target.
3. **First word doesn't match, but the intent clearly maps to one command** (e.g. "fix the spacing" → `layout`, "rewrite this error message" → `clarify`, "the colors feel flat" → `colorize`): load that command's reference and proceed as if invoked. If adjacent commands fit, choose the narrowest combination that satisfies the
   request; ask only when the choice changes the intended result.
4. **No clear command match**: general design invocation. Use the context and design guidance above, with the full request as scope.

Sub-commands use the gathered context without re-invoking `$impeccable`.
[reference/craft.md](reference/craft.md) owns implementation and optional visual
exploration. An existing brief can supply the context needed to proceed.

`teach` is a deprecated impeccable sub-command alias for `init`: if the user types `$impeccable teach`, load [reference/init.md](reference/init.md) and proceed as if they ran `$impeccable init`.

## Pin / Unpin

**Pin** creates a standalone shortcut so `$<command>` invokes `$impeccable <command>` directly. **Unpin** removes it. The script writes to every harness directory present in the project.

```bash
node "<impeccable-skill-dir>/scripts/pin.mjs" <pin|unpin> <command>
```

Valid `<command>` is any command from the table above. Report the script's result concisely. Confirm the new shortcut on success, relay stderr verbatim on error.
