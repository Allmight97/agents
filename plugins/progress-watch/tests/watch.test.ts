import { expect, test } from 'claude-code/testing'

import { DEFAULT_QUIET_MS, isQuiet, jobLine, jobMarker, newJob, outputPathFrom, parseCommits, parseStartArgs, parseTaskNotification, parseVmStat, requestProblem, scanLog, shownJobs, utf8Length, warnings } from '../hooks/watch.ts'

test('phase lines and real error lines are found', () => {
  const found = scanLog(['phase: tests', 'error[E0308]: mismatched types', 'fatal: not a git repository', "thread 'main' panicked at src/a.rs", 'test a::b ... FAILED', 'FAILED src/x.py', 'Traceback (most recent call last):'].join('\n'))
  expect(found.phases).toEqual(['tests'])
  expect(found.errors.length).toBe(6)
})

test('lines from a passing run are not errors', () => {
  const clean = ['cache-on-failure: true', 'test errors::tests::parse ... ok', 'test errors::tests::format ... ok', 'test errors::tests::round_trip ... ok', 'WARN Log rotation failed', 'Failed:     0, Passed: 9', 'no errors found', '0 failed']
  expect(scanLog(clean.join('\n')).errors).toEqual([])
})

test('a pattern per watch replaces the default rule', () => {
  expect(scanLog('BOOM here\nerror: not counted', 'BOOM').errors).toEqual(['BOOM here'])
})

test('a task notification gives its id, status and summary', () => {
  const text = '<task-notification>\n<task-id>b1</task-id>\n<status>failed</status>\n<summary>Background command "x" failed with exit code 3</summary>\n</task-notification>'
  expect(parseTaskNotification(text)).toEqual({ id: 'b1', status: 'failed', summary: 'Background command "x" failed with exit code 3' })
  expect(parseTaskNotification('plain text')).toBeUndefined()
})

test('the output path comes from the tool text, spaces included', () => {
  expect(outputPathFrom('Command running in background with ID: b1. Output is being written to: /tmp/a b/b1.output. You will be notified')).toBe('/tmp/a b/b1.output')
  expect(outputPathFrom('other words')).toBeUndefined()
})

test('git log output becomes commits, oldest first', () => {
  expect(parseCommits('bbb\x1fsecond\x1f200\naaa\x1ffirst\x1f100\n').map(c => c.sha)).toEqual(['aaa', 'bbb'])
})

test('free memory counts free, inactive, speculative and purgeable pages', () => {
  const vm = 'Mach Virtual Memory Statistics: (page size of 16384 bytes)\nPages free: 10.\nPages active: 99.\nPages inactive: 20.\nPages speculative: 1.\nPages purgeable: 1.\n'
  expect(parseVmStat(vm)).toBe(32 * 16384)
})

test('a job line names what is known, and a quiet job says so without calling it dead', () => {
  const now = 3_600_000
  const j = newJob({ id: 'b1', source: 'shell', label: 'build', phase: 'tests', errors: 1, lastError: 'error: boom', startedAt: 0, lastActivityAt: now - DEFAULT_QUIET_MS }, now)
  expect(isQuiet(j, now)).toBe(true)
  expect(jobLine(j, now)).toBe('build · phase tests · 1 errors, last: error: boom · 1h 0m · no activity for 12m')
  expect(jobLine({ ...j, status: 'failed', endedAt: now, errors: 0 }, now)).toBe('build · failed · phase tests · 1h 0m')
})

test('a shell a subagent started rolls up into that subagent, and ended jobs leave the row', () => {
  const now = 1_000_000
  const agent = newJob({ id: 'a1', source: 'agent', label: 'worker', lastActivityAt: 0 }, now)
  const child = newJob({ id: 'b1', source: 'shell', label: 'sleep', parentId: 'a1', phase: 'deep', lastActivityAt: now }, now)
  const old = newJob({ id: 'b2', source: 'shell', label: 'old', status: 'completed', endedAt: 0 }, now)
  const shown = shownJobs([agent, child, old], now)
  expect(shown.map(j => j.id)).toEqual(['a1'])
  expect(shown[0]?.phase).toBe('deep')
  expect(shown[0]?.lastActivityAt).toBe(now)
})

test('the row shows jobs with problems first, and a killed job is not a problem', () => {
  const now = 1_000_000
  const calm = newJob({ id: 'a', source: 'shell', label: 'calm' }, now)
  const bad = newJob({ id: 'b', source: 'shell', label: 'bad', errors: 2 }, now)
  const killed = newJob({ id: 'c', source: 'shell', label: 'killed', status: 'killed', endedAt: now }, now)
  expect(shownJobs([killed, calm, bad], now).map(j => j.id)).toEqual(['b', 'a', 'c'])
  expect(jobMarker(killed, now).mark).toBe('.')
})

test('a watch whose log has no phase line warns', () => {
  expect(warnings(newJob({ id: 'w1', source: 'watch', label: 'x', sawLines: true }, 0))).toEqual(['the log has lines but no "phase: <name>" line'])
})

test('start requests: arguments, and what is wrong with a bad one', () => {
  expect(parseStartArgs('start', '/r main a.log,b.log my label')).toEqual({ repo: '/r', branch: 'main', logs: ['a.log', 'b.log'], label: 'my label' })
  expect(parseStartArgs('log', 'a.log')).toEqual({ logs: ['a.log'], label: undefined })
  expect(requestProblem({ repo: '/r' })).toContain('go together')
  expect(requestProblem({})).toContain('give a log file')
  expect(requestProblem({ logs: ['a'], errorPattern: '(' })).toContain('not a valid')
  expect(requestProblem({ logs: ['a'] })).toBeUndefined()
})

test('byte length counts multi-byte characters', () => {
  expect(utf8Length('aé€😀')).toBe(1 + 2 + 3 + 4)
})
