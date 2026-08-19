---
name: orchestrate
description: Orchestrate bounded Codex subagents for independent research, evidence gathering, adversarial review, or parallel implementation. Use when the user explicitly requests subagent delegation; do not infer it from task size or complexity.
---

# Orchestrate

Keep requirements, cross-lane decisions, arbitration, and user-facing
presentation in the root agent. Move bounded independent work to the role that
can complete its deliverable when separation materially improves speed,
breadth, context hygiene, implementation throughput, or scrutiny.

## 1. Inspect The Live Surface

- Inspect the current spawn contract, available roles, active agents, and
  concurrency before assigning work.
- Select a role from its live description and permissions before considering a
  model override. Let role and agent configuration own model, reasoning, tool,
  and behavior defaults.
- Use the general role with an explicit model only when the live surface exposes
  a task-specific capability that no available role represents.

Complete this step when every candidate role and available slot comes from the
live surface rather than remembered configuration.

## 2. Choose The Delegated Lanes

- Delegate only work that can be bounded by one deliverable and a clear stop
  condition.
- Choose an available read-only role when the missing output is evidence from
  independent sources or code areas.
- Choose an available implementation role when the requested output is an
  authorized change and each slice has stable inputs, one owned surface,
  explicit exclusions, an integration point, and validation that can falsify
  its result.
- Choose an available independent-review role when the user or applicable
  workflow requests scrutiny of an existing artifact and proof surface before a
  consequential keep/reject decision.
- Choose an available batch role for repeated, independent transformations with
  one fixed contract and cheap validation.
- Keep a task in the root when delegation would add more coordination than
  evidence or execution value. Say so in one sentence and continue there.
- Preserve the user's authority boundary. Delegation does not authorize new
  mutations, external actions, credentials, or scope.

One lane owns each shared contract and integration point. Independent workers
may consume a settled contract in parallel when their files, generated
artifacts, decisions, and validation ownership do not overlap. When the contract
or interface is unresolved, settle it in root before partitioning implementation.

Complete this step only when every delegated lane has an independent deliverable
and one owner; otherwise keep the coupled work in root.

## 3. Write Each Assignment

Give every delegate:

- the exact outcome or question and its stable inputs;
- the owned surface, including files and integration point when edits are
  allowed;
- read/write authority and explicit exclusions;
- a stop condition and decisions to escalate;
- required validation;
- a compact output contract.

Pass only the context needed for the lane; inherit full history only when the
deliverable depends on it. For independent review, provide the artifact and
acceptance surface without leaking the root's preferred answer or suspected
finding.

Complete this step when every assignment is executable without reconstructing
missing authority, ownership, validation, or stop conditions.

## 4. Coordinate And Integrate

- Start independent lanes in parallel and keep the root focused on decisions,
  integration, or another non-overlapping lane.
- Wait for every result required by the final decision. Steer or stop a delegate
  when its lane becomes stale, blocked, duplicative, or out of scope.
- Treat delegate reports as evidence, not authority. Reconcile conflicts and
  validate consequential claims against the owning source.
- Return one integrated answer. Report material evidence, uncertainty,
  validation, and residual risk without replaying delegate activity.

Complete only after every result required by the decision has arrived or its
absence is reported as a material gap.
