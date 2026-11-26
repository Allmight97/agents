---
name: whittle
description: "Simplify an implementation or its tests, or audit them for accidental complexity, keeping required behavior. Use when the user invokes Whittle by name."
---

# Whittle

Remove accidental complexity without weakening the required outcome. Judge the
smallest solution by total system cost, not line count: implementation surface,
dependencies, conceptual branches, proof burden, maintenance, and change
amplification all count. Measure against the intended end state: the code that
would exist had the requirement been known from the start.

## Set The Mode

Use the mode established by the request:

- **Apply**: the user asked to simplify, change, fix, or build. Read
  [APPLY-MECHANICS.md](APPLY-MECHANICS.md) completely before editing.
- **Review**: the user asked for a Whittle audit, deletion candidates, or an
  over-engineering review. Read [REVIEW-MECHANICS.md](REVIEW-MECHANICS.md)
  completely. A review-only request leaves code unchanged; an audit-and-fix
  request continues through Apply for supported changes in the authorized scope.

If the requested review also asks whether code is correct, secure, performant,
or ready to merge, route that question to its owning review workflow. Do not
quietly broaden Whittle into a general review.

## Rank The Scope

Run `python3 scripts/complexity_rank.py <files in scope>` (or `--changed`) from
the target repository, with the path relative to this skill. The rank picks
where to look first: files with over-threshold functions (Biome for TS/JS,
lizard otherwise) and non-zero churn. It is never a score to lower. Split code
by job, never to pass a threshold; a cut that lowers `over_fns` while
`complexity` holds only moved branches. Density is context, not rank. A file
flagged `scc-only` is ranked by a weaker proxy; say so. When the script exits 3
(`scc` missing), skip this step and say so.

## Find The Smallest Owner

Understand the real flow, its callers, and its governing boundary before
choosing a cut. Stop at the first option that fully satisfies the requirement:

1. Remove work that does not need to exist.
2. Reuse the codebase owner that already performs it.
3. Use the standard library or native platform capability.
4. Reuse an already-owned dependency when that is cheaper than bespoke code.
5. Implement the smallest coherent solution at the boundary that owns it.

When two options work, prefer the one that leaves fewer concepts and places to
change. Direct code is valuable when it remains readable and correct on real
edge cases; compressing behavior into fewer lines is not simplification by
itself.

Compatibility paths kept for an older shape, such as aliases, modes, fallbacks,
shims, and forwarding wrappers, need a current caller or a named external
consumer. Search for callers before preserving one; without either, it is
removable work. Include scaffolding the change itself left from earlier
attempts. A production seam (an export, wrapper, or factory) that exists only
so tests can reach or replace something is removable work too; one that
production uses to isolate a real side effect, lifecycle transition, platform
variation, or external dependency stays.

For a bug, find the owning cause and affected sibling paths rather than
patching only the reported caller. Trace as far as needed to support that claim;
do not turn exhaustive caller enumeration into ceremony.

## Preserve Essential Complexity

Complexity earns keep when it protects an explicit requirement, governed
boundary, data integrity, security, accessibility, interoperability, cleanup,
or real platform variance. Preserve those obligations and simplify their
expression where possible. Scale machinery (a cache, pool, queue, or
configuration for variation) earns keep only against a stated or observed load
or variation; name it.

A test earns keep when it protects a plausible regression a user would notice,
through the observable contract that would show it. Where a broader test
already proves that contract, a narrower one needs a distinct risk of its
own; the repository's proof tiers decide where each belongs. Name
the protection a deletion would lose before cutting. A restatement of the
source, a read-back of what the test just set, a self-comparison, or mock
choreography rarely protects anything; exact serialization, interaction order,
and user-visible text can be real contracts. When the call is consequential
and still unclear, break the guarded code briefly and see whether the test
fails, leaving the tree as you found it; without that evidence, keep the test
and name the open question.

Honor an explicitly requested full implementation without repeatedly arguing
for a smaller product. Whittle chooses the simplest way to deliver the agreed
scope; it does not renegotiate settled scope.

## Proof And Stop

Use the owning repository's proof requirements. Prefer the smallest check that
can falsify the changed behavior at its stable boundary; do not add a framework,
fixture system, or per-function suite merely to make simplification look
responsible. When a cut removes an assumption about permissions, navigation,
persisted data, or external callers, prove the behavior that replaces it. A
small diff without adequate proof is unfinished.

Stop when further cuts would trade away clarity, ownership, behavior, or proof.
If the remaining differences are taste, say the code is already lean and ship.
