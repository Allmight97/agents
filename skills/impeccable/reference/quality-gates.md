# Quality Gates

Use these checks when writing or judging UI code.

## Color

- Verify contrast: body text needs 4.5:1, large text needs 3:1, and placeholder text needs 4.5:1.
- Gray text on colored backgrounds usually washes out. Use a darker shade of the background hue or a transparency of the foreground color.
- For new projects, choose a color strategy before colors: restrained, committed, full palette, or drenched.
- Do not default to cream/sand/beige, dark tool UI, or category-obvious palettes unless the product context actually earns them.
- Prefer OKLCH for new palettes.

## Typography

- Keep body line length around 65-75ch.
- Create hierarchy through scale and weight contrast. Avoid flat scales.
- Use no more than three font families; one well-tuned family often wins.
- Avoid all-caps body copy. Reserve uppercase for short labels, badges, or a deliberate brand system.
- Hero/display heading `clamp()` max should usually stay at or below `6rem`.
- Display heading letter spacing should not go tighter than `-0.04em`.
- Use `text-wrap: balance` on headings and `text-wrap: pretty` on long prose when supported.

## Layout

- Use cards only for real grouped units of information. Avoid nested cards.
- Use flexbox for one-dimensional flow and grid for two-dimensional layout.
- For responsive grids without breakpoints, prefer `repeat(auto-fit, minmax(280px, 1fr))`.
- Define a semantic z-index scale for dropdowns, sticky regions, modals, toasts, and tooltips.
- Test long labels and headings at narrow widths; text must not overflow its container.

## Motion

- Motion should clarify state, hierarchy, attention, or spatial change.
- Do not animate layout properties unless there is a specific reason.
- Provide `prefers-reduced-motion` behavior for every animation.
- Reveal animations must enhance already-visible content; do not ship content that depends on a transition class to become visible.

## Interaction

- Dropdowns inside `overflow: hidden` or `overflow: auto` containers will be clipped. Use native `dialog`, the popover API, fixed positioning, or a portal when the menu must escape.
- Buttons need verb-object labels when the action is not obvious from an icon.
- Link text needs standalone meaning.

## Copy

- Remove restated headings and intros that repeat the title.
- Avoid marketing filler: streamline, empower, supercharge, leverage, unleash, transform, seamless, world-class, enterprise-grade, next-generation, cutting-edge, game-changer, mission-critical.
- Avoid repeated aphoristic cadence: one serious sentence followed by a punchy short negation across multiple sections.
- Avoid "X theater", "actually X", and "not just X, it is Y" copy patterns.

## Refuse And Rewrite

Rewrite these patterns when they appear:

- Colored side-stripe borders on cards, list items, callouts, or alerts.
- Gradient text.
- Decorative glassmorphism.
- Hero metric templates: big number, small label, supporting stats, gradient accent.
- Endless identical icon-heading-text card grids.
- Tiny uppercase tracked eyebrows above every section.
- Numbered section markers unless the content is actually ordered.
- `border: 1px solid ...` plus a wide decorative shadow on the same element.
- `border-radius: 32px+` on cards, sections, or inputs.
- Hand-drawn or sketchy SVG illustrations as a fallback for real assets.
- Decorative repeating stripe backgrounds.

## Reflex Check

Before shipping a new visual direction, ask two questions:

- Could someone guess the theme and palette from the category alone?
- Could someone guess the aesthetic family from the category plus the obvious anti-reference?

If either answer is yes, revise the scene, palette, typography, or composition until the result is more specific to this product.
