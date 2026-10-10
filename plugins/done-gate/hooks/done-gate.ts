/**
 * done-gate — Claude Mod (EARLY ACCESS)
 *
 * Blocks the main loop from ending a turn while changed files have not passed
 * the checks they need.
 *
 *   - Proof is a git tree id of the whole working tree (tracked and untracked,
 *     ignored files left out), written through a private index under .git.
 *     Edits by Edit, Write, Bash or a subagent all change it.
 *   - `tool.call` on Bash: a command matching `checks` that ends without error
 *     records the tree it passed on.
 *   - `classic.Stop`: with `resolve`, the repository's command reads the
 *     changed files and passes on stdin and prints each unmet check; without
 *     it, any file under `paths` changed since the last pass is unmet. Blocks
 *     once; the retry (`stop_hook_active`) ends the turn with a toast.
 *   - Inactive in a repository without `.claude/done-gate.json`.
 */
import type { EngineInterface, Register } from 'claude-code'
import { CONFIG_PATH, configFault, decide, decideResolved, isCheck, parseConfig } from './gate.ts'
import type { Config, Pass, Verdict } from './gate.ts'

type Repo = { root: string; config: Config } | { root: string; fault: string }

let startTree: string | undefined
let lastPassTree: string | undefined
const passTrees = new Map<string, string>()
let queue: Promise<unknown> = Promise.resolve()

const serial = <T>(work: () => Promise<T>): Promise<T> => {
  const run = queue.then(work, work)
  queue = run.catch(() => undefined)
  return run
}

async function git($: EngineInterface, cwd: string, args: string[], env?: Record<string, string>) {
  const { exitCode, stdout, stderr } = await $.process.run(['git', ...args], { cwd, env })
  if (exitCode !== 0) throw new Error(`git ${args[0]}: ${stderr.trim()}`)
  return stdout.trim()
}

async function repoOf($: EngineInterface): Promise<Repo | undefined> {
  const cwd = await $.session.cwd()
  const root = await git($, cwd, ['rev-parse', '--show-toplevel']).catch(() => undefined)
  if (root === undefined) return undefined
  const path = `${root}/${CONFIG_PATH}`
  if (!(await $.fs.exists(path))) return undefined
  const parsed = parseConfig(await $.fs.read(path))
  return 'error' in parsed ? { root, fault: parsed.error } : { root, config: parsed }
}

const treeOf = ($: EngineInterface, root: string) =>
  serial(async () => {
    const index = await git($, root, ['rev-parse', '--path-format=absolute', '--git-path', 'done-gate.index'])
    const env = { GIT_INDEX_FILE: index }
    await git($, root, ['add', '--all'], env)
    return git($, root, ['write-tree'], env)
  })

const changedBetween = async ($: EngineInterface, root: string, from: string, to: string) =>
  from === to ? [] : (await git($, root, ['diff', '--name-only', from, to])).split('\n').filter(Boolean)

async function unmetChecks($: EngineInterface, root: string, resolve: string[], start: string, now: string) {
  const passes: Pass[] = []
  for (const [command, tree] of passTrees) {
    passes.push({ command, changed: await changedBetween($, root, tree, now) })
  }
  const stdin = JSON.stringify({ changed: await changedBetween($, root, start, now), passes })
  const { exitCode, stdout, stderr } = await $.process.run(resolve, { cwd: root, stdin })
  if (exitCode !== 0) throw new Error(`resolve exited ${exitCode}: ${stderr.trim()}`)
  return stdout.split('\n').map(line => line.trim()).filter(Boolean)
}

async function verdictAtStop($: EngineInterface, isRetry: boolean): Promise<Verdict> {
  const repo = await repoOf($)
  if (repo === undefined) return { kind: 'pass' }
  if ('fault' in repo) return isRetry ? { kind: 'pass' } : configFault(repo.fault)
  const now = await treeOf($, repo.root)
  startTree ??= now
  if (repo.config.resolve !== undefined) {
    const unmet = await unmetChecks($, repo.root, repo.config.resolve, startTree, now)
    return decideResolved({ unmet, isRetry })
  }
  const unproven = await changedBetween($, repo.root, lastPassTree ?? startTree, now)
  return decide({ config: repo.config, unproven, isRetry })
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const repo = await repoOf($).catch(() => undefined)
    if (repo !== undefined) startTree = await treeOf($, repo.root).catch(() => undefined)
    return next(e)
  })

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const ran = await next(e)
    if (ran.deny !== undefined || ran.isError === true) return ran
    const repo = await repoOf($).catch(() => undefined)
    if (repo !== undefined && 'config' in repo && isCheck(repo.config, e.command)) {
      const tree = await treeOf($, repo.root).catch(() => undefined)
      if (tree !== undefined) {
        lastPassTree = tree
        passTrees.set(e.command.trim(), tree)
      }
    }
    return ran
  })

  on('classic.Stop', async ($, e, next) => {
    const verdict = await verdictAtStop($, e.stop_hook_active)
    if (verdict.kind === 'block') return { block: verdict.reason }
    if (verdict.kind === 'release') $.ui.toast(`done-gate: ${verdict.reason}`)
    return next(e)
  }).catch(($, e, next) =>
    e.stop_hook_active || next.called
      ? next(e)
      : { block: 'done-gate: its check failed to run. Say in your reply that the work is unverified.' },
  )
}
