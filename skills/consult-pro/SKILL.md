---
name: consult-pro
description: Build, refine, and synthesize ChatGPT Pro consultation prompts. Use when the user asks for a paste-ready Pro prompt, wants Pro to audit, review, or critique a repo or plan, needs a follow-up after a Pro response, wants Pro feedback checked against local evidence, or wants a manual Pro consultation loop without browser monitoring.
---

# Consult Pro

## Purpose

Use Pro as an outside high-context critic, not as an oracle. Produce prompts
that give it enough source truth, constraints, and deliverables to find real
blind spots, then validate its response against local evidence before acting.

## Boundary

This skill owns the manual Pro consultation loop: prompt packaging, follow-up,
and response synthesis. It does not own the underlying repo decision, skill
design, or instruction rewrite; use the relevant project skill or
`$writing-great-skills` for that work after Pro's claims are checked.

## Workflow

1. Clarify the consultation lane:
   - **First pass:** create a paste-ready prompt for Pro.
   - **Follow-up:** summarize local changes, user reactions, and remaining
     questions for another Pro pass.
   - **Synthesis:** evaluate a Pro response and turn it into adopt/reject/defer
     actions.
2. Gather current facts before drafting:
   - Repo/project path, branch, commit, PR/issue links, current diff, and any
     relevant local findings.
   - What Pro can inspect directly, such as GitHub connector access to a branch.
   - What Pro cannot know, such as local-only files, unpushed changes, hidden
     user preferences, or recent command output.
3. Draft the prompt with a concrete objective, evidence routes, explicit
   constraints, and requested output shape.
4. Ask Pro for convergence-oriented criticism: findings, tradeoffs, and a clear
   end-state recommendation, not an endless review loop.
5. When Pro responds, validate material claims against current repo truth before
   changing files.

## Resources

- Read `references/prompt-guide.md` when creating or revising a Pro prompt.
- Read `references/templates.md` when the user wants a paste-ready prompt.
- Read `references/response-synthesis.md` when processing Pro's response.

## Output Rules

- Return prompts in fenced Markdown blocks so the user can paste them manually.
- Include paths, branch names, SHAs, dates, and links when known.
- Prefer direct asks such as "find remaining high-ROI infra cruft" over vague
  asks such as "give feedback."
- Ask Pro to distinguish `adopt`, `purge`, `defer`, and `reject` when the output
  affects repo changes.
- Skip praise, apologies, and model-identity boilerplate; ask for
  evidence-backed findings and a decision-oriented recommendation.
