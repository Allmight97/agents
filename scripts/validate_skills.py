#!/usr/bin/env python3
"""Validate every SKILL.md with the pinned Agent Skills validator.

Frontmatter stays within the specification plus `CLAUDE_KEYS`; see AGENTS.md.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_REF_PIN = "git+https://github.com/agentskills/agentskills.git@217be548739f21d6008915c29aefe320ea1a90af#subdirectory=skills-ref"
CLAUDE_KEYS = {"disable-model-invocation: true"}


def skills_ref() -> list[str]:
    if shutil.which("skills-ref"):
        return ["skills-ref"]
    if shutil.which("uvx"):
        return ["uvx", "--from", SKILLS_REF_PIN, "skills-ref"]
    sys.exit("install uv (for uvx) or skills-ref: python3 -m pip install " + SKILLS_REF_PIN)


def spec_copy(skill_dir: Path, scratch: Path) -> Path:
    head, sep, body = skill_dir.joinpath("SKILL.md").read_text().partition("\n---\n")
    kept = [line for line in head.splitlines() if line.strip() not in CLAUDE_KEYS]
    copy = scratch / skill_dir.name
    copy.mkdir()
    copy.joinpath("SKILL.md").write_text("\n".join(kept) + sep + body)
    return copy


def main() -> int:
    command = skills_ref()
    skill_dirs = sorted(p.parent for p in (ROOT / "plugins").rglob("SKILL.md"))
    failed = 0
    with tempfile.TemporaryDirectory() as scratch:
        for skill_dir in skill_dirs:
            result = subprocess.run([*command, "validate", str(spec_copy(skill_dir, Path(scratch)))], capture_output=True, text=True)
            if result.returncode != 0:
                failed += 1
                print(f"{skill_dir.relative_to(ROOT)}: {(result.stdout + result.stderr).strip()}")
    print(f"{len(skill_dirs)} skills checked, {failed} problems")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
