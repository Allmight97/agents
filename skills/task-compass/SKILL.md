---
name: task-compass
description: Frame a nontrivial request when the user mixes immediate solving, learning, system-building, or competing objectives, or asks for help focusing. Infer the primary outcome and proportionate proof burden, park secondary ideas, and proceed without making the user rewrite a voice-dictated prompt. Do not use for clear single-purpose tasks or casual conversation.
---

# Task Compass

Reduce the executive-function load of starting and steering the current task.
This is a compact control layer, not productivity coaching or a new system the
user must maintain.

## Orient

Infer these from the user's request instead of asking them to fill out a form:

1. The practical outcome that would make the task complete.
2. Explicit constraints, permissions, evidence, and stop conditions.
3. The primary mode:
   - **Solve** when completion means changing, restoring, producing, or deciding
     something now.
   - **Learn** when completion means understanding, explaining, comparing, or
     researching. Learning does not authorize implementation.
   - **Systematize** when completion means creating or improving a reusable
     workflow, tool, skill, or automation. Require evidence of repeated friction
     unless the user explicitly wants a speculative prototype.
4. The verification budget:
   - **High** for customer or production systems, credentials, deletion,
     firmware, billing, external communication, sensitive data, or changes that
     are hard to reverse. Inspect current state, preserve recovery where useful,
     and prove the exit condition.
   - **Medium** for code, scripts, local configuration, plugins, and repeatable
     maintenance. Use the narrowest check at the owning boundary and inspect the
     final result.
   - **Low** for reversible settings, personal tool trials, and curiosity work.
     Use one proportionate check or timebox, then stop.
5. Any adjacent objective whose pursuit would materially delay or broaden the
   primary outcome.

The mode identifies the primary completion condition; it does not ban useful
supporting work from another mode. The verification budget controls depth, not
safety, authorization, or explicit user requirements.

## Act

- When the request is safely inferable, choose the likely mode and verification
  budget and proceed. Do not ask the user to classify the task or rewrite the
  prompt.
- Show a one-line compass only when it resolves real ambiguity or changes the
  work, for example: `Compass: Solve; medium proof; park the reusable wrapper.`
  Otherwise keep the framing internal.
- Ask at most the smallest action-changing question when different plausible
  interpretations would materially change the outcome, authority, or risk.
  Recommend a default. Do not open a full decision interview.
- Treat typos, dictation artifacts, restarts, and conversational phrasing as
  normal. Recover intent from the whole request, preserve concrete nouns and
  constraints, and raise only genuine contradictions.
- When the user is overloaded, reduce the active surface to one recommended
  next action. Do not prescribe a timer, tracker, routine, or reminder unless
  requested.

## Control Scope Drift

When a later message or discovered fact introduces more work:

- Absorb it when it is necessary to reach the primary outcome.
- Treat it as a replacement when the user clearly reprioritizes.
- Otherwise keep it as a conversational parking item and finish the primary
  outcome first. Mention the parked item once when needed; do not maintain a
  visible ledger or create durable state unless asked.
- Reorient explicitly when the primary mode or verification budget changes.
  Do not silently turn a solve task into a redesign, a learning task into an
  implementation, or a local fix into a reusable system.

## Boundaries

- `grill-me` owns explicit pressure-testing and dependency-safe decision
  interviews. Task Compass should reduce questions and establish the next
  executable direction.
- `wayfinder` owns durable roadmaps for large or materially foggy work. Task
  Compass does not create issues or planning artifacts by itself.
- `whittle` owns simplifying an implementation. Task Compass decides what the
  current task is before implementation strategy takes over.
- Do not diagnose the user, moralize about focus, or turn an accessibility aid
  into another obligation.

At handoff, report the achieved outcome and proof. Mention a parked objective
only when preserving it helps the user decide what to do next.
