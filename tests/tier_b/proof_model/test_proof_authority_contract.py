from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from scripts.proof_authority import AuthorityError, validate_authority_documents

REPO_ROOT = Path(__file__).resolve().parents[3]


def _load_live_documents() -> tuple[dict, dict]:
    registry = yaml.safe_load(
        (REPO_ROOT / "config/retained_test_registry.yaml").read_text(encoding="utf-8")
    )
    manifest = yaml.safe_load((REPO_ROOT / "config/proof_blocks.yaml").read_text(encoding="utf-8"))
    return registry, manifest


def test_live_authority_covers_every_physical_test_once() -> None:
    registry, manifest = _load_live_documents()

    model = validate_authority_documents(registry, manifest, repo_root=REPO_ROOT)

    physical = {
        path.relative_to(REPO_ROOT).as_posix()
        for tier in ("tier_a", "tier_b", "tier_c")
        for path in (REPO_ROOT / "tests" / tier).rglob("test_*.py")
    }
    assert set(model.path_admissions) == physical
    assert len(model.path_admissions) == len(physical)


def test_live_alpha_promotion_resolves_exact_current_module_families() -> None:
    registry, manifest = _load_live_documents()

    model = validate_authority_documents(registry, manifest, repo_root=REPO_ROOT)
    promotion = model.promotion_sets["alpha_current"]

    assert promotion.proof_block_ids == (
        "m13_state_kernel_module_local_proof",
        "m13_sqlite_restart_contract",
        "m04_k07_packet_role_contract",
        "m01_source_admission_contract",
        "m07_k12_coefficient_modifier_contract",
        "m08_k13_playbook_catalogue_contract",
        "m02_k04_financial_calendar_contract",
        "m03_k05_k06_prepared_data_contract",
        "m05_k08_k09_serial_cognition_contract",
        "m06_k10_parallel_risk_contract",
        "m06_owner_fact_completeness_contract",
        "m09_k11_k14_capital_authority_contract",
        "m10_k15_execution_gateway_contract",
        "live_operational_boundaries_contract",
        "m11_k16_k17_portfolio_lifecycle_contract",
        "m12_k19_authoritative_replay_contract",
        "m00_final_composition_contract",
        "post_alpha_m00_transport_adapter_contract",
        "m00_upstream_workflow_contract",
    )
    assert len(promotion.test_paths) == 21
    assert all(
        model.path_admissions[path].lifecycle == "current_blocking" for path in promotion.test_paths
    )


def test_legacy_promotion_key_is_a_membership_identical_compatibility_alias() -> None:
    registry, manifest = _load_live_documents()

    model = validate_authority_documents(registry, manifest, repo_root=REPO_ROOT)

    assert (
        model.promotion_sets["pre_m00_current"].proof_block_ids
        == model.promotion_sets["alpha_current"].proof_block_ids
    )
    assert (
        model.promotion_sets["pre_m00_current"].test_paths
        == model.promotion_sets["alpha_current"].test_paths
    )


def test_duplicate_path_admission_is_rejected() -> None:
    registry, manifest = _load_live_documents()
    broken = deepcopy(registry)
    broken["canonical_admission_model"]["path_admissions"].append(
        deepcopy(broken["canonical_admission_model"]["path_admissions"][0])
    )

    with pytest.raises(AuthorityError, match="duplicate test_path"):
        validate_authority_documents(broken, manifest, repo_root=REPO_ROOT)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("tier", "Tier Z", "invalid tier"),
        ("lifecycle", "quietly_green", "invalid lifecycle"),
    ],
)
def test_invalid_family_domains_are_rejected(field: str, value: str, message: str) -> None:
    registry, manifest = _load_live_documents()
    broken = deepcopy(registry)
    broken["canonical_admission_model"]["test_families"][0][field] = value

    with pytest.raises(AuthorityError, match=message):
        validate_authority_documents(broken, manifest, repo_root=REPO_ROOT)


def test_unknown_family_reference_is_rejected() -> None:
    registry, manifest = _load_live_documents()
    broken = deepcopy(manifest)
    block = next(
        item
        for item in broken["proof_blocks"]
        if item["proof_block_id"] == "m01_source_admission_contract"
    )
    block["test_family_ids"] = ["not_a_registered_family"]

    with pytest.raises(AuthorityError, match="unknown test_family_id"):
        validate_authority_documents(registry, broken, repo_root=REPO_ROOT)


def test_current_block_command_cannot_disagree_with_registry_membership() -> None:
    registry, manifest = _load_live_documents()
    broken = deepcopy(manifest)
    block = next(
        item
        for item in broken["proof_blocks"]
        if item["proof_block_id"] == "m01_source_admission_contract"
    )
    block["command"] = "python -m pytest tests/tier_a/m02_k04/test_m02_k04_contract.py"

    with pytest.raises(AuthorityError, match="command test membership"):
        validate_authority_documents(registry, broken, repo_root=REPO_ROOT)


def test_current_block_requires_exact_normative_proposition_ids() -> None:
    registry, manifest = _load_live_documents()
    broken = deepcopy(manifest)
    block = next(
        item
        for item in broken["proof_blocks"]
        if item["proof_block_id"] == "m01_source_admission_contract"
    )
    block["normative_proposition_ids"] = []

    with pytest.raises(AuthorityError, match="normative_proposition_ids"):
        validate_authority_documents(registry, broken, repo_root=REPO_ROOT)


def test_live_control_surfaces_identify_comprehensive_debt_pack() -> None:
    from scripts.proof_authority import validate_active_control

    assert validate_active_control(REPO_ROOT) == "POST-ALPHA-COMPREHENSIVE-DEBT-RETIREMENT-V1"


def test_active_control_validation_accepts_post_alpha_transport_adapter_pack(
    tmp_path: Path,
) -> None:
    from scripts.proof_authority import validate_active_control

    canonical = tmp_path / "project_control/canonical_project_manager/EXEC_PLAN.md"
    canonical.parent.mkdir(parents=True)
    canonical.write_text(
        "**Status:** `COMPLETE:ALPHA_CONSOLIDATED_WITH_EXPLICIT_DEBT`\n",
        encoding="utf-8",
    )
    (tmp_path / "ROADMAP_LEDGER_V2.md").write_text(
        "| Active control pack | `POST-ALPHA-M00-TRANSPORT-ADAPTERS-V1` |\n",
        encoding="utf-8",
    )
    process = tmp_path / "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md"
    process.parent.mkdir(parents=True)
    process.write_text(
        "The current active bounded pack is " "`POST-ALPHA-M00-TRANSPORT-ADAPTERS-V1`\n",
        encoding="utf-8",
    )

    assert validate_active_control(tmp_path) == "POST-ALPHA-M00-TRANSPORT-ADAPTERS-V1"


def test_active_control_validation_accepts_comprehensive_debt_pack(
    tmp_path: Path,
) -> None:
    from scripts.proof_authority import validate_active_control

    canonical = tmp_path / "project_control/canonical_project_manager/EXEC_PLAN.md"
    canonical.parent.mkdir(parents=True)
    canonical.write_text(
        "**Status:** `COMPLETE:ALPHA_CONSOLIDATED_WITH_EXPLICIT_DEBT`\n",
        encoding="utf-8",
    )
    (tmp_path / "ROADMAP_LEDGER_V2.md").write_text(
        "| Active control pack | `POST-ALPHA-COMPREHENSIVE-DEBT-RETIREMENT-V1` |\n",
        encoding="utf-8",
    )
    process = tmp_path / "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md"
    process.parent.mkdir(parents=True)
    process.write_text(
        "The current active bounded pack is " "`POST-ALPHA-COMPREHENSIVE-DEBT-RETIREMENT-V1`\n",
        encoding="utf-8",
    )

    assert validate_active_control(tmp_path) == "POST-ALPHA-COMPREHENSIVE-DEBT-RETIREMENT-V1"


def test_active_control_validation_uses_pack_identity_not_gate_wording(
    tmp_path: Path,
) -> None:
    from scripts.proof_authority import validate_active_control

    canonical = tmp_path / "project_control/canonical_project_manager/EXEC_PLAN.md"
    canonical.parent.mkdir(parents=True)
    canonical.write_text(
        "**Status:** `ACTIVE:PRE_M00_TESTING_GUARDRAIL_REPAIR`\n",
        encoding="utf-8",
    )
    (tmp_path / "ROADMAP_LEDGER_V2.md").write_text(
        "| Current active slice | any lawful gate progression wording |\n"
        "| Active control pack | `PRE-M00-TESTING-GUARDRAIL-REPAIR-V1` |\n",
        encoding="utf-8",
    )
    process = tmp_path / "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md"
    process.parent.mkdir(parents=True)
    process.write_text(
        "The current active bounded pack is " "`PRE-M00-TESTING-GUARDRAIL-REPAIR-V1`\n",
        encoding="utf-8",
    )

    assert validate_active_control(tmp_path) == "PRE-M00-TESTING-GUARDRAIL-REPAIR-V1"


def test_active_control_validation_accepts_consolidated_alpha_state(
    tmp_path: Path,
) -> None:
    from scripts.proof_authority import validate_active_control

    canonical = tmp_path / "project_control/canonical_project_manager/EXEC_PLAN.md"
    canonical.parent.mkdir(parents=True)
    canonical.write_text(
        "**Status:** `COMPLETE:ALPHA_CONSOLIDATED_WITH_EXPLICIT_DEBT`\n",
        encoding="utf-8",
    )
    (tmp_path / "ROADMAP_LEDGER_V2.md").write_text(
        "| Active control pack | none — canonical ExecPlan only |\n",
        encoding="utf-8",
    )
    process = tmp_path / "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md"
    process.parent.mkdir(parents=True)
    process.write_text(
        "No subordinate bounded pack is active.\n",
        encoding="utf-8",
    )

    assert validate_active_control(tmp_path) == "CANONICAL:ALPHA_CONSOLIDATED"


def test_api_state_ownership_conflict_cannot_activate_legacy_and_current_families() -> None:
    registry, manifest = _load_live_documents()
    broken = deepcopy(registry)
    legacy = next(
        item
        for item in broken["canonical_admission_model"]["test_families"]
        if item["test_family_id"] == "path__tests_tier_a_api_test_fwd005_api_exposure_contract_py"
    )
    legacy["lifecycle"] = "current_nonblocking"

    with pytest.raises(AuthorityError, match="api_state_ownership"):
        validate_authority_documents(broken, manifest, repo_root=REPO_ROOT)


def test_api_state_ownership_lifecycles_are_explicit_and_not_in_current_promotion() -> None:
    registry, manifest = _load_live_documents()
    model = validate_authority_documents(registry, manifest, repo_root=REPO_ROOT)

    legacy = model.path_admissions["tests/tier_a/api/test_fwd005_api_exposure_contract.py"]
    current = model.path_admissions[
        "tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py"
    ]
    promoted = set(model.promotion_sets["alpha_current"].test_paths)

    assert legacy.lifecycle == "superseded_compatibility"
    assert current.lifecycle == "next_gate_expected_red"
    assert legacy.test_path not in promoted
    assert current.test_path not in promoted
