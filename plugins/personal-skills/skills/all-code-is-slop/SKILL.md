---
name: all-code-is-slop
description: >-
  Use when planning, briefing, reviewing or correcting engineering work, or
  editing AGENTS.md, rules or code comments. Decides where a fix belongs (code,
  type, lint, test or prose) and what review evidence counts. From Lauren Tan's
  talk "All Code Is Slop".
---
# All Code Is Slop

This skill holds the decisions. Numbers in parentheses are slide numbers from the talk; `references/talk-index.md` links each one to its moment in the video. Cite the slide number when a claim drives a decision.

## Outcome
Agents ship code you can trust without line-by-line human review, so velocity rises and quality doesn't fall (slides 5, 8). Human review shrinks to judging verification evidence (26).

## Where a correction goes
When an agent makes a mistake, put the fix in the first layer that can hold it (9-13, 25):

1. **Code.** Change an API or the architecture so the mistake can't happen. Ban APIs that take nuance to use well, except inside framework code (19). Enforce directory boundaries with import bans, including type-only imports (18, 20-21).
2. **Static check.** Use a type, lint, test or CI rule. The failure message names the fix and the root cause (24).
3. **Verification.** Use runtime checks (a feature map plus a CLI that drives the real app, 27-28), formal checks (TLA+ or Lean, 29), or UI fuzzing (30-35).
4. **Prose.** Use AGENTS.md, rules or skills only for judgment calls and for one line saying why a check exists.

Done when the new check fails on the violation and passes on the fix.

## Comments and markdown
The default is none. Agents use comments, docs, rules and skills to justify workarounds and to turn one-off corrections into permanent rules (22-24).

Keep a comment only when it carries a concrete reason that no check can encode. A comment that justifies a workaround means there's a root-cause bug: delete the comment and report the workaround. In the Cursor codebase, one justified setTimeout grew to 183 timers (23). Use pstack `/no-comments`.

Add no .md files, docs or rules unless the user asked for them.

## Sequencing
Block new occurrences with a check before cleaning up old ones (48). Agents copy whatever patterns the codebase holds, so leftovers spread (16).

## Review and automation
- Judge the verification artifacts: runs, CI links, screenshots, counts and proofs. An agent's summary isn't evidence (26).
- Widen auto-merge or triggered automation only where existing checks already make the output trustworthy. Don't automate a low-trust loop (49-51).

## Reported results
The talk's Grok Bot team numbers: comments fell from 65,824 to 1,227 (24), about 11k PRs merged in October (42), and the revert rate was 0.47% in October (45). Performance improved against a May baseline on startup and typing (47). Use these to justify the approach, not as targets.
