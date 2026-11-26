/**
 * band.ts — the pure half of the band above the prompt: no `$`, no engine.
 *
 * `bandLine` decides what the band says; the painters only draw it, as Desktop
 * elements or as terminal cells. The row is text with one gauge: the week's
 * bar, with a tick where an even pace through the week would be.
 */
import type { LifeColor } from './cache.ts'

export type BandModel = {
  fiveHour?: { pct: number; reset: string }
  week?: { pct: number; pace: number }
  ctx?: number
  cache?: { hit: number; clock?: string; clockColor: LifeColor }
  advice?: string
}

type Tone = 'green' | 'yellow' | 'red'
type Ink = Tone | 'dim' | 'label'

export type BandItem =
  | { kind: 'text'; text: string; ink: Ink; bold?: boolean }
  | { kind: 'weekBar'; pct: number; pace: number; tone: Tone }

const HEX: Record<Ink | 'track', string> = {
  green: '#3fb950',
  yellow: '#d29922',
  red: '#f85149',
  dim: '#8b949e',
  label: '#4a9fd8',
  track: '#8b949e',
}

export const usageTone = (pct: number): Tone => (pct >= 80 ? 'red' : pct >= 50 ? 'yellow' : 'green')
export const hitTone = (pct: number): Tone => (pct >= 90 ? 'green' : pct >= 50 ? 'yellow' : 'red')

const WEEK_MS = 7 * 24 * 3_600_000

/** Share of the week gone by, 0 to 1, from when the weekly window resets. */
export function weekPace(resetsAt: string | undefined, now: number): number {
  const at = resetsAt === undefined ? Number.NaN : Date.parse(resetsAt)
  if (!Number.isFinite(at)) return 0
  return Math.min(1, Math.max(0, 1 - (at - now) / WEEK_MS))
}

/** What the band says, left to right, with a dot between groups. */
export function bandLine(m: BandModel): BandItem[] {
  const groups: BandItem[][] = []
  const text = (t: string, ink: Ink, bold = false): BandItem => ({ kind: 'text', text: t, ink, bold })
  if (m.fiveHour) {
    const g = [text('5h', 'label'), text(`${m.fiveHour.pct}%`, usageTone(m.fiveHour.pct), true)]
    if (m.fiveHour.reset) g.push(text(m.fiveHour.reset, 'dim'))
    groups.push(g)
  }
  if (m.week) {
    const tone = usageTone(m.week.pct)
    groups.push([text('wk', 'label'), { kind: 'weekBar', pct: m.week.pct, pace: m.week.pace, tone }, text(`${m.week.pct}%`, tone, true)])
  }
  if (m.ctx !== undefined) groups.push([text('ctx', 'label'), text(`${m.ctx}%`, usageTone(m.ctx), true)])
  if (m.cache) {
    const g = [text('cache', 'label'), text(`${m.cache.hit}%`, hitTone(m.cache.hit), true)]
    if (m.cache.clock) g.push(text(m.cache.clock, m.cache.clockColor, true))
    groups.push(g)
  }
  if (m.advice) groups.push([text(m.advice, 'dim')])
  return groups.flatMap((g, i) => (i > 0 ? [text('·', 'dim'), ...g] : g))
}

export function weekAlt(item: Extract<BandItem, { kind: 'weekBar' }>): string {
  return `weekly limit ${item.pct}% used; an even pace would be ${Math.round(item.pace * 100)}%`
}

export const WEEK_BAR = { width: 64, height: 12 } as const

/** The week's bar as an SVG picture: its use filled in its colour, a tick at the even pace. */
export function weekBarSvg(item: Extract<BandItem, { kind: 'weekBar' }>): string {
  const { width: w, height: h } = WEEK_BAR
  const fill = Math.round((Math.min(100, item.pct) / 100) * w)
  const tick = Math.min(w - 2, Math.round(item.pace * w))
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect y="3" width="${w}" height="6" rx="3" fill="${HEX.track}" fill-opacity="0.3"/>${fill > 0 ? `<rect y="3" width="${Math.max(6, fill)}" height="6" rx="3" fill="${HEX[item.tone]}"/>` : ''}<rect x="${tick}" width="2" height="${h}" rx="1" fill="#e6edf3"/></svg>`
}

export type TerminalRun = { text: string; color: string; bold?: boolean }

export const inkHex = (ink: Ink): string => HEX[ink]

/** The terminal band as coloured runs, cut at `columns` cells. */
export function terminalRuns(items: BandItem[], columns: number): TerminalRun[] {
  const runs: TerminalRun[] = []
  items.forEach((item, i) => {
    const sep = i > 0 ? ' ' : ''
    if (item.kind === 'text') {
      runs.push({ text: `${sep}${item.text}`, color: HEX[item.ink], bold: item.bold })
      return
    }
    const cells = 6
    const filled = Math.round((Math.min(100, item.pct) / 100) * cells)
    const tick = Math.min(cells - 1, Math.round(item.pace * cells))
    if (sep) runs.push({ text: sep, color: HEX.dim })
    for (let c = 0; c < cells; c++) {
      runs.push(c === tick ? { text: '│', color: HEX.dim } : { text: c < filled ? '▰' : '▱', color: c < filled ? HEX[item.tone] : HEX.dim })
    }
  })
  const out: TerminalRun[] = []
  let used = 0
  for (const run of runs) {
    if (used >= columns) break
    const text = run.text.slice(0, columns - used)
    used += text.length
    out.push({ ...run, text })
  }
  return out
}
