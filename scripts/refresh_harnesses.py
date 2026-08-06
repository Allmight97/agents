#!/usr/bin/env python3
"""Refresh supported harnesses and prove personal-skills installation freshness."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import release_metadata


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ID = "personal-skills@personal"


class HarnessError(RuntimeError):
    pass


def run(*command: str) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise HarnessError(f"{' '.join(command)} failed: {detail}")
    return completed.stdout


def published_release() -> tuple[str, str, str]:
    version = release_metadata.validate()
    tag = f"v{version}"
    commit = run("git", "rev-parse", f"{tag}^{{commit}}").strip()
    head = run("git", "rev-parse", "HEAD").strip()
    if head != commit:
        raise HarnessError(
            f"HEAD {head[:12]} is not published release {tag} ({commit[:12]}); "
            "run this from the tagged release commit"
        )
    codex_version = release_metadata.load_json(release_metadata.CODEX_MANIFEST)[
        "version"
    ]
    return version, commit, codex_version


def find_plugin(items: list[dict[str, Any]]) -> dict[str, Any]:
    matches = [
        item
        for item in items
        if PLUGIN_ID
        in {
            item.get("pluginId"),
            item.get("id"),
            f"{item.get('name')}@{item.get('marketplaceName')}",
            f"{item.get('name')}@{item.get('marketplace')}",
        }
    ]
    if len(matches) != 1:
        raise HarnessError(f"expected one installed {PLUGIN_ID}, found {len(matches)}")
    return matches[0]


def codex(expected_version: str, refresh: bool) -> str:
    if shutil.which("codex") is None:
        return "Codex: unavailable (codex executable not found)"
    if refresh:
        run("codex", "plugin", "marketplace", "upgrade", "personal", "--json")
        run("codex", "plugin", "add", PLUGIN_ID, "--json")
    payload = json.loads(
        run(
            "codex",
            "plugin",
            "list",
            "--marketplace",
            "personal",
            "--available",
            "--json",
        )
    )
    plugin = find_plugin(payload.get("installed", []))
    actual = plugin.get("version")
    if actual != expected_version or not plugin.get("enabled"):
        raise HarnessError(
            f"Codex: expected enabled {expected_version}, found version={actual!r} "
            f"enabled={plugin.get('enabled')!r}"
        )
    return f"Codex: current at {actual}"


def claude(expected_version: str, refresh: bool) -> str:
    if shutil.which("claude") is None:
        return "Claude Code: unavailable (claude executable not found)"
    if refresh:
        run("claude", "plugin", "marketplace", "update", "personal")
        run("claude", "plugin", "update", PLUGIN_ID)
    payload = json.loads(run("claude", "plugin", "list", "--json"))
    items = payload if isinstance(payload, list) else payload.get("installed", [])
    plugin = find_plugin(items)
    actual = plugin.get("version")
    if actual != expected_version:
        raise HarnessError(
            f"Claude Code: expected {expected_version}, found {actual!r}"
        )
    return f"Claude Code: current at {actual}"


def cursor(expected_version: str, expected_commit: str) -> str:
    cursor_root = Path.home() / ".cursor" / "plugins"
    marketplace = (
        cursor_root
        / "marketplaces"
        / "github.com"
        / "allmight97"
        / "agents"
        / expected_commit
    )
    installed = (
        cursor_root
        / "cache"
        / "personal"
        / "personal-skills"
        / expected_commit
    )
    manifest_path = installed / ".cursor-plugin" / "plugin.json"
    missing = [path for path in (marketplace, installed, manifest_path) if not path.exists()]
    if missing:
        raise HarnessError(
            "Cursor: stale or absent. In Cursor's Plugins settings, refresh the "
            "Personal marketplace and update personal-skills, then rerun this command. "
            f"Missing expected release artifact {expected_commit[:12]}."
        )
    actual = release_metadata.load_json(manifest_path).get("version")
    if actual != expected_version:
        raise HarnessError(
            f"Cursor: commit matches but expected manifest {expected_version}, found {actual!r}"
        )
    return f"Cursor: current at {actual} ({expected_commit[:12]})"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Refresh CLI-supported harnesses and verify installed personal-skills "
            "against the current tagged release."
        )
    )
    result.add_argument(
        "--check-only",
        action="store_true",
        help="verify without running supported harness update commands",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        version, commit, codex_version = published_release()
    except (OSError, json.JSONDecodeError, KeyError, HarnessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    checks = (
        lambda: codex(codex_version, not args.check_only),
        lambda: claude(version, not args.check_only),
        lambda: cursor(version, commit),
    )
    results: list[str] = []
    errors: list[str] = []
    for check in checks:
        try:
            results.append(check())
        except (OSError, json.JSONDecodeError, KeyError, HarnessError) as error:
            errors.append(str(error))

    print(f"published release v{version}")
    print("\n".join(results))
    if errors:
        print("\n".join(f"error: {error}" for error in errors), file=sys.stderr)
        return 1
    print("all installed harness artifacts verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
