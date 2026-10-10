export type Config = {
  checks: RegExp[]
  paths: string[]
  hint: string
}

export type ConfigError = { error: string }

export type Verdict =
  | { kind: 'pass' }
  | { kind: 'block'; reason: string }
  | { kind: 'release'; reason: string }

export const CONFIG_PATH = '.claude/done-gate.json'

const isStrings = (value: unknown): value is string[] =>
  Array.isArray(value) && value.every(item => typeof item === 'string')

export function parseConfig(text: string): Config | ConfigError {
  let raw: unknown
  try {
    raw = JSON.parse(text)
  } catch {
    return { error: 'is not valid JSON' }
  }
  if (typeof raw !== 'object' || raw === null || Array.isArray(raw)) {
    return { error: 'must be a JSON object' }
  }
  const { checks, paths = [], hint } = raw as Record<string, unknown>
  if (!isStrings(checks) || checks.length === 0) {
    return { error: '"checks" must be a non-empty list of regular expressions' }
  }
  if (!isStrings(paths)) return { error: '"paths" must be a list of path prefixes' }
  if (hint !== undefined && typeof hint !== 'string') return { error: '"hint" must be a string' }
  let compiled: RegExp[]
  try {
    compiled = checks.map(pattern => new RegExp(pattern))
  } catch {
    return { error: '"checks" holds an invalid regular expression' }
  }
  return { checks: compiled, paths, hint: hint ?? checks[0] }
}

export const isCheck = (config: Config, command: string): boolean =>
  config.checks.some(pattern => pattern.test(command))

const guardedFiles =(config: Config, changed: readonly string[]): string[] =>
  config.paths.length === 0
    ? [...changed]
    : changed.filter(file => config.paths.some(prefix => file.startsWith(prefix)))

export function decide(input: {
  config: Config
  unproven: readonly string[]
  isRetry: boolean
}): Verdict {
  const files = guardedFiles(input.config, input.unproven)
  if (files.length === 0) return { kind: 'pass' }
  const sample = files.slice(0, 3).join(', ') + (files.length > 3 ? `, +${files.length - 3} more` : '')
  if (input.isRetry) {
    return { kind: 'release', reason: `finished without a passing check (${sample})` }
  }
  return {
    kind: 'block',
    reason:
      `done-gate: ${files.length} file(s) changed since the last passing check (${sample}). ` +
      `Run \`${input.config.hint}\` and fix any failure before you finish. ` +
      'If the check cannot run here, say why in your reply.',
  }
}

export const configFault = (error: string): Verdict => ({
  kind: 'block',
  reason: `done-gate: ${CONFIG_PATH} ${error}. Fix it or remove it before you finish.`,
})
