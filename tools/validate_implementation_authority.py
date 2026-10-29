#!/usr/bin/env python3
"""Validate an exact implementation-ready brief against a bounded ingress binding."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from nvda_desk.architecture.implementation_authority import (
    ImplementationAuthorityError,
    render_candidate_target,
    validate_implementation_authority,
)


def _repo_root() -> Path:
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    return Path(out.strip()).resolve()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--brief", required=True)
    args = parser.parse_args()
    root = _repo_root()
    try:
        binding = validate_implementation_authority(
            root,
            Path(args.binding).resolve(),
            Path(args.brief).resolve(),
        )
    except (ImplementationAuthorityError, OSError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}")
        return 2
    print(f"PASS: implementation authority brief_sha256={binding.brief_sha256}")
    rendered_targets = ", ".join(render_candidate_target(item) for item in binding.targets)
    print(f"candidate_targets: {rendered_targets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
