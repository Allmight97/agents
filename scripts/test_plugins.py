#!/usr/bin/env python3
"""Run every plugin's tests, found by file, so a new plugin needs no new line.

- A mod (`hooks/hooks.json`) with a `*.test.ts` or `*.test.tsx` file:
  `claude plugin validate` and `claude plugin test`.
- A `*.test.sh` file: `sh`.
- A `package.json` with a `test` script: `npm ci` when `node_modules` is
  missing, then `npm test`.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tests_in(plugin: Path, *patterns: str) -> list[Path]:
    return sorted(p for pattern in patterns for p in plugin.rglob(pattern) if "node_modules" not in p.parts)


def commands(plugin: Path) -> list[tuple[list[str], Path]]:
    found: list[tuple[list[str], Path]] = []
    if (plugin / "hooks" / "hooks.json").exists() and tests_in(plugin, "*.test.ts", "*.test.tsx"):
        found += [(["claude", "plugin", "validate", str(plugin)], ROOT), (["claude", "plugin", "test", str(plugin)], ROOT)]
    found += [(["sh", str(test)], ROOT) for test in tests_in(plugin, "*.test.sh")]
    package = plugin / "package.json"
    if package.exists() and "test" in json.loads(package.read_text()).get("scripts", {}):
        if not (plugin / "node_modules").exists():
            found.append((["npm", "ci", "--no-audit", "--no-fund"], plugin))
        found.append((["npm", "test"], plugin))
    return found


def main() -> int:
    failed: list[str] = []
    for plugin in sorted(p for p in (ROOT / "plugins").iterdir() if p.is_dir()):
        for command, cwd in commands(plugin):
            label = f"{plugin.name}: {' '.join(command[:3])}"
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
            print(f"{'ok  ' if result.returncode == 0 else 'FAIL'} {label}")
            if result.returncode != 0:
                failed.append(label)
                print((result.stdout + result.stderr).strip(), file=sys.stderr)
    if failed:
        print(f"{len(failed)} failed: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
