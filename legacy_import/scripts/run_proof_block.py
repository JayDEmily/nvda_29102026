#!/usr/bin/env python3
"""Purpose: Execute governed proof blocks from the manifest without inventing scope.

Inputs:
- `--block` governed block id from `config/proof_blocks.yaml`.
- `--mode` proof mode (`blocking`, `shadow`, `cleanup`, or `report`).
- optional `--manifest` path override.
- optional `--dry-run` and `--json` output controls.

Outputs:
- resolved command plan for the selected block;
- subprocess execution of the declared proof path when not in dry-run mode;
- deterministic non-zero exit on unknown block ids or malformed manifest entries.

Side Effects:
- may launch `make alpha-proof` or `make shadow-test` when not in dry-run mode.
- does not mutate manifest authority or infer scope from git diff.

Failure Modes:
- unknown block id;
- missing required manifest fields;
- unsupported tier entries;
- subprocess failure from the delegated proof command.

Checkpoints:
- `proof_block_manifest_loaded`
- `proof_block_resolution_complete`
- `proof_block_subprocess_delegated`
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "config" / "proof_blocks.yaml"
MANIFEST_TIER_A_ALLOWLIST_ENVVAR = "NVDA_MANIFEST_TIER_A_TESTS_JSON"
REQUIRED_FIELDS = {
    "canonical_label",
    "owned_surfaces",
    "shared_contract_surfaces",
    "tier_a_blocking_tests",
    "tier_b_shadow_tests",
    "tier_c_cleanup_families",
    "promotion_rules_from_shadow_to_blocking",
    "broad_proof_promotion_conditions",
    "checkpoint_required",
    "docstring_required_for_modified_boundaries",
}


class ManifestError(RuntimeError):
    """Raised when the proof manifest is malformed or incomplete."""


@dataclass(frozen=True)
class ResolvedPlan:
    block_id: str
    canonical_label: str
    mode: str
    tier_a_blocking_tests: list[str]
    tier_b_shadow_tests: list[str]
    tier_c_cleanup_families: list[str]
    command: list[str] | None
    env_overrides: dict[str, str]

    def to_json(self) -> str:
        return json.dumps(
            {
                "block_id": self.block_id,
                "canonical_label": self.canonical_label,
                "mode": self.mode,
                "tier_a_blocking_tests": self.tier_a_blocking_tests,
                "tier_b_shadow_tests": self.tier_b_shadow_tests,
                "tier_c_cleanup_families": self.tier_c_cleanup_families,
                "command": self.command,
                "env_overrides": self.env_overrides,
            },
            indent=2,
            sort_keys=True,
        )


def load_manifest(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ManifestError("Manifest root must be a mapping.")
    blocks = payload.get("blocks")
    if not isinstance(blocks, dict) or not blocks:
        raise ManifestError("Manifest must contain a non-empty blocks mapping.")
    return payload


def validate_block(block_id: str, block: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS - set(block))
    if missing:
        raise ManifestError(f"Block {block_id!r} is missing required fields: {missing}")
    for key in (
        "owned_surfaces",
        "shared_contract_surfaces",
        "tier_a_blocking_tests",
        "tier_b_shadow_tests",
        "tier_c_cleanup_families",
        "promotion_rules_from_shadow_to_blocking",
        "broad_proof_promotion_conditions",
    ):
        if not isinstance(block.get(key), list):
            raise ManifestError(f"Block {block_id!r} field {key!r} must be a list.")


def resolve_plan(payload: dict[str, Any], block_id: str, mode: str) -> ResolvedPlan:
    blocks = payload["blocks"]
    if block_id not in blocks:
        raise ManifestError(f"Unknown block id: {block_id}")
    block = blocks[block_id]
    if not isinstance(block, dict):
        raise ManifestError(f"Block {block_id!r} must map to an object.")
    validate_block(block_id, block)
    label = str(block["canonical_label"])
    tier_a_tests = [str(item) for item in block["tier_a_blocking_tests"]]
    tier_b_tests = [str(item) for item in block["tier_b_shadow_tests"]]
    tier_c_families = [str(item) for item in block["tier_c_cleanup_families"]]

    if mode == "blocking":
        if not tier_a_tests:
            raise ManifestError(f"Block {block_id!r} has no Tier A blocking tests.")
        return ResolvedPlan(
            block_id=block_id,
            canonical_label=label,
            mode=mode,
            tier_a_blocking_tests=tier_a_tests,
            tier_b_shadow_tests=tier_b_tests,
            tier_c_cleanup_families=tier_c_families,
            command=[
                "make",
                "alpha-proof",
                f"PYTHON={sys.executable}",
                f"PYTEST_ARGS={' '.join(tier_a_tests)}",
            ],
            env_overrides={
                MANIFEST_TIER_A_ALLOWLIST_ENVVAR: json.dumps(tier_a_tests, separators=(",", ":"))
            },
        )
    if mode == "shadow":
        return ResolvedPlan(
            block_id=block_id,
            canonical_label=label,
            mode=mode,
            tier_a_blocking_tests=tier_a_tests,
            tier_b_shadow_tests=tier_b_tests,
            tier_c_cleanup_families=tier_c_families,
            command=["make", "shadow-test"] if "repo_wide_pytest" in tier_b_tests else None,
            env_overrides={},
        )
    if mode in {"cleanup", "report"}:
        return ResolvedPlan(
            block_id=block_id,
            canonical_label=label,
            mode=mode,
            tier_a_blocking_tests=tier_a_tests,
            tier_b_shadow_tests=tier_b_tests,
            tier_c_cleanup_families=tier_c_families,
            command=None,
            env_overrides={},
        )
    raise ManifestError(f"Unsupported mode: {mode}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a governed proof block without inventing scope."
    )
    parser.add_argument("--block", required=True)
    parser.add_argument(
        "--mode", default="blocking", choices=("blocking", "shadow", "cleanup", "report")
    )
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        manifest = load_manifest(Path(args.manifest))
        plan = resolve_plan(manifest, args.block, args.mode)
    except ManifestError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.as_json or args.dry_run or plan.command is None:
        print(plan.to_json() if args.as_json else plan)
        if args.dry_run or plan.command is None:
            return 0
    env = os.environ.copy()
    env.update(plan.env_overrides)
    completed = subprocess.run(plan.command, cwd=REPO_ROOT, env=env, check=False)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
