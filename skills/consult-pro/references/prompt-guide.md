# Pro Prompt Guide

## Construction Rules

Use this structure for substantial Pro consultations:

1. **Objective:** one concrete outcome, not a topic.
2. **Current truth:** repo, branch, SHA, PR/issue links, local state, and what
   was already done.
3. **Problem frame:** why the decision matters, what friction or risk is being
   investigated, and what the owner will do with the answer.
4. **Evidence routes:** where Pro should inspect source, docs, diffs, linked PRs,
   or pasted artifacts. If Pro has GitHub connector access, name the remote and
   branch explicitly.
5. **Constraints:** what not to spend time on, what cannot be changed, and what
   kinds of recommendations are off-target.
6. **Output contract:** requested sections, severity ordering, file/line
   references, action categories, or merge/release recommendation.
7. **Convergence instruction:** ask Pro to help reach an end state. Avoid
   prompts that invite perpetual critique without decision pressure.

## What Works Well

- Give Pro a dense, self-contained problem brief with concrete artifacts.
- Invite harsh scrutiny where the owner wants it, especially for repo infra,
  testing friction, release workflows, architecture boundaries, and hidden
  maintenance cost.
- State user preferences when they change the decision: e.g. "nothing is sacred"
  or "minimal churn means fewer correction loops, not preserving bad seams."
- Ask Pro to separate evidence-backed findings from taste, preference, and
  speculative cleanup.
- Ask for a final recommendation with a small number of next actions.

## What To Avoid

- Do not over-explain model identity or generic reasoning style.
- Do not ask Pro to monitor a long-running browser response when the user will
  paste the answer back manually.
- Do not bury the actual ask below chat history. Summarize history as decision
  context and name only the parts that matter.
- Do not ask for "all possible improvements" unless the owner truly wants a
  broad audit. Prefer bounded scope with explicit expansion rules.
- Do not accept Pro findings as commands. Treat them as claims to verify.

## Output Contracts

For code/repo audit prompts, request:

- Findings ordered by severity.
- File/line references where possible.
- `adopt`, `purge`, `defer`, or `reject` disposition.
- Reason, impact, and trigger for deferred items.
- Clear merge/release/stop recommendation.

For planning prompts, request:

- Recommended end state.
- Chopping-block candidates and keeper reasons.
- Decision branches that materially change implementation.
- Next work block, limited to high-ROI actions.

For follow-up prompts, include:

- What changed since the last Pro response.
- Which Pro findings were adopted, rejected, purged, or deferred.
- Any user reactions that change priorities.
- Remaining uncertainty and exactly what Pro should decide now.
