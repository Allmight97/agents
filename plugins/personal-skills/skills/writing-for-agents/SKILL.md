---
name: writing-for-agents
description: "Write or audit guidance that agents read: SKILL.md files, AGENTS.md or CLAUDE.md, issues, specs, and handoffs. Use when the task is instruction clarity, rule placement, skill triggers, or a process audit of checks and workflows."
---

# Writing for Agents

A reference for any document an agent reads: a skill, an `AGENTS.md` or
`CLAUDE.md`, an issue, a spec, a handoff, a doc behind a pointer. The packaging
differs; the levers below do not. They make the agent take the same process on
every run.

Read the branch that matches the job:

- [Skill mechanics](SKILL-MECHANICS.md) when the document is a skill:
  invocation, router skills, client metadata, behavioral proof.
- [Instruction networks](INSTRUCTION-NETWORK-MECHANICS.md) when deciding where
  a rule belongs, or cutting down an existing set of rules.
- [Process audit](PROCESS-AUDIT.md) when the owner asks to audit a
  repository's guidance, checks, hooks, CI, or workflows for work a machine
  should do.

An audit of guidance reports each finding with its evidence and a proposed
disposition; it edits only when fixes are authorized.

## Should the line exist

Decide whether a line should exist before wording it. Ask in order:

1. Can a check, type, or test decide it? Build that; its failure message is
   the guidance.
2. Can a reader learn it from the code and its tests? Write nothing.
3. Otherwise write one line: the reason, or the outside fact (what a platform,
   protocol, tool, or provider does; an accepted risk; a product decision; an
   approval boundary).

A rule is mechanical when a fixed pattern decides it: a banned import or API, a
file location, a required shape. Enforce it with the strongest check that
works, in this order: a structure that removes the wrong path, a type, a lint
whose error names the fix, a test, then CI or a repository rule. Reuse what the
repository already runs. Prove the check fails on a violation, then cut the
prose to one line that names it. Prose keeps judgement calls and the reason a
check exists.

A line that restates what code does is a second copy; it goes stale when the
code moves. A rule that makes every code change edit guidance restates code.

## Context pointers

A context pointer is a line in context that names material outside it and
says when to reach for it. A skill description is one; an `AGENTS.md` line
naming a doc is another. The pointer's wording, not its target, decides how
reliably the agent loads the material. When must-have material is missed,
sharpen the pointer first; inline the material only if that fails.

A pointer states what the material is and lists its branches: the distinct
cases that should trigger it.

- Front-load the leading word.
- Write one trigger per branch. Synonyms for one branch are that branch
  written twice.
- Cut identity the body already carries.

## The two loads

Every document and pointer spends one of two budgets.

- **Context load** falls on the agent: every always-loaded line (an
  `AGENTS.md` line, a model-invoked skill description) costs tokens and
  attention on every turn, whether or not it fires.
- **Cognitive load** falls on the human, who is the index: which documents
  exist and when to reach for each. Spend it where human judgement matters.
  Remove it where it does not.

Material behind a pointer pays only for the pointer's line. Material with no
pointer rides entirely on the human's memory.

## Information hierarchy

A document holds steps (ordered actions) and reference (rules and facts
consulted on demand). Place each piece on a ladder ranked by how soon the agent
needs it:

1. In-file step.
2. In-file reference. A flat set of peer rules is fine.
3. Disclosed reference: a separate file behind a pointer, loaded only when the
   pointer fires.

Branching is the disclosure test: inline what every branch needs; disclose
what only some branches reach. Reference left inline buries the steps around
it.

Co-locate: keep a concept's definition, rules, and caveats under one heading,
so reading one part brings its neighbours. Scattering fragments one meaning
across places; duplication repeats it.

Sprawl is a document too long even when every line is live. Attention thins
across the excess. Cure it with the ladder: disclose, or split by branch.

## Completion criteria

Every step ends on a completion criterion: the condition that tells the agent
the step is done.

- **Clarity.** A vague bound ("understanding reached") invites premature
  completion: the agent ends the step because it can see the steps after it.
  Sharpen the bound first. Hide later steps only when the bound stays fuzzy
  and you observe the rush; hiding works only across a real context boundary,
  such as a subagent or a handoff.
- **Demand.** "Every changed caller accounted for" forces legwork that
  "produce a change list" does not. Demand binds flat reference too: "every
  rule applied".

The strongest criteria are checkable and exhaustive.

## Splitting

Split a document only when the cut earns the load it spends.

- **By sequence:** split off later steps when they tempt the agent to rush
  the current one. Merging sequences does the reverse.
- **By invocation:** see [Skill mechanics](SKILL-MECHANICS.md).

## Leading words

A leading word is a compact concept the model already knows, used as a token
the agent thinks with: _tight_ for "fast, deterministic, low-overhead"; _red_
for "the loop fails on the bug". Repeated, it anchors one behaviour in few
tokens. In a pointer it also anchors invocation, when the same word lives in
the owner's prompts, docs, and code. Prefer an existing word to a coined one;
a coined word recruits nothing and must be defined. Look for restatements a
leading word can retire.

Negation is the failure beside this lever: a prohibition names the forbidden
behaviour and makes it more available. State the target behaviour instead.
Keep a prohibition only for a hard boundary you cannot phrase positively, and
pair it with the positive target.

## Pruning

- **Single source of truth.** Each meaning has one owner, so a change is a
  one-place edit. Duplication costs upkeep and inflates a meaning's rank.
- **The environment is a source.** Scripts, config, the directory layout, and
  `--help` own their facts. A document that restates them is a cache that goes
  stale. Write what looking cannot find: the unwritten convention, the reason,
  the gotcha. Add a pointer only when a search would not find its target.
- **Relevance.** A line loses relevance when it never bears on the task or
  when what it describes changes. Without pruning, stale layers settle as
  sediment. After a decision, rewrite around the new state; do not append
  history.
- **No-ops.** Delete a sentence the model already obeys by default. The test
  is model-relative; settle a disagreement by running the document. Delete the
  whole sentence rather than trimming it. A leading word too weak to beat the
  default is a no-op too; use a stronger word.

## Issues, specs, and handoffs

Lead with current state and the next decision. Include scope, constraints,
open choices, and completion evidence where they change the next action. Label
facts, proposals, and unverified claims. A document for both a human and an
agent makes the human decision readable and keeps execution requirements
explicit. Use [visual-brief](../visual-brief/SKILL.md) when substantial
material needs a visual orientation.

A handoff lets a fresh agent continue the work:

- Save it to the OS temp directory unless the owner names a place.
- Name the skills the next agent should load.
- Reference specs, plans, issues, commits, and diffs by path or URL; do not
  copy them.
- Redact secrets and personal data.
- Tailor it to the next session's stated focus, and give the owner the path.
