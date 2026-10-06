#!/usr/bin/env python3
"""Validate every SKILL.md against the pinned Agent Skills validator.

Two client extension keys are allowed beyond the specification:
`disable-model-invocation` and `user-invocable`, both boolean. They are
stripped from a temporary copy before `skills-ref validate` runs, so the
portable validator still judges everything else.

Parity: `disable-model-invocation: true` requires
`agents/openai.yaml` `policy.allow_implicit_invocation: false`. The reverse is
not required: a skill may be explicit-only on Codex alone (whittle, diagnose,
to-issues) because Claude's flag also blocks one skill invoking another.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXTENSION_KEYS = {"disable-model-invocation", "user-invocable"}
SPEC_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    meta = yaml.safe_load(text[4:end])
    if not isinstance(meta, dict):
        raise ValueError("frontmatter is not a mapping")
    return meta, text[end + 5 :]


def codex_allows_implicit(skill_dir: Path) -> bool:
    policy_file = skill_dir / "agents" / "openai.yaml"
    if not policy_file.exists():
        return True
    data = yaml.safe_load(policy_file.read_text()) or {}
    return (data.get("policy") or {}).get("allow_implicit_invocation", True) is not False


def check_skill(skill_file: Path, scratch: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = skill_file.parent
    try:
        meta, body = split_frontmatter(skill_file.read_text())
    except ValueError as exc:
        return [str(exc)]

    for key in sorted(set(meta) - SPEC_KEYS - EXTENSION_KEYS):
        errors.append(f"unsupported frontmatter key: {key}")
    for key in sorted(set(meta) & EXTENSION_KEYS):
        if not isinstance(meta[key], bool):
            errors.append(f"{key} must be a boolean")

    if meta.get("disable-model-invocation") is True and codex_allows_implicit(skill_dir):
        errors.append(
            "disable-model-invocation: true requires agents/openai.yaml "
            "policy.allow_implicit_invocation: false"
        )

    portable = {k: v for k, v in meta.items() if k not in EXTENSION_KEYS}
    target = scratch / skill_dir.name
    target.mkdir(parents=True)
    (target / "SKILL.md").write_text(
        "---\n" + yaml.safe_dump(portable, sort_keys=False, allow_unicode=True, width=10**6) + "---\n" + body
    )
    result = subprocess.run(["skills-ref", "validate", str(target)], capture_output=True, text=True)
    if result.returncode != 0:
        errors.append((result.stdout + result.stderr).strip() or "skills-ref validate failed")
    shutil.rmtree(target)
    return errors


def main() -> int:
    if shutil.which("skills-ref") is None:
        print("skills-ref is not installed; see the pinned install in the CI workflow", file=sys.stderr)
        return 2
    skill_files = sorted(
        p
        for p in ROOT.rglob("SKILL.md")
        if ".git" not in p.parts and "node_modules" not in p.parts
    )
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for skill_file in skill_files:
            for error in check_skill(skill_file, Path(tmp)):
                failed += 1
                print(f"{skill_file.relative_to(ROOT)}: {error}")
    print(f"{len(skill_files)} skills checked, {failed} problems")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
