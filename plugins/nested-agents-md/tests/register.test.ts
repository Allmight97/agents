import { describe, expect, test } from 'claude-code/testing'
import type { Engine } from 'claude-code/testing'
import type { On } from 'claude-code'

const ROOT = '/repo'
const FILES = ['/repo/sub/calc.py', '/repo/sub/deep/x.py', '/repo/top.py', '/repo/claude/y.py']
const DIRS = ['/repo', '/repo/sub', '/repo/sub/deep', '/repo/sub2', '/repo/claude']
const AGENTS: Record<string, string> = {
  '/repo': '# root\n',
  '/repo/sub': '# sub rules\n',
  '/repo/sub/deep': '# deep rules\n',
  '/repo/sub2': '# sub2 rules\n',
  '/repo/claude': '# shadowed\n',
}
const CLAUDE: Record<string, string> = { '/repo/claude': '# claude dir\n' }

function projectOf(on: On, claudeAtRoot = false) {
  on('session.root', () => ({ value: ROOT }))
  on('session.cwd', () => ({ value: ROOT }))
  on('env.get', ($, e) => ({ value: e.name === 'HOME' ? '/home/me' : undefined }) as never)
  on('fs.stat', ($, e) => {
    const path = e.path
    const kind = FILES.includes(path) ? 'file' : DIRS.includes(path) ? 'dir' : undefined

    if (kind === undefined) {
      throw new Error('ENOENT')
    }

    return { value: { kind, size: 1, mtimeMs: 0, isLink: false } } as never
  })
  on('fs.ancestors', ($, e) => {
    const table = e.names.includes('AGENTS.md') ? AGENTS : CLAUDE

    if (e.of === undefined) {
      return { value: claudeAtRoot && table === CLAUDE ? [ancestor('/repo', 'CLAUDE.md', '#')] : [] }
    }

    const dirs = Object.keys(table).filter(dir => e.of?.startsWith(`${dir}/`) && dir.startsWith(`${ROOT}/`))
    const name = table === AGENTS ? 'AGENTS.md' : 'CLAUDE.md'

    return { value: dirs.sort().map(dir => ancestor(dir, name, table[dir] ?? '')) }
  })
  on('tool.call', () => ({ result: { text: 'ok' } }) as never)
}

const ancestor = (dir: string, name: string, content: string) => ({
  dir,
  name,
  content,
  parts: [{ path: `${dir}/${name}`, content }],
})

const bash = async ($: Engine, command: string) =>
  ((await $.tool.call({ tool: 'Bash', command } as never)) as { context?: string[] }).context ?? []

const fileTool = async ($: Engine, tool: 'Read' | 'Edit' | 'Write', file_path: string) =>
  ((await $.tool.call({ tool, file_path, content: 'x' } as never)) as { context?: string[] }).context ?? []

describe('nested-agents-md', () => {
  test('a shell read attaches the nested AGENTS.md chain, root excluded', async ($, on) => {
    projectOf(on)
    const context = await bash($, 'sed -n 1,20p sub/deep/x.py | head')

    expect(context).toEqual([
      'Contents of /repo/sub/AGENTS.md:\n\n# sub rules\n',
      'Contents of /repo/sub/deep/AGENTS.md:\n\n# deep rules\n',
    ])
  })

  test('each file attaches once per conversation', async ($, on) => {
    projectOf(on)
    await bash($, 'cat sub/calc.py')

    expect(await bash($, "grep -n 'def' /repo/sub/calc.py")).toEqual([])
  })

  test('after a Read the shell does not attach what the Read covered', async ($, on) => {
    projectOf(on)

    expect(await fileTool($, 'Read', '/repo/sub/calc.py')).toEqual([])
    expect(await bash($, 'cat sub/deep/x.py')).toEqual(['Contents of /repo/sub/deep/AGENTS.md:\n\n# deep rules\n'])
  })

  test('a Write of a new file attaches its folder chain', async ($, on) => {
    projectOf(on)

    expect(await fileTool($, 'Write', '/repo/sub2/new.py')).toEqual(['Contents of /repo/sub2/AGENTS.md:\n\n# sub2 rules\n'])
  })

  test('a shell write to a new file attaches its folder chain', async ($, on) => {
    projectOf(on)

    expect(await bash($, "cat > sub2/new.py <<'EOF'\nx = 1\nEOF")).toEqual(['Contents of /repo/sub2/AGENTS.md:\n\n# sub2 rules\n'])
  })

  test('a path after cd resolves against that folder', async ($, on) => {
    projectOf(on)

    expect(await bash($, 'cd sub && head -2 deep/x.py')).toEqual([
      'Contents of /repo/sub/AGENTS.md:\n\n# sub rules\n',
      'Contents of /repo/sub/deep/AGENTS.md:\n\n# deep rules\n',
    ])
  })

  test('a path spelled with .. resolves to the file it names', async ($, on) => {
    projectOf(on)

    expect(await bash($, 'head -2 ./sub/deep/../calc.py')).toEqual(['Contents of /repo/sub/AGENTS.md:\n\n# sub rules\n'])
  })

  test('a repo-wide search and words that are not files attach nothing', async ($, on) => {
    projectOf(on)

    expect(await bash($, 'grep -rn "sub/calc" . && git status && ls sub')).toEqual([])
  })

  test('a folder with its own CLAUDE.md is left to the engine', async ($, on) => {
    projectOf(on)

    expect(await bash($, 'cat claude/y.py')).toEqual([])
  })

  test('a project with a CLAUDE.md is left to the engine', async ($, on) => {
    projectOf(on, true)

    expect(await bash($, 'cat sub/calc.py')).toEqual([])
  })

  test('a new conversation context sends the files again', async ($, on) => {
    projectOf(on)
    on('prompt.context', ($, e) => ({ blocks: e.blocks, instructionFiles: e.instructionFiles }))
    await bash($, 'cat sub/calc.py')
    await $.prompt.context({ blocks: [], instructionFiles: [] })

    expect(await bash($, 'cat sub/calc.py')).toEqual(['Contents of /repo/sub/AGENTS.md:\n\n# sub rules\n'])
  })
})
