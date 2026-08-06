#!/usr/bin/env python3
"""Validate repository-owned plugin routing and native/portable parity."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
XCODEBUILDMCP_ARGS = ["-y", "xcodebuildmcp@2.7.0", "mcp"]
XCODE_DEVELOPER_DIR = "/Applications/Xcode-beta.app/Contents/Developer"
XCODEBUILDMCP_WORKFLOWS = {
    "coverage",
    "debugging",
    "device",
    "macos",
    "project-discovery",
    "project-scaffolding",
    "simulator",
    "simulator-management",
    "swift-package",
    "ui-automation",
    "utilities",
    "xcode-ide",
}


class ValidationError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"{path}: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: expected a JSON object")
    return value


def package_path(base: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.startswith("./"):
        raise ValidationError(f"{label}: expected a path beginning with './'")
    path = (base / value[2:]).resolve()
    try:
        path.relative_to(base.resolve())
    except ValueError as error:
        raise ValidationError(f"{label}: path escapes its package") from error
    return path


def validate_build_apple_apps(
    plugin_dir: Path,
    native_manifest: dict[str, Any],
) -> None:
    legacy_files = list((plugin_dir / "commands").glob("*.md"))
    legacy_metadata = plugin_dir / "agents" / "openai.yaml"
    if legacy_metadata.is_file():
        legacy_files.append(legacy_metadata)
    if legacy_files:
        names = ", ".join(
            str(path.relative_to(plugin_dir)) for path in sorted(legacy_files)
        )
        raise ValidationError(
            f"build-apple-apps: Xcode 27 misclassifies legacy plugin files: {names}"
        )

    portable_manifest = load_json(plugin_dir / "plugin.json")
    if portable_manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValidationError("build-apple-apps: wrong portable plugin schema")
    for field in ("name", "version", "description"):
        if portable_manifest.get(field) != native_manifest.get(field):
            raise ValidationError(
                f"build-apple-apps: native and portable {field} have drifted"
            )

    native_mcp_path = package_path(
        plugin_dir,
        native_manifest.get("mcpServers"),
        "build-apple-apps native MCP",
    )
    native_servers = load_json(native_mcp_path).get("mcpServers")
    portable_mcp = load_json(plugin_dir / "mcp.json")
    if portable_mcp.get("$schema") != MCP_SCHEMA:
        raise ValidationError("build-apple-apps: wrong portable MCP schema")
    portable_servers = portable_mcp.get("mcpServers")
    if not isinstance(native_servers, dict) or not isinstance(portable_servers, dict):
        raise ValidationError("build-apple-apps: both MCP files need mcpServers objects")
    if set(native_servers) != set(portable_servers):
        raise ValidationError("build-apple-apps: native and portable server names differ")

    for name, native_server in native_servers.items():
        portable_server = portable_servers[name]
        if not isinstance(native_server, dict) or not isinstance(portable_server, dict):
            raise ValidationError(f"build-apple-apps: MCP server {name!r} must be an object")
        portable_native_shape = dict(portable_server)
        if portable_native_shape.pop("type", None) != "stdio":
            raise ValidationError(f"build-apple-apps: portable server {name!r} is not stdio")
        if portable_native_shape != native_server:
            raise ValidationError(f"build-apple-apps: MCP server {name!r} has drifted")

    server = native_servers.get("xcodebuildmcp")
    if not isinstance(server, dict) or server.get("command") != "npx":
        raise ValidationError("build-apple-apps: xcodebuildmcp must run through npx")
    if server.get("args") != XCODEBUILDMCP_ARGS:
        raise ValidationError("build-apple-apps: xcodebuildmcp must remain pinned to 2.7.0")
    environment = server.get("env")
    if not isinstance(environment, dict):
        raise ValidationError("build-apple-apps: xcodebuildmcp env is missing")
    if environment.get("DEVELOPER_DIR") != XCODE_DEVELOPER_DIR:
        raise ValidationError("build-apple-apps: DEVELOPER_DIR has drifted")
    if environment.get("XCODEBUILDMCP_SENTRY_DISABLED") != "true":
        raise ValidationError("build-apple-apps: Sentry telemetry must remain disabled by default")
    raw_workflows = environment.get("XCODEBUILDMCP_ENABLED_WORKFLOWS")
    if not isinstance(raw_workflows, str):
        raise ValidationError("build-apple-apps: workflow allowlist is missing")
    workflows = raw_workflows.split(",")
    if len(workflows) != len(set(workflows)) or set(workflows) != XCODEBUILDMCP_WORKFLOWS:
        raise ValidationError("build-apple-apps: workflow allowlist has drifted")


def validate() -> None:
    entries = load_json(MARKETPLACE).get("plugins")
    if not isinstance(entries, list):
        raise ValidationError("marketplace plugins must be an array")
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValidationError("marketplace plugin entry must be an object")
        name = entry.get("name")
        if not isinstance(name, str) or not name or name in seen:
            raise ValidationError(f"invalid or duplicate marketplace plugin name: {name!r}")
        seen.add(name)
        source = entry.get("source")
        if not isinstance(source, dict) or source.get("source") != "local":
            continue
        plugin_dir = package_path(ROOT, source.get("path"), f"marketplace {name}")
        native_manifest = load_json(plugin_dir / ".codex-plugin" / "plugin.json")
        if native_manifest.get("name") != name:
            raise ValidationError(f"marketplace {name}: native manifest name differs")
        if name == "build-apple-apps":
            validate_build_apple_apps(plugin_dir, native_manifest)


def main() -> int:
    try:
        validate()
    except ValidationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print("marketplace routing and plugin parity are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
