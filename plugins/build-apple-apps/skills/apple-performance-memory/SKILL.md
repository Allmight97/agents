---
name: apple-performance-memory
description: Diagnose Apple app launch/runtime performance, SwiftUI invalidation, hangs, Instruments traces, Top Functions, ETTrace profiles, dSYMs, memgraphs, leaks, retain cycles, and Foundation Models traces. Use when an Apple app is slow, janky, memory-heavy, leaking, hanging, or needs before/after profiling evidence.
---

# Apple Performance / Memory

## Purpose

Use this skill when the question is runtime cost, not merely build correctness. Start with code and scenario clarity, then pick the smallest trace that answers the question.

## Workflow

1. Define the scenario.
   - launch, first screen, scroll, navigation, search, import/export, HealthKit sync, model generation, background work, watch handoff, or memory growth
   - same scheme, destination, configuration, data, and steps for before/after comparisons

2. Inspect code first.
   - SwiftUI body churn, expensive computed properties, broad Observation invalidation, unstable IDs, nested lists, image decoding, synchronous work on the main actor
   - retain cycles, long-lived tasks, unbounded caches, NotificationCenter/KVO/timer ownership, task cancellation, and actor isolation problems

3. Pick the proof.
   - Instruments or `xctrace` for CPU, hangs, allocation, leaks, and launch
   - Top Functions for hot-stack narrowing
   - ETTrace helpers for iOS Simulator latency and stack comparison
   - dSYM collection when traces need symbolication
   - memgraph helpers for retained objects and leaks
   - Foundation Models Instrument for prompt, response, token, and tool-call behavior
   - XcodeBuildMCP coverage/log workflows when the issue is tied to tests or runtime logs

4. Run the narrow command.
   - Keep raw trace files out of git unless the repo explicitly stores performance artifacts.
   - Store temporary evidence under `/private/tmp` or another ignored location.
   - Preserve the exact command, destination, device, OS, build configuration, and app version.

5. Fix and compare.
   - Make one causal change at a time where possible.
   - Re-run the same scenario.
   - Report before/after evidence and residual risk.

## Bundled Helpers

- `scripts/analyze_flamegraph_json.py`
- `scripts/collect_ios_dsyms.sh`
- `scripts/capture_sim_memgraph.sh`
- `scripts/summarize_memgraph_leaks.py`

## References

- `references/swiftui/`
