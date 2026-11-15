"""PROPOSAL ONLY: exact Ruff baseline verifier for immutable admitted proof bytes.

Not wired into CI. Use only after independent review and owner acceptance.
"""
from __future__ import annotations

import collections
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config/lint/PROPOSED_SHA_BOUND_RUFF_BASELINE.json"
EXPECTED_MANIFEST_SHA256 = "d38367ce1f63a1731c0cd9b69e12af021a291d71b0206f83ba17f3b69dbfc97c"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict:
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise ValueError(f"expected JSON object: {path}")
    return result


def canonical_diagnostics(root: Path, results: list[dict]) -> list[dict]:
    normalized = []
    for result in results:
        original = Path(result["filename"]).resolve()
        if not original.is_relative_to(root):
            raise ValueError(f"Ruff returned a path outside repository: {original}")
        position = result["location"]
        normalized.append(
            {
                "path": original.relative_to(root).as_posix(),
                "code": result["code"],
                "message": result["message"],
                "row": position["row"],
                "column": position["column"],
            }
        )
    return sorted(
        normalized,
        key=lambda x: (x["path"], x["row"], x["column"], x["code"], x["message"]),
    )


def diagnostics_hash(diagnostics: list[dict]) -> str:
    payload = (json.dumps(diagnostics, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return sha256_bytes(payload)


def verify_admission(root: Path, entry: dict) -> None:
    path = entry["path"]
    if not path.startswith("tests/product/") or not path.endswith(".py"):
        raise ValueError(f"not a product proof path: {path}")
    source = root / path
    if source.is_symlink() or not source.resolve().is_relative_to(root):
        raise ValueError(f"admitted source is a symlink or escapes repository: {path}")
    source_sha = sha256_bytes(source.read_bytes())
    if source_sha != entry["sha256"]:
        raise ValueError(f"admitted source bytes changed: {path}")

    admission = root / entry["admission_path"]
    pointer = read_json(admission)["current_generation"]
    if pointer is None or pointer["path"] != entry["generation_path"]:
        raise ValueError(f"selected generation changed for {path}")
    generation = root / pointer["path"]
    if generation.is_symlink() or not generation.resolve().is_relative_to(root):
        raise ValueError(f"generation is a symlink or escapes repository: {path}")
    generation_sha = sha256_bytes(generation.read_bytes())
    if pointer["sha256"] != generation_sha or generation_sha != entry["generation_sha256"]:
        raise ValueError(f"generation bytes or pointer changed for {path}")

    record = read_json(generation)
    if record["claim_id"] != entry["claim_id"]:
        raise ValueError(f"claim identity changed: {path}")
    category = entry["admission_kind"]
    if category not in ("family_files", "support_files"):
        raise ValueError("invalid admission row category")
    matches = [x for x in record[category] if x["path"] == path]
    if len(matches) != 1 or matches[0]["sha256"] != source_sha:
        raise ValueError(f"current generation does not admit exact bytes: {path}")


def verify(root: Path, manifest: dict, ruff: Path) -> tuple[int, str]:
    if manifest.get("schema_version") != "1.0":
        raise ValueError("unsupported proposal schema")
    if manifest.get("status") != "PROPOSED_NOT_ACCEPTED":
        raise ValueError("proposal status changed without independent authority")
    declared = manifest.get("files")
    if not isinstance(declared, list) or len(declared) != 7:
        raise ValueError("expected exactly seven documented immutable paths")
    paths = [x["path"] for x in declared]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate manifest paths")
    if paths != sorted(paths):
        raise ValueError("manifest paths not canonically sorted")

    version = subprocess.run([str(ruff), "--version"], cwd=root, text=True, capture_output=True)
    if version.returncode or version.stdout.strip() != manifest["ruff_version"]:
        raise ValueError("Ruff executable/version differs from reviewed candidate")
    for entry in declared:
        verify_admission(root, entry)

    run = subprocess.run(
        [str(ruff), "check", "--output-format=json", "src", "tests", "tools"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if run.returncode not in (0, 1):
        raise ValueError(f"Ruff crashed or command invalid: {run.stderr}")
    diagnostics = canonical_diagnostics(root, json.loads(run.stdout))
    counts = collections.Counter(item["path"] for item in diagnostics)
    expected_counts = {x["path"]: x["diagnostic_count"] for x in declared}
    if dict(counts) != expected_counts:
        raise ValueError(f"Ruff findings changed by path: observed={counts}")
    if len(diagnostics) != manifest["diagnostic_count"]:
        raise ValueError("Ruff finding total changed")
    digest = diagnostics_hash(diagnostics)
    if digest != manifest["diagnostic_set_sha256"]:
        raise ValueError("Ruff finding identities, locations or messages changed")
    if run.returncode != 1:
        raise ValueError("expected existing historical findings from original admitted bytes")
    return len(diagnostics), digest


def main() -> int:
    ruff = ROOT / ".venv/bin/ruff"
    if not ruff.is_file():
        binary = shutil.which("ruff")
        if binary is None:
            print("BLOCKED: exact Ruff tool unavailable", file=sys.stderr)
            return 2
        ruff = Path(binary)
    try:
        if sha256_bytes(MANIFEST.read_bytes()) != EXPECTED_MANIFEST_SHA256:
            raise ValueError("baseline manifest byte identity changed")
        count, digest = verify(ROOT, read_json(MANIFEST), ruff)
    except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"PROPOSED_BASELINE_REJECTED: {exc}", file=sys.stderr)
        return 1
    print(f"PROPOSED_BASELINE_EXACT_MATCH: {count} immutable historical diagnostics; {digest}")
    print("NOT AN ACCEPTED LINT POLICY OR CI/PROMOTION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
