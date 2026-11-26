#!/usr/bin/env python3
"""Check what `claude plugin validate` skips.

Each catalog source is a folder in this repo whose manifest name matches its
catalog entry and has no top-level `bin/` (claude.ai and Cowork refuse such
a plugin), and each copied file matches its original: an installed plugin
is its own folder and cannot read a file in another plugin.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
COPIES = {
    ROOT / "plugins/complexity-lens/scripts/complexity_rank.py": ROOT
    / "plugins/personal-skills/skills/whittle/scripts/complexity_rank.py",
}


class ValidationError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"{path.relative_to(ROOT)}: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{path.relative_to(ROOT)}: expected a JSON object")
    return value


def plugin_roots() -> dict[Path, str]:
    roots: dict[Path, str] = {}
    for entry in load_json(MARKETPLACE).get("plugins", []):
        name, source = entry.get("name"), entry.get("source")
        if not isinstance(source, str):
            raise ValidationError(f"{name}: source must be a relative path in this repo")
        plugin_dir = (ROOT / source).resolve()
        if not plugin_dir.is_relative_to(ROOT) or not plugin_dir.is_dir():
            raise ValidationError(f"{name}: {source} is not a directory in this repo")
        if name in roots.values():
            raise ValidationError(f"duplicate plugin name {name}")
        manifest = load_json(plugin_dir / ".claude-plugin" / "plugin.json")
        if manifest.get("name") != name:
            raise ValidationError(f"{name}: manifest name is {manifest.get('name')!r}")
        if (plugin_dir / "bin").exists():
            raise ValidationError(f"{name}: a top-level bin/ makes claude.ai refuse the plugin")
        roots[plugin_dir] = name
    return roots


def validate() -> None:
    plugin_roots()
    for copy, original in COPIES.items():
        if copy.read_bytes() != original.read_bytes():
            raise ValidationError(
                f"{copy.relative_to(ROOT)} differs from {original.relative_to(ROOT)}; copy the original over it"
            )


def main() -> int:
    try:
        validate()
    except ValidationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print("marketplace sources and copies are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
