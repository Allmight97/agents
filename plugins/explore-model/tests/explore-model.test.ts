// Run with: claude plugin test plugins/explore-model
import { describe, expect, test } from 'claude-code/testing'
import { withExploreDefaults } from '../hooks/explore-model.ts'

const defaults = { model: 'haiku', effort: 'medium' }

describe('withExploreDefaults', () => {
  test('fills model and effort on an Explore call that names neither', () => {
    expect(withExploreDefaults({ subagent_type: 'Explore', prompt: 'find x' }, defaults)).toEqual({
      subagent_type: 'Explore',
      prompt: 'find x',
      model: 'haiku',
      effort: 'medium',
    })
  })

  test('keeps a model or effort the call chose', () => {
    expect(withExploreDefaults({ subagent_type: 'Explore', model: 'opus' }, defaults)).toEqual({
      subagent_type: 'Explore',
      model: 'opus',
      effort: 'medium',
    })
  })

  test('leaves other subagent types alone', () => {
    const call = { subagent_type: 'general-purpose', prompt: 'do y' }
    expect(withExploreDefaults(call, defaults)).toBe(call)
  })
})
