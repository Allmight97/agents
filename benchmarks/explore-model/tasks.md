# Tasks

Each task is one Explore subagent call against `/Users/jstar/Projects/audiobook-boss`
(read only). Every combination gets the same prompt text. Only `model` and
`effort` change. The description must start `bench T<n> c<k>` (round 1) or
`b2 R<n> k<k> r<rep>` (round 2) so `cost.py` can find the run.

Every prompt ends with the same report shape:

> Report: ANSWER (each hop or location as path:line function), CONFIDENCE
> (high/medium/low with one reason), WRONG_LEADS (leads checked that turned
> out wrong). Under 400 words.

## Round 1: ordinary searches

- **T1 cross-boundary trace.** Trace the Audible sign-in path from the
  frontend code that starts sign-in, through the Tauri IPC command, to the
  Rust code that stores the credential.
- **T2 guard and callers.** When the user selects a title from metadata lookup
  or search results, where does the app detect and drop a stale result (one
  that arrives after the selection or query changed)? Name the function that
  makes that check and every function that calls it.
- **T3 negative finding.** Which Rust functions compute or write the iTunSMPB
  gapless-timing tag, and what is the call chain from the encode/processing
  job down to them? (Correct answer: no Rust code writes it.)
- **T4 locator and runner.** During decryption of an Audible title, how does
  the engine reach the AAXClean helper? Name the function that locates the
  helper binary, the function that runs it, and the call chain from the
  decrypt job down to them.
- **T5 exhaustive list.** List every Tauri command the desktop host
  registers, and for each one the Rust file and function that handles it. Say
  where they are registered.

## Round 2: harder searches

- **R1 exhaustive breadth.** List every place in the crates/abb-engine
  production code (not tests) that produces SessionOutcome::Superseded, as
  path:line and the enclosing function.
- **R2 false premise.** Where does the frontend (TypeScript under src/)
  validate or normalize metadata field values such as title, author, or
  narrator before sending them to the engine? (Correct answer: it does not.)
- **R3 tedious cross-check.** Which entries in
  scripts/rust-complexity-allowlist.txt name a function that no longer exists
  in the named file? (Correct answer at the pinned commit: none.)
- **R4 careful read.** In crates/abb-engine/src/session/runtime.rs, list every
  condition under which begin_lookup_apply returns without starting an apply,
  what state (if any) it changes on that path, and which SessionOutcome each
  path produces. Also say what happens on the success path.
