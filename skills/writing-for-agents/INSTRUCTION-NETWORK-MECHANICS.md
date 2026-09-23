# Instruction Network Mechanics

Use for repository instructions, global guidance, or deciding where a rule
belongs. Shared writing guidance lives in [SKILL.md](SKILL.md).

## Find the owner

Inspect the instruction chain applicable to the requested paths and the
sources that own the behavior being changed. Widen inspection when a rule
crosses those boundaries; a local correction needs no unrelated subtree census.

| Meaning | Smallest useful owner |
| --- | --- |
| Personal working preference across projects | Global instructions |
| Repository-wide invariant | Root instruction file |
| Local interface, command, or non-obvious trap | Applicable nested instructions |
| Reusable task procedure | Skill |
| Temporary work state | Active issue or requested spec |
| Durable rationale that changes later decisions | Decision record or existing canon |
| Fact already owned by code or configuration | Reference that source |
| Generic coaching, duplicate rule, or stale state | Delete |

Create nested guidance when a distinct boundary or recurring wrong-path work
justifies it. Prefer fixing the code boundary, type, test, or script when that
removes the need for prose. Durable rules must state their operative meaning
without relying on mutable issue wording.

For recurring mistakes that can be checked mechanically, inspect existing
checks and where they run. Repair a disconnected or silently failing check
before adding another rule or enforcement mechanism.

## Retain useful constraints

Keep non-obvious project requirements and actual user preferences. Route
optional documentation by the question it answers. Avoid mandatory broad
reading, arbitrary process quotas, and repeated completion checklists.

Distinguish product invariants, preferences, and approval requirements.
An authorized change to an interface includes updating its owning contract and
relevant proof. A rule should pause only the affected action when authority or
a consequential decision is unresolved.

## Verify the result

For guidance-only edits, run `git diff --check`, check changed pointers and
removed terms, and read representative affected instruction chains. Confirm
that relocated rules have one owner and that retained constraints still apply.
Report what changed and any untested behavior claims; these checks do not
establish that the model performs better.

For discovery behavior, consult the target client's current documentation:
[Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Claude Code guidance](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md).
