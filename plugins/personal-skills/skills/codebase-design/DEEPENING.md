# Deepening Existing Modules

Read after choosing modules to consolidate whose caller burden or scattered
ownership is worth changing. Shared design criteria live in
[SKILL.md](SKILL.md).

## Dependencies

Inspect what must stay together and what actually needs substitution:

- **In-process computation:** test through the owner that exposes the behavior.
  Consolidation helps only when responsibilities belong together.
- **Local infrastructure:** prefer existing realistic test fixtures when their
  behavior covers the relevant contract. A stand-in's differences may still need
  an integration check against the real dependency.
- **Owned remote service:** keep service authority and network failures explicit.
  Introduce a seam or adapter only when it reduces caller knowledge or supports
  a necessary proof path; a network boundary alone does not mandate a framework.
- **Third-party dependency:** isolate provider details where they would otherwise
  leak. Local doubles prove owned logic, while contract or integration evidence
  is needed for assumptions about the provider.

An interface with one implementation may still own a concrete lifecycle or
isolation requirement; judge that obligation before collapsing it.

## Test Migration

Add proof at the stable interface before deleting tests the move made
redundant; judge each test by [whittle](../whittle/SKILL.md)'s rule.

Complete when callers use the intended owner, obsolete paths are removed, and
proof covers preserved behavior plus each changed point where two owners pass
data or control.
