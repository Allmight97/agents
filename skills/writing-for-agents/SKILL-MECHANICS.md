# Skill Mechanics

Read this branch when writing, auditing, or restructuring an Agent Skill or its
client metadata. The shared writing rules remain in [SKILL.md](SKILL.md).

## Set The Contract

Name the skill's job, target clients, invocation mode, and authorized surface.
An audit alone remains read-only; requested updates change the skill and client
metadata the user placed in scope. Audit wording does not cancel edit authority
provided elsewhere in the same request.

For a shared portable skill:

- follow the [Agent Skills specification](https://agentskills.io/specification);
- make the directory and `name` agree;
- make `description` state the job and distinct trigger branches;
- add optional frontmatter and resource directories only when a real consumer
  needs them;
- keep client presentation and policy in the client's supported metadata.

Inspect metadata for the clients actually targeted. Preserve unrelated client
settings rather than expanding a narrow edit into a distribution audit.

## Invocation

A model-invoked skill spends context through its visible description; an
explicit-only skill spends human attention because the user must remember it.
Keep automatic discovery by default and preserve existing invocation policy.
Change to explicit-only only when the user requests it. Sensitive operations
need their own authorization boundary; they do not imply an invocation-policy
change.

In shared Codex-compatible `SKILL.md` files, do not invent unsupported
frontmatter to control invocation. Use `agents/openai.yaml` for Codex policy and
validate the equivalent mechanism in every other target client before relying
on it.

Descriptions are context pointers:

- state the capability and the task that needs it concisely;
- keep identity and procedure in the body;
- include exclusions only when they prevent demonstrated misrouting.

Split a skill only when a distinct task needs independent discovery,
another skill must reach it directly, or a real sequence boundary prevents
premature completion. Otherwise keep branch-only mechanics behind a precise
pointer in the owning skill.

## Structure And Disclosure

Classify each piece as an in-skill step, in-skill reference, disclosed
reference, or external reference. Inline material every branch needs; disclose
substantial branch-only material. A missing reference is first a pointer defect,
not proof that everything belongs in `SKILL.md`.

Inspect every line for:

- **duplication**: the same meaning has more than one owner;
- **sediment**: stale material survived because adding felt safer than deleting;
- **sprawl**: live material obscures the active path and should be disclosed;
- **cache**: prose copies truth the environment can reveal cheaply;
- **no-op**: the instruction does not change behavior relative to the target
  model;
- **negation**: the forbidden behavior is primed instead of the positive target.

Settle consequential uncertainty with a focused behavioral trial rather than
adding speculative rules.

## Audit Or Edit Loop

1. Map obvious, ambiguous, and near-miss prompts from the description and every
   client metadata surface.
2. Inspect the first move, steps, reference, pointers, and completion criteria.
3. Resolve conflicts against the surface that owns the behavior.
4. In audit mode, report evidence and the smallest patch. In edit mode, apply
   only the authorized patch and keep client metadata aligned.
5. Validate portable structure and every target client's metadata.
6. Forward-test realistic positive, ambiguous, near-miss, and regression prompts
   when uncertainty could change the design.
7. Inspect the final diff and distinguish structural validation from behavioral
   evidence.

The loop is complete when the trigger boundary, first move, output behavior,
and validation claims are all supported by inspectable evidence.

Use `$skill-creator` when available for creation mechanics and structural
validation. For a complex or risky revision, consider an independent behavioral
trial when delegation is available and authorized. Give the evaluator a
realistic request and minimum raw artifacts without the intended answer or
prior conclusions. Bound side effects and use temporary outputs. Report what
was actually observed; structural validation alone does not prove behavior.
