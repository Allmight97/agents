import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Job, SystemStats, WatchEvent } from '../types'
import {
  DEFAULT_QUIET_MS,
  fmtClock,
  fmtDuration,
  fmtSystem,
  GIT_LOG_FORMAT,
  HEARTBEAT_MS,
  heartbeatText,
  isQuiet,
  isRunning,
  jobLine,
  jobMarker,
  MAX_ROW_JOBS,
  newJob,
  outputPathFrom,
  parseCommits,
  parseLoad,
  parseStartArgs,
  parseTaskNotification,
  parseVmStat,
  POLL_MS,
  pushEvents,
  requestProblem,
  scanLog,
  short,
  shownJobs,
  statusText,
  trimJobs,
  utf8Length,
  warnings,
} from './watch.ts'
import type { StartRequest } from './watch.ts'

const PANE = 'progress'
const COMMAND = 'progress'
const TOOL = 'watch'
const AGENT_ENDED = new Set(['completed', 'failed', 'killed'])

const jobsAtom = atom({ plugin: 'progress-watch', key: 'jobs' } as const, [], { shape: 'jobs-1' })
const eventsAtom = atom({ plugin: 'progress-watch', key: 'events' } as const, [], { shape: 'events-1' })
const systemAtom = atom({ plugin: 'progress-watch', key: 'system' } as const, null, { shape: 'system-1' })
const heartbeatAtom = atom({ plugin: 'progress-watch', key: 'heartbeatAt' } as const, null, { shape: 'heartbeat-1' })

let timer: { cancel: () => void } | undefined
let chain: Promise<unknown> = Promise.resolve()
let isPollQueued = false

function serial<T>(work: () => Promise<T>): Promise<T> {
  const run = chain.then(work, work)
  chain = run.catch(() => undefined)
  return run
}

type Scan = { patch: Partial<Job>; events: WatchEvent[]; isDone?: boolean }

async function git($: EngineInterface, repo: string, args: string[]) {
  return $.process.run(['git', '-C', repo, ...args], { timeoutMs: 20_000 })
}

async function absolute($: EngineInterface, path: string): Promise<string> {
  if (path.startsWith('/')) return path
  if (path.startsWith('~/')) return `${await $.env.get('HOME')}${path.slice(1)}`
  return `${await $.session.cwd()}/${path}`
}

async function fileSize($: EngineInterface, path: string): Promise<number | undefined> {
  return $.fs.stat(path).then(s => s.size).catch(() => undefined)
}

async function addEvents($: EngineInterface, add: WatchEvent[]) {
  if (add.length === 0) return
  await update($, eventsAtom, list => pushEvents(list, add))
  const firstError = add.find(ev => ev.kind === 'error')
  if (firstError) $.ui.toast(short(firstError.text, 200))
  for (const ev of add) {
    if (ev.kind === 'quiet') $.ui.toast(short(ev.text, 200))
  }
}

async function addJob($: EngineInterface, job: Job, text: string) {
  await update($, jobsAtom, jobs => trimJobs([...jobs, job]))
  await addEvents($, [{ at: job.startedAt, kind: 'start', text }])
  void poll($)
}

async function mergeJob($: EngineInterface, id: string, patch: Partial<Job>) {
  await update($, jobsAtom, jobs => jobs.map(j => (j.id === id ? { ...j, ...patch } : j)))
}

async function startWatch($: EngineInterface, req: StartRequest): Promise<string> {
  const problem = requestProblem(req)
  if (problem) throw new Error(problem)
  const now = Date.now()
  let repo: string | undefined
  let head: string | undefined
  if (req.repo && req.branch) {
    const repoArg = await absolute($, req.repo)
    const top = await git($, repoArg, ['rev-parse', '--show-toplevel'])
    if (top.exitCode !== 0) throw new Error(`${repoArg} is not a git repository: ${top.stderr.trim()}`)
    repo = top.stdout.trim()
    const tip = await git($, repo, ['rev-parse', '--verify', '--quiet', `refs/heads/${req.branch}`])
    if (tip.exitCode !== 0) throw new Error(`branch ${req.branch} does not exist in ${repo}`)
    head = tip.stdout.trim()
  }
  const logs = []
  const notes = []
  let phase: string | undefined
  for (const raw of req.logs ?? []) {
    const path = await absolute($, raw)
    const size = await fileSize($, path)
    if (size === undefined) notes.push(`${path} does not exist yet`)
    if (size) phase = scanLog((await $.process.run(['cat', path], { timeoutMs: 20_000 })).stdout).phases.pop() ?? phase
    logs.push({ path, offset: size ?? 0 })
  }
  const label = req.label ?? (repo ? `${repo.split('/').pop()}@${req.branch}` : (logs[0]?.path.split('/').pop() ?? 'watch'))
  const job = newJob(
    {
      id: `w${now.toString(36).slice(-5)}`,
      source: 'watch',
      label,
      logs,
      repo,
      branch: req.branch,
      head,
      phase,
      errorPattern: req.errorPattern,
      quietMs: req.quietMinutes ? req.quietMinutes * 60_000 : DEFAULT_QUIET_MS,
    },
    now,
  )
  const text = `watching ${label}: ${[repo && `${repo} branch ${req.branch} at ${head?.slice(0, 8)}`, ...logs.map(l => l.path)].filter(Boolean).join(', ')}`
  await addJob($, job, text)
  return [`${job.id}: ${text}`, ...notes.map(n => `note: ${n}`), 'A log marks phases with lines "phase: <name>"; "phase: done" ends the watch.'].join('\n')
}

async function endJob($: EngineInterface, id: string, status: string, summary?: string) {
  await serial(async () => {
    const job = (await read($, jobsAtom)).find(j => j.id === id)
    if (!job || !isRunning(job)) return
    const now = Date.now()
    const scan = await scanJob($, job, now, true).catch(err => ({ patch: { lastProblem: String(err) }, events: [] as WatchEvent[] }))
    await mergeJob($, id, { ...scan.patch, status, summary, endedAt: now })
    const text = `${job.label} ${status} after ${fmtDuration(now - job.startedAt)}${summary ? `: ${summary}` : ''}`
    await addEvents($, [...scan.events, { at: now, kind: 'end', text }])
    if (status !== 'completed' || now - job.startedAt >= 60_000) $.ui.toast(short(text, 200))
    $.ui.invalidate('ui.render')
  })
}

async function stopJobs($: EngineInterface, id?: string): Promise<string> {
  const running = (await read($, jobsAtom)).filter(isRunning)
  const targets = id ? running.filter(j => j.id === id) : running.filter(j => j.source === 'watch')
  if (targets.length === 0) return id ? `no running job has id ${id}` : 'no watch is running'
  for (const j of targets) await endJob($, j.id, 'stopped')
  return `stopped following: ${targets.map(j => j.label).join(', ')}`
}

async function scanCommits($: EngineInterface, j: Job, now: number): Promise<Scan> {
  if (!j.repo || !j.branch) return { patch: {}, events: [] }
  const tip = await git($, j.repo, ['rev-parse', '--verify', '--quiet', `refs/heads/${j.branch}`])
  if (tip.exitCode !== 0) throw new Error(`branch ${j.branch} is gone from ${j.repo}`)
  const sha = tip.stdout.trim()
  if (sha === j.head) return { patch: {}, events: [] }
  const isAhead = j.head ? (await git($, j.repo, ['merge-base', '--is-ancestor', j.head, sha])).exitCode === 0 : false
  const out = await git($, j.repo, ['log', '-n', '50', `--format=${GIT_LOG_FORMAT}`, isAhead ? `${j.head}..${sha}` : sha])
  const commits = isAhead ? parseCommits(out.stdout) : parseCommits(out.stdout).slice(-1)
  const events: WatchEvent[] = isAhead ? [] : [{ at: now, kind: 'error', text: `${j.label}: branch ${j.branch} was rewritten` }]
  for (const c of commits) events.push({ at: now, kind: 'commit', text: `${j.label}: ${c.sha} ${c.subject}` })
  const last = commits[commits.length - 1]
  return {
    patch: {
      head: sha,
      commits: j.commits + commits.length,
      lastCommit: last ? `${last.sha} ${last.subject}` : j.lastCommit,
      lastCommitAt: last ? last.at : j.lastCommitAt,
      errors: j.errors + (isAhead ? 0 : 1),
      lastError: isAhead ? j.lastError : `branch ${j.branch} was rewritten`,
      lastActivityAt: now,
      quietFlagged: false,
    },
    events,
  }
}

async function readNewLines($: EngineInterface, path: string, offset: number, isFinal: boolean) {
  const size = await fileSize($, path)
  if (size === undefined || size === offset) return { text: '', offset }
  const from = size < offset ? 0 : offset
  const out = await $.process.run(['tail', '-c', `+${from + 1}`, path], { timeoutMs: 20_000 })
  if (out.exitCode !== 0) throw new Error(`cannot read ${path}: ${out.stderr.trim()}`)
  const end = isFinal ? out.stdout.length - 1 : out.stdout.lastIndexOf('\n')
  if (end < 0) return { text: '', offset: from }
  const text = out.stdout.slice(0, end + 1)
  return { text, offset: from + utf8Length(text) }
}

async function scanLogs($: EngineInterface, j: Job, now: number, isFinal: boolean): Promise<Scan> {
  const logs = []
  const events: WatchEvent[] = []
  let phase = j.phase
  let errors = j.errors
  let lastError = j.lastError
  let sawLines = j.sawLines
  let hasNewText = false
  let isDone = false
  for (const log of j.logs) {
    const fresh = await readNewLines($, log.path, log.offset, isFinal)
    logs.push({ path: log.path, offset: fresh.offset })
    if (!fresh.text) continue
    hasNewText = true
    const found = scanLog(fresh.text, j.errorPattern)
    sawLines = sawLines || found.lines > 0
    phase = found.phases[found.phases.length - 1] ?? phase
    isDone = isDone || phase === 'done' && found.phases.length > 0
    errors += found.errors.length
    lastError = found.errors[found.errors.length - 1] ?? lastError
    for (const text of found.phases) events.push({ at: now, kind: 'phase', text: `${j.label}: ${text}` })
    for (const text of found.errors) events.push({ at: now, kind: 'error', text: `${j.label}: ${text}` })
  }
  if (!hasNewText) return { patch: {}, events }
  return { patch: { logs, phase, errors, lastError, sawLines, lastActivityAt: now, quietFlagged: false }, events, isDone }
}

async function scanActivity($: EngineInterface, j: Job, now: number): Promise<Scan> {
  if (!j.activityFile) return { patch: {}, events: [] }
  const size = await fileSize($, j.activityFile)
  if (size === undefined || size === j.activitySize) return { patch: {}, events: [] }
  return { patch: { activitySize: size, lastActivityAt: now, quietFlagged: false }, events: [] }
}

async function scanJob($: EngineInterface, j: Job, now: number, isFinal = false): Promise<Scan> {
  const commits = await scanCommits($, j, now)
  const merged = { ...j, ...commits.patch }
  const logs = await scanLogs($, merged, now, isFinal)
  const activity = await scanActivity($, { ...merged, ...logs.patch }, now)
  return { patch: { ...commits.patch, ...logs.patch, ...activity.patch }, events: [...commits.events, ...logs.events, ...activity.events], isDone: logs.isDone }
}

async function readSystem($: EngineInterface): Promise<SystemStats> {
  const at = Date.now()
  const ctl = await $.process.run(['sysctl', '-n', 'vm.loadavg', 'hw.ncpu', 'hw.memsize'])
  const vm = await $.process.run(['vm_stat'])
  if (ctl.exitCode !== 0 || vm.exitCode !== 0) throw new Error(`system figures unreadable: ${(ctl.stderr || vm.stderr).trim()}`)
  const [loadLine = '', cpus, mem] = ctl.stdout.trim().split('\n')
  return { at, load1: parseLoad(loadLine.replace(/[{}]/g, '')), cpus: Number(cpus) || undefined, totalBytes: Number(mem) || undefined, freeBytes: parseVmStat(vm.stdout) }
}

async function pollJob($: EngineInterface, job: Job, now: number) {
  const events: WatchEvent[] = []
  let patch: Partial<Job> = {}
  let isDone = false
  try {
    const scan = await scanJob($, job, now)
    patch = { ...scan.patch, lastProblem: undefined }
    isDone = Boolean(scan.isDone) && job.source === 'watch'
    events.push(...scan.events)
  } catch (err) {
    const problem = err instanceof Error ? err.message : String(err)
    patch = { lastProblem: problem }
    if (problem !== job.lastProblem) {
      patch = { ...patch, errors: job.errors + 1, lastError: problem }
      events.push({ at: now, kind: 'error', text: `${job.label}: watcher: ${problem}` })
    }
  }
  const after = { ...job, ...patch }
  if (isQuiet(after, now) && !after.quietFlagged) {
    patch = { ...patch, quietFlagged: true }
    events.push({ at: now, kind: 'quiet', text: `${job.label}: no activity for ${fmtDuration(now - after.lastActivityAt)}` })
  }
  await mergeJob($, job.id, patch)
  await addEvents($, events)
  return isDone
}

async function pollAgents($: EngineInterface, running: readonly Job[]) {
  const agents = running.filter(j => j.source === 'agent')
  if (agents.length === 0) return []
  const list = await $.agent.list()
  const ended: { id: string; status: string }[] = []
  for (const job of agents) {
    const info = list.find(a => a.id === job.id)
    if (!info) ended.push({ id: job.id, status: 'ended' })
    else if (AGENT_ENDED.has(info.status)) ended.push({ id: job.id, status: info.status })
    else if (info.status !== job.agentState) await mergeJob($, job.id, { agentState: info.status })
  }
  return ended
}

async function pollSystem($: EngineInterface, running: readonly Job[], now: number) {
  let system = await read($, systemAtom)
  try {
    system = await readSystem($)
    await update($, systemAtom, () => system)
  } catch (err) {
    await addEvents($, [{ at: now, kind: 'error', text: `watcher: ${err instanceof Error ? err.message : String(err)}` }])
  }
  const beat = await read($, heartbeatAtom)
  if (beat === null) {
    await update($, heartbeatAtom, () => now)
  } else if (now - beat >= HEARTBEAT_MS) {
    await update($, heartbeatAtom, () => now)
    await addEvents($, [{ at: now, kind: 'heartbeat', text: heartbeatText(running, system, now) }])
  }
}

async function poll($: EngineInterface) {
  if (isPollQueued) return
  isPollQueued = true
  let ended: { id: string; status: string }[] = []
  await serial(async () => {
    isPollQueued = false
    const running = (await read($, jobsAtom)).filter(isRunning)
    if (running.length === 0) {
      await update($, heartbeatAtom, () => null)
      return
    }
    const now = Date.now()
    await pollSystem($, running, now)
    ended = await pollAgents($, running)
    for (const job of running) {
      if (await pollJob($, job, now)) ended.push({ id: job.id, status: 'completed' })
    }
    $.ui.invalidate('ui.render')
  }).catch(err => $.ui.log(`progress-watch: poll failed: ${err}`))
  for (const e of ended) await endJob($, e.id, e.status)
  $.ui.invalidate('ui.render')
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const r = await next(e)
    await $.command
      .register({ name: COMMAND, description: 'Background jobs: phases, errors, activity; add a log or a branch to follow', argumentHint: '[status | log <files> [label] | start <repo> <branch> [files|-] [label] | stop [id]]', immediate: true })
      .catch(err => $.ui.log(`progress-watch: /${COMMAND} not registered: ${err}`))
    await $.tool
      .register({
        name: TOOL,
        description:
          'Read or extend the progress row. Background Bash jobs and background subagents are followed automatically: do not start anything for them, and do not build a watcher with Monitor to show progress. This tool never wakes you; a job\'s exit does. action "status" returns every job: phase, errors, activity, logs, warnings. action "start" follows a log file a job writes elsewhere (a worker writing that log must be told: lines "phase: <name>" mark phases, "phase: done" ends the watch) or new commits on a git branch. action "stop" ends a watch, or stops following a job by id.',
        inputSchema: {
          type: 'object',
          properties: {
            action: { type: 'string', enum: ['status', 'start', 'stop'] },
            repo: { type: 'string', description: 'Absolute path of a git repository; needs branch (start)' },
            branch: { type: 'string', description: 'Branch whose new commits are shown; needs repo (start)' },
            logs: { type: 'array', items: { type: 'string' }, description: 'Absolute paths of log files a job appends to (start)' },
            label: { type: 'string', description: 'Short name of the job (start)' },
            quietMinutes: { type: 'number', description: 'Minutes without activity before the row says so; default 12 (start)' },
            errorPattern: { type: 'string', description: 'Regular expression for error lines, in place of the default rule (start)' },
            id: { type: 'string', description: 'Job id from status (stop); without it every watch stops' },
          },
          required: ['action'],
        },
      })
      .catch(err => $.ui.log(`progress-watch: tool not registered: ${err}`))
    timer?.cancel()
    timer = $.clock.every(POLL_MS, () => void poll($))
    void poll($)
    return r
  })

  on('session.end', async ($, e, next) => {
    if (e.reason !== 'clear') {
      timer?.cancel()
      timer = undefined
    }
    return next(e)
  })

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const r = await next(e)
    const taskId = (r.result as { backgroundTaskId?: string } | undefined)?.backgroundTaskId
    if (!taskId) return r
    const now = Date.now()
    const path = outputPathFrom(r.text)
    const label = short(e.description ?? e.command, 50)
    await addJob($, newJob({ id: taskId, source: 'shell', label, parentId: e.agentId, logs: path ? [{ path, offset: 0 }] : [], pathLost: !path }, now), `${label}: started`)
    if (!path) await addEvents($, [{ at: now, kind: 'error', text: `${label}: output file not named in the expected words; phases and errors will not show` }])
    return r
  })

  on('tool.call', { tool: 'Agent' }, async ($, e, next) => {
    const r = await next(e)
    const result = r.result as { status?: string; agentId?: string; outputFile?: string } | undefined
    if (result?.status !== 'async_launched' || !result.agentId) return r
    const label = short(e.description, 50)
    await addJob($, newJob({ id: result.agentId, source: 'agent', label, parentId: e.agentId, activityFile: result.outputFile, agentState: 'running' }, Date.now()), `${label}: started`)
    return r
  })

  on('tool.call', { tool: 'TaskStop' }, async ($, e, next) => {
    const r = await next(e)
    const id = e.task_id ?? e.shell_id
    if (id && !r.deny && !r.isError) void endJob($, id, 'killed', 'stopped by TaskStop')
    return r
  })

  on('session.append', async ($, e, next) => {
    const isEngineRow = e.origin?.kind === 'engine' || e.origin?.kind === 'task-notification'
    const content = e.message.content
    const text = isEngineRow && Array.isArray(content) ? content.map(b => (b.type === 'text' ? b.text : '')).join('') : ''
    const note = parseTaskNotification(text)
    if (note) {
      const job = (await read($, jobsAtom)).find(j => j.id === note.id)
      if (job?.source === 'shell') void endJob($, note.id, note.status, note.summary)
    }
    return next(e)
  })

  on('command.run', { command: COMMAND }, async ($, e) => {
    const [verb = '', ...rest] = e.args.trim().split(/\s+/)
    try {
      if (verb === 'start' || verb === 'log') {
        const req = parseStartArgs(verb, rest.join(' '))
        return { text: typeof req === 'string' ? req : await startWatch($, req) }
      }
      if (verb === 'stop') return { text: await stopJobs($, rest[0]) }
      if (verb === 'status') return { text: statusText(await read($, jobsAtom), await read($, eventsAtom), await read($, systemAtom), Date.now()) }
    } catch (err) {
      return { text: `progress-watch: ${err instanceof Error ? err.message : String(err)}` }
    }
    await $.ui.open({ id: PANE, title: 'progress', focus: true })
    return { text: 'progress pane opened' }
  })

  on('tool.call', { tool: 'mcp__progress-watch__watch' }, async ($, e) => {
    const input = e as { action?: string; id?: string } & StartRequest
    try {
      if (input.action === 'status') return { result: statusText(await read($, jobsAtom), await read($, eventsAtom), await read($, systemAtom), Date.now()) }
      if (input.action === 'stop') return { result: await stopJobs($, input.id) }
      if (input.action === 'start') return { result: await startWatch($, input) }
      return { deny: 'action must be status, start or stop' }
    } catch (err) {
      return { deny: err instanceof Error ? err.message : String(err) }
    }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const now = Date.now()
    const shown = shownJobs(await read($, jobsAtom), now)
    if (shown.length === 0 || e.props.hasSurvey) return next(e)
    const below = await next(e)
    const system = await read($, systemAtom)
    const { Box, Text } = $.ui.resolve(e)
    const row = shown.slice(-MAX_ROW_JOBS)
    const hidden = shown.length - row.length
    return (
      <Box flexDirection="column">
        {below}
        {row.map((j, i) => {
          const { mark, color } = jobMarker(j, now)
          const tail = i === 0 && system ? ` · ${fmtSystem(system)}` : ''
          const more = i === 0 && hidden > 0 ? `+${hidden} more · ` : ''
          return (
            <Box key={`progress-watch-${j.id}`} flexDirection="row" columnGap={1}>
              <Text color={color} bold>{mark}</Text>
              <Text wrap="truncate-end">{`${more}${jobLine(j, now)}${tail}`}</Text>
            </Box>
          )
        })}
      </Box>
    )
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const jobs = await read($, jobsAtom)
    const events = await read($, eventsAtom)
    const system = await read($, systemAtom)
    const beat = await read($, heartbeatAtom)
    const now = Date.now()
    const running = jobs.filter(isRunning)
    const ended = jobs.filter(j => !isRunning(j)).slice(-5).reverse()
    const room = Math.max(3, (e.viewport?.rows ?? 30) - 8 - (running.length + ended.length) * 2)
    const COLOR: Record<WatchEvent['kind'], string | undefined> = { start: 'cyan', phase: 'cyan', commit: 'green', error: 'red', quiet: 'yellow', heartbeat: undefined, end: 'yellow' }
    return (
      <Box flexDirection="column">
        {jobs.length === 0 ? <Text dimColor>{'No jobs yet. Background Bash jobs and subagents appear here by themselves. /progress log <file> or /progress start <repo> <branch> adds more.'}</Text> : null}
        {[...running, ...ended].map(j => {
          const { color } = jobMarker(j, now)
          const lines = [...j.logs.map(l => l.path), ...(j.repo ? [`${j.repo} · ${j.branch}`] : []), ...warnings(j), ...(j.lastCommit ? [`last commit ${j.lastCommit}`] : [])]
          return (
            <Box key={j.id} flexDirection="column">
              <Text color={color} wrap="truncate-end">{`${jobLine(j, now)} · ${j.id}`}</Text>
              {lines.map(line => (
                <Text dimColor wrap="truncate-end">{`  ${line}`}</Text>
              ))}
            </Box>
          )
        })}
        {system ? <Text>{`${fmtSystem(system)}${beat !== null ? ` · next heartbeat in ${fmtDuration(beat + HEARTBEAT_MS - now + 59_999)}` : ''}`}</Text> : null}
        <Text dimColor>events, newest first</Text>
        {events
          .slice(-room)
          .reverse()
          .map(ev => (
            <Text color={COLOR[ev.kind]} dimColor={ev.kind === 'heartbeat'} wrap="truncate-end">
              {`${fmtClock(ev.at)} ${ev.kind} ${ev.text}`}
            </Text>
          ))}
      </Box>
    )
  })
}
