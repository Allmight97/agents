// Run with: claude plugin test plugins/session-meter
import { describe, expect, test } from 'claude-code/testing'
import { addTurn, fmtReset, fmtResetShort, limitLabel, limitsToWake, planLimits, share, usageColor, wakeText } from '../hooks/usage.ts'

const usage = { input_tokens: 10, output_tokens: 5, cache_read_input_tokens: 80, cache_creation_input_tokens: 10 }
const NOW = Date.parse('2026-10-10T12:00:00Z')

describe('plan limits', () => {
  test('a limit wakes once per window: a dip does not arm it again, a new reset does', () => {
    const at = (percentUsed: number, resetsAt = '2026-10-15T23:00:00Z') => [{ kind: 'seven_day', percentUsed, resetsAt }, { kind: 'other_window', percentUsed: 99 }]
    const below = limitsToWake(at(89), {})
    expect(below.wake).toEqual([])
    const crossed = limitsToWake(at(92), below.alerted)
    expect(crossed.wake.map(l => l.kind)).toEqual(['seven_day'])
    const dipped = limitsToWake(at(89.9), crossed.alerted)
    expect(dipped.wake).toEqual([])
    expect(limitsToWake(at(91), dipped.alerted).wake).toEqual([])
    expect(limitsToWake(at(92, '2026-10-15T23:00:20Z'), dipped.alerted).wake).toEqual([])
    expect(limitsToWake(at(93, '2026-10-22T23:00:00Z'), dipped.alerted).wake.map(l => l.kind)).toEqual(['seven_day'])
  })

  test('the wake text names the limit and its reset', () => {
    expect(wakeText([{ kind: 'seven_day', percentUsed: 91.4, resetsAt: '2026-10-10T16:14:00Z' }], NOW)).toContain('wk 91% (resets in 4h 14m)')
  })

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
    expect(fmtResetShort('2026-10-10T16:14:00Z', NOW)).toBe('4h14m')
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
