---
name: whittle
description: Simplify an implementation or audit code solely for accidental complexity. Use only when the user explicitly invokes Whittle to apply YAGNI, remove unnecessary code, reuse an existing owner, prefer standard or native capabilities, or run a read-only bloat review. Do not infer it from ordinary implementation or review work; correctness, security, performance, merge-readiness, and architecture reviews belong to their specialist owners.
---

# Whittle

Remove accidental complexity without weakening the required outcome. Judge the
smallest solution by total system cost, not line count: implementation surface,
dependencies, conceptual branches, proof burden, maintenance, and change
amplification all count.

## Set The Mode

Use the mode established by the request:

- **Apply**: the user asked to simplify, change, fix, or build. Read
  [APPLY-MECHANICS.md](APPLY-MECHANICS.md) completely before editing.
- **Review**: the user asked for a Whittle audit, deletion candidates, or an
  over-engineering review. Read [REVIEW-MECHANICS.md](REVIEW-MECHANICS.md)
  completely and apply nothing.

If the requested review also asks whether code is correct, secure, performant,
or ready to merge, route that question to its owning review workflow. Do not
quietly broaden Whittle into a general review.

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

For a bug, find the owning cause and affected sibling paths rather than
patching only the reported caller. Trace as far as needed to support that claim;
do not turn exhaustive caller enumeration into ceremony.

## Preserve Essential Complexity

Complexity earns keep when it protects an explicit requirement, governed
boundary, data integrity, security, accessibility, interoperability, cleanup,
or real platform variance. Preserve those obligations and simplify their
expression where possible.

Honor an explicitly requested full implementation without repeatedly arguing
for a smaller product. Whittle chooses the simplest way to deliver the agreed
scope; it does not renegotiate settled scope.

## Proof And Stop

Use the owning repository's proof requirements. Prefer the smallest check that
can falsify the changed behavior at its stable boundary; do not add a framework,
fixture system, or per-function suite merely to make simplification look
responsible. A small diff without adequate proof is unfinished.

Stop when further cuts would trade away clarity, ownership, behavior, or proof.
If the remaining differences are taste, say the code is already lean and ship.
