"""Console entry points for the kernel's structural controls."""

from __future__ import annotations

import argparse
from pathlib import Path

from .dependencies import analyse_repository
from .promotion import run_promotion_set
from .validation import validate_architecture


def _repository_root(value: str | None) -> Path:
    return Path(value or ".").resolve()


def validate_main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root")
    args = parser.parse_args()
    for line in validate_architecture(_repository_root(args.repository_root)):
        print(line)
    print("PASS: structural architecture validation")
    return 0


def dependencies_main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root")
    args = parser.parse_args()
    violations = analyse_repository(_repository_root(args.repository_root))
    for violation in violations:
        location = f" {violation.source_file}:{violation.line}" if violation.source_file else ""
        print(f"{violation.code}:{location} {violation.message}")
    if violations:
        return 1
    print("PASS: dependency direction and cycle validation")
    return 0


def public_seams_main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root")
    args = parser.parse_args()
    violations = [
        item
        for item in analyse_repository(_repository_root(args.repository_root))
        if item.code == "PRIVATE_SEAM"
    ]
    for violation in violations:
        print(f"{violation.source_file}:{violation.line}: {violation.message}")
    if violations:
        return 1
    print("PASS: public-seam validation")
    return 0


def promotion_main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root")
    parser.add_argument("--set", default="architecture_kernel")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    return run_promotion_set(
        _repository_root(args.repository_root),
        args.set,
        check_only=args.check_only,
    )
