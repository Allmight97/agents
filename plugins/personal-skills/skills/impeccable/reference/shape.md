Shape the UX and UI for a feature before any code is written. This command produces a **design brief**: a structured artifact that guides implementation through discovery, not guesswork.

**Scope**: Design planning only. This command does NOT write code. It produces the thinking that makes code good.

**Output**: A design brief that can be handed off to $impeccable craft, or directly to $impeccable for freeform implementation. When visual direction probes are used, the images are supporting artifacts, not the primary output.

## Discover The Missing Decisions

Use the request, existing product/design context, and relevant code to establish
purpose, audience, content, scope, and constraints. Ask about unresolved choices
that materially change the design. Keep each round manageable and avoid asking
again about supplied or settled answers.

Make design recommendations as evidence emerges. A sparse brief may need an
interview; a clear brief can be shaped directly. The prompts below are a menu of
decision areas, not a questionnaire that every task must complete.

### Purpose & Context
- What is this feature for? What problem does it solve?
- Who specifically will use it? (Not "users"; be specific: role, context, frequency)
- What does success look like? How will you know this feature is working?
- What's the user's state of mind when they reach this feature? (Rushed? Exploring? Anxious? Focused?)

### Content & Data
- What content or data does this feature display or collect?
- What are the realistic ranges? (Minimum, typical, maximum, e.g., 0 items, 5 items, 500 items)
- What are the edge cases? (Empty state, error state, first-time use, power user)
- Is any content dynamic? What changes and how often?
- What visual assets are real content here? Note required images, product shots, illustrations, maps, textures, diagrams, generated objects, or existing project assets.

### Design Direction

Clarify the visual decisions that matter. Use supplied identity and references;
ask only about consequential gaps.

- **Color strategy for this surface.** Pick one: Restrained / Committed / Full palette / Drenched. Can override the project default if the surface earns it (e.g. a drenched hero inside an otherwise Restrained product).
- **Theme via scene sentence.** Write one sentence of physical context for this surface: who uses it, where, under what ambient light, in what mood. The sentence forces dark vs light. If it doesn't, add detail until it does.
- **Two or three named anchor references.** Specific products, brands, objects. Not adjectives like "modern" or "clean."

### Scope

Infer scope from the request. Ask when ambiguity between a sketch, prototype,
and production feature would change the work.

- **Fidelity.** Sketch / mid-fi / high-fi / production-ready?
- **Breadth.** One screen / a flow / a whole surface?
- **Interactivity.** Static visual / interactive prototype / shipped-quality component?
- **Time intent.** Quick exploration, or polish until it ships?

Scope answers are task-scoped. Don't write them to PRODUCT.md or DESIGN.md; carry them through the design brief only.

### Constraints
- Are there technical constraints? (Framework, performance budget, browser support)
- Are there content constraints? (Localization, dynamic text length, user-generated content)
- Mobile/responsive requirements?
- Accessibility requirements beyond WCAG AA?

### Anti-Goals
- What should this NOT be? What would be a wrong direction?
- What's the biggest risk of getting this wrong?

## Visual Exploration

Use generated probes when requested or when a visual comparison would resolve
an important uncertainty. Read [codex.md](codex.md) for the palette/mock/asset
handoff. Tool availability alone does not make probes mandatory. Supplied
references, sketches, or a clear design recommendation may be sufficient.

## Design Brief

Present the intended behavior, visual direction, scope, key states, interactions,
and content requirements. Use a compact brief for a clear feature and the fuller
structure below for a complex flow. Preserve meaningful unresolved choices;
a recommendation is not the same as a user-owned decision being settled.

A standalone shape request ends with the brief and any needed decision. If the
user already authorized implementation or delegated design choices, continue
through [craft.md](craft.md) once action-changing decisions are settled. Honor
explicit requests to review the brief before coding.

### Brief Structure

**1. Feature Summary** (2-3 sentences)
What this is, who it's for, what it needs to accomplish.

**2. Primary User Action**
The single most important thing a user should do or understand here.

**3. Design Direction**
Relevant color strategy, setting, and concrete visual references when available. Reference PRODUCT.md and DESIGN.md where they already answer, and note any per-surface overrides.

If probes were used, name the chosen direction and what they clarified.

**4. Scope**
Fidelity, breadth, interactivity, and time intent from the Scope section of the interview. Task-scoped; these don't persist beyond the brief.

**5. Layout Strategy**
High-level spatial approach: what gets emphasis, what's secondary, how information flows. Describe the visual hierarchy and rhythm, not specific CSS.

**6. Key States**
List every state the feature needs: default, empty, loading, error, success, edge cases. For each, note what the user needs to see and feel.

**7. Interaction Model**
How users interact with this feature. What happens on click, hover, scroll? What feedback do they get? What's the flow from entry to completion?

**8. Content Requirements**
What copy, labels, empty state messages, error messages, and microcopy are needed. Note any dynamic content and its realistic ranges. For image-led surfaces, also list the required image/media roles and their likely source (project asset, generated raster, semantic SVG/CSS, canvas/WebGL, icon library, or accepted omission).

**9. Recommended References**
Based on the brief, list which impeccable reference files would be most valuable during implementation (e.g., layout.md for complex layouts, animate.md for animated features, interaction-design.md for form-heavy features, typeset.md for typography-driven pages, colorize.md for color-led brands).

**10. Open Questions**
Only decisions or evidence gaps that materially affect the next action. Use
delegated judgment for routine choices and identify user-owned decisions.
