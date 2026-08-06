#!/usr/bin/env python3
"""Refresh supported harnesses and prove personal-skills installation freshness."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import release_metadata


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ID = "personal-skills@personal"
CURSOR_LOG_TIMESTAMP = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})")
CURSOR_SKILL_COUNT = re.compile(r'"skillCount":(\d+)')


class HarnessError(RuntimeError):
    pass


def run(*command: str) -> str:
    return run_in(ROOT, *command)


def run_in(cwd: Path, *command: str) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
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


def remote_main_commit() -> str:
    output = run("git", "ls-remote", "origin", "refs/heads/main").strip()
    if not output:
        raise HarnessError("Cursor: origin/main could not be resolved")
    return output.split(maxsplit=1)[0]


def cursor_loader_proof(local: Path) -> int:
    """Prove Cursor loaded the local plugin after its source last changed."""
    logs = Path.home() / "Library" / "Application Support" / "Cursor" / "logs"
    if not logs.exists():
        raise HarnessError("Cursor: loader logs are unavailable; open Cursor and reload")

    anchor = max(
        (local / ".git" / "HEAD").stat().st_mtime,
        (local / ".cursor-plugin" / "plugin.json").stat().st_mtime,
    )
    loaded_at: datetime | None = None
    skill_proofs: list[tuple[datetime, int]] = []
    for path in logs.rglob("*.log"):
        if path.stat().st_mtime < anchor:
            continue
        try:
            lines = path.read_text(errors="replace").splitlines()
        except OSError:
            continue
        for line in lines:
            match = CURSOR_LOG_TIMESTAMP.match(line)
            if match is None:
                continue
            observed = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S.%f")
            if observed.timestamp() < anchor:
                continue
            if "loadUserLocalPlugin personal-skills loaded" in line:
                loaded_at = min(loaded_at, observed) if loaded_at else observed
            if "CursorPluginsAgentSkillsService load completed" in line:
                count = CURSOR_SKILL_COUNT.search(line)
                if count:
                    skill_proofs.append((observed, int(count.group(1))))

    local_skill_count = sum(
        1
        for path in (local / "skills").iterdir()
        if (path / "SKILL.md").is_file()
    )
    loaded_skills = max(
        (count for observed, count in skill_proofs if loaded_at and observed >= loaded_at),
        default=0,
    )
    if loaded_at is None or loaded_skills < local_skill_count:
        raise HarnessError(
            "Cursor: source is current but the loader has not proven this revision. "
            "Run Developer: Reload Window, then rerun this command"
        )
    return loaded_skills


def cursor_local(
    expected_version: str, expected_commit: str, local: Path, refresh: bool
) -> str:
    if local.is_symlink() or not (local / ".git").exists():
        raise HarnessError(
            f"Cursor: {local} must be a real Git clone inside Cursor's local-plugin "
            "directory; Cursor rejects symlinks whose targets are outside it"
        )

    dirty = run_in(local, "git", "status", "--porcelain").strip()
    if dirty:
        raise HarnessError(
            "Cursor: local plugin clone has uncommitted changes; preserve or discard "
            "them explicitly before synchronization"
        )

    if refresh:
        run_in(local, "git", "fetch", "origin", "main")
        run_in(local, "git", "switch", "--detach", expected_commit)

    manifest_path = local / ".cursor-plugin" / "plugin.json"
    actual_version = release_metadata.load_json(manifest_path).get("version")
    if actual_version != expected_version:
        raise HarnessError(
            f"Cursor: local manifest expected {expected_version}, found {actual_version!r}"
        )

    local_commit = run_in(local, "git", "rev-parse", "HEAD").strip()
    remote_commit = remote_main_commit()
    if local_commit != expected_commit or remote_commit != expected_commit:
        raise HarnessError(
            "Cursor: local source is not the exact published release: "
            f"local={local_commit[:12]} origin/main={remote_commit[:12]} "
            f"release={expected_commit[:12]}"
        )

    loaded_skills = cursor_loader_proof(local)

    return (
        f"Cursor: local clone current at {actual_version} "
        f"({expected_commit[:12]}); loader verified {loaded_skills} skills"
    )


def cursor(expected_version: str, expected_commit: str, refresh: bool) -> str:
    cursor_root = Path.home() / ".cursor" / "plugins"
    local = cursor_root / "local" / "personal-skills"
    if local.exists() or local.is_symlink():
        return cursor_local(expected_version, expected_commit, local, refresh)

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
            "Cursor: no trusted local plugin and the marketplace artifact is stale or "
            "absent. Clone the agents repository into "
            "~/.cursor/plugins/local/personal-skills, then rerun this command. "
            "Missing expected marketplace artifact "
            f"{expected_commit[:12]}."
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
        lambda: cursor(version, commit, not args.check_only),
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
