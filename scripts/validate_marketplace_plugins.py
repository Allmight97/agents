#!/usr/bin/env python3
"""Validate repository-owned plugin routing and native/portable parity."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
GROK_MARKETPLACE = ROOT / ".grok-plugin" / "marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CURSOR_MARKETPLACE = ROOT / ".cursor-plugin" / "marketplace.json"
GROK_LOCAL_PLUGIN_PATHS = {
    "personal-skills": "./plugins/personal-skills",
    "build-apple-apps": "./plugins/build-apple-apps",
    "m365-tenant-ops": "./plugins/m365-tenant-ops",
    "native-browser-bridge": "./plugins/native-browser-bridge",
}
MANIFEST_DIRS = (".claude-plugin", ".codex-plugin", ".cursor-plugin", ".grok-plugin")
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
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label}: expected a relative path")
    path = (base / value).resolve()
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


def validate_portable_manifest(
    plugin_dir: Path,
    native_manifest: dict[str, Any],
) -> None:
    portable_path = plugin_dir / "plugin.json"
    if not portable_path.is_file():
        return
    portable_manifest = load_json(portable_path)
    if portable_manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValidationError(f"{plugin_dir.name}: wrong portable plugin schema")
    for field in ("name", "version", "description"):
        if portable_manifest.get(field) != native_manifest.get(field):
            raise ValidationError(
                f"{plugin_dir.name}: native and portable {field} have drifted"
            )


def grok_local_path(source: Any, label: str) -> str:
    if isinstance(source, str):
        path = source
    elif isinstance(source, dict) and source.get("type") == "local":
        path = source.get("path")
    else:
        raise ValidationError(f"{label}: expected a local source with a ./ path")
    if not isinstance(path, str) or not path.startswith("./"):
        raise ValidationError(f"{label}: expected a path beginning with './'")
    return path


def validate_grok_marketplace() -> None:
    marketplace = load_json(GROK_MARKETPLACE)
    if marketplace.get("name") != "personal":
        raise ValidationError(".grok-plugin/marketplace.json name must be 'personal'")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        raise ValidationError("Grok marketplace plugins must be an array")

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValidationError("Grok marketplace plugin entry must be an object")
        name = entry.get("name")
        if not isinstance(name, str) or not name or name in seen:
            raise ValidationError(f"invalid or duplicate Grok plugin name: {name!r}")
        seen.add(name)
        if name not in GROK_LOCAL_PLUGIN_PATHS:
            raise ValidationError(f"Grok marketplace has unexpected plugin: {name}")
        path = grok_local_path(entry.get("source"), f"Grok marketplace {name}")
        expected = GROK_LOCAL_PLUGIN_PATHS[name]
        if path != expected:
            raise ValidationError(
                f"Grok marketplace {name}: expected path {expected}, found {path}"
            )
        plugin_dir = package_path(ROOT, path, f"Grok marketplace {name}")
        if not (plugin_dir / "skills").is_dir():
            raise ValidationError(f"Grok marketplace {name}: missing skills/")
        grok_manifest = plugin_dir / ".grok-plugin" / "plugin.json"
        if grok_manifest.is_file() and load_json(grok_manifest).get("name") != name:
            raise ValidationError(f"Grok marketplace {name}: .grok-plugin/plugin.json name differs")

    missing = set(GROK_LOCAL_PLUGIN_PATHS) - seen
    if missing:
        raise ValidationError(
            "Grok marketplace is missing plugins: " + ", ".join(sorted(missing))
        )


def catalog_names(path: Path) -> set[str]:
    return {
        entry.get("name")
        for entry in load_json(path).get("plugins", [])
        if isinstance(entry, dict)
    }


def validate_claude_only_plugins() -> None:
    """Claude-only mods list in the Claude catalog and nowhere else.

    A mod's hooks/hooks.json names function-hook "modules", which Codex, Cursor,
    and Grok auto-discover and cannot parse, so no other catalog or manifest may
    carry the plugin. A hooks.json with command "hooks" is portable and may list
    elsewhere.
    """
    other_catalogs = {
        "Codex": catalog_names(MARKETPLACE),
        "Cursor": catalog_names(CURSOR_MARKETPLACE),
        "Grok": catalog_names(GROK_MARKETPLACE),
    }
    for entry in load_json(CLAUDE_MARKETPLACE).get("plugins", []):
        name = entry.get("name")
        if name == "personal-skills":
            continue
        plugin_dir = package_path(ROOT, entry.get("source"), f"Claude marketplace {name}")
        manifest = load_json(plugin_dir / ".claude-plugin" / "plugin.json")
        if manifest.get("name") != name:
            raise ValidationError(f"Claude marketplace {name}: manifest name differs")
        hooks_file = plugin_dir / "hooks" / "hooks.json"
        if not hooks_file.is_file() or "modules" not in load_json(hooks_file):
            continue
        for client, names in other_catalogs.items():
            if name in names:
                raise ValidationError(
                    f"{name}: a Claude-only mod cannot appear in the {client} catalog"
                )
        for foreign in (".codex-plugin", ".cursor-plugin", ".grok-plugin", "plugin.json"):
            if (plugin_dir / foreign).exists():
                raise ValidationError(f"{name}: a Claude-only mod cannot carry {foreign}")


def catalog_plugin_roots() -> dict[Path, str]:
    """Every plugin root a catalog names by relative path, with its catalog and name."""
    roots: dict[Path, str] = {}
    for label, path in (
        ("Codex", MARKETPLACE),
        ("Claude", CLAUDE_MARKETPLACE),
        ("Cursor", CURSOR_MARKETPLACE),
        ("Grok", GROK_MARKETPLACE),
    ):
        for entry in load_json(path).get("plugins", []):
            if not isinstance(entry, dict):
                continue
            source = entry.get("source")
            if isinstance(source, dict):
                is_local = "local" in (source.get("source"), source.get("type"))
                source = source.get("path") if is_local else None
            if not isinstance(source, str):
                continue
            name = entry.get("name")
            plugin_dir = package_path(ROOT, source, f"{label} marketplace {name}")
            if not plugin_dir.is_dir():
                raise ValidationError(f"{label} marketplace {name}: {source} is not a directory")
            roots.setdefault(plugin_dir, f"{label} marketplace {name}")
    return roots


def validate_plugin_roots_are_flat() -> None:
    """The repo root is a marketplace, not a plugin, and no plugin root contains another manifest.

    claude.ai's marketplace sync rejects a plugin whose tree holds a nested
    .claude-plugin/plugin.json; the other harnesses would read a nested manifest
    as part of the outer plugin.
    """
    for manifest_dir in MANIFEST_DIRS:
        if (ROOT / manifest_dir / "plugin.json").exists():
            raise ValidationError(
                f"{manifest_dir}/plugin.json at the repo root makes the marketplace a plugin"
            )
    roots = catalog_plugin_roots()
    for plugin_dir, label in roots.items():
        for nested in plugin_dir.rglob("plugin.json"):
            if nested.parent.name in MANIFEST_DIRS and nested.parent.parent != plugin_dir:
                raise ValidationError(
                    f"{label}: nested plugin manifest {nested.relative_to(ROOT)}"
                )
        for other in roots:
            if other != plugin_dir and other.is_relative_to(plugin_dir):
                raise ValidationError(
                    f"{label}: contains another plugin root {other.relative_to(ROOT)}"
                )


def validate() -> None:
    validate_plugin_roots_are_flat()
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
        validate_portable_manifest(plugin_dir, native_manifest)
        if name == "build-apple-apps":
            validate_build_apple_apps(plugin_dir, native_manifest)

    validate_grok_marketplace()
    validate_claude_only_plugins()


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
