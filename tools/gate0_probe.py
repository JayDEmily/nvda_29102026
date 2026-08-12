from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
from contextlib import suppress
from pathlib import Path


def repo_root() -> Path:
    return Path(
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    ).resolve()


def git_dir(root: Path) -> Path:
    raw = subprocess.check_output(["git", "rev-parse", "--git-dir"], cwd=root, text=True).strip()
    p = Path(raw)
    return (p if p.is_absolute() else root / p).resolve()


def attempt_write(path: Path) -> dict[str, object]:
    allowed = False
    error: str | None = None
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.write(fd, b"nvda-gate0-probe\n")
        os.close(fd)
        allowed = True
    except OSError as exc:
        error = f"{type(exc).__name__}:{exc.errno}"
    finally:
        if allowed:
            with suppress(OSError):
                path.unlink()
    return {"path": str(path), "write_allowed": allowed, "error": error}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True)
    parser.add_argument("--nonce", required=True)
    parser.add_argument("--run-nonce", required=True)
    args = parser.parse_args()
    root = repo_root()
    token = args.nonce[:16]
    probes = {
        "repository": attempt_write(root / f".nvda_gate0_probe_{token}"),
        "git_metadata": attempt_write(git_dir(root) / f"nvda_gate0_probe_{token}"),
        "slash_tmp": attempt_write(Path("/tmp") / f"nvda_gate0_probe_{token}"),
        "home": attempt_write(Path.home() / f".nvda_gate0_probe_{token}"),
    }
    passed = (
        platform.system() == "Linux"
        and platform.machine() == "x86_64"
        and all(not item["write_allowed"] for item in probes.values())
    )
    result = {
        "gate0_probe": True,
        "role": args.role,
        "nonce": args.nonce,
        "run_nonce": args.run_nonce,
        "passed": passed,
        "platform": {"system": platform.system(), "machine": platform.machine()},
        "repo_root": str(root),
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "probes": probes,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
