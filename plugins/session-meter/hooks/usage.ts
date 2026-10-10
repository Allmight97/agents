/**
 * usage.ts — the pure half of session-meter's context, plan-limit and
 * subagent views: no `$`, no engine.
 */

export type Limit = { kind: string; percentUsed: number; resetsAt?: string }

export type Tokens = { input: number; output: number }

export type AgentTally = Tokens & { id: string; label: string; turns: number }

export type StepUsage = {
  input_tokens: number
  output_tokens: number
  cache_read_input_tokens: number
  cache_creation_input_tokens: number
}

const LIMIT_LABEL: Record<string, string> = { five_hour: '5h', seven_day: 'wk' }

export const limitLabel = (kind: string): string => LIMIT_LABEL[kind] ?? kind.replace(/_/g, ' ')

/** Plan limits in a fixed order: five-hour, then weekly, then any other window. */
export const planLimits = (limits: readonly Limit[]): Limit[] =>
  [...limits].sort((a, b) => rank(a.kind) - rank(b.kind))

const rank = (kind: string) => (kind === 'five_hour' ? 0 : kind === 'seven_day' ? 1 : 2)

/** Green below 50%, yellow below 80%, red from 80%. */
export function usageColor(pct: number): 'green' | 'yellow' | 'red' {
  return pct >= 80 ? 'red' : pct >= 50 ? 'yellow' : 'green'
}

/** Time until `resetsAt`, as `4h 14m`, `2d 3h` or `12m`; empty when unknown or past. */
export function fmtReset(resetsAt: string | undefined, now: number): string {
  const at = resetsAt === undefined ? Number.NaN : Date.parse(resetsAt)
  const mins = Math.floor((at - now) / 60_000)
  if (!Number.isFinite(mins) || mins <= 0) return ''
  const days = Math.floor(mins / 1440)
  const hours = Math.floor((mins % 1440) / 60)
  if (days > 0) return `${days}d ${hours}h`
  return hours > 0 ? `${hours}h ${mins % 60}m` : `${mins}m`
}

/** `fmtReset` without the space, for the band: `4h14m`. */
export const fmtResetShort = (resetsAt: string | undefined, now: number): string => fmtReset(resetsAt, now).replace(' ', '')

export const stepTokens = (u: StepUsage): Tokens => ({
  input: u.input_tokens + u.cache_read_input_tokens + u.cache_creation_input_tokens,
  output: u.output_tokens,
})

export function addTurn(tally: AgentTally | undefined, id: string, label: string, usage: StepUsage): AgentTally {
  const t = stepTokens(usage)
  return {
    id,
    label: tally?.label ?? label,
    turns: (tally?.turns ?? 0) + 1,
    input: (tally?.input ?? 0) + t.input,
    output: (tally?.output ?? 0) + t.output,
  }
}

/** Share of all tokens, 0 to 100, rounded. */
export function share(part: Tokens, total: Tokens): number {
  const all = total.input + total.output
  return all === 0 ? 0 : Math.round(((part.input + part.output) / all) * 100)
}
