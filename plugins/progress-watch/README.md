# progress-watch

A Claude Code mod that shows what long background work is doing, in a row above
the prompt. Nobody starts it. Every background Bash job and background subagent
appears by itself and leaves when it ends.

It only shows. No update starts a conversation turn. A job's exit wakes the
agent through Claude Code's own notification, so the agent needs no watcher of
its own; Monitor stays for an event that must wake the agent.

## What it shows

The row has one line per job, at most three, problems first:

```
> run the tests · phase integration · 14m · load 3.4/16 · free 22.2G of 48.0G
! nightly build · 2 errors, last: error[E0308]: mismatched types · 41m
~ cargo build · 22m · no activity for 13m
```

- `>` running, `!` an error was seen or the job failed, `~` no activity for 12
  minutes, `.` ended. An ended job stays for 2 minutes.
- A shell job's phase comes from lines `phase: <name>` in its output. Its errors
  come from output lines such as `error:`, `fatal:`, `FAILED`, `panicked` and
  `Traceback`.
- A subagent shows its state and activity, plus phases and errors from any
  background command it started. Its own output is a transcript, not text.
- `~` means no new output. A silent build step is normal, so the mod does not
  call the job dead.

`/progress` opens a pane with every job, its paths and warnings, the system
figures with a 10-minute heartbeat, and the newest events first. Errors, the `~`
flag and failed or killed jobs also raise a toast.

## Adding to it

Use these when a job writes somewhere other than its own output, or to follow
commits. A watch ends on a log line `phase: done` or on `stop`. A worker writing
a watched log must be told the `phase:` format; `status` warns when a log has
lines but no phase line.

```
/progress log <file[,file]> [label]
/progress start <repo path> <branch> [file[,file] | -] [label]
/progress status
/progress stop [id]
```

The agent uses the tool `mcp__progress-watch__watch`: `action` `status`, `start`
(`logs`, `repo` and `branch`, `label`, `quietMinutes`, `errorPattern`) or `stop`
(`id`). `errorPattern` replaces the default error rule for one watch.

## What it cannot show

- **Output path:** Claude Code names a shell job's output file only in text
  written for the model, so the mod reads the path from that text. If the
  wording changes, the row says `output path unknown` and an error event appears;
  the job's end still shows.
- **After a restart:** a resumed session starts with no jobs. Claude Code ends
  background work with its session and tells the agent, so a watch must be
  started again.
- **Auto-followed jobs** use the 12-minute limit and the default error rule. Only
  a watch can change them.
- **CPU and memory** come from `sysctl` and `vm_stat`, so they work on macOS only.
  Elsewhere an error event says so and the rest keeps working.

## Install

Needs function hooks (Claude Code 2.1.287 or later).

```bash
claude plugin install progress-watch@personal
```

Test with `claude plugin test plugins/progress-watch`.
