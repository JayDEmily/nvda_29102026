#!/usr/bin/env python3
"""Stdlib-only text normaliser for bridge-owned text files."""

from __future__ import annotations

from pathlib import Path

CHECK_ROOTS = ("src", "scripts", "tests")
TEXT_SUFFIXES = {".py", ".md", ".toml", ".diff"}


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
    changed = 0
    for path in iter_text_files(repo_root):
        text = path.read_text(encoding="utf-8")
        normalised = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
        if normalised != text:
            path.write_text(normalised, encoding="utf-8")
            changed += 1
    print(f"Normalised {changed} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
