# Craft

Build the requested feature with coherent design, working interactions, and
visual proof. Use the existing framework, build pipeline, component patterns,
and icon set. For a new project, choose a proportionate stack from the brief;
ask when a material integration or product choice depends on the answer.

## Establish Direction

Use the user's brief, references, existing identity, and project context. Name
what will be built and any consequential assumptions. PRODUCT.md is useful
context, not a prerequisite for implementation.

When the user requests design exploration, or unresolved choices materially
change the result, use [shape.md](shape.md). A clear brief or delegated design
judgment is sufficient to proceed; do not repeat settled questions.

Use [codex.md](codex.md) when generated mockups or raster assets would help, or
when the user requests them. Tool availability alone does not require a palette
image, mockup round, or an approval ceremony. Preserve any checkpoints the user
requested; otherwise exercise the design judgment they delegated.

Load layout, typography, interaction, motion, color, responsive, or copy
references only when the feature needs their detailed guidance. The shared
quality bar is in [quality-gates.md](quality-gates.md).

## Implement The Direction

Treat an accepted visual direction as a contract for composition, hierarchy,
density, imagery, and distinctive motifs. Translate it into semantic UI and
working state; keep text and controls accessible instead of rasterizing them.

- Use real supplied content and verified asset sources. Clearly label sample
  data when the requested prototype needs it.
- Implement the relevant keyboard, pointer, focus, loading, error, empty, and
  overflow behavior for the feature. Verify accessible names and control roles.
- Keep image-driven concepts image-driven; use real or generated imagery where
  the subject depends on it. CSS decoration cannot replace required content.
- Edit source and run the actual project pipeline. Put consumed assets in the
  project and verify their paths, resolution, crop, and responsive behavior.
- Add motion where it helps, respect reduced motion, and check expensive effects
  in the browser. Preserve the requested scope when polishing.

If new evidence conflicts with a consequential design choice, resolve it before
implementing dependent work. Routine implementation details do not require
renewed approval.

## Verify And Finish

Inspect the running result at relevant widths and states. Read screenshots you
capture; for long pages, inspect the main sections at usable resolution. Compare
the actual result with the brief or accepted mock, fix material gaps, and run
required build and code checks.

Report the implemented result, visual and functional checks, and remaining
limitations. If browser access is unavailable, distinguish static/build proof
from unverified appearance or interactions. Continue any already-authorized
next step through its owning workflow.
