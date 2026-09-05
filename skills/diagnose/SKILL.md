---
name: diagnose
description: Diagnose and fix bugs or performance regressions using a focused reproduction, competing explanations, and evidence that tests the cause. Use for debugging reported failures or slow behavior.
---

# Diagnose

Establish what fails, find its owning cause, and prove the correction against
that behavior. Scale the investigation to the uncertainty: a clear local defect
does not need the same process as an intermittent production failure.

## Establish The Signal

Read the relevant owner guidance and enough code, logs, and recent changes to
identify the actual path. Prefer a focused failing test, command, captured
trace, or browser interaction that reproduces the user's symptom. Make it fast
and repeatable where possible; minimize only while doing so helps isolate the
cause. Preserve the original scenario for final verification.

For intermittent failures, record attempts and failure frequency. Choose a
sample size that can distinguish the proposed fix; one passing run is weak
evidence. Stress only an environment where that load is authorized.

If reproduction is unavailable, continue with evidence from code, logs, traces,
and history. Label hypotheses and the missing runtime proof. Ask for the
specific access or artifact needed when it blocks further progress. Production
instrumentation and access changes require their own authorization.

Use [the human-assisted loop template](scripts/hitl-loop.template.sh) when the
trigger requires manual interaction and a repeatable capture would help.
Redact secrets and keep captured content to what the diagnosis needs.

## Test The Cause

State the leading explanation and its falsifiable prediction. Consider credible
alternatives when evidence is ambiguous; a fixed hypothesis count adds no proof.
Choose the next inspection or probe that distinguishes them and update the
explanation when evidence contradicts it.

Prefer a debugger, focused logs, or a minimal experiment. For performance,
measure the relevant scenario before changing it; preserve workload and
configuration for the comparison. Tag temporary instrumentation for cleanup.

## Fix And Verify

Fix the owning cause and affected sibling paths within scope. When a useful
regression test can exercise the real failure, make it fail before the fix and
pass afterward. Choose the lowest test tier that reaches the bug; an assertion
that bypasses the failed handoff cannot prove it.

Recheck the original scenario and run the owning project's required checks.
Remove temporary instrumentation and task-owned harnesses that no longer earn
keep. If runtime proof remains unavailable, report what the code and checks
establish and what remains unverified rather than claiming the bug reproduced
or was conclusively fixed.

Lead the result with the cause, correction, and evidence. Recommend broader
architecture work only when the investigation exposed a concrete remaining
problem; use `improve-codebase-architecture` when that scan is requested.
