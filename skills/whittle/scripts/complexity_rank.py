#!/usr/bin/env python3
"""Rank files by where complexity and recent change meet.

Score = (functions over the per-function threshold) x (recent commits). Biome
counts TS/JS functions over the cognitive threshold; lizard counts functions in
other languages over the cyclomatic (CCN) threshold. Without either count the
score falls back to scc Complexity x recent commits and the file is flagged
`scc-only`. Density (Complexity per 100 code lines) is context.
Exit 3 when scc is missing; 0 otherwise.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

BIOME_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts"}
BIOME_RULE = "complexity/noExcessiveCognitiveComplexity"
COMPLEXITY_MESSAGE = re.compile(r"Excessive complexity of (\d+)")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def score(over_threshold_fns: int | None, scc_complexity: int, churn: int | None) -> int | None:
    """The one place the metric lives. Swap this to change the ranking."""
    if churn is None:
        return None
    base = over_threshold_fns if over_threshold_fns is not None else scc_complexity
    return base * churn


def repo_root(cwd: Path) -> Path | None:
    result = run(["git", "rev-parse", "--show-toplevel"], cwd)
    return Path(result.stdout.strip()) if result.returncode == 0 else None


def default_branch(root: Path) -> str:
    head = run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"], root)
    if head.returncode == 0:
        return head.stdout.strip()
    for name in ("main", "master"):
        if run(["git", "rev-parse", "--verify", "--quiet", name], root).returncode == 0:
            return name
    return "HEAD"


def changed_files(root: Path) -> list[str]:
    base = run(["git", "merge-base", "HEAD", default_branch(root)], root).stdout.strip() or "HEAD"
    diff = run(["git", "diff", "--name-only", "--diff-filter=d", base], root).stdout
    return [line for line in diff.splitlines() if line and (root / line).is_file()]


def churn_of(root: Path, rel: str, days: int, min_age_days: int) -> tuple[int, str | None]:
    times = run(["git", "log", "--follow", "--format=%ct", "--", rel], root).stdout.split()
    if not times:
        return 0, "untracked"
    if time.time() - int(times[-1]) < min_age_days * 86400:
        return 0, "young"
    count = run(["git", "log", f"--since={days} days ago", "--format=%h", "--", rel], root).stdout.split()
    return len(count), None


def find_biome(root: Path) -> list[str] | None:
    local = root / "node_modules" / ".bin" / "biome"
    if local.exists():
        return [str(local)]
    for launcher in (["bunx", "biome"], ["npx", "--no-install", "biome"]):
        if shutil.which(launcher[0]) and run(launcher + ["--version"], root).returncode == 0:
            return launcher
    return None


def biome_complexities(biome: list[str], root: Path, files: list[str], only: bool) -> dict[str, list[int]]:
    cmd = biome + ["lint", "--reporter=json", "--max-diagnostics=none"]
    if only:
        cmd.append(f"--only={BIOME_RULE}")
    result = run(cmd + files, root)
    start = result.stdout.find("{")
    found: dict[str, list[int]] = {}
    if start == -1:
        return found
    for diag in json.loads(result.stdout[start:]).get("diagnostics", []):
        match = COMPLEXITY_MESSAGE.search(diag.get("message", ""))
        if diag.get("category", "").endswith(BIOME_RULE) and match:
            found.setdefault(diag["location"]["path"], []).append(int(match.group(1)))
    return found


# The newest lizard at least 10 days old; 1.24.1 is let in early because it
# counts Rust match arms. Delete the package exception after 2026-10-16.
UVX_LIZARD = ["uvx", "--exclude-newer", "10 days", "--exclude-newer-package", "lizard=2026-10-06", "lizard"]


def find_lizard() -> list[str] | None:
    if shutil.which("uvx"):
        return UVX_LIZARD
    return ["lizard"] if shutil.which("lizard") else None


def lizard_counts(root: Path, files: list[str], ccn: int) -> dict[str, dict]:
    lizard = find_lizard()
    if lizard is None or not files:
        return {}
    result = run(lizard + ["--csv", *files], root)
    if result.returncode != 0:
        return {}
    # CSV columns: nloc, ccn, token, param, length, location, file, function, ...
    functions: dict[str, list[int]] = {}
    for row in csv.reader(io.StringIO(result.stdout)):
        if len(row) > 6 and row[1].isdigit():
            functions.setdefault(row[6], []).append(int(row[1]))
    return {
        f: {"over": sum(1 for c in found if c > ccn), "exempt": False, "source": "lizard"}
        for f, found in functions.items()
    }


def biome_counts(root: Path, candidates: list[str], threshold: int) -> dict[str, dict]:
    if not candidates or not (root / "biome.json").exists():
        return {}
    biome = find_biome(root)
    if biome is None:
        return {}
    # --only ignores config overrides, so exempt files still get a count; a file
    # the normal run does not flag is exempt by an override.
    forced = biome_complexities(biome, root, candidates, only=True)
    enforced = biome_complexities(biome, root, candidates, only=False)
    return {
        f: {
            "over": sum(1 for c in forced.get(f, []) if c > threshold),
            "exempt": bool(forced.get(f)) and not enforced.get(f),
            "source": "biome",
        }
        for f in candidates
    }


def linter_counts(root: Path, files: list[str], args: argparse.Namespace) -> dict[str, dict]:
    biome_files = [f for f in files if Path(f).suffix in BIOME_EXTENSIONS]
    other_files = [f for f in files if Path(f).suffix not in BIOME_EXTENSIONS]
    counts: dict[str, dict] = {}
    if args.linters in ("auto", "lizard"):
        counts.update(lizard_counts(root, other_files, args.ccn))
    if args.linters in ("auto", "biome"):
        counts.update(biome_counts(root, biome_files, args.threshold))
    return counts


def scc_by_file(root: Path, files: list[str]) -> dict[str, dict]:
    result = run(["scc", "--format", "json", "--by-file", "--cognitive", *files], root)
    if result.returncode != 0:
        sys.exit(f"scc failed: {result.stderr.strip()}")
    rows = {}
    for language in json.loads(result.stdout):
        for entry in language["Files"]:
            rows[entry["Location"]] = entry
    return rows


def build_rows(root: Path, files: list[str], args: argparse.Namespace, in_git: bool) -> list[dict]:
    scc = scc_by_file(root, files)
    linter = linter_counts(root, files, args)
    rows = []
    for rel in files:
        entry = scc.get(rel)
        if entry is None:
            continue
        flags = []
        churn = None
        if in_git:
            churn, churn_flag = churn_of(root, rel, args.churn_days, args.min_age_days)
            if churn_flag:
                flags.append(churn_flag)
        else:
            flags.append("no-git")
        count = linter.get(rel)
        over = count["over"] if count else None
        if count and count["exempt"]:
            flags.append("exempt")
        if over is None:
            flags.append("scc-only")
        code = entry["Code"]
        rows.append(
            {
                "file": rel,
                "language": entry["Language"],
                "code": code,
                "complexity": entry["Complexity"],
                "cognitive": entry["Cognitive"],
                "density": round(entry["Complexity"] * 100 / code, 1) if code else 0.0,
                "churn": churn,
                "over_threshold_fns": over,
                "per_function_source": count["source"] if count else None,
                "score": score(over, entry["Complexity"], churn),
                "flags": flags,
            }
        )
    rows.sort(key=lambda r: (r["score"] is None, -(r["score"] or 0), r["file"]))
    return rows


def render_table(rows: list[dict]) -> str:
    header = ["score", "over_fns", "source", "churn", "complexity", "density", "code", "flags", "file"]
    lines = ["  ".join(header)]
    for r in rows:
        cells = [
            "-" if r["score"] is None else r["score"],
            "-" if r["over_threshold_fns"] is None else r["over_threshold_fns"],
            r["per_function_source"] or "-",
            "-" if r["churn"] is None else r["churn"],
            r["complexity"],
            r["density"],
            r["code"],
            ",".join(r["flags"]) or "-",
            r["file"],
        ]
        lines.append("  ".join(str(c) for c in cells))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="*", help="files to rank")
    parser.add_argument("--changed", action="store_true", help="files changed since the merge-base with the default branch, plus working-tree edits")
    parser.add_argument("--threshold", type=int, default=20, help="Biome cognitive complexity per TS/JS function (default 20; values below the repo's Biome max undercount)")
    parser.add_argument("--ccn", type=int, default=10, help="lizard cyclomatic complexity per function in other languages (default 10)")
    parser.add_argument("--churn-days", type=int, default=90)
    parser.add_argument("--min-age-days", type=int, default=30, help="files younger than this get churn 0")
    parser.add_argument("--linters", choices=["auto", "biome", "lizard", "none"], default="auto", help="per-function source: auto = Biome for TS/JS, lizard for the rest, when available")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if shutil.which("scc") is None:
        if args.json:
            print(json.dumps({"error": "scc not installed"}))
        else:
            print("scc not installed; skipping complexity ranking")
        return 3

    cwd = Path.cwd()
    root = repo_root(cwd)
    in_git = root is not None
    root = root or cwd
    files = [str(Path(p).resolve().relative_to(root)) for p in args.paths]
    if args.changed:
        if not in_git:
            sys.exit("--changed needs a git repository")
        files += changed_files(root)
    files = sorted(set(files))
    rows = build_rows(root, files, args, in_git) if files else []
    print(json.dumps(rows, indent=2) if args.json else render_table(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
