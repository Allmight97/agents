---
name: all-code-is-slop
description: >-
  Verify agent-written code by evidence instead of line-by-line review: runtime,
  formal and UI fuzz checks, what review evidence counts, and blocking new
  occurrences before cleaning up old ones. Use when deciding how to verify agent
  work, judging review evidence, deciding whether a comment or doc should exist,
  or widening auto-merge or automation.
---

# All Code Is Slop

This skill holds the decisions. Numbers in parentheses are slide numbers from the talk; `references/talk-index.md` links each one to its moment in the video. Cite the slide number when a claim drives a decision.

## Outcome

Agents ship code you can trust without line-by-line human review, so velocity rises and quality doesn't fall (slides 5, 8). Human review shrinks to judging verification evidence (26).

## Verification

For where a correction belongs (code, type, lint, test or prose), use the `writing-for-agents` skill. The talk's code-layer moves: ban APIs that take nuance to use well, except inside the module that wraps them in a safe API (19), and enforce directory boundaries with import bans, including type-only imports (18, 20-21).

When a static check cannot hold the correction, add verification (11, 26):

- **Runtime:** a feature map plus a CLI that drives the real app (27-28).
- **Formal:** TLA+ or Lean (29).
- **UI fuzzing:** property-based tests that drive the interface (30-35).

Done when the new check fails on the violation and passes on the fix.

## Comments and markdown

Write no comment or Markdown by default. Agents use comments, docs, rules and skills to justify workarounds and to turn one-off corrections into permanent rules (22-24).

Keep a comment only when it carries a concrete reason that no check can encode. A comment that justifies a workaround means there's a root-cause bug: delete the comment and report the workaround. In the Cursor codebase, one justified setTimeout grew to 183 timers (23).

Update existing docs a change makes wrong, in the same change; create a new doc, rule or .md file only when the user asks.

## Sequencing

Block new occurrences with a check before cleaning up old ones (48). Agents copy whatever patterns the codebase holds, so leftovers spread (16).

## Review and automation

- Judge the verification artifacts: runs, CI links, screenshots, counts and proofs. An agent's summary isn't evidence (26).
- Widen auto-merge or triggered automation only where existing checks already make the output trustworthy. Don't automate a low-trust loop (49-51).
