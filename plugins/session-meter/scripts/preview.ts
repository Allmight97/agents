// Writes an HTML page that draws the Desktop band for sample states at its real size: bun scripts/preview.ts <out.html>
import { bandLine, inkHex, WEEK_BAR, weekBarSvg } from '../hooks/band.ts'
import type { BandModel } from '../hooks/band.ts'

const states: [string, BandModel][] = [
  ['quiet', { fiveHour: { pct: 17, reset: '2h1m' }, week: { pct: 11, pace: 0.08 }, ctx: 44, cache: { hit: 98, clock: '58:35', clockColor: 'green' } }],
  ['busy', { fiveHour: { pct: 62, reset: '1h4m' }, week: { pct: 62, pace: 0.57 }, ctx: 61, cache: { hit: 85, clock: '18:02', clockColor: 'yellow' } }],
  ['hot', { fiveHour: { pct: 91, reset: '12m' }, week: { pct: 88, pace: 0.7 }, ctx: 92, cache: { hit: 40, clock: '0:41', clockColor: 'red' }, advice: 'expires soon' }],
]
const row = ([name, m]: [string, BandModel]) => {
  const items = bandLine(m).map(item =>
    item.kind === 'weekBar'
      ? `<img width="${WEEK_BAR.width}" height="${WEEK_BAR.height}" src="data:image/svg+xml;utf8,${encodeURIComponent(weekBarSvg(item))}">`
      : `<span style="color:${inkHex(item.ink)};${item.bold ? 'font-weight:600' : ''}">${item.text}</span>`,
  )
  return `<p>${name}</p><div class="band">${items.join('')}</div>`
}
const html = `<!doctype html><meta charset="utf-8"><style>body{background:#1e1e1e;color:#ccc;font:13px -apple-system,sans-serif;padding:16px}.band{display:flex;align-items:center;gap:8px;font:13px ui-monospace,Menlo,monospace;padding:8px;border:1px solid #333;border-radius:8px;width:fit-content}</style>${states.map(row).join('')}`
await Bun.write(process.argv[2] ?? 'band-preview.html', html)
