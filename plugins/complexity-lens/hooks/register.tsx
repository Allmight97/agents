import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Row } from '../types'

const rows = atom({ plugin: 'complexity-lens', key: 'rows' } as const, [])
const problem = atom({ plugin: 'complexity-lens', key: 'problem' } as const, null)

const WATCHED = ['Read', 'Edit', 'Write'] as const
const SHOWN = 4
const CODE = /\.(rs|ts|tsx|js|jsx|py|go)$/

async function measure($: EngineInterface, path: string): Promise<{ row: Row; before?: Row } | undefined> {
  try {
    const ran = await $.process.run(
      ['python3', `${$.plugin.root}/scripts/complexity_rank.py`, '--json', path],
      { timeoutMs: 20000 },
    )
    if (ran.exitCode !== 0) {
      await update($, problem, () => `rank exit ${ran.exitCode}`)
      return undefined
    }
    const [row] = JSON.parse(ran.stdout) as Row[]
    if (!row) return undefined
    const before = (await read($, rows)).find(r => r.file === row.file)
    await update($, rows, list =>
      [row, ...list.filter(r => r.file !== row.file)].slice(0, 12),
    )
    if (
      before &&
      row.over_threshold_fns !== null &&
      before.over_threshold_fns !== null &&
      row.over_threshold_fns > before.over_threshold_fns
    ) {
      $.ui.toast(`${row.file}: functions over limit ${before.over_threshold_fns} → ${row.over_threshold_fns}`)
    }
    await update($, problem, () => null)
    return { row, before }
  } catch (err) {
    await update($, problem, () => `rank failed: ${String(err).slice(0, 60)}`)
    return undefined
  }
}

function agentNote(row: Row, before?: Row): string | undefined {
  const over = row.over_threshold_fns ?? 0
  const grew =
    before !== undefined &&
    row.over_threshold_fns !== null &&
    before.over_threshold_fns !== null &&
    row.over_threshold_fns > before.over_threshold_fns
  if (over === 0 && row.score === 0 && !grew) return undefined
  const change = grew ? ` (was ${before?.over_threshold_fns}; this edit added one)` : ''
  return (
    `complexity-lens: ${row.file} has ${row.over_threshold_fns ?? 'unknown'} function(s) over the per-function limit (${row.per_function_source === 'lizard' ? 'cyclomatic 10, lizard' : row.per_function_source === 'biome' ? 'cognitive 20, Biome' : 'not counted'})${change}; ` +
    `file complexity ${row.complexity}, ${row.density} per 100 lines, recent churn ${row.churn ?? 'n/a'}, hotspot score ${row.score}` +
    `${row.flags.length ? ` [${row.flags.join(', ')}]` : ''}. Keep new functions under the limit, or name the reason.`
  )
}


function label(r: Row): string {
  const parts = [
    `complexity ${r.complexity}`,
    `${Math.round(r.density)} per 100 lines`,
    ...(r.over_threshold_fns === null ? [] : [`${r.over_threshold_fns} over limit`]),
    `changed ${r.churn ?? '?'}×`,
    `score ${r.score}`,
  ]
  const notes = r.flags.map(f => (f === 'scc-only' ? 'rough' : f === 'young' ? 'new file' : f))
  const name = r.file.split('/').slice(-2).join('/')
  return `${name}  ${parts.join(' · ')}${notes.length ? `  (${notes.join(', ')})` : ''}`
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

  on('tool.call', { tool: WATCHED }, async ($, e, next) => {
    const result = await next(e)
    const path = e.file_path
    if (!scc || !path || result.deny !== undefined || result.isError || !CODE.test(path)) return result
    if (e.tool === 'Read') {
      void measure($, path)
      return result
    }
    const measured = await measure($, path)
    const note = measured ? agentNote(measured.row, measured.before) : undefined
    return note ? { ...result, context: [...(result.context ?? []), note] } : result
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const list = await read($, rows)
    const issue = await read($, problem)
    if (list.length === 0 && issue === null) return next(e)

    const below = await next(e)
    const { Box, Text } = $.ui.resolve(e)
    const top = [...list].sort((a, b) => b.score - a.score || b.complexity - a.complexity).slice(0, SHOWN)

    return (
      <Box flexDirection="column">
        {below}
        {issue !== null ? <Text color="yellow">complexity-lens: {issue}</Text> : null}
        {top.map(r => (
          <Text key={r.file} dimColor={r.score === 0}>
            {label(r)}
          </Text>
        ))}
      </Box>
    )
  })
}
