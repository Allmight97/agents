#!/usr/bin/env python3
"""List removed names that something in the repository still references.

Removed names are definitions on deleted diff lines (base to working tree) that
no added line defines again; explicit names add removals a diff cannot show,
such as config keys or flags. A name still defined anywhere counts as moved.
Prints each leftover reference and exits 1; prints nothing and exits 0 when
every removed name is gone; exits 2 when no removed definition was found;
exits 3 when git cannot answer.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NoReturn

from complexity_rank import default_branch, repo_root, run

MODIFIERS = r"(?:(?:export|default|declare|abstract|async|unsafe|pub(?:\([^)]*\))?|extern(?:\s+\"[^\"]*\")?)\s+)*"
NAME = r"([A-Za-z_$][\w$]*)"
DEFINITION = re.compile(
    rf"^\s*{MODIFIERS}(?:const\s+)?(?:unsafe\s+)?"
    rf"(?:def|class|function\*?|fn|struct|enum|trait|interface|type|func(?:\s*\([^)]*\))?|mod)\s+{NAME}"
)
TOP_LEVEL_BINDING = re.compile(rf"^{MODIFIERS}(?:const|let|var|static)\s+(?:mut\s+)?{NAME}")
PROSE_SUFFIXES = {".md", ".mdx", ".markdown", ".rst", ".txt", ".adoc"}


def fail(message: str) -> NoReturn:
    print(message, file=sys.stderr)
    sys.exit(3)


def defined_name(path: str, line: str) -> str | None:
    if Path(path).suffix in PROSE_SUFFIXES:
        return None
    match = DEFINITION.match(line) or TOP_LEVEL_BINDING.match(line)
    return match.group(1) if match else None


def removed_from_diff(root: Path, base: str) -> set[str]:
    diff = run(["git", "diff", "-U0", "--no-prefix", base], root)
    if diff.returncode != 0:
        fail(f"git diff {base} failed: {diff.stderr.strip()}")
    removed: set[str] = set()
    added: set[str] = set()
    path = ""
    in_header = False
    for line in diff.stdout.splitlines():
        if line.startswith(("diff --git ", "@@")):
            in_header = line.startswith("diff")
        elif in_header:
            if line.startswith(("--- ", "+++ ")) and line[4:] != "/dev/null":
                path = line[4:]
        elif line.startswith("-") and (name := defined_name(path, line[1:])):
            removed.add(name)
        elif line.startswith("+") and (name := defined_name(path, line[1:])):
            added.add(name)
    return removed - added


def references(root: Path, name: str) -> list[str] | None:
    """Hits for name, or None when a hit still defines it."""
    grep = run(["git", "grep", "-n", "-I", "-w", "--untracked", "-F", "-e", name], root)
    hits = grep.stdout.splitlines()
    for hit in hits:
        path, _, text = hit.split(":", 2)
        if defined_name(path, text) == name:
            return None
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("names", nargs="*", help="removed names a diff cannot show (config keys, flags, strings)")
    parser.add_argument("--base", help="diff base (default: merge-base with the default branch)")
    args = parser.parse_args()

    root = repo_root(Path.cwd())
    if root is None:
        fail("leftover_refs needs a git repository")
    base = args.base or run(["git", "merge-base", "HEAD", default_branch(root)], root).stdout.strip() or "HEAD"
    names = set(args.names) | removed_from_diff(root, base)
    if not names:
        print(f"no removed definitions found since {base}; pass removed names explicitly")
        return 2

    leftover = False
    for name in sorted(names):
        hits = references(root, name)
        if hits:
            leftover = True
            print(f"{name}:")
            print("\n".join(f"  {hit}" for hit in hits))
    return 1 if leftover else 0


if __name__ == "__main__":
    sys.exit(main())
