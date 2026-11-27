#!/usr/bin/env python3
"""Render a recipe tree (JSON) as a colorized Tabular Recipe Notation table.

Usage: render_recipe_table.py RECIPE.json [--format html|md] [-o OUT]

The JSON is a tree. The root is the last step; every step lists its inputs;
leaves are ingredients. Layout follows from the tree, so spans never need
hand placement:

  ingredient  {"qty": "2 cups", "item": "celery, diced"}
  step        {"step": "Saute", "note": "medium-low, 10 min",
               "kind": "heat", "inputs": [ ... ]}   # kind is optional

Rows are ingredients in depth-first order. A step's column is one past its
deepest input, its cell spans the rows of its ingredients, and it stretches
right until its parent's column, so every grid cell is covered exactly once.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

KINDS = ("prep", "combine", "heat", "rest", "finish")
VERBS = {
    "prep": "cut chop dice mince slice grate zest peel trim cube crush grind halve julienne measure sift rinse drain pat grease line soak",
    "combine": "mix whisk stir toss fold combine beat cream knead add pour moisten season blend fill layer coat dredge assemble spread top",
    "heat": "bake roast saute sear fry boil simmer melt toast broil grill brown poach steam heat reduce cook caramelize blanch braise preheat",
    "rest": "rest chill cool marinate proof rise freeze set refrigerate steep",
}
CALLOUT = re.compile(
    r"(\d+(?:[.,]\d+)?\s*°\s*[FC]"
    r"|\d+(?:[.,]\d+)?(?:\s*[–-]\s*\d+(?:[.,]\d+)?)?\s*(?:min(?:ute)?s?|hrs?|hours?|sec(?:ond)?s?|h)\b)",
    re.IGNORECASE,
)


@dataclass
class Node:
    qty: str = ""
    item: str = ""
    step: str = ""
    note: str = ""
    kind: str = ""
    inputs: list["Node"] = field(default_factory=list)
    col: int = 0
    first_row: int = 0
    last_row: int = 0

    @property
    def is_leaf(self) -> bool:
        return not self.step


def parse(raw: dict, where: str = "dish") -> Node:
    if "step" in raw:
        inputs = raw.get("inputs") or []
        if not inputs:
            raise ValueError(f"{where}: step '{raw['step']}' has no inputs; give it at least one ingredient or step")
        kind = raw.get("kind") or infer_kind(raw["step"])
        if kind and kind not in KINDS:
            raise ValueError(f"{where}: kind '{kind}' is not one of {', '.join(KINDS)}")
        return Node(step=raw["step"], note=raw.get("note", ""), kind=kind,
                    inputs=[parse(r, f"{where} > {raw['step']}") for r in inputs])
    if "item" in raw:
        return Node(qty=raw.get("qty", ""), item=raw["item"])
    raise ValueError(f"{where}: each node needs 'step' (with 'inputs') or 'item'; got keys {sorted(raw)}")


def infer_kind(verb: str) -> str:
    words = re.findall(r"[a-z]+", verb.lower().replace("é", "e"))
    for kind, verbs in VERBS.items():
        if any(w in verbs.split() for w in words):
            return kind
    return ""


def layout(root: Node) -> list[Node]:
    leaves: list[Node] = []

    def walk(node: Node) -> None:
        if node.is_leaf:
            node.first_row = node.last_row = len(leaves)
            node.col = 0
            leaves.append(node)
            return
        for child in node.inputs:
            walk(child)
        node.col = 1 + max(c.col for c in node.inputs)
        node.first_row = node.inputs[0].first_row
        node.last_row = node.inputs[-1].last_row

    walk(root)
    return leaves


def callouts(text: str) -> str:
    out, last = [], 0
    for m in CALLOUT.finditer(text):
        out.append(html.escape(text[last:m.start()]))
        out.append(f'<span class="callout">{html.escape(m.group(0))}</span>')
        last = m.end()
    out.append(html.escape(text[last:]))
    return "".join(out)


def render_html(recipe: dict, root: Node) -> str:
    leaves = layout(root)
    # Grid columns: 0 = quantity, 1 = ingredient (tree col 0), k+1 = tree col k.
    cells: dict[tuple[int, int], str] = {}

    def place(node: Node, end_col: int) -> None:
        rows = node.last_row - node.first_row + 1
        if node.is_leaf:
            span = end_col  # item covers tree cols 0..end_col-1
            cells[(node.first_row, 0)] = f'<td class="qty">{html.escape(node.qty)}</td>'
            cells[(node.first_row, 1)] = f'<td class="item"{attr("colspan", span)}>{html.escape(node.item)}</td>'
            return
        cls = "step finish" if node is root else f"step {node.kind or 'other'}"
        span = end_col - node.col
        note = f'<span class="note">{callouts(node.note)}</span>' if node.note else ""
        cells[(node.first_row, node.col + 1)] = (
            f'<td class="{cls}"{attr("rowspan", rows)}{attr("colspan", span)}>'
            f'<strong>{html.escape(node.step)}</strong>{note}</td>')
        for child in node.inputs:
            place(child, node.col)

    place(root, root.col + 1)
    body = "\n".join(
        "<tr>" + "".join(cells[(r, c)] for c in sorted(k for (rr, k) in cells if rr == r)) + "</tr>"
        for r in range(len(leaves)))
    title = html.escape(recipe.get("title", "Recipe"))
    meta = " · ".join(callouts(m) for m in recipe.get("meta", []))
    meta = (meta + " · " if meta else "") + "Read left to right: each box combines everything to its left."
    notes = "".join(f"<li>{callouts(n)}</li>" for n in recipe.get("notes", []))
    notes = f'<ul class="notes">{notes}</ul>' if notes else ""
    source = recipe.get("source", "")
    source = f'<p class="source">Source: {html.escape(source)}</p>' if source else ""
    return TEMPLATE.format(title=title, meta=meta, rows=body, notes=notes, source=source)


def attr(name: str, n: int) -> str:
    return f' {name}="{n}"' if n > 1 else ""


def render_md(recipe: dict, root: Node) -> str:
    """Fallback for surfaces without HTML: numbered steps in cook order."""
    layout(root)
    lines = [f"## {recipe.get('title', 'Recipe')}"]
    if recipe.get("meta"):
        lines.append("_" + " · ".join(md_callouts(m) for m in recipe["meta"]) + "_")
    lines.append("")
    numbers: dict[int, int] = {}

    def walk(node: Node) -> None:
        for child in node.inputs:
            if not child.is_leaf:
                walk(child)
        parts = []
        for child in node.inputs:
            if child.is_leaf:
                parts.append(f"**{child.qty}** {child.item}".strip() if child.qty else child.item)
            else:
                parts.append(f"(step {numbers[id(child)]})")
        numbers[id(node)] = len(numbers) + 1
        note = f" — {md_callouts(node.note)}" if node.note else ""
        lines.append(f"{numbers[id(node)]}. **{node.step.upper()}** {' + '.join(parts)}{note}")

    walk(root)
    lines += [f"- {md_callouts(n)}" for n in recipe.get("notes", [])]
    return "\n".join(lines) + "\n"


def md_callouts(text: str) -> str:
    return CALLOUT.sub(lambda m: f"`{m.group(0)}`", text)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --ink:#282828; --muted:#6f6f6f; --line:#3b3b39; --paper:#ffffff;
  --ingr-bg:#f5f3e7; --qty:#6b5a1e;
  --prep:#e8f0fb; --combine:#fdf3dc; --heat:#fbe4dc; --rest:#e6f2f4; --other:#ffffff;
  --finish:#eaf1e1; --finish-ink:#2f5d1f;
  --callout-bg:#fff0c2; --callout-ink:#7a3d00;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --ink:#ececec; --muted:#a8a8a8; --line:#8a8a84; --paper:#1b1b1a;
    --ingr-bg:#2c2a22; --qty:#e2c76b;
    --prep:#1f2a3a; --combine:#3a3220; --heat:#3d2420; --rest:#1d3236; --other:#1b1b1a;
    --finish:#24331d; --finish-ink:#b9e0a3;
    --callout-bg:#4a3a10; --callout-ink:#ffd98a;
  }}
}}
body {{ font: 15px/1.35 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  color:var(--ink); background:var(--paper); margin:2rem; }}
h1 {{ font-size:1.9rem; margin:0 0 .3rem; }}
.meta {{ color:var(--muted); margin:0 0 1.2rem; }}
.wrap {{ overflow-x:auto; }}
table {{ border-collapse:collapse; border:2px solid var(--line); }}
td {{ border:1px solid var(--line); padding:.55rem .7rem; vertical-align:middle; }}
td.qty {{ background:var(--ingr-bg); color:var(--qty); font-weight:700; white-space:nowrap; }}
td.item {{ background:var(--ingr-bg); white-space:nowrap; }}
td.step {{ text-align:center; min-width:5.5rem; }}
td.step strong {{ display:block; font-size:1.05rem; }}
td.step .note {{ display:block; font-size:.8rem; color:var(--muted); margin-top:.2rem; }}
td.prep {{ background:var(--prep); }} td.combine {{ background:var(--combine); }}
td.heat {{ background:var(--heat); }} td.rest {{ background:var(--rest); }}
td.other {{ background:var(--other); }}
td.finish {{ background:var(--finish); }} td.finish strong {{ color:var(--finish-ink); }}
.callout {{ background:var(--callout-bg); color:var(--callout-ink); font-weight:600;
  border-radius:.3em; padding:0 .25em; white-space:nowrap; }}
.notes, .source {{ color:var(--muted); font-size:.9rem; }}
@media print {{ body {{ margin:0; }} .wrap {{ overflow:visible; }} }}
</style></head>
<body>
<h1>{title}</h1>
<p class="meta">{meta}</p>
<div class="wrap"><table>
{rows}
</table></div>
{notes}{source}
</body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("recipe", type=Path)
    ap.add_argument("--format", choices=("html", "md"), default="html")
    ap.add_argument("-o", "--out", type=Path)
    args = ap.parse_args()
    recipe = json.loads(args.recipe.read_text())
    root = parse(recipe["dish"])
    text = render_html(recipe, root) if args.format == "html" else render_md(recipe, root)
    if args.out:
        args.out.write_text(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
