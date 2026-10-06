# Critique

Assess the requested interface and recommend concrete improvements. A
critique-only request leaves implementation unchanged. A critique-and-fix
request continues through authorized corrections after the assessment.

## Establish The Target

Resolve the surface to its source path and/or live URL. Read the relevant
product/design context and inspect the actual user path. Read an existing
`.impeccable/critique/ignore.md` when it records deliberately excluded findings;
use it within the current request's scope.

## Assess Design And Gather Evidence

First record a design assessment from source and available browser inspection:
hierarchy, information flow, visual character, typography, color, interaction,
accessibility, states, and copy. Identify specific effects on the user's task.
Aesthetic sameness can support a design finding; it is not proof of a defect by
itself.

Then use the bundled detector on supported markup files or directories:

```bash
node "<impeccable-skill-dir>/scripts/detect.mjs" --json <target>
```

Exit 0 means no detector findings; 2 means findings. URLs and CSS-only files are
not CLI targets. Inspect viewable targets with available browser tools. If a
detector overlay would help, read [live.md](live.md) for supported injection and
server cleanup. An overlay is optional; claim it only after observing it render.

Record visual judgment before detector findings to reduce anchoring. Work
sequentially by default. Use independent agents only when requested or already
authorized and useful, with bounded briefs and separate task tabs. Follow the
live browser and agent APIs; do not require a specific role or unsupported
mutation capability. Report missing tooling as an evidence limit.

For a comprehensive scored review or an audience walkthrough, read
[critique-rubric.md](critique-rubric.md). Use its heuristic scores consistently
when comparing runs; omit unsupported numeric judgments for a narrow review.

## Synthesize

Lead with the strongest finding and recommended action. Reconcile design and
detector evidence, remove false positives, and report only supported issues.
Each issue needs a concrete location or UI element, triggering state, user
impact, and credible correction. Rank by impact:

- **P0:** blocks the primary task.
- **P1:** materially impairs usability or access.
- **P2:** significant friction with a usable path remaining.
- **P3:** bounded refinement; omit pure preferences unless requested.

Name strengths when they help preserve useful design choices. Include the
actual proof, unresolved limitations, and cleanup of resources the task started.
A clean detector does not prove a good experience. Ask only about choices that
change the next action; do not force a follow-up interview after every critique.

## Retain A Snapshot When Useful

When the user requests a retained critique or the project already uses this
backlog, use the existing helper. Honor read-only or chat-only constraints.

1. Resolve a stable slug:
   `node "<impeccable-skill-dir>/scripts/critique-storage.mjs" slug "<path-or-url>"`.
   Skip persistence if the target cannot be resolved.
2. Write the finalized report body to OS temp. Keep transient run status out of
   the body so the archive does not describe its own persistence as pending.
3. Pass JSON metadata through `IMPECCABLE_CRITIQUE_META` with `target`,
   `p0_count`, `p1_count`, and `total_score` only when a full scored assessment was
   performed. Run:
   `node "<impeccable-skill-dir>/scripts/critique-storage.mjs" write "<slug>" "<body-file>"`.
4. Remove the temporary body after the write attempt. Report the written path
   or a concrete persistence failure without blocking the critique itself.
5. For comparable scored runs, inspect:
   `node "<impeccable-skill-dir>/scripts/critique-storage.mjs" trend "<slug>" 5`.
   Compare only the same scope and rubric; label missing scores as unscored.

Recommend a specific next correction or command. Continue implementation when
already authorized, then verify the changed user path.
