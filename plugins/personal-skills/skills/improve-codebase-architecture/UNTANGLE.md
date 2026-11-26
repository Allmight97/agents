# Untangle A Whole Codebase

Use when the user asks to untangle or refactor the whole codebase, or a named
area of it, to the end. This mode changes code; a scan-only request stays with
the Explore and Recommend steps in [SKILL.md](SKILL.md). It uses the lens there
(hidden links, needless links, surplus, special cases) and the
`codebase-design` vocabulary.

## 1. List every problem

Change nothing yet. Walk the whole scope with the lens and write every problem
into a decision log: one line each, with a `file:line` and what goes wrong.
Record every special case too. Keep the log outside the source tree (OS temp)
unless the repository names a place for it; it carries the work across
compaction and sessions.

Useful aids:

- Strip function bodies with a script so the whole codebase fits in context.
- Have subagents summarize parts of the codebase so you can reason across all
  of it.
- Script a dependency graph of what imports what, and rerun it as you go.
- Use git history as evidence of how often pieces change and what changes
  together.

## 2. Redesign from first principles

Work out each fix as if the system had known today's requirements from the
start. Look for the one fix behind several problems; do not fix special cases
one by one. Test every fix against the lens: pieces that change together end up
together, pieces that do not are not tied, and everything depends on what
changes less. Write each fix in the log above the problems it solves:

```md
- Make the general `Dialog` return focus to whatever had it before it opened,
  so the wait and the flag can both go.
  - `ui/LogoutDialog.tsx:30` waits 100ms after closing for the input to take focus.
  - `ui/SettingsDialog.tsx:61` sets a global `skipRefocus` flag to stop that.
```

Done when every problem line sits under a fix or is marked kept, with its
reason.

## 3. Fix everything on the list

Start where the most problems meet. Apply the fixes. Remove the special cases
the redesign makes unnecessary and keep the ones the system still needs. Do
not hunt for bugs separately; a structural fix may remove some, and the report
in step 5 names them.

## 4. Check and repeat until done

Search the result for special cases, hidden links, needless links, and
surplus, then fix what they find: use fresh subagents where the client
supports them, otherwise a fresh pass from the log alone. Stop only when:

- every remaining special case is in the log with the requirement that keeps
  it;
- a typical change lands in one place;
- no import points at a module more volatile than itself;
- the fresh pass finds nothing left worth fixing;
- intended behavior is the same as at the start, apart from bugs the refactor
  fixed, proven by the repository's checks at the end.

## 5. Report

Report the log path, the fixes applied, the special-case count before and
after, and the bugs the refactor removed.
