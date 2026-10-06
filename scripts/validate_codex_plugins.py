#!/usr/bin/env python3
"""Run the pinned Codex plugin validator on every plugin that ships a Codex manifest.

The validator is the plugin-creator sample Codex removed upstream on 2026-09-27;
it predates the `disable-model-invocation` skill key and rejects it, while the
Codex runtime ignores the key. Each plugin is validated from a copy with that
key stripped, so the manifest, interface, and `agents/openai.yaml` checks still
hold.

Usage: validate_codex_plugins.py PATH_TO_validate_plugin.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

from validate_skills import split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
STRIPPED_KEY = "disable-model-invocation"


def strip_key(copy: Path) -> None:
    for skill_file in copy.rglob("SKILL.md"):
        meta, body = split_frontmatter(skill_file.read_text())
        if STRIPPED_KEY not in meta:
            continue
        del meta[STRIPPED_KEY]
        skill_file.write_text(
            "---\n"
            + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=10**6)
            + "---\n"
            + body
        )


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    validator = Path(sys.argv[1]).resolve()
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for manifest in sorted(ROOT.glob("plugins/*/.codex-plugin/plugin.json")):
            plugin_dir = manifest.parents[1]
            copy = Path(tmp).resolve() / plugin_dir.name
            shutil.copytree(plugin_dir, copy, ignore=shutil.ignore_patterns(".git", "node_modules"))
            strip_key(copy)
            result = subprocess.run(
                [sys.executable, str(validator), str(copy)], capture_output=True, text=True
            )
            output = (result.stdout + result.stderr).strip().replace(str(copy), str(plugin_dir))
            print(output)
            failed += result.returncode != 0
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
