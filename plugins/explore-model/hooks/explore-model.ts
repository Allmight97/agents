/**
 * explore-model — Claude Mod (EARLY ACCESS)
 *
 * The built-in Explore subagent runs on the main conversation's model unless
 * the Agent call names one. This fills `model` and `effort` on Explore calls
 * that leave them out, so Explore keeps Anthropic's prompt and read-only tools
 * and only the model changes. A call that names either keeps its own choice.
 */
import type { Register } from 'claude-code'

type Defaults = { model: string; effort: string }

export function withExploreDefaults<T extends { subagent_type?: string; model?: string; effort?: string }>(
  input: T,
  defaults: Defaults,
): T {
  if (input.subagent_type !== 'Explore') return input
  return { ...input, model: input.model ?? defaults.model, effort: input.effort ?? defaults.effort }
}

export const register: Register = (on, options) => {
  const defaults: Defaults = {
    model: typeof options.model === 'string' ? options.model : 'haiku',
    effort: typeof options.effort === 'string' ? options.effort : 'medium',
  }
  on('tool.call', { tool: 'Agent' }, ($, e, next) => next(withExploreDefaults(e, defaults)))
}
