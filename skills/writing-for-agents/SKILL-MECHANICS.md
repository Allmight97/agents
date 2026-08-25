# Skill Mechanics

Read this branch when writing, auditing, or restructuring an Agent Skill or its
client metadata. The shared writing rules remain in [SKILL.md](SKILL.md).

## Set The Contract

Name the skill's job, target clients, invocation mode, and authorized surface.
An audit remains read-only; an edit changes only the skill and client metadata
the user placed in scope.

For a shared portable skill:

- follow the [Agent Skills specification](https://agentskills.io/specification);
- make the directory and `name` agree;
- make `description` state the job and distinct trigger branches;
- add optional frontmatter and resource directories only when a real consumer
  needs them;
- keep client presentation and policy in the client's supported metadata.

The contract is set when every target client and metadata surface is named and
no portability assumption remains implicit.

## Invocation

A model-invoked skill spends context through its visible description; an
explicit-only skill spends human attention because the user must remember it.
Keep automatic discovery unless independent invocation would be harmful or the
user explicitly chooses an explicit-only contract.

In shared Codex-compatible `SKILL.md` files, do not invent unsupported
frontmatter to control invocation. Use `agents/openai.yaml` for Codex policy and
validate the equivalent mechanism in every other target client before relying
on it.

Descriptions are context pointers:

- front-load a leading word users naturally put in prompts;
- name one trigger per behavior branch rather than listing synonyms;
- keep identity and procedure in the body;
- include exclusions only when they prevent demonstrated misrouting.

Split a skill only when a distinct leading word must trigger independently,
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

Use `$skill-creator` for scaffolding or procedural creation mechanics. Use
`$skill-bench` when blind comparative trials are warranted; its report owns the
behavioral verdict.
