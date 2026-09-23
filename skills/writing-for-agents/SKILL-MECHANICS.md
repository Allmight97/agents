# Skill Mechanics

Use for skill triggers, structure, client metadata, or behavioral validation.
Shared writing guidance lives in [SKILL.md](SKILL.md).

## Discovery and portability

Identify the skill's job and actual target clients. Preserve existing
invocation policy unless the user asks to change it. Keep automatic discovery
for new skills by default; sensitivity of an action belongs in its permission
boundary.

Descriptions should name the capability and the task that needs it. Put
procedure in the body and add exclusions only when they prevent plausible
misrouting. Check neighboring descriptions when their jobs overlap.

Keep shared files valid against the [Agent Skills specification](https://agentskills.io/specification):
directory and name agree, and metadata is supported by its consumer. Codex
invocation policy belongs in `agents/openai.yaml`; preserve unrelated settings.
Verify client-specific behavior for the clients affected by the change.
A body edit does not require proving every distribution channel again.

## Structure

Keep purpose, essential constraints, and shared decisions in `SKILL.md`.
Disclose substantial branch-specific procedures, examples, or scripts with
clear loading conditions. A short single-purpose skill can remain one file.
Split skills only when independent discovery or a real execution boundary
helps the task.

Retain non-obvious domain knowledge, working preferences, and fragile
operational sequences. Remove generic coaching and repeated contracts.
Consider every model and client the shared skill serves before removing a
guardrail on the assumption that one model no longer needs it.

## Validation

Use `$skill-creator` when available for creation mechanics and its structural
validator. Check changed references and affected client metadata. Structural
validity establishes packaging, not useful model behavior.

When a routing or workflow change has consequential uncertainty, compare
realistic tasks against the current and proposed guidance. Include a relevant
task, a nearby task that should stay out, and any known regression. Test without
the skill as well when its added value is the question. Compare task quality,
unnecessary reads or questions, and whether the requested work finishes;
word count alone cannot decide the result.

Use independent trials only when delegation is authorized and the evidence
earns the cost. Give the evaluator the request and minimum raw artifacts,
without the preferred answer. Bound side effects and keep trial output outside
the source tree. Report observed outcomes and remaining uncertainty.
