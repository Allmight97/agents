import type { Job, SystemStats, WatchEvent } from '../types'

export const POLL_MS = 15_000
export const HEARTBEAT_MS = 10 * 60_000
export const DEFAULT_QUIET_MS = 12 * 60_000
export const RECENT_END_MS = 2 * 60_000
export const KEEP_EVENTS = 200
export const KEEP_ENDED = 30
export const MAX_ROW_JOBS = 3

const PHASE = /^\s*phase\s*[:=-]\s*(.+?)\s*$/i
const ERROR_PREFIX = /^\s*(error|fatal|panic)(\[[^\]]*\])?\s*:|^\s*\[(error|fatal)\]/i
const ERROR_SIGNAL = /^thread '.*' panicked|^Traceback \(most recent call last\)|^\s*FAILED\b|\.\.\. FAILED\s*$|^\s*FAIL\s|^npm ERR!/

export type LogFindings = { phases: string[]; errors: string[]; lines: number }

export function scanLog(text: string, errorPattern?: string): LogFindings {
  const custom = errorPattern ? new RegExp(errorPattern) : undefined
  const phases: string[] = []
  const errors: string[] = []
  let lines = 0
  for (const line of text.split(/\r?\n/)) {
    if (line.trim()) lines += 1
    const phase = PHASE.exec(line)
    if (phase?.[1]) phases.push(phase[1])
    else if (custom ? custom.test(line) : ERROR_PREFIX.test(line) || ERROR_SIGNAL.test(line)) errors.push(line.trim())
  }
  return { phases, errors, lines }
}

export function parseTaskNotification(text: string): { id: string; status: string; summary?: string } | undefined {
  if (!text.includes('<task-notification>')) return undefined
  const id = /<task-id>([^<]+)<\/task-id>/.exec(text)?.[1]
  const status = /<status>([^<]+)<\/status>/.exec(text)?.[1]
  if (!id || !status) return undefined
  return { id, status, summary: /<summary>([^<]*)<\/summary>/.exec(text)?.[1] }
}

export function outputPathFrom(toolText: string | undefined): string | undefined {
  return /written to: (.+?\.output)\./.exec(toolText ?? '')?.[1]
}

export function newJob(fields: Pick<Job, 'id' | 'source' | 'label'> & Partial<Job>, now: number): Job {
  return { status: 'running', startedAt: now, logs: [], commits: 0, errors: 0, lastActivityAt: now, quietMs: DEFAULT_QUIET_MS, ...fields }
}

export const short = (text: string, max: number) => (text.length > max ? `${text.slice(0, max - 1)}…` : text)

export type Commit = { sha: string; subject: string; at: number }

export const GIT_LOG_FORMAT = '%h%x1f%s%x1f%ct'

export function parseCommits(stdout: string): Commit[] {
  return stdout
    .split('\n')
    .filter(Boolean)
    .map(line => {
      const [sha = '', subject = '', ct = ''] = line.split('\x1f')
      return { sha, subject, at: Number(ct) * 1000 }
    })
    .reverse()
}

export function parseVmStat(text: string): number | undefined {
  const page = Number(/page size of (\d+) bytes/.exec(text)?.[1])
  const pages = (name: string) => Number(new RegExp(`Pages ${name}:\\s+(\\d+)`).exec(text)?.[1] ?? 0)
  if (!page) return undefined
  return (pages('free') + pages('inactive') + pages('speculative') + pages('purgeable')) * page
}

export function parseLoad(text: string): number | undefined {
  const n = Number(/[\d.]+/.exec(text)?.[0])
  return Number.isFinite(n) ? n : undefined
}

export function fmtDuration(ms: number): string {
  if (ms < 60_000) return '<1m'
  const mins = Math.floor(ms / 60_000)
  const h = Math.floor(mins / 60)
  if (h >= 24) return `${Math.floor(h / 24)}d ${h % 24}h`
  return h > 0 ? `${h}h ${mins % 60}m` : `${mins}m`
}

export const fmtGb = (bytes: number) => `${(bytes / 2 ** 30).toFixed(1)}G`

export function fmtClock(at: number): string {
  const d = new Date(at)
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

export function fmtSystem(s: SystemStats): string {
  const load = s.load1 === undefined ? 'load ?' : `load ${s.load1.toFixed(1)}${s.cpus ? `/${s.cpus}` : ''}`
  const mem = s.freeBytes === undefined ? 'free ?' : `free ${fmtGb(s.freeBytes)}${s.totalBytes ? ` of ${fmtGb(s.totalBytes)}` : ''}`
  return `${load} · ${mem}`
}

export const isRunning = (j: Job) => j.status === 'running'

export const isQuiet = (j: Job, now: number) => isRunning(j) && now - j.lastActivityAt >= j.quietMs

export function rollUp(job: Job, all: readonly Job[]): Job {
  const children = all.filter(c => c.parentId === job.id)
  if (children.length === 0) return job
  const latest = children.reduce((a, b) => (b.lastActivityAt > a.lastActivityAt ? b : a))
  return {
    ...job,
    phase: job.phase ?? latest.phase,
    errors: job.errors + children.reduce((n, c) => n + c.errors, 0),
    lastError: job.lastError ?? children.find(c => c.lastError)?.lastError,
    lastActivityAt: Math.max(job.lastActivityAt, latest.lastActivityAt),
  }
}

export function shownJobs(all: readonly Job[], now: number): Job[] {
  const ids = new Set(all.map(j => j.id))
  return all
    .filter(j => !j.parentId || !ids.has(j.parentId))
    .map(j => rollUp(j, all))
    .filter(j => isRunning(j) || now - (j.endedAt ?? 0) < RECENT_END_MS)
    .sort((a, b) => rowRank(a, now) - rowRank(b, now))
}

function rowRank(j: Job, now: number): number {
  if (j.errors > 0 || j.status === 'failed') return 0
  if (isQuiet(j, now)) return 1
  return isRunning(j) ? 2 : 3
}

export function jobLine(j: Job, now: number): string {
  const ended = !isRunning(j)
  return [
    j.label,
    ...(ended ? [j.status] : j.agentState && j.agentState !== 'running' ? [j.agentState] : []),
    ...(j.phase ? [`phase ${j.phase}`] : []),
    ...(j.branch ? [j.commits === 0 ? 'no commits yet' : `${j.commits} commits, last ${fmtDuration(now - (j.lastCommitAt ?? now))} ago`] : []),
    ...(j.errors > 0 ? [`${j.errors} errors, last: ${short(j.lastError ?? '', 60)}`] : []),
    ...(j.pathLost ? ['output path unknown'] : []),
    fmtDuration((j.endedAt ?? now) - j.startedAt),
    ...(isQuiet(j, now) ? [`no activity for ${fmtDuration(now - j.lastActivityAt)}`] : []),
  ].join(' · ')
}

export function jobMarker(j: Job, now: number): { mark: string; color: string } {
  if (j.errors > 0 || j.status === 'failed') return { mark: '!', color: 'red' }
  if (isQuiet(j, now)) return { mark: '~', color: 'yellow' }
  return isRunning(j) ? { mark: '>', color: 'cyan' } : { mark: '.', color: 'green' }
}

export function warnings(j: Job): string[] {
  const out: string[] = []
  if (j.source === 'watch' && j.sawLines && !j.phase) out.push('the log has lines but no "phase: <name>" line')
  if (j.pathLost) out.push('Claude Code did not name this job\'s output file in the expected words, so phases and errors are not read')
  if (j.lastProblem) out.push(`watcher: ${j.lastProblem}`)
  return out
}

export function statusText(all: readonly Job[], events: readonly WatchEvent[], system: SystemStats | null, now: number): string {
  if (all.length === 0) return 'no jobs followed in this session'
  const rows = all.map(j =>
    [
      `${j.id} [${j.source}] ${jobLine(j, now)}`,
      `  last activity ${fmtDuration(now - j.lastActivityAt)} ago`,
      ...j.logs.map(l => `  log ${l.path}`),
      ...(j.repo ? [`  repo ${j.repo} branch ${j.branch}`] : []),
      ...(j.summary ? [`  ${j.summary}`] : []),
      ...warnings(j).map(w => `  warning: ${w}`),
    ].join('\n'),
  )
  const recent = events.slice(-15).map(e => `${fmtClock(e.at)} ${e.kind} ${e.text}`)
  return [...rows, ...(system ? [fmtSystem(system)] : []), 'recent events:', ...recent].join('\n')
}

export function heartbeatText(running: readonly Job[], s: SystemStats | null, now: number): string {
  const oldest = Math.min(...running.map(j => j.startedAt))
  return `heartbeat: ${running.length} running, oldest ${fmtDuration(now - oldest)}${s ? ` · ${fmtSystem(s)}` : ''}`
}

export const pushEvents = (list: readonly WatchEvent[], add: readonly WatchEvent[]): WatchEvent[] =>
  [...list, ...add].slice(-KEEP_EVENTS)

export function trimJobs(jobs: readonly Job[]): Job[] {
  const ended = jobs.filter(j => !isRunning(j))
  const drop = new Set(ended.slice(0, Math.max(0, ended.length - KEEP_ENDED)).map(j => j.id))
  return jobs.filter(j => !drop.has(j.id))
}

export type StartRequest = { repo?: string; branch?: string; logs?: string[]; label?: string; quietMinutes?: number; errorPattern?: string }

const splitLogs = (word: string | undefined) => (word && word !== '-' ? word.split(',').filter(Boolean) : [])

export function parseStartArgs(verb: string, args: string): StartRequest | string {
  const words = args.trim().split(/\s+/).filter(Boolean)
  if (verb === 'log') {
    const [logs, ...label] = words
    if (!logs) return 'usage: /progress log <log file[,log file]> [label]'
    return { logs: splitLogs(logs), label: label.length ? label.join(' ') : undefined }
  }
  if (words.length < 2) return 'usage: /progress start <repo path> <branch> [log file[,log file] | -] [label]'
  const [repo = '', branch = '', logs, ...label] = words
  return { repo, branch, logs: splitLogs(logs), label: label.length ? label.join(' ') : undefined }
}

export function requestProblem(req: StartRequest): string | undefined {
  if (Boolean(req.repo) !== Boolean(req.branch)) return 'repo and branch go together: give both or neither'
  if (!req.repo && !req.logs?.length) return 'give a log file, or a repo and a branch; background jobs are followed without this tool'
  if (req.quietMinutes !== undefined && !(req.quietMinutes > 0)) return 'quietMinutes must be above 0'
  if (req.errorPattern) {
    try {
      new RegExp(req.errorPattern)
    } catch (err) {
      return `errorPattern is not a valid regular expression: ${err instanceof Error ? err.message : String(err)}`
    }
  }
  return undefined
}

export function utf8Length(text: string): number {
  let n = 0
  for (const ch of text) {
    const c = ch.codePointAt(0) ?? 0
    n += c < 0x80 ? 1 : c < 0x800 ? 2 : c < 0x10000 ? 3 : 4
  }
  return n
}
