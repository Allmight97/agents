import { expect, test } from 'claude-code/testing'

const PANE = {
  plugin: 'progress-watch',
  component: 'Pane',
  requestId: 'progress',
  props: { title: 'progress', isFocused: false, bodyColumns: 80, placement: 'dock', scroll: { offset: 0, bodyRows: 30 }, view: {} },
} as const

test('the pane says jobs appear by themselves when there are none, on every surface', async $ => {
  for (const surface of ['terminal', 'desktop', 'mobile'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect((await ui.find({ type: 'Text', text: /No jobs yet/ }))?.text).toContain('by themselves')
    await ui.unmount()
  }
})

test('the pane shows a running job with its figures and events', async ($, on) => {
  const now = Date.now()
  const job = { id: 'w1', source: 'watch', label: 'refactor', startedAt: now - 3_600_000, status: 'running', logs: [{ path: '/l.log', offset: 0 }], repo: '/r', branch: 'b', commits: 2, lastCommit: 'abc fix', lastCommitAt: now, phase: 'tests', errors: 1, lastError: 'error: boom', lastActivityAt: now, quietMs: 720000 }
  const values: Record<string, unknown> = {
    jobs: { shape: 'jobs-1', value: [job] },
    events: { shape: 'events-1', value: [{ at: now, kind: 'error', text: 'refactor: error: boom' }] },
    system: { shape: 'system-1', value: { at: now, load1: 2.5, cpus: 16, freeBytes: 2 ** 33, totalBytes: 2 ** 35 } },
    heartbeatAt: { shape: 'heartbeat-1', value: now },
  }
  on('state.get', (_, e) => ({ value: { value: values[e.key], version: 1 } }))
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect((await ui.find({ type: 'Text', text: /^refactor/ }))?.text).toContain('phase tests · 2 commits')
  expect((await ui.find({ type: 'Text', text: /^load/ }))?.text).toMatch(/^load 2\.5\/16 · free 8\.0G of 32\.0G/)
  expect((await ui.find({ type: 'Text', text: /error: boom$/ }))?.text).toMatch(/error refactor: error: boom$/)
  await ui.unmount()
})
