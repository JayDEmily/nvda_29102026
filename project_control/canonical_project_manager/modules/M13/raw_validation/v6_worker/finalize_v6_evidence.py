"""Deterministically compress raw outputs and build the V6 evidence manifest."""

from __future__ import annotations

import gzip
import hashlib
from pathlib import Path

WORKER = Path(__file__).resolve().parent
MANIFEST = WORKER / "M13_V6_EVIDENCE_SHA256SUMS.txt"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    compressed = 0
    for directory_name in (
        "mutant_runs",
        "retained_mutant_runs",
        "validation_runs",
    ):
        directory = WORKER / directory_name
        for path in sorted(directory.rglob("*.txt")):
            if path.name.endswith(".command.txt"):
                continue
            target = path.with_suffix(path.suffix + ".gz")
            target.write_bytes(gzip.compress(path.read_bytes(), compresslevel=9, mtime=0))
            path.unlink()
            with gzip.open(target, "rb") as stream:
                stream.read()
            compressed += 1

    files = sorted(
        path
        for path in WORKER.rglob("*")
        if path.is_file()
        and path != MANIFEST
        and "__pycache__" not in path.parts
        and not path.name.endswith(".pyc")
    )
    MANIFEST.write_text(
        "\n".join(f"{_sha256(path)}  {path.relative_to(WORKER).as_posix()}" for path in files)
        + "\n",
        encoding="utf-8",
    )
    print(f"compressed_raw_outputs={compressed}")
    print(f"manifest_entries={len(files)}")
    print("gzip_integrity=PASS")
    print("evidence_manifest=PASS")


if __name__ == "__main__":
    main()
