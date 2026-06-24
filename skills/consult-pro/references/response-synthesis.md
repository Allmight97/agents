# Pro Response Synthesis

## Validation Pass

Treat every Pro finding as a claim:

1. Locate the cited file, script, doc, branch, issue, or release artifact.
2. Check whether the claim is still true on the current local branch.
3. Separate evidence-backed defects from preference, style, or speculative
   cleanup.
4. Identify whether the item is already fixed, superseded, or made irrelevant by
   a purge.

## Disposition Rules

- **Adopt:** the finding is true, in scope, and the fix has clear ROI.
- **Purge:** the surface is low-value or historically accidental, and deletion is
  cleaner than repair.
- **Defer:** the finding is true but not technically in scope; record owner,
  trigger, and reason. Do not defer for politeness.
- **Reject:** the finding is false, already handled, or conflicts with a stronger
  repo invariant.

## Work Block Shape

When turning a Pro response into work:

- Group like-kind items under one owner.
- Prefer deletion over redesign when the value case is weak.
- Preserve high-value diagnostics only when the keeper reason is one sentence
  and concrete.
- Keep tests owner-scoped and fast unless the change genuinely crosses runtime,
  release, or data-safety boundaries.
- End with a follow-up prompt only when Pro can resolve a remaining decision
  better than local repo inspection can.

## Final Report Shape

Report:

- What Pro found that was valid.
- What was adopted, purged, deferred, or rejected.
- What local verification was run.
- What remains, with the reason it remains.
- Whether another Pro pass is worth the latency.
