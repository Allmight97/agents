#!/usr/bin/env python3
"""Behavior checks for render_recipe_table.py, run by scripts/test_plugins.py."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "render_recipe_table.py"
EXAMPLE = HERE.parent / "examples" / "stuffing-muffins.json"


def run(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, input=stdin)


def grid_widths(page: str) -> list[int]:
    """Expand rowspan/colspan and return how many grid columns each row fills."""
    rows = re.findall(r"<tr>(.*?)</tr>", page, re.S)
    filled = [0] * len(rows)
    for r, row in enumerate(rows):
        for cell in re.findall(r"<td([^>]*)>", row):
            rs = int((re.search(r'rowspan="(\d+)"', cell) or [0, 1])[1])
            cs = int((re.search(r'colspan="(\d+)"', cell) or [0, 1])[1])
            for k in range(r, r + rs):
                filled[k] += cs
    return filled


def main() -> int:
    html_out = run(str(EXAMPLE))
    assert html_out.returncode == 0, html_out.stderr
    page = html_out.stdout
    widths = grid_widths(page)
    assert len(widths) == 9, f"one row per ingredient: {widths}"
    assert len(set(widths)) == 1, f"every row must fill the same number of columns: {widths}"
    assert page.count('class="step finish"') == 1, "exactly one final cell"
    assert re.search(r'class="step finish" rowspan="9"', page), "final step spans every ingredient row"
    assert '<span class="callout">175°C</span>' in page, "temperatures are called out"
    assert '<span class="callout">10–15 min</span>' in page, "time ranges are called out"

    md = run(str(EXAMPLE), "--format", "md")
    assert md.returncode == 0, md.stderr
    steps = re.findall(r"^\d+\. \*\*([^*]+)\*\*", md.stdout, re.M)
    assert not re.search(r"°F|\d\s*(?:cups?|tbsp|tsp|oz|lb|inch)\b", md.stdout), "example output is metric"
    assert steps[0] == "CUT" and steps[-1] == "BAKE", steps
    assert steps.index("MELT") < steps.index("SAUTÉ") < steps.index("TOSS"), "inputs come before the step that uses them"

    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad.json"
        bad.write_text('{"dish": {"step": "Bake", "inputs": []}}')
        err = run(str(bad))
        assert err.returncode != 0 and "has no inputs" in err.stderr, err.stderr
    print("ok render_recipe_table")
    return 0


if __name__ == "__main__":
    sys.exit(main())
