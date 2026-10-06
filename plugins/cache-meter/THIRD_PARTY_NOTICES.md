# Third-Party Notices

`cache-meter` is adapted from `prompt-cache-control` in
[`davila7/claude-code-templates`](https://github.com/davila7/claude-code-templates),
path `cli-tool/components/mods/observability/prompt-cache-control`, taken at
commit `ef41915c4b69c2b8e2dfa37ae65977e438f853d0`. The upstream author is
`claude-code-templates`.

## Changes

- Renamed to `cache-meter`; the hooks module is `hooks/cache-meter.tsx`.
- The `AbovePrompt` band is one compact line with no bar and no glyphs. It sizes
  itself to `bodyColumns`, drops parts when narrow, and draws what other band
  mods return beneath it.
- The hit percentage is colored by ratio (green from 90%, yellow from 50%, red
  below). The upstream band colored its bar by advice state.
- `Advice` gained a short phrase (`short`) for the band. The full text stays in
  the `/cache` pane and the toasts.
- Fixes for `noUncheckedIndexedAccess` type errors. The cache model, `/cache`
  pane, toasts, `userConfig`, and the other tests are unchanged.

## License

MIT License

Copyright (c) 2025 Daniel (San) Ávila

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
