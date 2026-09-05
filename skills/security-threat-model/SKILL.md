---
name: security-threat-model
description: Build a repository-grounded threat model of assets, trust boundaries, attacker capabilities, abuse paths, and mitigations. Use when the user explicitly requests threat modeling; ordinary code review and architecture summaries do not trigger it.
---

# Repository Threat Model

Produce a threat model specific to the system's real exposure and usage.
Anchor architectural claims in source, configuration, and existing owner docs;
keep assumptions and recommended controls distinct from verified behavior.

## Scope And Context

Identify the requested repository or path, intended usage, deployment model,
sensitive assets, authentication expectations, and external entrypoints. Reuse
existing evidence rather than requiring a separate repository-summary artifact.
Separate runtime behavior from build/CI tooling and tests where their authority
or attacker access differs.

Resolve discoverable facts from the repository. Ask early about missing context
that materially changes risk ranking. When a useful conditional model is
possible, proceed with explicit assumptions and the conclusions they affect;
do not require a confirmation round for context already supplied. If an unknown
makes the requested conclusion untenable, identify that exact limitation.

## Model The Risks

Map data flows and concrete trust boundaries, including validation,
authentication, authorization, and resource ownership. Identify assets and
realistic attacker capabilities, including capabilities the attacker lacks.

Describe supported abuse paths from entrypoint through the relevant controls to
impact. Rank them by qualitative likelihood and impact, accounting for existing
mitigations. Avoid quotas that manufacture threats or force every boundary to
have a vulnerability.

For material threats, distinguish existing controls, gaps, recommended changes,
and residual risk. Tie recommendations to their owning source or configuration.
A threat model does not by itself prove a vulnerability or authorize remediation.

## Report And Check

Read [the report guide](references/prompt-template.md) for the evidence and
output contract. Use [controls and assets](references/security-controls-and-assets.md)
only when the system needs a broader category check.

Verify the major in-scope entrypoints and boundaries were considered, the
ranking reflects exposure, and unresolved assumptions remain visible. Default
to a chat report for a small scope. Use a user-specified or repository-owned
location for a requested durable file; otherwise use OS temp when a file helps.
Report proof limits and the highest-value next action.
