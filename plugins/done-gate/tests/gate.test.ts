// Run with: claude plugin test plugins/done-gate
import { describe, expect, test } from 'claude-code/testing'
import { decide, isCheck, parseConfig } from '../hooks/gate.ts'
import type { Config } from '../hooks/gate.ts'

const config = (over: object = {}): Config => {
  const parsed = parseConfig(JSON.stringify({ checks: ['^bash scripts/verify\\.sh'], paths: ['src/', 'crates/'], ...over }))
  if ('error' in parsed) throw new Error(parsed.error)
  return parsed
}

describe('parseConfig', () => {
  test('rejects a config without checks', () => {
    expect(parseConfig('{"paths": ["src/"]}')).toEqual({ error: '"checks" must be a non-empty list of regular expressions' })
  })

  test('rejects text that is not JSON', () => {
    expect(parseConfig('checks: verify')).toEqual({ error: 'is not valid JSON' })
  })

  test('rejects an invalid pattern', () => {
    expect(parseConfig('{"checks": ["("]}')).toEqual({ error: '"checks" holds an invalid regular expression' })
  })

  test('uses the first check as the hint when none is given', () => {
    expect(config().hint).toBe('^bash scripts/verify\\.sh')
  })
})

describe('isCheck', () => {
  test('matches a configured command and not another', () => {
    expect(isCheck(config(), 'bash scripts/verify.sh engine')).toBe(true)
    expect(isCheck(config(), 'echo bash scripts/verify.sh')).toBe(false)
  })
})

describe('decide', () => {
  test('passes when nothing guarded is unproven', () => {
    expect(decide({ config: config(), unproven: ['README.md', 'docs/a.md'], isRetry: false })).toEqual({ kind: 'pass' })
  })

  test('blocks the first stop with the unproven guarded files and the hint', () => {
    const verdict = decide({ config: config({ hint: 'bash scripts/verify.sh' }), unproven: ['src/a.ts', 'docs/a.md'], isRetry: false })
    expect(verdict.kind).toBe('block')
    expect(verdict.kind === 'block' && verdict.reason.includes('1 file(s)')).toBe(true)
    expect(verdict.kind === 'block' && verdict.reason.includes('src/a.ts')).toBe(true)
    expect(verdict.kind === 'block' && verdict.reason.includes('`bash scripts/verify.sh`')).toBe(true)
  })

  test('releases the retry so the turn cannot loop', () => {
    expect(decide({ config: config(), unproven: ['crates/x.rs'], isRetry: true }).kind).toBe('release')
  })

  test('guards every file when paths is empty', () => {
    expect(decide({ config: config({ paths: [] }), unproven: ['README.md'], isRetry: false }).kind).toBe('block')
  })
})
