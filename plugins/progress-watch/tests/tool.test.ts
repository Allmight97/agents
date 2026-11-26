import { expect, test } from 'claude-code/testing'

const WATCH = 'mcp__progress-watch__watch'

test('the tool reads its arguments, says what is wrong, and reports no jobs', async $ => {
  expect(JSON.stringify(await $.tool.call({ tool: WATCH, action: 'start' }))).toContain('give a log file')
  expect(JSON.stringify(await $.tool.call({ tool: WATCH, action: 'stop' }))).toContain('no watch is running')
  expect(JSON.stringify(await $.tool.call({ tool: WATCH, action: 'status' }))).toContain('no jobs followed')
})

test('a background Bash job is followed by itself, and its exit notice ends it', async ($, on) => {
  on('tool.call', { tool: 'Bash' }, () => ({
    result: { stdout: '', stderr: '', interrupted: false, backgroundTaskId: 'b1' },
    text: 'Command running in background with ID: b1. Output is being written to: /nowhere/b1.output. You will be notified',
  }))
  await $.tool.call({ tool: 'Bash', command: 'make test', description: 'run the tests', run_in_background: true })
  expect(JSON.stringify(await $.tool.call({ tool: WATCH, action: 'status' }))).toContain('b1 [shell] run the tests')
  await $.session.append({
    message: { type: 'user', role: 'user', content: [{ type: 'text', text: '<task-notification>\n<task-id>b1</task-id>\n<status>failed</status>\n<summary>exit code 3</summary>\n</task-notification>' }] },
    door: 'queue',
    origin: { kind: 'engine' },
    uuid: '00000000-0000-4000-8000-000000000001',
  })
  let status = ''
  for (let i = 0; i < 50 && !status.includes('· failed'); i += 1) status = JSON.stringify(await $.tool.call({ tool: WATCH, action: 'status' }))
  expect(status).toContain('run the tests · failed')
})
