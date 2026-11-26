# Instruction Network Mechanics

Shared writing guidance lives in [SKILL.md](SKILL.md).

## Find the owner

Inspect the instruction chain applicable to the requested paths and the
sources that own the behavior being changed. Widen inspection when a rule
crosses those boundaries; a local correction needs no unrelated subtree census.

| Meaning | Smallest useful owner |
| --- | --- |
| Personal working preference across projects | Global instructions |
| Repository-wide invariant | Root instruction file |
| Local reason, outside constraint, or non-obvious trap | Applicable nested instructions |
| Reusable task procedure | Skill |
| Temporary work state | Active issue or requested spec |
| Durable rationale that changes later decisions | Beside the rule it justifies: owning instructions or the enforcing code |
| Fact or behavior the code or configuration shows (a transition list, an interface or file inventory, "X owns Y") | None: see "The environment is a source" in [SKILL.md](SKILL.md) |
| Generic coaching, duplicate rule, or stale state | Delete |

Create nested guidance when a distinct boundary or recurring wrong-path work
justifies it. Prefer fixing the code boundary, type, test, or script when that
removes the need for prose. Durable rules must state their operative meaning
without relying on mutable issue wording.

Scope required reading to the paths a rule governs. Give each step one
completion criterion instead of a recurring checklist. When authority or a
consequential decision is unresolved, pause only the action it affects.

## Cut an existing network

Sort each unit by the three questions in [SKILL.md](SKILL.md): a reason or
outside fact stays; a rule a fixed pattern decides moves to a check; a
restatement of the code and a pointer a search would find go.

- Open the code before deleting a unit as a restatement. If the code does not
  show the claim plainly, keep its reason as one line or pin it with a test.
- A reason buried in narration keeps only the reason, with the symbol or file
  it is about.
- Behavior that spans files belongs to a test when one can pin it. Prose keeps
  what no test can: a lock order, a race that must never happen.
- Build a missing check before deleting the prose it replaces. If the code
  already breaks the rule, fix the code or delete the rule: a rule the code
  does not follow is a false line.
- A heading that invites narration (an interface, ownership, or file-list
  section) goes with its content.
- Losing a reason costs more than leaving a line. When unsure, keep one line.

## Verify the result

For guidance-only edits, run `git diff --check`, check changed pointers and
removed terms, and confirm each relocated rule has one owner. These checks do
not show that the model behaves better; report behavior claims as untested.

For discovery behavior, consult the target client's current documentation:
[Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Claude Code guidance](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md).
