---
name: whittle
description: >
  Force the simplest solution that actually works: question whether the task
  needs to exist, reuse existing code, prefer stdlib/native features, and keep
  the diff small. Use when asked to simplify an implementation, take the lazy
  path, apply YAGNI, or remove over-engineering while doing the work.
---

# Whittle

Build the simplest solution that actually works. The best code is the code never
written.

## The ladder

Stop at the first rung that holds, after understanding the problem and tracing
the real flow end to end:

1. **Does this need to exist?** Speculative need -> skip it, say so in one line. (YAGNI)
2. **Already in this codebase?** Reuse the helper, util, type, or pattern that lives here. Re-implementing what's a few files over is the most common slop.
3. **Stdlib does it?** Use it.
4. **Native platform feature covers it?** `<input type="date">` over a picker lib, CSS over JS, DB constraint over app code.
5. **Already-installed dependency solves it?** Use it. Never add a new one for what a few lines can do.
6. **Can it be one line?** One line.
7. **Only then:** the minimum code that works.

Two rungs work -> take the higher one and move on.

**Bug fix = root cause, not symptom.** Before editing, grep every caller of the function to touch. One guard in the shared function is a smaller diff than a guard per caller, and patching only the path the ticket names leaves every sibling caller still broken.

## Rules

- No unrequested abstractions: no interface with one implementation, no factory for one product, no config for a value that never changes.
- No scaffolding "for later"; later can scaffold for itself.
- Deletion over addition. Boring over clever.
- Fewest files possible. Shortest working diff wins.
- Complex request? Ship the lazy version and question it in the same response: "Did X; Y covers it. Need full X? Say so." Never stall on an answer you can default.
- Two stdlib options, same size? Take the one correct on edge cases. Lazy means less code, not the flimsier algorithm.

## Output

Code first. Then at most three short lines: what was skipped, when to add it. No
essays, no feature tours, no design notes. If the explanation is longer than the
code, delete the explanation. Explanation the user explicitly asked for (a
report, a walkthrough, per-phase notes) is not debt -- give it in full.

Pattern: `[code] -> skipped: [X], add when [Y].`

## Never simplify away

Input validation at trust boundaries, error handling that prevents data loss,
security, accessibility, anything explicitly requested. User insists on the full
version -> build it, no re-arguing.

Never lazy about understanding the problem. The ladder shortens the solution,
never the reading. Trace every file the change touches and the actual flow
before picking a rung. A small diff you don't understand is a second bug, not
efficiency.

The platform is never the spec ideal: a real clock drifts, a real sensor reads
off. Leave the calibration knob, not just less code.

Lazy code without its check is unfinished. Non-trivial logic (a branch, a loop, a
parser, a money/security path) leaves ONE runnable check behind, the smallest
thing that fails if the logic breaks: an `assert`-based `demo()`/`__main__`
self-check or one small `test_*.py`. No frameworks, no fixtures, no per-function
suites unless asked. Trivial one-liners need no test -- YAGNI applies to tests too.
