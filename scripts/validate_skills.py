#!/usr/bin/env python3
"""Validate every SKILL.md with the pinned Agent Skills validator.

Frontmatter stays within the specification because claude.ai skill uploads
reject any other key.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_REF_PIN = "git+https://github.com/agentskills/agentskills.git@217be548739f21d6008915c29aefe320ea1a90af#subdirectory=skills-ref"


def skills_ref() -> list[str]:
    if shutil.which("skills-ref"):
        return ["skills-ref"]
    if shutil.which("uvx"):
        return ["uvx", "--from", SKILLS_REF_PIN, "skills-ref"]
    sys.exit("install uv (for uvx) or skills-ref: python3 -m pip install " + SKILLS_REF_PIN)


def main() -> int:
    command = skills_ref()
    skill_dirs = sorted(p.parent for p in (ROOT / "plugins").rglob("SKILL.md"))
    failed = 0
    for skill_dir in skill_dirs:
        result = subprocess.run([*command, "validate", str(skill_dir)], capture_output=True, text=True)
        if result.returncode != 0:
            failed += 1
            print(f"{skill_dir.relative_to(ROOT)}: {(result.stdout + result.stderr).strip()}")
    print(f"{len(skill_dirs)} skills checked, {failed} problems")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
