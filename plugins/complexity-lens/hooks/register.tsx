import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Row, Shown } from '../types'

const rows = atom({ plugin: 'complexity-lens', key: 'rows' } as const, [])
const problem = atom({ plugin: 'complexity-lens', key: 'problem' } as const, null)

const WATCHED = ['Read', 'Edit', 'Write'] as const
const SHOWN = 4
const CODE = /\.(rs|ts|tsx|js|jsx|py|go)$/

async function measure($: EngineInterface, path: string): Promise<Shown | undefined> {
  try {
    const ran = await $.process.run(
      ['python3', `${$.plugin.root}/scripts/complexity_rank.py`, '--json', path],
      { timeoutMs: 20000, cwd: path.slice(0, path.lastIndexOf('/')) || '/' },
    )
    if (ran.exitCode !== 0) {
      await update($, problem, () => `rank exit ${ran.exitCode}`)
      return undefined
    }
    const [measured] = JSON.parse(ran.stdout) as Row[]
    if (!measured) return undefined
    const before = (await read($, rows)).find(r => r.file === measured.file)
    const row: Shown = { ...measured, baseline: before ? before.baseline : measured.over_threshold_fns }
    await update($, rows, list => [row, ...list.filter(r => r.file !== row.file)].slice(0, 12))
    if (grew(row)) {
      $.ui.toast(`${row.file}: functions over limit ${row.baseline} → ${row.over_threshold_fns}`)
    }
    await update($, problem, () => null)
    return row
  } catch (err) {
    await update($, problem, () => `rank failed: ${String(err).slice(0, 60)}`)
    return undefined
  }
}

function grew(r: Shown): boolean {
  return r.over_threshold_fns !== null && r.baseline !== null && r.over_threshold_fns > r.baseline
}

type Level = 'grew' | 'over' | 'calm'

function level(r: Shown): Level {
  if (grew(r)) return 'grew'
  return (r.over_threshold_fns ?? 0) > 0 ? 'over' : 'calm'
}

const LEVEL_RANK: Record<Level, number> = { grew: 0, over: 1, calm: 2 }
const LEVEL_COLOR: Record<Level, string | undefined> = { grew: 'red', over: 'yellow', calm: undefined }

function agentNote(row: Shown): string | undefined {
  const over = row.over_threshold_fns ?? 0
  if (over === 0 && row.score === 0 && !grew(row)) return undefined
  const change = grew(row) ? ` (was ${row.baseline} at the start of this request)` : ''
  const limit =
    row.per_function_source === 'lizard'
      ? 'cyclomatic 10, lizard'
      : row.per_function_source === 'biome'
        ? 'cognitive 20, Biome'
        : 'not counted'
  return (
    `complexity-lens: ${row.file} has ${row.over_threshold_fns ?? 'unknown'} function(s) over the per-function limit (${limit})${change}; ` +
    `file complexity ${row.complexity}, ${row.density} per 100 lines, recent churn ${row.churn ?? 'n/a'}, hotspot score ${row.score}` +
    `${row.flags.length ? ` [${row.flags.join(', ')}]` : ''}. Keep new functions under the limit, or name the reason.`
  )
}

function overText(r: Shown): string | undefined {
  if (r.over_threshold_fns === null) return undefined
  return grew(r) ? `${r.over_threshold_fns} over limit (+${r.over_threshold_fns - (r.baseline ?? 0)})` : `${r.over_threshold_fns} over limit`
}

function details(r: Shown): string {
  const notes = r.flags.map(f => (f === 'scc-only' ? 'rough' : f === 'young' ? 'new file' : f))
  const parts = [
    `complexity ${r.complexity}`,
    `${Math.round(r.density)} per 100 lines`,
    `changed ${r.churn ?? '?'}×`,
    `score ${r.score}`,
  ]
  return `${parts.join(' · ')}${notes.length ? `  (${notes.join(', ')})` : ''}`
}

export const register: Register = on => {
  let scc = true

  on('session.start', async ($, e, next) => {
    try {
      await $.process.run(['scc', '--version'], { timeoutMs: 5000 })
    } catch (err) {
      scc = false
      await update($, problem, () => `scc unavailable: ${String(err).slice(0, 60)}`)
    }
    return next(e)
  })

  on('prompt.submit', async ($, e, next) => {
    await update($, rows, () => [])
    await update($, problem, () => null)
    return next(e)
  })

  on('tool.call', { tool: WATCHED }, async ($, e, next) => {
    const result = await next(e)
    const path = e.file_path
    if (!scc || !path || result.deny !== undefined || result.isError || !CODE.test(path)) return result
    if (e.tool === 'Read') {
      void measure($, path)
      return result
    }
    const measured = await measure($, path)
    const note = measured ? agentNote(measured) : undefined
    return note ? { ...result, context: [...(result.context ?? []), note] } : result
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const list = await read($, rows)
    const issue = await read($, problem)
    if (list.length === 0 && issue === null) return next(e)

    const below = await next(e)
    const { Box, Text } = $.ui.resolve(e)
    const top = [...list]
      .sort((a, b) => LEVEL_RANK[level(a)] - LEVEL_RANK[level(b)] || b.score - a.score || b.complexity - a.complexity)
      .slice(0, SHOWN)

    return (
      <Box flexDirection="column">
        {below}
        {issue !== null ? <Text color="yellow">complexity-lens: {issue}</Text> : null}
        {top.map(r => {
          const lvl = level(r)
          const over = overText(r)
          return (
            <Box key={r.file} flexDirection="row" columnGap={1}>
              <Text color={LEVEL_COLOR[lvl]} bold={lvl === 'grew'} dimColor={lvl === 'calm'}>
                {r.file.split('/').slice(-2).join('/')}
              </Text>
              {over === undefined ? null : (
                <Text color={LEVEL_COLOR[lvl]} bold={lvl === 'grew'} dimColor={lvl === 'calm'}>
                  {over}
                </Text>
              )}
              <Text dimColor wrap="truncate-end">
                {details(r)}
              </Text>
            </Box>
          )
        })}
      </Box>
    )
  })
}
