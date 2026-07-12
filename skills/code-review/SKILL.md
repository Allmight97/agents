---
name: code-review
description: Read-only review of a PR, branch, diff, or worktree changes for correctness, requested behavior, regressions, scope creep, proof gaps, and merge readiness. Use when asked to review changed code or decide whether work is safe to merge. Route over-engineering-only reviews to whittle-review and repository-wide structural scans to improve-codebase-architecture.
---

# Code Review

Review the changed behavior and lead with the merge decision. Report material
findings; do not fix them unless the user separately asks for implementation.

## Select the Review Owner

Choose one route before reviewing:

- **Changed code, PR, branch, diff, or merge readiness** → continue here.
- **Deletion, bloat, YAGNI, or over-engineering only** → `whittle-review`; stop.
- **Repository-wide refactor targets or structural scan** →
  `improve-codebase-architecture`; stop. That scan remains explicit-only.
- **Independent terminal evidence before merge or release** → Review Auditor;
  stop when that independent role is available and explicitly requested.
- **Explicit security best-practice audit or threat model** → the matching
  security skill; stop.

Ordinary code review may report an architectural problem only when the changed
code introduces a concrete ownership, coupling, change-amplification,
testability, or correctness risk. Tie it to the diff and impact. Do not scan the
untouched repository, design a replacement architecture, or invoke an
architecture review automatically.

## Pin the Review Target

Resolve the target before judging code:

1. For a PR, read live base/head metadata and confirm the code under review
   matches the live head. Do not prove a stale local checkout.
2. Use a fixed point the user supplied when present.
3. For branch work, infer the upstream default branch and verify the merge-base
   before asking the user.
4. For an explicit worktree review, include staged and unstaged changes against
   `HEAD` and state that untracked files are or are not included.

Record the base, head, merge-base or worktree scope, and commit list. Stop on an
invalid ref, an empty target, unresolved merge state, or ambiguous PR/branch
identity.

## Establish the Expected Behavior

Inspect, in order:

1. nearest applicable `AGENTS.md`, `CLAUDE.md`, or repository guidance;
2. originating issue, PR body, spec, acceptance criteria, or user request;
3. changed code plus enough callers, tests, and owner surfaces to understand
   the real behavior;
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
   to cause defects or repeated change. Route a dedicated deletion audit to
   `whittle-review` rather than turning this into a style pass.

Trace affected paths beyond the diff when needed. Run targeted read-only checks
when they can falsify a finding or merge claim. Do not modify code, comments,
tests, issues, or review threads during a review-only request.

Use parallel reviewers only when the diff is large enough to contain genuinely
independent surfaces. Give each a bounded axis or owned path. The root reviewer
deduplicates and reranks every finding; subagent reports are evidence, not the
final verdict.

## Finding Standard

Rank findings by merge impact:

- **P0 — stop:** catastrophic loss, compromise, or unusable release.
- **P1 — blocker:** concrete correctness, safety, security, or regression bug.
- **P2 — should fix:** material contract/spec gap, scope error, or missing proof.
- **P3 — follow-up:** bounded maintainability risk with a credible failure path;
  omit preferences and speculative cleanup.

Each finding must include:

- exact file and tight line range;
- triggering condition or scenario;
- user/system impact;
- evidence from code, contract, or failing proof;
- smallest credible correction or proof needed.

Do not report formatting, naming taste, generic best practices, or issues that
tooling already enforces. If no material finding survives verification, say so.

## Output

Lead with one verdict:

- **DO NOT MERGE** — unresolved P0/P1 or missing proof for a consequential claim.
- **MERGE WITH CHANGES** — no blocker, but material P2 work remains.
- **MERGE** — no material finding; state residual uncertainty and skipped proof.

Then provide:

1. severity-ordered findings;
2. proof run and proof still missing;
3. scope/spec mismatches;
4. routed follow-up, only when another owner is genuinely needed.

Do not bury the verdict beneath process narration. A clean review is:
`MERGE — no material findings`, followed by proof and residual risk.
