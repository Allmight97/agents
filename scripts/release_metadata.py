#!/usr/bin/env python3
"""Synchronize and validate personal-skills release metadata."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
PERSONAL_SKILLS = ROOT / "plugins" / "personal-skills"
PERSONAL_SKILLS_SOURCE_PATH = "./plugins/personal-skills"
CLAUDE_MANIFEST = PERSONAL_SKILLS / ".claude-plugin" / "plugin.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CURSOR_MANIFEST = PERSONAL_SKILLS / ".cursor-plugin" / "plugin.json"
CURSOR_MARKETPLACE = ROOT / ".cursor-plugin" / "marketplace.json"
CODEX_MANIFEST = PERSONAL_SKILLS / ".codex-plugin" / "plugin.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
GROK_MANIFEST = PERSONAL_SKILLS / ".grok-plugin" / "plugin.json"
GROK_MARKETPLACE = ROOT / ".grok-plugin" / "marketplace.json"
WHITTLE_RANKER = PERSONAL_SKILLS / "skills" / "whittle" / "scripts" / "complexity_rank.py"
COMPLEXITY_LENS_RANKER = ROOT / "plugins" / "complexity-lens" / "scripts" / "complexity_rank.py"
CURSOR_MARKETPLACE_ENTRY_KEYS = {
    "name",
    "source",
    "description",
    "minClientVersions",
}
PERSONAL_SKILLS_SOURCES = {
    CLAUDE_MARKETPLACE: PERSONAL_SKILLS_SOURCE_PATH,
    CURSOR_MARKETPLACE: PERSONAL_SKILLS_SOURCE_PATH[2:],
    CODEX_MARKETPLACE: {"source": "local", "path": PERSONAL_SKILLS_SOURCE_PATH},
    GROK_MARKETPLACE: {"type": "local", "path": PERSONAL_SKILLS_SOURCE_PATH},
}

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
CHANGELOG_RELEASE_RE = re.compile(
    r"^## \[(?P<version>[^]]+)] - \d{4}-\d{2}-\d{2}$", re.MULTILINE
)


class ReleaseMetadataError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def latest_changelog_version() -> str:
    match = CHANGELOG_RELEASE_RE.search(CHANGELOG.read_text(encoding="utf-8"))
    if match is None:
        raise ReleaseMetadataError("CHANGELOG.md has no dated release section")
    return match.group("version")


def personal_skills_entry(path: Path) -> dict[str, Any]:
    marketplace = load_json(path)
    entries = [
        entry
        for entry in marketplace.get("plugins", [])
        if entry.get("name") == "personal-skills"
    ]
    if len(entries) != 1:
        raise ReleaseMetadataError(
            f"{path.relative_to(ROOT)} must contain exactly one personal-skills entry"
        )
    return entries[0]


def base_codex_version(version: str) -> str:
    marker = "+codex."
    if marker not in version:
        raise ReleaseMetadataError(
            f"{CODEX_MANIFEST.relative_to(ROOT)} version must include +codex.<cachebuster>"
        )
    base, cachebuster = version.split(marker, 1)
    if not cachebuster:
        raise ReleaseMetadataError("Codex cachebuster cannot be empty")
    return base


def validate() -> str:
    expected = latest_changelog_version()
    if SEMVER_RE.fullmatch(expected) is None:
        raise ReleaseMetadataError(
            f"latest changelog version {expected!r} is not supported semantic versioning"
        )

    versions = {
        CLAUDE_MANIFEST: load_json(CLAUDE_MANIFEST).get("version"),
        CURSOR_MANIFEST: load_json(CURSOR_MANIFEST).get("version"),
        GROK_MANIFEST: load_json(GROK_MANIFEST).get("version"),
        CODEX_MANIFEST: base_codex_version(
            str(load_json(CODEX_MANIFEST).get("version", ""))
        ),
    }
    mismatches = [
        f"{path.relative_to(ROOT)}: expected {expected}, found {actual}"
        for path, actual in versions.items()
        if actual != expected
    ]

    for path, source in PERSONAL_SKILLS_SOURCES.items():
        entry = personal_skills_entry(path)
        if "version" in entry:
            mismatches.append(
                f"{path.relative_to(ROOT)}: personal-skills must not duplicate manifest version"
            )
        if entry.get("source") != source:
            mismatches.append(
                f"{path.relative_to(ROOT)}: personal-skills source must be "
                f"{json.dumps(source)}"
            )

    unsupported_cursor_keys = (
        set(personal_skills_entry(CURSOR_MARKETPLACE)) - CURSOR_MARKETPLACE_ENTRY_KEYS
    )
    if unsupported_cursor_keys:
        mismatches.append(
            ".cursor-plugin/marketplace.json: unsupported personal-skills keys "
            + ", ".join(sorted(unsupported_cursor_keys))
        )

    if COMPLEXITY_LENS_RANKER.read_bytes() != WHITTLE_RANKER.read_bytes():
        mismatches.append(
            f"{COMPLEXITY_LENS_RANKER.relative_to(ROOT)} differs from "
            f"{WHITTLE_RANKER.relative_to(ROOT)}; run release_metadata.py set"
        )

    if mismatches:
        raise ReleaseMetadataError("release metadata drift:\n- " + "\n- ".join(mismatches))

    return expected


def synchronize(version: str, cachebuster: str | None) -> str:
    if SEMVER_RE.fullmatch(version) is None:
        raise ReleaseMetadataError(f"unsupported semantic version: {version!r}")

    changelog_version = latest_changelog_version()
    if changelog_version != version:
        raise ReleaseMetadataError(
            "update CHANGELOG.md first: "
            f"latest release is {changelog_version}, requested {version}"
        )

    token = cachebuster or datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    if not re.fullmatch(r"[0-9A-Za-z.-]+", token):
        raise ReleaseMetadataError(
            "Codex cachebuster may contain only letters, numbers, dots, and hyphens"
        )

    for path in (CLAUDE_MANIFEST, CURSOR_MANIFEST, GROK_MANIFEST):
        manifest = load_json(path)
        manifest["version"] = version
        write_json(path, manifest)

    codex_manifest = load_json(CODEX_MANIFEST)
    codex_manifest["version"] = f"{version}+codex.{token}"
    write_json(CODEX_MANIFEST, codex_manifest)

    for path, source in PERSONAL_SKILLS_SOURCES.items():
        marketplace = load_json(path)
        entry = next(
            item
            for item in marketplace["plugins"]
            if item.get("name") == "personal-skills"
        )
        entry.pop("version", None)
        entry["source"] = source
        write_json(path, marketplace)

    shutil.copyfile(WHITTLE_RANKER, COMPLEXITY_LENS_RANKER)

    return validate()


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Synchronize or validate personal-skills release metadata."
    )
    subcommands = result.add_subparsers(dest="command", required=True)
    subcommands.add_parser("check", help="fail when release metadata has drifted")
    set_parser = subcommands.add_parser(
        "set", help="set every manifest from the latest CHANGELOG release and copy the shared ranker"
    )
    set_parser.add_argument("version", help="release version, for example 0.10.0")
    set_parser.add_argument(
        "--codex-cachebuster",
        help="override the default UTC timestamp used for Codex cache invalidation",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "set":
            version = synchronize(args.version, args.codex_cachebuster)
            print(f"synchronized personal-skills {version}")
        else:
            version = validate()
            print(f"release metadata aligned at {version}")
    except (OSError, json.JSONDecodeError, KeyError, StopIteration, ReleaseMetadataError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
