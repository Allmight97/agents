export type LogCursor = { path: string; offset: number }

export type Job = {
  id: string
  source: 'shell' | 'agent' | 'watch'
  label: string
  startedAt: number
  status: string
  endedAt?: number
  summary?: string
  parentId?: string
  agentState?: string
  logs: LogCursor[]
  pathLost?: boolean
  activityFile?: string
  activitySize?: number
  repo?: string
  branch?: string
  head?: string
  commits: number
  lastCommit?: string
  lastCommitAt?: number
  phase?: string
  errors: number
  lastError?: string
  errorPattern?: string
  lastActivityAt: number
  quietMs: number
  quietFlagged?: boolean
  sawLines?: boolean
  lastProblem?: string
}

export type WatchEventKind = 'start' | 'phase' | 'commit' | 'error' | 'quiet' | 'heartbeat' | 'end'

export type WatchEvent = { at: number; kind: WatchEventKind; text: string }

export type SystemStats = { at: number; load1?: number; cpus?: number; freeBytes?: number; totalBytes?: number }

declare module 'claude-code' {
  interface PluginState {
    'progress-watch': {
      jobs: Shaped<Job[]>
      events: Shaped<WatchEvent[]>
      system: Shaped<SystemStats | null>
      heartbeatAt: Shaped<number | null>
    }
  }
}
