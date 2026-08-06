#!/usr/bin/env python3
"""Synchronize and validate personal-skills release metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CURSOR_MANIFEST = ROOT / ".cursor-plugin" / "plugin.json"
CURSOR_MARKETPLACE = ROOT / ".cursor-plugin" / "marketplace.json"
CODEX_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
CURSOR_MARKETPLACE_ENTRY_KEYS = {
    "name",
    "source",
    "description",
    "minClientVersions",
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
            ".codex-plugin/plugin.json version must include +codex.<cachebuster>"
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
        ".claude-plugin/plugin.json": load_json(CLAUDE_MANIFEST).get("version"),
        ".cursor-plugin/plugin.json": load_json(CURSOR_MANIFEST).get("version"),
        ".codex-plugin/plugin.json": base_codex_version(
            str(load_json(CODEX_MANIFEST).get("version", ""))
        ),
    }
    mismatches = [
        f"{path}: expected {expected}, found {actual}"
        for path, actual in versions.items()
        if actual != expected
    ]

    for path in (CLAUDE_MARKETPLACE, CURSOR_MARKETPLACE):
        entry = personal_skills_entry(path)
        if "version" in entry:
            mismatches.append(
                f"{path.relative_to(ROOT)}: personal-skills must not duplicate manifest version"
            )

    cursor_entry = personal_skills_entry(CURSOR_MARKETPLACE)
    if "source" not in cursor_entry:
        mismatches.append(
            ".cursor-plugin/marketplace.json: personal-skills source is required"
        )
    unsupported_cursor_keys = set(cursor_entry) - CURSOR_MARKETPLACE_ENTRY_KEYS
    if unsupported_cursor_keys:
        mismatches.append(
            ".cursor-plugin/marketplace.json: unsupported personal-skills keys "
            + ", ".join(sorted(unsupported_cursor_keys))
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

    for path in (CLAUDE_MANIFEST, CURSOR_MANIFEST):
        manifest = load_json(path)
        manifest["version"] = version
        write_json(path, manifest)

    codex_manifest = load_json(CODEX_MANIFEST)
    codex_manifest["version"] = f"{version}+codex.{token}"
    write_json(CODEX_MANIFEST, codex_manifest)

    for path in (CLAUDE_MARKETPLACE, CURSOR_MARKETPLACE):
        marketplace = load_json(path)
        entry = next(
            item
            for item in marketplace["plugins"]
            if item.get("name") == "personal-skills"
        )
        entry.pop("version", None)
        write_json(path, marketplace)

    return validate()


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Synchronize or validate personal-skills release metadata."
    )
    subcommands = result.add_subparsers(dest="command", required=True)
    subcommands.add_parser("check", help="fail when release metadata has drifted")
    set_parser = subcommands.add_parser(
        "set", help="set every manifest from the latest CHANGELOG release"
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
