---
name: orchestrate
description: Orchestrate bounded Codex subagents for independent research, evidence gathering, adversarial review, or parallel implementation. Use only when the user explicitly invokes this skill; do not infer it from task size or complexity.
---

# Orchestrate

Keep requirements, cross-lane decisions, arbitration, and user-facing
presentation in the root agent. Move bounded independent work to the role that
can complete its deliverable when separation materially improves speed,
breadth, context hygiene, implementation throughput, or scrutiny.

## 1. Inspect The Live Surface

- Inspect the current spawn contract, available roles, active agents, and
  concurrency before assigning work.
- Select roles from their live descriptions and permissions. The custom agent
  definitions own each role's job, model, reasoning, tool surface, and behavior;
  do not restate or cache them here.

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
- Keep a task in the root when delegation would add more coordination than
  evidence or execution value. Say so in one sentence and continue there.
- Preserve the user's authority boundary. Delegation does not authorize new
  mutations, external actions, credentials, or scope.

One lane owns each shared contract and integration point. Independent workers
may consume a settled contract in parallel when their files, generated
artifacts, decisions, and validation ownership do not overlap. When the contract
or interface is unresolved, settle it in root before partitioning implementation.

## 3. Write Each Assignment

Give every delegate:

- the exact outcome or question and its stable inputs;
- the owned surface, including files and integration point when edits are
  allowed;
- read/write authority and explicit exclusions;
- a stop condition and decisions to escalate;
- required validation;
- a compact output contract.

Pass only the context needed for the lane. For independent review, provide the
artifact and acceptance surface without leaking the root's preferred answer or
suspected finding.

## 4. Coordinate And Integrate

- Start independent lanes in parallel and keep the root focused on decisions,
  integration, or another non-overlapping lane.
- Wait for every result required by the final decision. Steer or stop a delegate
  when its lane becomes stale, blocked, duplicative, or out of scope.
- Treat delegate reports as evidence, not authority. Reconcile conflicts and
  validate consequential claims against the owning source.
- Return one integrated answer. Report material evidence, uncertainty,
  validation, and residual risk without replaying delegate activity.
