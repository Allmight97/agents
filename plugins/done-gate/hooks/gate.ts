export type Config = {
  checks: RegExp[]
  paths: string[]
  hint: string
  resolve?: string[]
}

export type ConfigError = { error: string }

export type Verdict =
  | { kind: 'pass' }
  | { kind: 'block'; reason: string }
  | { kind: 'release'; reason: string }

export type Pass = { command: string; changed: string[] }

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
  const { checks, paths = [], hint, resolve } = raw as Record<string, unknown>
  if (!isStrings(checks) || checks.length === 0) {
    return { error: '"checks" must be a non-empty list of regular expressions' }
  }
  if (!isStrings(paths)) return { error: '"paths" must be a list of path prefixes' }
  if (hint !== undefined && typeof hint !== 'string') return { error: '"hint" must be a string' }
  if (resolve !== undefined && (!isStrings(resolve) || resolve.length === 0)) {
    return { error: '"resolve" must be a non-empty command and argument list' }
  }
  let compiled: RegExp[]
  try {
    compiled = checks.map(pattern => new RegExp(pattern))
  } catch {
    return { error: '"checks" holds an invalid regular expression' }
  }
  return { checks: compiled, paths, hint: hint ?? checks[0], resolve }
}

export const isCheck = (config: Config, command: string): boolean =>
  config.checks.some(pattern => pattern.test(command))

const guardedFiles = (config: Config, changed: readonly string[]): string[] =>
  config.paths.length === 0
    ? [...changed]
    : changed.filter(file => config.paths.some(prefix => file.startsWith(prefix)))

const listed = (items: readonly string[]) =>
  items.slice(0, 3).join(', ') + (items.length > 3 ? `, +${items.length - 3} more` : '')

function verdict(unmet: readonly string[], isRetry: boolean, block: string): Verdict {
  if (unmet.length === 0) return { kind: 'pass' }
  if (isRetry) return { kind: 'release', reason: `finished without a passing check (${listed(unmet)})` }
  return { kind: 'block', reason: `${block} If the check cannot run here, say why in your reply.` }
}

export function decide(input: { config: Config; unproven: readonly string[]; isRetry: boolean }): Verdict {
  const files = guardedFiles(input.config, input.unproven)
  return verdict(
    files,
    input.isRetry,
    `done-gate: ${files.length} file(s) changed since the last passing check (${listed(files)}). ` +
      `Run \`${input.config.hint}\` and fix any failure before you finish.`,
  )
}

export function decideResolved(input: { unmet: readonly string[]; isRetry: boolean }): Verdict {
  return verdict(
    input.unmet,
    input.isRetry,
    `done-gate: these checks have not passed on the current files: ${input.unmet.join('; ')}. ` +
      'Run them and fix any failure before you finish.',
  )
}

export const configFault = (error: string): Verdict => ({
  kind: 'block',
  reason: `done-gate: ${CONFIG_PATH} ${error}. Fix it or remove it before you finish.`,
})
