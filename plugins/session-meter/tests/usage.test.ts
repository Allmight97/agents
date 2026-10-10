// Run with: claude plugin test plugins/session-meter
import { describe, expect, test } from 'claude-code/testing'
import { addTurn, fmtReset, limitLabel, planLimits, share, usageColor } from '../hooks/usage.ts'

const usage = { input_tokens: 10, output_tokens: 5, cache_read_input_tokens: 80, cache_creation_input_tokens: 10 }
const NOW = Date.parse('2026-10-10T12:00:00Z')

describe('plan limits', () => {
  test('orders five-hour, then weekly, then other windows', () => {
    const kinds = planLimits([
      { kind: 'other_window', percentUsed: 1 },
      { kind: 'seven_day', percentUsed: 2 },
      { kind: 'five_hour', percentUsed: 3 },
    ]).map(l => limitLabel(l.kind))
    expect(kinds).toEqual(['5h', 'wk', 'other window'])
  })

  test('colours use green, then yellow from 50%, then red from 80%', () => {
    expect([usageColor(49), usageColor(50), usageColor(80)]).toEqual(['green', 'yellow', 'red'])
  })

  test('formats the time until a reset, and nothing once it passed', () => {
    expect(fmtReset('2026-10-10T16:14:00Z', NOW)).toBe('4h 14m')
    expect(fmtReset('2026-10-12T15:00:00Z', NOW)).toBe('2d 3h')
    expect(fmtReset('2026-10-10T11:00:00Z', NOW)).toBe('')
    expect(fmtReset(undefined, NOW)).toBe('')
  })
})

describe('subagent tally', () => {
  test('adds each turn, counting cached prompt tokens as input', () => {
    const once = addTurn(undefined, 'a1', 'Explore: find callers', usage)
    const twice = addTurn(once, 'a1', 'ignored', usage)
    expect(twice).toEqual({ id: 'a1', label: 'Explore: find callers', turns: 2, input: 200, output: 10 })
  })

  test('share is a rounded percent of all tokens, zero for an empty session', () => {
    expect(share({ input: 25, output: 0 }, { input: 75, output: 25 })).toBe(25)
    expect(share({ input: 0, output: 0 }, { input: 0, output: 0 })).toBe(0)
  })
})
