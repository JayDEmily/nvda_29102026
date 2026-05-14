"""Run a named proof block from config/proof_blocks.yaml."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

PROOF_BLOCKS_PATH = Path("config/proof_blocks.yaml")


def _load_manifest() -> dict[str, Any]:
    if not PROOF_BLOCKS_PATH.exists():
        raise SystemExit(f"{PROOF_BLOCKS_PATH} not found")
    payload = yaml.safe_load(PROOF_BLOCKS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"{PROOF_BLOCKS_PATH} must decode to a mapping")
    return payload


def _iter_blocks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = manifest.get("proof_blocks") or []
    if not isinstance(blocks, list):
        raise SystemExit("proof_blocks must be a list")
    invalid = [index for index, block in enumerate(blocks) if not isinstance(block, dict)]
    if invalid:
        raise SystemExit(
            "proof_blocks contains non-mapping entries: " + ", ".join(map(str, invalid))
        )
    return blocks


def _find_block(block_id: str, manifest: dict[str, Any]) -> dict[str, Any]:
    blocks = _iter_blocks(manifest)
    for block in blocks:
        if block.get("proof_block_id") == block_id:
            return block
    available = ", ".join(str(block.get("proof_block_id")) for block in blocks)
    raise SystemExit(f"unknown proof block {block_id!r}; available: {available}")


def _list_blocks(
    manifest: dict[str, Any], *, as_json: bool = False, detailed: bool = False
) -> None:
    blocks = _iter_blocks(manifest)
    block_ids = [block.get("proof_block_id", "<missing proof_block_id>") for block in blocks]
    if as_json:
        payload: dict[str, Any] = {"proof_blocks": block_ids}
        if detailed:
            payload["proof_block_summaries"] = [_block_summary(block) for block in blocks]
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    for block_id in block_ids:
        print(block_id)


def _block_summary(block: dict[str, Any]) -> dict[str, Any]:
    return {
        "proof_block_id": block.get("proof_block_id"),
        "tier": block.get("tier"),
        "lifecycle": block.get("lifecycle"),
        "command": block.get("command"),
        "owns": list(block.get("owns") or []),
    }


def _resolve_command(command: str) -> list[str]:
    parts = shlex.split(command)
    if parts and parts[0] == "python":
        return [sys.executable, *parts[1:]]
    return parts


def _write_receipt(path: str | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    receipt_path = Path(path)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _validate_owned_paths(block: dict[str, Any]) -> None:
    owns = block.get("owns") or []
    if not isinstance(owns, list):
        raise SystemExit("proof block owns must be a list")
    missing = [str(path) for path in owns if not Path(str(path)).exists()]
    if missing:
        raise SystemExit("proof block owns missing paths: " + ", ".join(missing))


def _validate_block(block: dict[str, Any]) -> dict[str, Any]:
    proof_block_id = block.get("proof_block_id")
    if not isinstance(proof_block_id, str) or not proof_block_id.strip():
        raise SystemExit("proof block has missing proof_block_id")
    command = block.get("command")
    if not isinstance(command, str) or not command.strip():
        raise SystemExit(f"proof block {proof_block_id!r} has no command")
    _validate_owned_paths(block)
    return {
        "proof_block_id": proof_block_id,
        "command": command,
        "owns": list(block.get("owns") or []),
    }


def _validate_all_blocks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = _iter_blocks(manifest)
    summaries = [_validate_block(block) for block in blocks]
    seen: set[str] = set()
    duplicates: list[str] = []
    for summary in summaries:
        block_id = summary["proof_block_id"]
        if block_id in seen:
            duplicates.append(block_id)
        seen.add(block_id)
    if duplicates:
        raise SystemExit("duplicate proof_block_id values: " + ", ".join(duplicates))
    return summaries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--block", help="proof_block_id to run")
    parser.add_argument("--describe", help="proof_block_id to describe without running")
    parser.add_argument("--check", help="proof_block_id to validate without running")
    parser.add_argument(
        "--check-all",
        action="store_true",
        help="validate every manifest proof block without running commands",
    )
    parser.add_argument(
        "--receipt", help="optional JSON receipt path for describe/check/run/check-all"
    )
    parser.add_argument("--list", action="store_true", help="list available block ids")
    parser.add_argument("--json", action="store_true", help="emit --list output as JSON")
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="include proof-block summaries when used with --list --json",
    )
    args = parser.parse_args()

    manifest = _load_manifest()
    if args.list:
        _list_blocks(manifest, as_json=args.json, detailed=args.detailed)
        return 0
    if args.describe:
        block = _find_block(args.describe, manifest)
        summary = _block_summary(block)
        _write_receipt(args.receipt, {"mode": "describe", "status": "PASS", **summary})
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.check:
        block = _find_block(args.check, manifest)
        summary = _validate_block(block)
        _write_receipt(
            args.receipt,
            {
                "mode": "check",
                "proof_block_id": args.check,
                "status": "PASS",
                "exit_code": 0,
                **summary,
            },
        )
        print(f"proof_block_check=PASS {args.check}")
        return 0
    if args.check_all:
        summaries = _validate_all_blocks(manifest)
        proof_block_ids = [summary["proof_block_id"] for summary in summaries]
        _write_receipt(
            args.receipt,
            {
                "mode": "check_all",
                "status": "PASS",
                "exit_code": 0,
                "block_count": len(summaries),
                "proof_block_ids": proof_block_ids,
                "checked_blocks": summaries,
            },
        )
        print(f"proof_blocks_check_all=PASS count={len(summaries)}")
        return 0
    if not args.block:
        raise SystemExit("Usage: scripts/run_proof_block.py --block <proof_block_id>")

    block = _find_block(args.block, manifest)
    summary = _validate_block(block)
    command = summary["command"]

    print(f"proof_block_id={args.block}")
    print(f"command={command}")
    resolved_command = _resolve_command(command)
    completed = subprocess.run(resolved_command, check=False)
    _write_receipt(
        args.receipt,
        {
            "mode": "run",
            "proof_block_id": args.block,
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "exit_code": completed.returncode,
            "command": command,
            "resolved_command": resolved_command,
            "owns": list(block.get("owns") or []),
        },
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
