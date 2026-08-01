"""Validate and reconcile retained-test and proof-block authority.

This module implements the M14 admission-control boundary.  It does not decide
module semantics; it verifies that executable proof membership is derived from
one explicit retained-test admission model.
"""

from __future__ import annotations

import argparse
import json
import shlex
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml


REGISTRY_PATH = Path("config/retained_test_registry.yaml")
MANIFEST_PATH = Path("config/proof_blocks.yaml")
ALLOWED_TIERS = frozenset({"Tier A", "Tier B", "Tier C"})
ACTIVE_CLAIM_LIFECYCLES = frozenset({"current_blocking", "current_nonblocking", "next_gate_expected_red"})
ALLOWED_LIFECYCLES = frozenset(
    {
        "current_blocking",
        "current_nonblocking",
        "next_gate_expected_red",
        "superseded_compatibility",
        "historical",
    }
)


class AuthorityError(ValueError):
    """Raised when test admission or proof selection authority is inconsistent."""


@dataclass(frozen=True)
class TestFamily:
    test_family_id: str
    tier: str
    lifecycle: str
    normative_proposition_ids: tuple[str, ...]


@dataclass(frozen=True)
class PathAdmission:
    test_path: str
    test_family_id: str
    tier: str
    lifecycle: str


@dataclass(frozen=True)
class ProofBlock:
    proof_block_id: str
    tier: str
    test_family_ids: tuple[str, ...]
    normative_proposition_ids: tuple[str, ...]
    command: str
    test_paths: tuple[str, ...]


@dataclass(frozen=True)
class PromotionSet:
    promotion_set_id: str
    proof_block_ids: tuple[str, ...]
    test_family_ids: tuple[str, ...]
    test_paths: tuple[str, ...]


@dataclass(frozen=True)
class AuthorityModel:
    families: Mapping[str, TestFamily]
    path_admissions: Mapping[str, PathAdmission]
    proof_blocks: Mapping[str, ProofBlock]
    promotion_sets: Mapping[str, PromotionSet]

    def to_dict(self) -> dict[str, Any]:
        return {
            "families": {key: asdict(value) for key, value in self.families.items()},
            "path_admissions": {
                key: asdict(value) for key, value in self.path_admissions.items()
            },
            "proof_blocks": {
                key: asdict(value) for key, value in self.proof_blocks.items()
            },
            "promotion_sets": {
                key: asdict(value) for key, value in self.promotion_sets.items()
            },
        }


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AuthorityError(f"{label} must be a mapping")
    return value


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise AuthorityError(f"{label} must be a list")
    return value


def _require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AuthorityError(f"{label} must be a non-empty string")
    return value.strip()


def _string_tuple(value: Any, label: str, *, nonempty: bool = False) -> tuple[str, ...]:
    items = _require_list(value, label)
    result = tuple(_require_nonempty_string(item, f"{label} item") for item in items)
    if nonempty and not result:
        raise AuthorityError(f"{label} must contain at least one value")
    if len(result) != len(set(result)):
        raise AuthorityError(f"{label} contains duplicate values")
    return result


def _physical_test_paths(repo_root: Path) -> set[str]:
    result: set[str] = set()
    for tier in ("tier_a", "tier_b", "tier_c"):
        root = repo_root / "tests" / tier
        if not root.exists():
            continue
        result.update(path.relative_to(repo_root).as_posix() for path in root.rglob("test_*.py"))
    return result


def _tier_for_path(test_path: str) -> str:
    if test_path.startswith("tests/tier_a/"):
        return "Tier A"
    if test_path.startswith("tests/tier_b/"):
        return "Tier B"
    if test_path.startswith("tests/tier_c/"):
        return "Tier C"
    raise AuthorityError(f"test_path is outside governed tier roots: {test_path}")


def _resolve_command_test_paths(command: str, repo_root: Path) -> tuple[str, ...]:
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        raise AuthorityError(f"invalid proof command quoting: {exc}") from exc

    resolved: set[str] = set()
    for token in parts:
        if not token.startswith("tests/"):
            continue
        candidate = repo_root / token
        if candidate.is_file():
            if candidate.name.startswith("test_") and candidate.suffix == ".py":
                resolved.add(candidate.relative_to(repo_root).as_posix())
            continue
        if candidate.is_dir():
            resolved.update(
                path.relative_to(repo_root).as_posix()
                for path in candidate.rglob("test_*.py")
            )
            continue
        raise AuthorityError(f"proof command references missing test path: {token}")
    return tuple(sorted(resolved))


def _validate_registry(
    registry: Mapping[str, Any], repo_root: Path
) -> tuple[dict[str, TestFamily], dict[str, PathAdmission], dict[str, tuple[str, ...]]]:
    if registry.get("schema_version") != "v4":
        raise AuthorityError("retained-test registry schema_version must be v4")
    model = _require_mapping(
        registry.get("canonical_admission_model"), "canonical_admission_model"
    )

    declared_tiers = frozenset(
        _string_tuple(model.get("allowed_tiers"), "allowed_tiers", nonempty=True)
    )
    if declared_tiers != ALLOWED_TIERS:
        raise AuthorityError("allowed_tiers does not match the governed tier domain")
    declared_lifecycles = frozenset(
        _string_tuple(
            model.get("allowed_lifecycles"), "allowed_lifecycles", nonempty=True
        )
    )
    if declared_lifecycles != ALLOWED_LIFECYCLES:
        raise AuthorityError(
            "allowed_lifecycles does not match the governed lifecycle domain"
        )

    families: dict[str, TestFamily] = {}
    for index, raw in enumerate(
        _require_list(model.get("test_families"), "test_families")
    ):
        item = _require_mapping(raw, f"test_families[{index}]")
        family_id = _require_nonempty_string(
            item.get("test_family_id"), f"test_families[{index}].test_family_id"
        )
        if family_id in families:
            raise AuthorityError(f"duplicate test_family_id: {family_id}")
        tier = _require_nonempty_string(item.get("tier"), f"family {family_id} tier")
        if tier not in ALLOWED_TIERS:
            raise AuthorityError(f"invalid tier for family {family_id}: {tier}")
        lifecycle = _require_nonempty_string(
            item.get("lifecycle"), f"family {family_id} lifecycle"
        )
        if lifecycle not in ALLOWED_LIFECYCLES:
            raise AuthorityError(
                f"invalid lifecycle for family {family_id}: {lifecycle}"
            )
        proposition_ids = _string_tuple(
            item.get("normative_proposition_ids", []),
            f"family {family_id} normative_proposition_ids",
        )
        if lifecycle == "current_blocking" and not proposition_ids:
            raise AuthorityError(
                f"current blocking family {family_id} requires normative_proposition_ids"
            )
        families[family_id] = TestFamily(
            test_family_id=family_id,
            tier=tier,
            lifecycle=lifecycle,
            normative_proposition_ids=proposition_ids,
        )

    path_admissions: dict[str, PathAdmission] = {}
    family_paths: dict[str, list[str]] = {family_id: [] for family_id in families}
    for index, raw in enumerate(
        _require_list(model.get("path_admissions"), "path_admissions")
    ):
        item = _require_mapping(raw, f"path_admissions[{index}]")
        test_path = _require_nonempty_string(
            item.get("test_path"), f"path_admissions[{index}].test_path"
        )
        if test_path in path_admissions:
            raise AuthorityError(f"duplicate test_path admission: {test_path}")
        family_id = _require_nonempty_string(
            item.get("test_family_id"),
            f"path_admissions[{index}].test_family_id",
        )
        family = families.get(family_id)
        if family is None:
            raise AuthorityError(
                f"path admission {test_path} references unknown test_family_id {family_id}"
            )
        physical_tier = _tier_for_path(test_path)
        if physical_tier != family.tier:
            raise AuthorityError(
                f"tier mismatch for {test_path}: path={physical_tier}, family={family.tier}"
            )
        if not (repo_root / test_path).is_file():
            raise AuthorityError(f"admitted test_path does not exist: {test_path}")
        path_admissions[test_path] = PathAdmission(
            test_path=test_path,
            test_family_id=family_id,
            tier=family.tier,
            lifecycle=family.lifecycle,
        )
        family_paths[family_id].append(test_path)

    for index, raw in enumerate(
        _require_list(model.get("exclusive_claim_groups", []), "exclusive_claim_groups")
    ):
        group = _require_mapping(raw, f"exclusive_claim_groups[{index}]")
        group_id = _require_nonempty_string(
            group.get("conflict_group_id"),
            f"exclusive_claim_groups[{index}].conflict_group_id",
        )
        family_ids = _string_tuple(
            group.get("family_ids"),
            f"exclusive_claim_groups[{index}].family_ids",
            nonempty=True,
        )
        unknown = sorted(family_id for family_id in family_ids if family_id not in families)
        if unknown:
            raise AuthorityError(
                f"exclusive claim group {group_id} references unknown test_family_id values: "
                + ", ".join(unknown)
            )
        active = [
            family_id
            for family_id in family_ids
            if families[family_id].lifecycle in ACTIVE_CLAIM_LIFECYCLES
        ]
        if len(active) > 1:
            raise AuthorityError(
                f"exclusive claim group {group_id} has conflicting active families: "
                + ", ".join(active)
            )

    unused_families = sorted(
        family_id for family_id, paths in family_paths.items() if not paths
    )
    if unused_families:
        raise AuthorityError(
            "test families without path admissions: " + ", ".join(unused_families)
        )

    physical = _physical_test_paths(repo_root)
    admitted = set(path_admissions)
    missing = sorted(physical - admitted)
    stale = sorted(admitted - physical)
    if missing or stale:
        parts: list[str] = []
        if missing:
            parts.append("unadmitted physical tests: " + ", ".join(missing))
        if stale:
            parts.append("stale admitted tests: " + ", ".join(stale))
        raise AuthorityError("; ".join(parts))

    return families, path_admissions, {
        family_id: tuple(sorted(paths)) for family_id, paths in family_paths.items()
    }


def _validate_manifest(
    manifest: Mapping[str, Any],
    families: Mapping[str, TestFamily],
    family_paths: Mapping[str, tuple[str, ...]],
    repo_root: Path,
) -> tuple[dict[str, ProofBlock], dict[str, PromotionSet]]:
    if manifest.get("schema_version") != "v2":
        raise AuthorityError("proof manifest schema_version must be v2")

    raw_blocks = _require_list(manifest.get("proof_blocks"), "proof_blocks")
    raw_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw in enumerate(raw_blocks):
        item = _require_mapping(raw, f"proof_blocks[{index}]")
        block_id = _require_nonempty_string(
            item.get("proof_block_id"), f"proof_blocks[{index}].proof_block_id"
        )
        if block_id in raw_by_id:
            raise AuthorityError(f"duplicate proof_block_id: {block_id}")
        raw_by_id[block_id] = item

    raw_sets = _require_mapping(manifest.get("promotion_sets"), "promotion_sets")
    promotion_block_ids: set[str] = set()
    for set_id, raw in raw_sets.items():
        item = _require_mapping(raw, f"promotion_sets.{set_id}")
        promotion_block_ids.update(
            _string_tuple(
                item.get("proof_block_ids"),
                f"promotion_sets.{set_id}.proof_block_ids",
                nonempty=True,
            )
        )

    proof_blocks: dict[str, ProofBlock] = {}
    for block_id, item in raw_by_id.items():
        tier = _require_nonempty_string(item.get("tier"), f"block {block_id} tier")
        if tier not in ALLOWED_TIERS:
            raise AuthorityError(f"invalid tier for proof block {block_id}: {tier}")
        command = _require_nonempty_string(
            item.get("command"), f"block {block_id} command"
        )
        test_family_ids = _string_tuple(
            item.get("test_family_ids", []), f"block {block_id} test_family_ids"
        )
        proposition_ids = _string_tuple(
            item.get("normative_proposition_ids", []),
            f"block {block_id} normative_proposition_ids",
        )
        if block_id in promotion_block_ids:
            if not test_family_ids:
                raise AuthorityError(
                    f"promotion proof block {block_id} requires test_family_ids"
                )
            if not proposition_ids:
                raise AuthorityError(
                    f"promotion proof block {block_id} requires normative_proposition_ids"
                )

        expected_paths: set[str] = set()
        for family_id in test_family_ids:
            family = families.get(family_id)
            if family is None:
                raise AuthorityError(
                    f"proof block {block_id} references unknown test_family_id {family_id}"
                )
            if family.tier != tier:
                raise AuthorityError(
                    f"proof block {block_id} tier {tier} disagrees with family {family_id} tier {family.tier}"
                )
            expected_paths.update(family_paths[family_id])

        command_paths = set(_resolve_command_test_paths(command, repo_root))
        if test_family_ids and command_paths != expected_paths:
            raise AuthorityError(
                f"proof block {block_id} command test membership disagrees with registry: "
                f"command={sorted(command_paths)}, registry={sorted(expected_paths)}"
            )
        proof_blocks[block_id] = ProofBlock(
            proof_block_id=block_id,
            tier=tier,
            test_family_ids=test_family_ids,
            normative_proposition_ids=proposition_ids,
            command=command,
            test_paths=tuple(sorted(command_paths)),
        )

    promotion_sets: dict[str, PromotionSet] = {}
    for set_id, raw in raw_sets.items():
        item = _require_mapping(raw, f"promotion_sets.{set_id}")
        block_ids = _string_tuple(
            item.get("proof_block_ids"),
            f"promotion_sets.{set_id}.proof_block_ids",
            nonempty=True,
        )
        selected_families: list[str] = []
        selected_paths: list[str] = []
        for block_id in block_ids:
            block = proof_blocks.get(block_id)
            if block is None:
                raise AuthorityError(
                    f"promotion set {set_id} references unknown proof_block_id {block_id}"
                )
            selected_families.extend(block.test_family_ids)
            selected_paths.extend(block.test_paths)
        if len(selected_families) != len(set(selected_families)):
            raise AuthorityError(
                f"promotion set {set_id} selects a test family more than once"
            )
        if len(selected_paths) != len(set(selected_paths)):
            raise AuthorityError(f"promotion set {set_id} selects a test path more than once")
        selected_family_set = set(selected_families)
        nonblocking = sorted(
            family_id
            for family_id in selected_family_set
            if families[family_id].lifecycle != "current_blocking"
        )
        if nonblocking:
            raise AuthorityError(
                f"promotion set {set_id} includes non-current-blocking families: "
                + ", ".join(nonblocking)
            )
        promotion_sets[str(set_id)] = PromotionSet(
            promotion_set_id=str(set_id),
            proof_block_ids=block_ids,
            test_family_ids=tuple(selected_families),
            test_paths=tuple(selected_paths),
        )

    if "pre_m00_current" in promotion_sets:
        selected = set(promotion_sets["pre_m00_current"].test_family_ids)
        blocking = {
            family_id
            for family_id, family in families.items()
            if family.lifecycle == "current_blocking"
        }
        if selected != blocking:
            raise AuthorityError(
                "pre_m00_current does not resolve the exact current_blocking family set: "
                f"missing={sorted(blocking - selected)}, extra={sorted(selected - blocking)}"
            )

    return proof_blocks, promotion_sets


def validate_authority_documents(
    registry: Mapping[str, Any],
    manifest: Mapping[str, Any],
    *,
    repo_root: Path = Path("."),
) -> AuthorityModel:
    """Validate already-loaded authority documents against the repository tree."""

    resolved_root = repo_root.resolve()
    families, path_admissions, family_paths = _validate_registry(
        registry, resolved_root
    )
    proof_blocks, promotion_sets = _validate_manifest(
        manifest, families, family_paths, resolved_root
    )
    return AuthorityModel(
        families=families,
        path_admissions=path_admissions,
        proof_blocks=proof_blocks,
        promotion_sets=promotion_sets,
    )


def validate_active_control(repo_root: Path = Path(".")) -> str:
    """Require the canonical plan, live roadmap and process overlay to agree."""

    resolved_root = repo_root.resolve()
    canonical = (
        resolved_root / "project_control/canonical_project_manager/EXEC_PLAN.md"
    ).read_text(encoding="utf-8")
    roadmap = (resolved_root / "ROADMAP_LEDGER_V2.md").read_text(encoding="utf-8")
    process = (
        resolved_root / "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md"
    ).read_text(encoding="utf-8")
    expected_plan = "**Status:** `ACTIVE:PRE_M00_TESTING_GUARDRAIL_REPAIR`"
    expected_roadmap = (
        "| Current active slice | Pre-M00 testing guardrail repair — active; "
        "M00 not started |"
    )
    expected_process = (
        "The current active bounded pack is "
        "`PRE-M00-TESTING-GUARDRAIL-REPAIR-V1`"
    )
    missing = [
        label
        for label, text, expected in (
            ("canonical ExecPlan", canonical, expected_plan),
            ("live roadmap", roadmap, expected_roadmap),
            ("process overlay", process, expected_process),
        )
        if expected not in text
    ]
    if missing:
        raise AuthorityError(
            "active control state is not singular and reconciled: " + ", ".join(missing)
        )
    return "PRE-M00-TESTING-GUARDRAIL-REPAIR-V1"


def load_and_validate_authority(
    *,
    repo_root: Path = Path("."),
    registry_path: Path = REGISTRY_PATH,
    manifest_path: Path = MANIFEST_PATH,
) -> AuthorityModel:
    """Load and validate the repository authority documents."""

    resolved_root = repo_root.resolve()
    try:
        registry = yaml.safe_load(
            (resolved_root / registry_path).read_text(encoding="utf-8")
        )
        manifest = yaml.safe_load(
            (resolved_root / manifest_path).read_text(encoding="utf-8")
        )
    except (OSError, yaml.YAMLError) as exc:
        raise AuthorityError(f"authority document load failed: {exc}") from exc
    model = validate_authority_documents(registry, manifest, repo_root=resolved_root)
    validate_active_control(resolved_root)
    return model


def _summary(model: AuthorityModel) -> dict[str, Any]:
    lifecycle_counts: dict[str, int] = {}
    for family in model.families.values():
        lifecycle_counts[family.lifecycle] = lifecycle_counts.get(family.lifecycle, 0) + 1
    return {
        "status": "PASS",
        "family_count": len(model.families),
        "test_path_count": len(model.path_admissions),
        "proof_block_count": len(model.proof_blocks),
        "promotion_sets": {
            set_id: {
                "proof_block_count": len(value.proof_block_ids),
                "test_family_count": len(value.test_family_ids),
                "test_path_count": len(value.test_paths),
            }
            for set_id, value in model.promotion_sets.items()
        },
        "family_lifecycle_counts": dict(sorted(lifecycle_counts.items())),
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate authority")
    parser.add_argument("--json", action="store_true", help="emit JSON summary")
    parser.add_argument(
        "--describe-set", metavar="PROMOTION_SET", help="describe a resolved set"
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    if not args.check and not args.describe_set:
        parser.error("one of --check or --describe-set is required")
    try:
        model = load_and_validate_authority()
    except AuthorityError as exc:
        print(f"proof_authority=FAIL {exc}")
        return 2
    if args.describe_set:
        promotion = model.promotion_sets.get(args.describe_set)
        if promotion is None:
            print(f"proof_authority=FAIL unknown promotion set {args.describe_set}")
            return 2
        print(json.dumps(asdict(promotion), indent=2, sort_keys=True))
        return 0
    summary = _summary(model)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(
            "proof_authority=PASS "
            f"families={summary['family_count']} "
            f"tests={summary['test_path_count']} "
            f"blocks={summary['proof_block_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
