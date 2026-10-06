export type Row = {
  file: string
  code: number
  complexity: number
  density: number
  churn: number | null
  over_threshold_fns: number | null
  per_function_source: 'biome' | 'lizard' | null
  score: number
  flags: string[]
}

declare module 'claude-code' {
  interface PluginState {
    'complexity-lens': { rows: Row[]; problem: string | null }
  }
}
