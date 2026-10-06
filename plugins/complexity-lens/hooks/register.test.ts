import { describe, expect, test } from 'claude-code/testing'
import type { Engine } from 'claude-code/testing'
import type { On } from 'claude-code'

const ROW = {
  file: 'src/app.ts',
  code: 120,
  complexity: 80,
  density: 66.7,
  churn: 4,
  over_threshold_fns: 2,
  per_function_source: 'biome',
  score: 8,
  flags: [],
}

type Runs = string[][]

function fakeEngine(on: On, rows: object[], runs: Runs, exitCode = 0) {
  on('process.run', (_$, e) => {
    const argv = (e as unknown as { argv: string[] }).argv
    runs.push(argv)
    const isRank = argv.some(a => a.endsWith('complexity_rank.py'))
    return { value: { exitCode: isRank ? exitCode : 0, stdout: isRank ? JSON.stringify(rows) : 'scc 3.0', stderr: '' } } as never
  })
  on('session.start', (_$, e) => ({ cwd: e.cwd }) as never)
  on('tool.call', () => ({ result: { text: 'ok' } }) as never)
  on('ui.toast', () => ({ value: undefined }))
  on('ui.render', ($, e) => {
    const { Text } = $.ui.resolve(e)
    return h(Text, { key: 'below' }, 'other mod band') as never
  })
}

const edit = ($: Engine, tool: 'Edit' | 'Read' = 'Edit') =>
  $.tool.call({ tool, file_path: '/repo/src/app.ts' } as never)

const start = ($: Engine) => $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true } as never)

describe('complexity-lens', () => {
  test('an Edit of a file with functions over the limit adds a context line for the model', async ($, on) => {
    const runs: Runs = []
    fakeEngine(on, [ROW], runs)
    await start($)
    const result = (await edit($)) as { context?: string[] }
    expect(result.context?.[0]).toContain('src/app.ts has 2 function(s) over the per-function limit (cognitive 20, Biome)')
    expect(runs.some(argv => argv.includes('--json') && argv.includes('/repo/src/app.ts'))).toBe(true)
  })

  test('a file with no function over the limit and no hotspot score adds nothing', async ($, on) => {
    fakeEngine(on, [{ ...ROW, over_threshold_fns: 0, score: 0 }], [])
    await start($)
    const result = (await edit($)) as { context?: string[] }
    expect(result.context).toBeUndefined()
  })

  test('the band draws what the layers beneath draw plus its own rows', async ($, on) => {
    fakeEngine(on, [ROW], [])
    await start($)
    await edit($)
    const ui = await $.ui.mount({ plugin: 'complexity-lens', surface: 'terminal', component: 'AbovePrompt', props: { hasSurvey: false, bodyColumns: 100 } as never })
    expect(await ui.find({ type: 'Text', text: 'other mod band' })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /app\.ts {2}complexity 80 · 67 per 100 lines · 2 over limit · changed 4× · score 8/ })).toBeDefined()
    await ui.unmount()
  })

  test('with nothing measured the band is exactly what the layers beneath draw', async ($, on) => {
    fakeEngine(on, [ROW], [])
    await start($)
    const ui = await $.ui.mount({ plugin: 'complexity-lens', surface: 'terminal', component: 'AbovePrompt', props: { hasSurvey: false, bodyColumns: 100 } as never })
    expect(await ui.findAll({ type: 'Text' })).toHaveLength(1)
    await ui.unmount()
  })
})
