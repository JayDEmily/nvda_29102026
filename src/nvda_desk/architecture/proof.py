"""Exact test admission, proof-block and promotion-set validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from .schema import validate_document

_PROPOSITION_RE = re.compile(r"\bAK-[A-Z]+-[0-9]{3}\b")


@dataclass(frozen=True, slots=True)
class ProofState:
    families: tuple[dict, ...]
    blocks: tuple[dict, ...]
    promotion_sets: tuple[dict, ...]

    def paths_for_set(self, promotion_set_id: str) -> tuple[str, ...]:
        promotion = next(
            (item for item in self.promotion_sets if item["id"] == promotion_set_id), None
        )
        if promotion is None:
            raise KeyError(f"unknown promotion set: {promotion_set_id}")
        block_ids = set(promotion["proof_block_ids"])
        family_ids = {
            family_id
            for block in self.blocks
            if block["id"] in block_ids
            for family_id in block["family_ids"]
        }
        return tuple(
            sorted(family["path"] for family in self.families if family["id"] in family_ids)
        )


def load_and_validate_proof_state(repository_root: Path) -> ProofState:
    config_root = repository_root / "config" / "proof"
    schema_root = repository_root / "schemas"
    specs = (
        ("test_families.yaml", "test_family.schema.json"),
        ("proof_blocks.yaml", "proof_block.schema.json"),
        ("promotion_sets.yaml", "promotion_set.schema.json"),
    )
    for config_name, schema_name in specs:
        validate_document(config_root / config_name, schema_root / schema_name)
    families_doc = yaml.safe_load((config_root / "test_families.yaml").read_text(encoding="utf-8"))
    blocks_doc = yaml.safe_load((config_root / "proof_blocks.yaml").read_text(encoding="utf-8"))
    sets_doc = yaml.safe_load((config_root / "promotion_sets.yaml").read_text(encoding="utf-8"))
    state = ProofState(
        tuple(families_doc["test_families"]),
        tuple(blocks_doc["proof_blocks"]),
        tuple(sets_doc["promotion_sets"]),
    )
    validate_proof_state(repository_root, state)
    return state


def validate_proof_state(repository_root: Path, state: ProofState) -> None:
    family_ids = [item["id"] for item in state.families]
    family_paths = [item["path"] for item in state.families]
    block_ids = [item["id"] for item in state.blocks]
    set_ids = [item["id"] for item in state.promotion_sets]
    for label, values in (
        ("family IDs", family_ids),
        ("family paths", family_paths),
        ("block IDs", block_ids),
        ("set IDs", set_ids),
    ):
        if len(values) != len(set(values)):
            raise ValueError(f"duplicate {label}")

    admitted_paths = set(family_paths)
    physical_paths = {
        path.relative_to(repository_root).as_posix()
        for test_root in (
            repository_root / "tests" / "architecture",
            repository_root / "tests" / "bootstrap",
        )
        if test_root.exists()
        for path in test_root.rglob("test_*.py")
    }
    if physical_paths != admitted_paths:
        raise ValueError(
            f"test admission mismatch; unadmitted={sorted(physical_paths - admitted_paths)}, "
            f"missing={sorted(admitted_paths - physical_paths)}"
        )

    propositions = set()
    for path in (repository_root / "docs" / "architecture").glob("*.md"):
        propositions.update(_PROPOSITION_RE.findall(path.read_text(encoding="utf-8")))
    unknown_props = sorted(
        {prop for family in state.families for prop in family["proposition_ids"]} - propositions
    )
    if unknown_props:
        raise ValueError(f"test families cite unknown propositions: {unknown_props}")

    families_by_id = {item["id"]: item for item in state.families}
    blocks_by_id = {item["id"]: item for item in state.blocks}
    sets_by_id = {item["id"]: item for item in state.promotion_sets}
    memberships: dict[str, int] = {family_id: 0 for family_id in family_ids}
    for block in state.blocks:
        for family_id in block["family_ids"]:
            if family_id not in families_by_id:
                raise ValueError(f"block {block['id']} references unknown family {family_id}")
            memberships[family_id] += 1
            family = families_by_id[family_id]
            if family["proof_block_id"] != block["id"]:
                raise ValueError(f"family {family_id} and block {block['id']} disagree")
            if family["tier"] != block["tier"] or family["lifecycle"] != block["lifecycle"]:
                raise ValueError(
                    f"family {family_id} and block {block['id']} tier/lifecycle disagree"
                )
    if any(count != 1 for count in memberships.values()):
        raise ValueError(f"each family must belong to exactly one block: {memberships}")

    for promotion in state.promotion_sets:
        for block_id in promotion["proof_block_ids"]:
            if block_id not in blocks_by_id:
                raise ValueError(
                    f"promotion set {promotion['id']} references unknown block {block_id}"
                )
            block = blocks_by_id[block_id]
            if (
                block["tier"] != promotion["required_tier"]
                or block["lifecycle"] != promotion["lifecycle"]
            ):
                raise ValueError(f"promotion set {promotion['id']} and block {block_id} disagree")
    for family in state.families:
        for set_id in family["promotion_sets"]:
            if set_id not in sets_by_id:
                raise ValueError(f"family {family['id']} references unknown promotion set {set_id}")
            if family["proof_block_id"] not in sets_by_id[set_id]["proof_block_ids"]:
                raise ValueError(
                    f"family {family['id']} is not reachable through promotion set {set_id}"
                )
        if family["lifecycle"] == "current_blocking" and not family["promotion_sets"]:
            raise ValueError(f"current-blocking family {family['id']} lacks promotion membership")
