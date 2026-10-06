# nested-agents-md

A Claude Code mod. Claude Code's built-in `agents-md` mod loads a nested
`AGENTS.md` only when Claude opens a file with the Read tool. Files Claude
reads or changes through Bash (`cat`, `sed`, heredocs) or the Edit and Write
tools get no nested guidance. This mod closes that gap.

When a Bash command names a file under the project root, or Edit or Write
changes one, the mod attaches each `AGENTS.md` between the root and that file
that this conversation has not had yet. It uses the same
`Contents of <path>:` frame as `agents-md`.

- Bash: words in the command that are existing files, plus redirect and `tee`
  targets (a heredoc that creates a file). Directories, patterns, and command
  output count for nothing, so `grep -rn foo .` attaches nothing.
- Read: attaches nothing, but marks what `agents-md` delivers so the mod does
  not send it again. The reverse cannot be known: a file this mod sent first
  comes once more on a later Read of that folder.
- Like `agents-md` in its default mode: a project with its own `CLAUDE.md`, or
  a folder with one, is left to the engine. Each file goes once per
  conversation and again after compaction or `/clear`.

Why it exists: anthropics/claude-code#90450. In Auto and bypass modes Claude
Code tells the model to prefer Bash for reads and edits, so nested `AGENTS.md`
never load. Delete this mod when Claude Code loads nested `AGENTS.md` on every
file access.

Needs Claude Code 2.1.287 or later (mods are on by default). Test with
`claude plugin test plugins/nested-agents-md`.
