---
name: impeccable
description: Design, critique, polish, or rework a frontend interface -- websites, landing pages, dashboards, product UI, components, forms, onboarding, or empty states. Use for UX, visual hierarchy, accessibility, performance, typography, layout, color, and motion review; making bland designs bolder or loud ones quieter; live browser iteration on UI; or ambitious visual effects. Not for backend-only or non-UI tasks.
---

Design and iterate real frontend interfaces with explicit UX choices, implementation, and browser proof where visual behavior matters.

## Setup

You MUST do these steps before proceeding:

1. Run `node /Users/jstar/.agents/skills/impeccable/scripts/context.mjs` once per session. If you've already seen its output in this conversation, do not re-run it. The script either prints the project's PRODUCT.md (and DESIGN.md when present) as a markdown block, or tells you it's missing. Follow whatever it prints. **If it reports `NO_PRODUCT_MD`, use `reference/init.md` for build/shape/document/setup work. For a bounded critique, audit, polish, or one-off UI review, continue from the user-named surface and existing code evidence instead of blocking on setup.** If the output ends with an `UPDATE_AVAILABLE` directive, ask the user once about updating, then continue. It never blocks the current task.
2. If the user invoked a sub-command (`craft`, `shape`, `audit`, `polish`, ...), you MUST read `reference/<command>.md` next. Non-optional. The reference defines the command's flow; without it you will skip steps the user expects.
3. Familiarize yourself with any existing design system, conventions, and components in the code. Read at least one project file (CSS / tokens / theme / a representative component or page). **Required even when you've loaded a sub-command reference in step 2.** Don't reinvent the wheel; use what's there when it works, branch out when the UX wins.
4. Read the matching register reference. **This is non-optional; skipping it produces generic output.** If the project is marketing, a landing page, a campaign, long-form content, or a portfolio (design IS the product), read `reference/brand.md`. If it is app UI, admin, a dashboard, or a tool (design SERVES the product), read `reference/product.md`. Pick by first match: (1) task cue ("landing page" vs "dashboard"); (2) surface in focus (the page, file, or route being worked on); (3) `register` field in PRODUCT.md.
5. **If the project is brand-new (no existing CSS tokens / theme / committed brand colors found in step 3)**, run `node /Users/jstar/.agents/skills/impeccable/scripts/palette.mjs` to receive a brand seed color and composition guidance. This is the anchor for your primary brand color. Compose the rest of the palette (bg, surface, ink, accent, muted) around it per the script's instructions. Use OKLCH throughout. **Skip this step only if step 3 found committed brand colors in existing tokens; in that case identity-preservation wins.**
6. Before writing or judging UI code for `craft`, `critique`, `audit`, `polish`, `bolder`, `quieter`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`, `clarify`, `adapt`, `optimize`, or a general design request, read `reference/quality-gates.md`. Skip it for pure routing/menu, `pin`, `unpin`, `init`, and `document` work unless visual judgment is needed.

## Design guidance

Make the interface coherent with the product, audience, and existing design system. Prefer working implementation over mockup prose. Verify the result with the browser when layout, interaction, responsiveness, animation, or visual polish is part of the task.

Use the smallest intervention that fixes the user-visible problem: copy, spacing, hierarchy, color, state handling, or interaction before broader redesign. When the change is a critique rather than an edit, lead with ranked findings and concrete next actions.

Detailed visual quality checks live in `reference/quality-gates.md`; load that file when setup step 6 applies.

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

1. **No argument**: the user is asking "what should I do?" Make the menu context-aware instead of static. Setup has already run `context.mjs`; if that reported `NO_PRODUCT_MD`, recommend `init` for setup work and otherwise use current code evidence to suggest bounded review or polish commands. Otherwise run `node /Users/jstar/.agents/skills/impeccable/scripts/context-signals.mjs` once and read its JSON, then lead with the **2-3 highest-value next commands**, each with a one-line reason pulled from the signals, followed by the full menu (the table above, grouped by category). **Never auto-run a command; the recommendation is a suggestion the user confirms.**

   Reason over the signals; there is no score to obey:
   - `setup.hasDesign` false while `setup.hasCode` true → `document` (capture the visual system).
   - `critique.latest` is `null` → the project has never been critiqued; for a set-up project with a real surface, offering `$impeccable critique <surface>` is a strong default.
   - `critique.latest` with a low `score` or non-zero `p0` / `p1` → `polish` (it reads that snapshot as its backlog), or re-run `critique` if the snapshot looks stale.
   - `git.changedFiles` pointing at one surface → scope `audit` or `polish` to those files specifically, naming them.
   - `devServer.running` true → `live` is available for in-browser iteration; if false, don't lead with `live`.
   - Otherwise group by intent exactly as init's "Recommend starting points" step does (build new / improve what's there / iterate visually), tailored to `setup.register`.

   **If `scan.targets` is non-empty, run `node /Users/jstar/.agents/skills/impeccable/scripts/detect.mjs --json <scan.targets joined by spaces>` once** (the bundled detector over local files: no network, no npx). `scan.via` tells you what they are: `git-changes` (the markup/style files in your dirty tree, the most relevant set), `source-dir` (e.g. `src`, `app`), `html`, or `root`. Fold the hits into your picks: many quality / contrast hits → `audit` or `polish`; a specific slop family → the matching command (gradient text or eyebrows → `quieter` / `typeset`, flat or gray palette → `colorize`, and so on). It's a real, current signal that beats guessing. If detect errors or the tree is large and slow, skip it and recommend the user run `audit` themselves; never block the suggestion on it.

   Keep it to 2-3 pointed picks with the exact command to type. The menu stays the fallback; the recommendation is the lede.
2. **First word matches a command**: load its reference file and follow its instructions. Everything after the command name is the target.
3. **First word doesn't match, but the intent clearly maps to one command** (e.g. "fix the spacing" → `layout`, "rewrite this error message" → `clarify`, "the colors feel flat" → `colorize`): load that command's reference and proceed as if invoked. If two commands could fit, ask once which.
4. **No clear command match**: general design invocation. Apply the setup steps, the General rules, and the loaded register reference, using the full argument as context.

Setup (context gathering, register) is already loaded by then; sub-commands don't re-invoke `$impeccable`.

If the first word is `craft`, setup still runs first, but [reference/craft.md](reference/craft.md) owns the rest of the flow. If setup invokes `init` as a blocker, finish init, refresh context, then resume the original command and target.

`teach` is a deprecated impeccable sub-command alias for `init`: if the user types `$impeccable teach`, load [reference/init.md](reference/init.md) and proceed as if they ran `$impeccable init`. Do not intercept the separate `$teach` skill.

## Pin / Unpin

**Pin** creates a standalone shortcut so `$<command>` invokes `$impeccable <command>` directly. **Unpin** removes it. The script writes to every harness directory present in the project.

```bash
node /Users/jstar/.agents/skills/impeccable/scripts/pin.mjs <pin|unpin> <command>
```

Valid `<command>` is any command from the table above. Report the script's result concisely. Confirm the new shortcut on success, relay stderr verbatim on error.
