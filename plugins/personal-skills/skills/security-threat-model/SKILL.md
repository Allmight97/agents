---
name: security-threat-model
description: "Threat model a repository or path: assets, trust boundaries, attacker capabilities, ranked abuse paths, and mitigations."
---

# Repository Threat Model

Produce a threat model specific to the system's real exposure and usage.
Anchor architectural claims in source, configuration, and existing owner docs.

## Scope And Context

Read [the report guide](references/report-guide.md) before modelling; its
evidence contract governs every claim.

Identify the requested repository or path, intended usage, deployment model,
sensitive assets, authentication expectations, and external entrypoints.
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
mitigations.

A threat model does not by itself prove a vulnerability or authorize remediation.

## Report And Check

Use [controls and assets](references/security-controls-and-assets.md) when the
repository's assets or controls do not map cleanly to the boundaries you found.

The model is done when every entrypoint and trust boundary found in Scope And
Context appears as an abuse path or as considered with its controls named, the
ranking reflects exposure, and unresolved assumptions remain visible. Default
to a chat report for a small scope. Use a user-specified or repository-owned
location for a requested durable file; otherwise use OS temp when a file helps.
Report proof limits and the highest-value next action.
