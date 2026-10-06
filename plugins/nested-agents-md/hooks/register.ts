import type { EngineInterface, FsAncestor, On } from 'claude-code'

const AGENTS_NAMES = ['AGENTS.md', '.claude/AGENTS.md'] as const
const CLAUDE_NAMES = ['CLAUDE.md', '.claude/CLAUDE.md', 'CLAUDE.local.md'] as const
const MAIN_LOOP = 'main'
const MAX_TOKENS = 32
const TOKEN = /"((?:[^"\\]|\\.)*)"|'([^']*)'|([^\s"'|;&<>()`]+)/g
const WRITTEN = /(?:>>?|\btee(?:\s+-a)?)\s*(?:"([^"]*)"|'([^']*)'|([^\s"'|;&<>()`]+))/g
const NONE: readonly FsAncestor[] = []

type Target = { path: string; mayBeNew: boolean }

export function register(on: On): void {
  const given = new Map<string, Set<string>>()
  let handed = new Set<string>()
  let isClaudeProject: boolean | undefined
  let rootSeen: string | undefined

  on('prompt.context', ($, e, next) => {
    const files = e.instructionFiles

    return next(e).finally(() => {
      given.clear()
      handed = new Set(files?.map(file => normal(file.path)))
    })
  })

  on('agent.spawn', { fork: true }, async ($, e, next) => {
    const result = await next(e)

    if (result.agentId !== undefined) {
      given.set(result.agentId, new Set(given.get(e.parentAgentId ?? MAIN_LOOP)))
    }

    return result
  })

  on('tool.call', async ($, e, next) => {
    const result = await next(e)
    const paths = pathsOf(e)
    const isSettled = paths === undefined || result.deny !== undefined || result.isError

    if (isSettled || !(await attaches($))) {
      return result
    }

    const root = await $.session.root()

    if (root !== rootSeen) {
      rootSeen = root
      isClaudeProject = undefined
      given.clear()
    }

    isClaudeProject ??= (await $.fs.ancestors({ names: CLAUDE_NAMES })).length > 0

    if (isClaudeProject) {
      return result
    }

    const loop = e.agentId ?? MAIN_LOOP
    const sent = given.get(loop) ?? new Set<string>()
    given.set(loop, sent)
    const targets = await targetsOf($, paths, root)
    const fresh: FsAncestor[] = []

    for (const target of targets) {
      for (const file of await nestedOf($, target, root)) {
        const path = normal(file.parts[0]?.path ?? `${file.dir}/${file.name}`)

        if (!sent.has(path) && !handed.has(path)) {
          sent.add(path)
          fresh.push(file)
        }
      }
    }

    const isObservedOnly = e.tool === 'Read' || fresh.length === 0

    return isObservedOnly
      ? result
      : { ...result, context: [...(result.context ?? []), ...fresh.flatMap(frames)] }
  })
}

function pathsOf(e: { tool: string } & Record<string, unknown>): Target[] | undefined {
  if (e.tool === 'Bash' && typeof e.command === 'string') {
    const written = [...e.command.matchAll(WRITTEN)].map(match => ({ path: match[1] ?? match[2] ?? match[3] ?? '', mayBeNew: true }))

    return [...written, ...tokensOf(e.command).map(path => ({ path, mayBeNew: false }))]
  }

  const isFileTool = e.tool === 'Read' || e.tool === 'Edit' || e.tool === 'Write'

  return isFileTool && typeof e.file_path === 'string' ? [{ path: e.file_path, mayBeNew: e.tool === 'Write' }] : undefined
}

function tokensOf(command: string): string[] {
  const tokens: string[] = []

  for (const match of command.matchAll(TOKEN)) {
    const raw = match[1] ?? match[2] ?? match[3] ?? ''
    const token = raw.includes('=') ? raw.slice(raw.lastIndexOf('=') + 1) : raw
    const isPathLike = token !== '' && !token.startsWith('-') && !/[$*?[\]{}]/.test(token)

    if (isPathLike) {
      tokens.push(token)
    }

    if (tokens.length === MAX_TOKENS) {
      break
    }
  }

  return tokens
}

async function targetsOf($: EngineInterface, targets: Target[], root: string): Promise<string[]> {
  const [cwd, home] = await Promise.all([$.session.cwd(), $.env.get('HOME')])
  const kept = await Promise.all(
    targets.map(async ({ path, mayBeNew }) => {
      const absolute = absoluteOf(path, cwd, home)

      return path !== '' && isBelow(absolute, root) && (await isFileTarget($, absolute, mayBeNew)) ? absolute : undefined
    }),
  )

  return [...new Set(kept.filter(path => path !== undefined))]
}

async function isFileTarget($: EngineInterface, path: string, mayBeNew: boolean): Promise<boolean> {
  const kind = await kindOf($, path)
  const isNewFile = mayBeNew && kind === undefined && (await kindOf($, dirOf(path))) === 'dir'

  return kind === 'file' || isNewFile
}

const kindOf = ($: EngineInterface, path: string) =>
  $.fs.stat(path).then(
    stat => stat.kind,
    () => undefined,
  )

async function nestedOf($: EngineInterface, of: string, root: string): Promise<readonly FsAncestor[]> {
  const [agents, claude] = await Promise.all([
    $.fs.ancestors({ names: AGENTS_NAMES, of, below: root }),
    $.fs.ancestors({ names: CLAUDE_NAMES, of, below: root }),
  ]).catch((): [typeof NONE, typeof NONE] => [NONE, NONE])
  const claudeDirs = new Set(claude.map(file => normal(file.dir)))

  return agents.filter(file => !claudeDirs.has(normal(file.dir)) && isBelow(file.dir, root))
}

const frames = (file: FsAncestor): string[] =>
  file.parts.map(part => `Contents of ${part.path}:\n\n${part.content}`)

async function attaches($: EngineInterface): Promise<boolean> {
  const [simple, attachmentsOff] = await Promise.all([
    $.env.get('CLAUDE_CODE_SIMPLE'),
    $.env.get('CLAUDE_CODE_DISABLE_ATTACHMENTS'),
  ])

  return !isOn(simple) && !isOn(attachmentsOff)
}

const isOn = (value: string | undefined): boolean =>
  value !== undefined && ['1', 'true', 'yes', 'on'].includes(value.trim().toLowerCase())

function absoluteOf(path: string, cwd: string, home: string | undefined): string {
  if ((path === '~' || path.startsWith('~/')) && home !== undefined) {
    return `${home.replace(/\/+$/, '')}${path.slice(1)}`
  }

  return path.startsWith('/') ? path : `${cwd.replace(/\/+$/, '')}/${path}`
}

const normal = (path: string): string =>
  path
    .replaceAll('\\', '/')
    .replace(/\/\.(?=\/|$)/g, '')
    .replace(/(?<=.)\/+$/, '')

const isBelow = (path: string, dir: string): boolean => normal(path).startsWith(`${normal(dir)}/`)

const dirOf = (path: string): string => normal(path).replace(/\/[^/]*$/, '') || '/'
