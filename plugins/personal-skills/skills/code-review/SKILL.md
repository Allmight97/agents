---
name: code-review
description: "Merge-readiness review of changed code: correctness, security, requested behavior, and missing proof, ending in a merge verdict. Use when the owner asks to review a change or whether it is ready to merge, or another skill requests a code review."
---

# Code Review

Review the changed behavior and lead with material findings or the requested
merge decision. A review-only request leaves code, comments, tests, issues, and
review threads unchanged; fixes follow the Fixes section when authorized.

## Select the Review Owner

Choose one route before reviewing:

- **Changed code, PR, branch, diff, or merge readiness** → continue here.
- **Simplification review** (Whittle named or not) → `whittle` review mode;
  stop.
- **Repository-wide refactor targets or structural scan** →
  `improve-codebase-architecture`; stop.
- **Threat model of a repository or path** → `security-threat-model`; stop.

Ordinary code review may report an architectural problem only when the changed
code introduces a concrete ownership, coupling, change-amplification,
testability, or correctness risk. Tie it to the diff and impact. Do not scan the
untouched repository, design a replacement architecture, or invoke an
architecture review automatically.

## Pin the Review Target

Resolve the target before judging code:

1. For a PR, read live base/head metadata and review the live head; fetch it
   when the local checkout differs.
2. Use a fixed point the user supplied when present.
3. For branch work, infer the upstream default branch and verify the merge-base
   before asking the user.
4. For an explicit worktree review, include staged and unstaged changes against
   `HEAD` and state that untracked files are or are not included.

Record the relevant base/head or worktree scope. Resolve invalid or ambiguous
refs before judging them; report an empty diff as no changes to review. For an
unresolved merge, review conflict intent only if that is the requested target;
a merge-ready verdict requires a resolved result.

## Establish the Expected Behavior

Inspect, in order:

1. every applicable `AGENTS.md`, `CLAUDE.md`, or repository guidance file
   along the changed paths, from the root down, not only the nearest;
2. originating issue, PR body, spec, acceptance criteria, or user request;
3. changed code plus every caller and test of each changed signature, return
   value, error, and default;
4. documented verification commands for the affected owner.

Infer the originating source from PR metadata, commit messages, branch names,
and repository links before asking. If no spec exists, continue with repository
contracts and state the limitation; do not invent requirements.

## Review Order

Review in this order so style and tidiness cannot mask behavior:

1. **Correctness and safety** — wrong outcomes, data loss, broken error paths,
   concurrency/lifetime faults, security regressions, and platform failures.
2. **Requested behavior** — missing or partial requirements, unrequested
   behavior, scope creep, and changed semantics not acknowledged by the source.
3. **Contracts and integration** — caller/callee mismatch, owner-boundary
   violations, compatibility, migration, cleanup, and rollback behavior.
4. **Proof** — missing regression tests, tests at the wrong seam, stale mocks,
   skipped owner checks, or evidence that cannot falsify the claim.
5. **Maintainability introduced by the diff** — only concrete complexity likely
   to cause defects or repeated change. Keep a dedicated simplification review
   distinct from a merge verdict.

Trace affected paths beyond the diff when needed. Run targeted read-only checks
when they can falsify a finding or merge claim. When the change's safety rests
on one fact, prove that fact by running the real code (a scratch script or test
outside the source tree); a written argument is not proof.

Use parallel reviewers when delegation is authorized and the diff contains
independent surfaces that benefit from separate scrutiny. Give each a bounded
axis or owned path. The root reviewer deduplicates and reranks every finding;
subagent reports are evidence, not the final verdict.

## Search the Diff

Judge whole touched functions, not only changed lines. Then search on purpose:

- **Removed behavior.** For each deleted or replaced path, list what it did
  and find where each duty happens now. A duty with no new home is a
  candidate.
- **Callers and callees.** Follow every changed signature, return value,
  error, and default to the code on the other side.
- **Security,** when the diff touches a trust boundary: input parsing, file
  paths, authentication, secrets, cryptography, deserialization, subprocesses,
  or outbound requests. Report a vulnerability only with an exploit path: who
  controls the input, how it reaches the sink, and what they gain. Leave out
  resource-exhaustion denial of service, hardening with no exploit, and test
  code. Use current official docs for the stack and label general knowledge.
- **Resource handoff,** when the diff passes a resource between owners: a
  temp file to its final path, a worker aborted while still writing, cleanup
  registration and removal, or a retry. Trace the path value through every
  register and remove call; a removal call alone does not show that ownership
  ended. State which outcome the user sees when the work succeeds but cleanup
  fails, and which owner retries the leftover path.

Verify each candidate before reporting it: **confirmed** (the trigger is shown
or proven), **plausible** (a credible trigger, not proven; label it), or
**refuted** (drop it). Report confirmed findings by default; add plausible
ones when the user asks for a thorough review. After the first list, sweep the
diff once more for areas no candidate touched.

## Finding Standard

Rank findings by merge impact:

- **P0 — stop:** catastrophic loss, compromise, or unusable release.
- **P1 — blocker:** concrete correctness, safety, security, or regression bug,
  or missing proof for a consequential claim.
- **P2 — should fix:** material contract/spec gap, scope error, or other
  missing proof.
- **P3 — follow-up:** bounded maintainability risk with a credible failure path;
  omit preferences and speculative cleanup.

Each finding must include:

- exact file and tight line range;
- triggering condition or scenario;
- user/system impact;
- evidence from code, contract, or failing proof;
- smallest credible correction or proof needed.

Report only findings that fit P0–P3; leave anything tooling already enforces to
the tooling. If no material finding survives verification, say so.

## Output

For merge-readiness requests, lead with one verdict:

- **DO NOT MERGE** — unresolved P0/P1.
- **MERGE WITH CHANGES** — no P0/P1, but P2 work remains.
- **MERGE** — no P0–P2 finding; list P3 follow-ups, residual uncertainty, and
  skipped proof.

For other reviews, lead with the highest-impact finding or no material findings.
Include only applicable sections:

1. severity-ordered findings;
2. proof run and proof still missing;
3. scope/spec mismatches;
4. routed follow-up, only when another owner is needed.

A clean review is `MERGE — no material findings`, followed by proof and
residual risk.

## Fixes

When the user authorized review and fixes, finish the assessment first, then
carry supported fixes through the owning implementation checks. Fix a security
finding one finding or tight cluster at a time, in its own commit; name any
behavior change first, and ask before a fix that breaks current behavior.
