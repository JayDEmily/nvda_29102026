#!/usr/bin/env python3
"""Stdlib-only source hygiene checks for the AI patch bridge."""

from __future__ import annotations

import sys
from pathlib import Path

CHECK_ROOTS = ("src", "scripts", "tests")
TEXT_SUFFIXES = {".py", ".md", ".toml", ".diff"}
MAX_LINE_LENGTH = 120


def iter_text_files(repo_root: Path):
    for root_name in CHECK_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix in TEXT_SUFFIXES:
                yield path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    failures: list[str] = []
    for path in iter_text_files(repo_root):
        rel = path.relative_to(repo_root)
        text = path.read_text(encoding="utf-8")
        if not text.endswith("\n"):
            failures.append(f"{rel}: missing final newline")
        for number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                failures.append(f"{rel}:{number}: trailing whitespace")
            if path.suffix == ".py" and len(line) > MAX_LINE_LENGTH:
                failures.append(f"{rel}:{number}: line longer than {MAX_LINE_LENGTH}")
    if failures:
        print("Bridge hygiene check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Bridge hygiene check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
