// Run with: claude plugin test plugins/done-gate
import { describe, expect, test } from 'claude-code/testing'
import type { Engine } from 'claude-code/testing'
import type { On } from 'claude-code'

type Files = Record<string, string>
type Repo = { files: Files; resolveInputs: { changed: string[]; passes: { command: string; changed: string[] }[] }[] }

function fakeRepo(on: On, onBash: (command: string, files: Files) => void = () => {}): Repo {
  const repo: Repo = { files: { 'src/a.ts': '1', 'src/b.ts': '1' }, resolveInputs: [] }
  const trees: Files[] = []
  const ok = (stdout = '') => ({ value: { exitCode: 0, stdout, stderr: '' } }) as never
  on('session.start', ($, e) => ({ cwd: e.cwd }) as never)
  on('classic.Stop', () => ({}))
  on('session.cwd', () => ({ value: '/repo' }))
  on('fs.exists', ($, e) => ({ value: e.path === '/repo/.claude/done-gate.json' }))
  on('fs.read', () => ({ value: JSON.stringify({ checks: ['^bash verify\\.sh'], resolve: ['resolve'] }) }) as never)
  on('process.run', ($, e) => {
    const [cmd, ...args] = e.argv
    if (cmd === 'resolve') {
      repo.resolveInputs.push(JSON.parse(e.init?.stdin ?? '{}'))
      return ok()
    }
    if (args[0] === 'rev-parse') return ok(args.includes('--show-toplevel') ? '/repo' : '/repo/.git/done-gate.index')
    if (args[0] === 'add') return ok()
    if (args[0] === 'write-tree') return ok(String(trees.push({ ...repo.files }) - 1))
    if (args[0] === 'diff') {
      const [from, to] = [trees[Number(args[2])] ?? {}, trees[Number(args[3])] ?? {}]
      return ok([...new Set([...Object.keys(from), ...Object.keys(to)])].filter(f => from[f] !== to[f]).sort().join('\n'))
    }
    throw new Error(`unexpected command ${e.argv.join(' ')}`)
  })
  on('tool.call', ($, e) => {
    const input = e as unknown as { tool: string; command?: string; file_path?: string }
    if (input.tool === 'Bash') onBash(input.command ?? '', repo.files)
    if (input.file_path !== undefined) repo.files[input.file_path.replace('/repo/', '')] = 'edited'
    return { result: { text: 'ok' } } as never
  })
  return repo
}

const start = ($: Engine) => $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true } as never)
const bash = ($: Engine, command: string) => $.tool.call({ tool: 'Bash', command } as never)
const stop = ($: Engine) => $.classic.Stop({ stop_hook_active: false } as never) as Promise<{ block?: string }>

describe('done-gate counts only what this session changed', () => {
  test('a branch switch and another agent\'s edit are not the session\'s changes', async ($, on) => {
    const repo = fakeRepo(on, (command, files) => {
      if (command === 'git checkout other') Object.assign(files, { 'src/a.ts': '2', 'src/branch-only.ts': '1' })
    })
    await start($)
    await bash($, 'git checkout other')
    repo.files['src/b.ts'] = 'codex'
    await $.tool.call({ tool: 'Edit', file_path: '/repo/src/mine.ts', old_string: 'a', new_string: 'b' } as never)
    await stop($)
    expect(repo.resolveInputs.at(-1)?.changed).toEqual(['src/mine.ts'])
  })

  test('a file changed by a Bash command counts, and a later pass covers it', async ($, on) => {
    const repo = fakeRepo(on, (command, files) => {
      if (command.startsWith('sed -i')) files['src/a.ts'] = 'sed'
    })
    await start($)
    await bash($, "sed -i 's/1/2/' src/a.ts")
    await bash($, 'bash verify.sh')
    repo.files['src/b.ts'] = 'codex'
    await stop($)
    expect(repo.resolveInputs.at(-1)).toEqual({ changed: ['src/a.ts'], passes: [{ command: 'bash verify.sh', changed: [] }] })
  })

  test('a chained command that also edits after a checkout still counts its edit', async ($, on) => {
    const repo = fakeRepo(on, (command, files) => {
      if (command.includes('&&')) Object.assign(files, { 'src/a.ts': '2', 'src/b.ts': 'sed' })
    })
    await start($)
    await bash($, "git checkout other && sed -i 's/1/2/' src/b.ts")
    await stop($)
    expect(repo.resolveInputs.at(-1)?.changed).toEqual(['src/a.ts', 'src/b.ts'])
  })
})
