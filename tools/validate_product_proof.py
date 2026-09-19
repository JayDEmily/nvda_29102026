#!/usr/bin/env python3
"""Validate the separate Raw Signal product-proof control surface."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from nvda_desk.architecture.registry import ArchitectureRegistry
from nvda_desk.architecture.schema import validate_document


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected mapping document")
    return value


def _case_dimension_valid(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    allowed = {"cases", "not_applicable_reason"}
    if set(value) - allowed:
        return False
    cases = value.get("cases", [])
    reason = value.get("not_applicable_reason")
    if not isinstance(cases, list) or any(not isinstance(item, str) or not item for item in cases):
        return False
    if reason is not None and (not isinstance(reason, str) or not reason):
        return False
    return bool(cases) ^ bool(reason)


def _allowed_authority_bindings(bicp: dict[str, Any]) -> dict[str, set[str]]:
    allowed: dict[str, set[str]] = {}
    route = bicp["route_receipt"]
    for item in route["complete_context"]:
        allowed[item["authority_id"]] = set(item["proposition_locators"])
    for item in bicp["authority_catalogue"]:
        authority_id = item["authority_id"]
        if item.get("authority_kind") == "IRB_PROPOSITION":
            allowed.setdefault(authority_id, set()).add(authority_id)
        locator = item.get("locator")
        if authority_id.startswith("IRB-BC") and isinstance(locator, str):
            allowed.setdefault(authority_id, set()).add(locator)
    return allowed


def validate_product_proof(repository_root: Path) -> list[str]:
    config_root = repository_root / "config" / "product_proof"
    schema_root = repository_root / "schemas"
    specs = (
        ("authority.yaml", "product_proof_authority.schema.json"),
        ("families.yaml", "product_proof_family.schema.json"),
        ("aggregates.yaml", "product_proof_aggregate.schema.json"),
    )
    for config_name, schema_name in specs:
        validate_document(config_root / config_name, schema_root / schema_name)

    authority = _load_yaml(config_root / "authority.yaml")
    families_doc = _load_yaml(config_root / "families.yaml")
    aggregates_doc = _load_yaml(config_root / "aggregates.yaml")

    bicp_path = repository_root / authority["bicp"]["path"]
    irb_path = repository_root / authority["irb"]["path"]
    if _sha256(bicp_path) != authority["bicp"]["sha256"]:
        raise ValueError("BICP hash mismatch")
    if _sha256(irb_path) != authority["irb"]["sha256"]:
        raise ValueError("IRB hash mismatch")
    bicp = json.loads(bicp_path.read_text(encoding="utf-8"))
    if bicp["packet_id"] != authority["bicp"]["packet_id"]:
        raise ValueError("BICP packet identity mismatch")

    product_obligations = [
        item for item in bicp["proof_obligations"] if "-PROD-" in item["proof_id"]
    ]
    architecture_obligations = {
        item["proof_id"] for item in bicp["proof_obligations"] if "-ARCH-" in item["proof_id"]
    }
    product_ids = [item["proof_id"] for item in product_obligations]
    required_ids = authority["required_product_proof_ids"]
    if product_ids != required_ids:
        raise ValueError(
            f"product obligation set/order mismatch; BICP={product_ids}, configured={required_ids}"
        )
    forbidden = set(authority["forbidden_predecessor_proof_ids"])
    if forbidden & set(required_ids):
        raise ValueError("forbidden predecessor product proof ID entered current authority")
    if any(item["tier_treatment"] != "NOT_CLASSIFIED" for item in product_obligations):
        raise ValueError("BICP product tier treatment is not NOT_CLASSIFIED")
    if authority["product_tier_treatment"] != "NOT_CLASSIFIED":
        raise ValueError("product proof tier classification drift")

    route_ids = [item["authority_id"] for item in bicp["route_receipt"]["complete_context"]]
    if route_ids != authority["routed_authority_ids"]:
        configured_route_ids = authority["routed_authority_ids"]
        raise ValueError(
            f"routed authority mismatch; BICP={route_ids}, "
            f"configured={configured_route_ids}"
        )

    registry = ArchitectureRegistry.from_repository(repository_root)
    target_id = authority["implementation_target"]["object_id"]
    target = next(
        (item for item in registry.objects if item.id == target_id),
        None,
    )
    if target is None or target.status != "active":
        raise ValueError("product-proof implementation target is not an active architecture object")
    if target.package != authority["implementation_target"]["package"]:
        raise ValueError("product-proof target package mismatch")
    if target.public_seam != authority["implementation_target"]["public_seam"]:
        raise ValueError("product-proof target public seam mismatch")

    families = families_doc["families"]
    family_ids = [item["id"] for item in families]
    family_paths = [item["path"] for item in families]
    if len(family_ids) != len(set(family_ids)):
        raise ValueError("duplicate product-proof family IDs")
    if len(family_paths) != len(set(family_paths)):
        raise ValueError("duplicate product-proof family paths")

    physical_root = repository_root / "tests" / "product"
    physical_paths = (
        {
            path.relative_to(repository_root).as_posix()
            for path in physical_root.rglob("test_*.py")
        }
        if physical_root.exists()
        else set()
    )
    admitted_paths = set(family_paths)
    if physical_paths != admitted_paths:
        unadmitted = sorted(physical_paths - admitted_paths)
        missing = sorted(admitted_paths - physical_paths)
        raise ValueError(
            f"product-test admission mismatch; unadmitted={unadmitted}, "
            f"missing={missing}"
        )

    obligation_by_id = {item["proof_id"]: item for item in product_obligations}
    allowed_bindings = _allowed_authority_bindings(bicp)
    for family in families:
        if family["implementation_target_id"] != authority["implementation_target"]["object_id"]:
            raise ValueError(f"family {family['id']} targets the wrong implementation identity")
        if family["tier_treatment"] != "NOT_CLASSIFIED":
            raise ValueError(f"family {family['id']} introduces product Tier A/B/C drift")
        obligation_ids = family["proof_obligation_ids"]
        unknown = set(obligation_ids) - set(required_ids)
        if unknown:
            raise ValueError(
                f"family {family['id']} cites non-current product obligations: "
                f"{sorted(unknown)}"
            )
        if set(obligation_ids) & architecture_obligations:
            raise ValueError(
                f"family {family['id']} contaminates product proof with "
                "architecture obligations"
            )
        if set(obligation_ids) & forbidden:
            raise ValueError(f"family {family['id']} cites forbidden predecessor proof IDs")

        bound_authorities: set[str] = set()
        for binding in family["authority_bindings"]:
            authority_id = binding["authority_id"]
            proposition_ids = set(binding["proposition_ids"])
            if authority_id not in allowed_bindings:
                raise ValueError(
                    f"family {family['id']} cites authority outside BICP-routed/current "
                    f"proposition authority: {authority_id}"
                )
            invalid_props = proposition_ids - allowed_bindings[authority_id]
            if invalid_props:
                raise ValueError(
                    f"family {family['id']} cites unbound propositions for "
                    f"{authority_id}: {sorted(invalid_props)}"
                )
            bound_authorities.add(authority_id)
        for obligation_id in obligation_ids:
            linked = set(obligation_by_id[obligation_id]["authority_refs"])
            if not (linked & bound_authorities):
                raise ValueError(
                    f"family {family['id']} lacks exact authority binding linked to {obligation_id}"
                )

        for dimension, value in family["case_coverage"].items():
            if not _case_dimension_valid(value):
                raise ValueError(
                    f"family {family['id']} case dimension {dimension} must contain "
                    "cases xor not_applicable_reason"
                )
        expected_command = f"python -m pytest {family['path']}"
        if family["command"] != expected_command:
            raise ValueError(
                f"family {family['id']} command must be exactly {expected_command!r}"
            )

    aggregates = aggregates_doc["aggregates"]
    if len(aggregates) != 1:
        raise ValueError("exactly one Raw Signal product aggregate is required")
    aggregate = aggregates[0]
    if aggregate["id"] != authority["claim_id"]:
        raise ValueError("aggregate/authority claim ID mismatch")
    if aggregate["implementation_target_id"] != authority["implementation_target"]["object_id"]:
        raise ValueError("aggregate implementation target mismatch")
    if aggregate["required_proof_obligation_ids"] != required_ids:
        raise ValueError("aggregate required obligation set/order mismatch")
    if set(aggregate["family_ids"]) != set(family_ids):
        raise ValueError("aggregate family membership must equal the admitted family registry")

    covered = {proof_id for family in families for proof_id in family["proof_obligation_ids"]}
    required = set(required_ids)
    if not families:
        expected_state = "INCOMPLETE_NO_PHYSICAL_FAMILIES"
    elif covered == required:
        expected_state = "READY_FOR_PROOF"
    else:
        expected_state = "INCOMPLETE_COVERAGE"
    if aggregate["state"] != expected_state:
        raise ValueError(
            f"aggregate state mismatch; expected {expected_state}, got {aggregate['state']}"
        )
    if covered - required:
        raise ValueError(f"aggregate covers non-current obligations: {sorted(covered - required)}")

    return [
        "PASS: product-proof control configuration is structurally and semantically bound",
        f"BICP: {bicp['packet_id']} sha256={authority['bicp']['sha256']}",
        f"implementation target: {authority['implementation_target']['object_id']}",
        f"required product obligations: {len(required_ids)}",
        f"admitted physical product families: {len(families)}",
        f"covered product obligations: {len(covered)}/{len(required)}",
        f"aggregate: {aggregate['id']} state={aggregate['state']}",
        f"separate architecture proof axis: {authority['architecture_proof_axis']}",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path)
    args = parser.parse_args()
    root = (args.repository or Path(__file__).resolve().parents[1]).resolve()
    try:
        for line in validate_product_proof(root):
            print(line)
    except Exception as exc:  # fail closed with attributable message
        print(f"FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
