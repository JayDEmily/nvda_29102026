from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from nvda_desk.capital.authority import (
    build_capital_deployment_receipt,
    evaluate_capital_deployment,
)
from nvda_desk.config.coefficient_authority import CoefficientAuthorityService
from nvda_desk.contracts.capital import CapitalDeploymentAuthorityInput
from nvda_desk.contracts.downstream import DownstreamLiveInventorySnapshot
from nvda_desk.contracts.eligibility import (
    EligibilityAdmissibilitySurface,
    PlaybookEligibilityOutput,
)
from nvda_desk.contracts.execution import ExecutionExpressionInput, ExecutionExpressionOutput
from nvda_desk.contracts.posture import PermissionState
from nvda_desk.contracts.upstream_signal import (
    RawUpstreamSignalInput,
    UpstreamSignalCoverageEntry,
)
from nvda_desk.domain.execution.candidate_expression import evaluate_execution_expression
from nvda_desk.persistence.durable_sql import DurableSqliteStore
from nvda_desk.repositories.position_repository import PositionRepository
from nvda_desk.review.packet_service import DailyReviewPacket, ReviewSafeRendering
from nvda_desk.upstream.raw_signal_coverage import build_upstream_signal_coverage_map
from nvda_desk.upstream.raw_signal_ingress import ingest_raw_upstream_signal

_REPO_ROOT = Path(__file__).resolve().parents[3]


def test_c007_new_signal_family_is_registry_driven_and_preserves_source_identity() -> None:
    entry = UpstreamSignalCoverageEntry(
        owner="market_context",
        signal_family_id="opening_hft_intensity",
        source_scope="NVDA",
        packet_fields=["intensity"],
    )
    coverage = build_upstream_signal_coverage_map([entry])
    signal = RawUpstreamSignalInput(
        source_id="source-record-1",
        signal_family_id="opening_hft_intensity",
        scope_id="NVDA",
        payload={"intensity": 0.8},
    )

    result = ingest_raw_upstream_signal(
        raw_signal=signal,
        dataset_packet_payload={"unchanged": True},
        admitted_signal_families=coverage.admitted_signal_family_ids,
    )

    assert result.sanity_trace.source_id == "source-record-1"
    assert result.sanity_trace.signal_family_id == "opening_hft_intensity"
    assert result.trace_envelope["source_id"] == "source-record-1"
    assert result.dataset_packet_payload == {"unchanged": True}
    assert result.trade_decision_side_effects == []


def test_c007_raw_signal_contract_carries_source_observation_time() -> None:
    assert {"source_time_utc", "observed_at_utc"} & set(RawUpstreamSignalInput.model_fields)


def test_c014_identifier_role_matrix_is_complete_and_has_no_unowned_mandatory_role() -> None:
    matrix_path = (
        _REPO_ROOT
        / "project_control"
        / "normative_authority_top_down_alignment"
        / "IDENTIFIER_LINEAGE_PROOF_MATRIX.tsv"
    )
    with matrix_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    required_roles = {
        "source_capture_id",
        "bundle_id",
        "packet_id",
        "trace_id",
        "run_id",
        "scenario_id",
        "candidate_id",
        "policy_id",
        "receipt_id",
        "dataset_id",
        "input_fingerprint",
    }
    observed = {row["role_id"] for row in rows}
    assert required_roles.issubset(observed)
    assert len(observed) == len(rows)
    for row in rows:
        assert row["authoritative_originator"].strip()
        assert row["forbidden_creators"].strip()
        if "yes" in row["mandatory"].lower():
            failure = row["failure_when_absent"].lower()
            assert any(token in failure for token in ("fail", "withhold", "withheld"))


def test_c022_durable_sql_surface_remains_bounded_demo_storage_not_material_state_owner() -> None:
    public_methods = {name for name in vars(DurableSqliteStore) if not name.startswith("_")}
    assert public_methods == {
        "initialise_schema",
        "seed_dev_data",
        "list_intraday_bars",
        "list_option_snapshots",
        "list_session_calendars",
    }
    assert (
        not {
            "write_position",
            "append_receipt",
            "record_risk_decision",
            "write_capital_state",
        }
        & public_methods
    )


def test_c029_coefficient_receipt_preserves_baseline_effective_values_and_closed_authority() -> (
    None
):
    receipt = CoefficientAuthorityService().build_replay_receipt(
        active_modifier_ids=["negative_gamma_stress"],
        owner_stage="posture",
    )
    values = {item.coefficient_id: item for item in receipt.resolved_coefficients}

    assert receipt.authority_id
    assert receipt.schema_version
    assert len(receipt.replay_fingerprint) == 64
    assert values["max_risk_per_trade"].baseline_value == 0.35
    assert values["max_risk_per_trade"].effective_value == 0.25
    assert values["max_risk_per_trade"].modifier_inputs == ["negative_gamma_stress"]
    assert "capital_deployment_decision" in receipt.closed_authority_classes
    assert "hidden_strategy_change" in receipt.closed_authority_classes


def test_c030_coefficient_authority_document_is_path_substitutable_and_replay_versioned(
    tmp_path: Path,
) -> None:
    source_path = _REPO_ROOT / "config" / "coefficient_authority.v1.yaml"
    payload = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    payload["authority_id"] = "coefficient_authority_substitution_fixture"
    replacement = tmp_path / "replacement.yaml"
    replacement.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    receipt = CoefficientAuthorityService(replacement).build_replay_receipt(
        active_modifier_ids=["negative_gamma_stress"],
        owner_stage="posture",
    )

    assert receipt.authority_id == "coefficient_authority_substitution_fixture"
    assert receipt.schema_version == "v1"
    assert len(receipt.replay_fingerprint) == 64


def test_c034_execution_expression_carries_candidate_identity_without_capital_or_broker_authority() -> (
    None
):
    output = evaluate_execution_expression(
        execution_input=ExecutionExpressionInput(),
        eligibility_output=PlaybookEligibilityOutput(
            admissibility_surface=EligibilityAdmissibilitySurface(
                permission_state=PermissionState.ALLOW,
            ),
            active_family_ids=["momentum_breakout"],
            registry_id="registry-v1",
        ),
    )

    assert "candidate_id" in ExecutionExpressionOutput.model_fields
    payload = output.model_dump(mode="json")
    assert not {
        "authorised_notional_usd",
        "authorised_deployable_pct",
        "broker_order_id",
        "execution_allowed",
    } & set(payload)


def _capital_input(**overrides: object) -> CapitalDeploymentAuthorityInput:
    payload: dict[str, object] = {
        "final_risk_action": "proceed",
        "final_risk_receipt_id": "final-risk-1",
        "serial_candidate_id": "candidate-1",
        "serial_candidate_eligible": True,
        "serial_confidence": 0.5,
        "downstream_pre_deployment_allowed": True,
        "downstream_pre_deployment_receipt_id": "pre-deployment-1",
        "parallel_risk_packet_id": "parallel-risk-1",
        "parallel_risk_envelope_state": "broad",
        "parallel_risk_hard_blocks": [],
        "parallel_risk_caution_flags": [],
        "coefficient_min_deployable_floor_pct": 0.0,
        "temporal_event_window_active": False,
        "temporal_event_risk": "normal",
        "capital_state_snapshot_id": "capital-state-1",
        "available_capital_usd": 100_000.0,
        "bounded_policy_id": "capital-policy-v1",
        "requested_deployable_pct": 10.0,
        "max_deployable_pct": 10.0,
        "inventory_pct": 0.0,
    }
    payload.update(overrides)
    return CapitalDeploymentAuthorityInput(**payload)


def test_c037_capital_receipt_is_reproducible_and_serial_confidence_does_not_size() -> None:
    low = _capital_input(serial_confidence=0.1)
    high = _capital_input(serial_confidence=0.9)
    low_decision = evaluate_capital_deployment(low, receipt_id="capital-receipt-1")
    high_decision = evaluate_capital_deployment(high, receipt_id="capital-receipt-1")

    assert low_decision.authorised_deployable_pct == high_decision.authorised_deployable_pct
    assert low_decision.authorised_notional_usd == high_decision.authorised_notional_usd
    low_receipt = build_capital_deployment_receipt(
        receipt_id="capital-receipt-1", context=low, decision=low_decision
    )
    replay_receipt = build_capital_deployment_receipt(
        receipt_id="capital-receipt-1", context=low, decision=low_decision
    )
    assert low_receipt == replay_receipt
    assert low_receipt.input_trace.bounded_policy_id == "capital-policy-v1"
    assert low_receipt.placement_authority_opened is False


def test_c040_inventory_fill_reconciliation_is_idempotent_and_snapshot_remains_read_only() -> None:
    from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService

    service = DownstreamLiveInventoryService(position_repository=PositionRepository())
    event = {
        "fill_evidence_id": "fill-1",
        "position_id": "position-1",
        "symbol": "NVDA",
        "declared_exposure_delta": 10.0,
    }
    first = service.reconcile_fill_evidence([event], reconciliation_id="reconciliation-1")
    assert isinstance(first, DownstreamLiveInventorySnapshot)
    try:
        service.reconcile_fill_evidence([event], reconciliation_id="reconciliation-2")
    except ValueError as exc:
        assert "duplicate fill_evidence_id" in str(exc)
    else:
        raise AssertionError("duplicate fill evidence was applied twice")
    assert "serial_stage_outputs" not in DownstreamLiveInventorySnapshot.model_fields


def test_c042_overnight_carry_contract_carries_policy_version_and_next_session_source_identity() -> (
    None
):
    from nvda_desk.downstream.overnight_carry import (
        OvernightCarryEvaluation,
        OvernightCarryReplayResult,
    )

    assert "policy_version" in OvernightCarryEvaluation.model_fields
    assert {
        "next_session_source_id",
        "next_session_source_artifact_id",
    } & set(OvernightCarryReplayResult.model_fields)


def test_c044_review_packets_expose_missing_material_and_source_lineage_without_runtime_authority() -> (
    None
):
    assert {
        "missing_material_ids",
        "missing_material_flags",
    } & set(DailyReviewPacket.model_fields)
    assert {
        "source_packet_ids",
        "source_receipt_ids",
        "source_artifact_ids",
    } & set(DailyReviewPacket.model_fields)
    assert ReviewSafeRendering.model_fields["runtime_authority_mutated"].default is False


def _unit4_policy_digest(value: object) -> str:
    import hashlib
    import json
    from collections.abc import Mapping
    from pathlib import Path as FilePath

    def normalise(item: object) -> object:
        if isinstance(item, Mapping):
            return {
                str(key): normalise(member)
                for key, member in sorted(item.items(), key=lambda pair: str(pair[0]))
            }
        if isinstance(item, (set, frozenset)):
            values = [normalise(member) for member in item]
            return sorted(values, key=lambda member: json.dumps(member, sort_keys=True))
        if isinstance(item, (list, tuple)):
            return [normalise(member) for member in item]
        if isinstance(item, FilePath):
            return str(item)
        return item

    encoded = json.dumps(normalise(value), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@pytest.mark.parametrize(
    ("module_name", "attribute_name", "frozen_kind", "expected_digest"),
    [
        pytest.param(
            "nvda_desk.calendar.operational.events",
            "_MATERIALITY_RANK",
            "mapping",
            "4168a026c8caf40979f2d26a546d821ed0df0c4499aca74d2a343d04d75d6c6a",
            id="calendar-materiality-rank",
        ),
        pytest.param(
            "nvda_desk.capital.authority",
            "_CONSUMED_INPUTS",
            "tuple",
            "5cc66f28e7852229313fb519bde7dbbc3837d6e1377c4d1be1394f02120da7e3",
            id="capital-consumed-inputs",
        ),
        pytest.param(
            "nvda_desk.contracts.packets",
            "K07_LINEAGE_MATRIX",
            "mapping",
            "0b85dfa7ec303f8b7214d71a76384e879c4e8d5baa8ec35382dc68b043a571b6",
            id="k07-lineage-matrix",
        ),
        pytest.param(
            "nvda_desk.contracts.packets",
            "K07_ROLE_CHECKS",
            "mapping",
            "afb950011c1a49ad1bdb4599f107af4f2bc5a29a8407220fd5ab8f4356846e0c",
            id="k07-role-checks",
        ),
        pytest.param(
            "nvda_desk.contracts.parallel_risk",
            "NON_TEMPORAL_STAGE_NOTES",
            "mapping",
            "3e3b3a8d99d07f5763871b9375b408c65d793c033932defe2ac41d23dadb272c",
            id="parallel-risk-stage-notes",
        ),
        pytest.param(
            "nvda_desk.contracts.serial_spine",
            "SERIAL_STAGE_DEPENDENCIES",
            "mapping",
            "f6b4c72ed31d56bd5bb9486ada7f65d6b54ccbc7ef0b29800e062aa687c33096",
            id="serial-spine-dependencies",
        ),
        pytest.param(
            "nvda_desk.contracts.serial_spine",
            "SERIAL_STAGE_OUTPUT_SCHEMAS",
            "mapping",
            "1fe2a3fb7df8ee9b0f07a85309a67eac9c0c693c23ce34382ac29f7dd997ee99",
            id="serial-spine-output-schemas",
        ),
        pytest.param(
            "nvda_desk.domain.parallel_risk.candidate_audit",
            "_BLOCK_TAGS",
            "frozenset",
            "34a086dd3974ee22c91552d385cf82a5498d016c90ac0b36f692e3b133c04ff4",
            id="parallel-risk-block-tags",
        ),
        pytest.param(
            "nvda_desk.domain.parallel_risk.candidate_audit",
            "_CAUTION_TAGS",
            "frozenset",
            "8e04275ab183aa55d2c1790b5862557d06290770782df56ec3154a46890cb49b",
            id="parallel-risk-caution-tags",
        ),
        pytest.param(
            "nvda_desk.domain.parallel_risk.family_aggregation",
            "_STATE_RANK",
            "mapping",
            "92eb696543ba9d4a91276717e5b5458900ef62ca105d6a68f01caa618592e7f5",
            id="parallel-risk-state-rank",
        ),
        pytest.param(
            "nvda_desk.domain.posture.permission",
            "DEFAULT_POSTURE_COEFFICIENTS",
            "mapping",
            "fd2e8c707d119833b4b45ad3be30158890444f0c7895abc99b62b28230748856",
            id="posture-default-coefficients",
        ),
        pytest.param(
            "nvda_desk.m05_serial_cognition.contracts",
            "SERIAL_STAGE_DEPENDENCIES",
            "mapping",
            "f6b4c72ed31d56bd5bb9486ada7f65d6b54ccbc7ef0b29800e062aa687c33096",
            id="m05-stage-dependencies",
        ),
        pytest.param(
            "nvda_desk.m05_serial_cognition.contracts",
            "STAGE_OWNER_IDS",
            "mapping",
            "12cddfe0c6993b10b5dcad1413ba4fe1259d01f5c27df0c8b62229844d17a9bc",
            id="m05-stage-owner-ids",
        ),
        pytest.param(
            "nvda_desk.m05_serial_cognition.contracts",
            "ALLOWED_STAGE_AUTHORITY_OWNERS",
            "mapping",
            "dbacf5c1685383fdf18fd3d8554619d17ef73fdaac2bfe39071dea580366304f",
            id="m05-stage-authority-owners",
        ),
        pytest.param(
            "nvda_desk.m05_serial_cognition.contracts",
            "ALLOWED_STAGE_FACT_IDS",
            "mapping",
            "0b704b58459e2aee64aaa20370bba0d703115ab846c73e29cd83bad8dec2a0ef",
            id="m05-stage-fact-ids",
        ),
        pytest.param(
            "nvda_desk.vocabulary_builder",
            "GOVERNED_SOURCE_PATHS",
            "tuple",
            "3d9065ca376df0abdc2dca944a9bd4ec2d5c8ce5117126bee0975ff83e330199",
            id="vocabulary-governed-paths",
        ),
        pytest.param(
            "nvda_desk.vocabulary_builder",
            "_HEADER_FIELDS",
            "mapping",
            "808055d94f8ad547b8c08bcf01ae2c39ec5ac246e028bf845878aa4d951a7a74",
            id="vocabulary-header-fields",
        ),
        pytest.param(
            "nvda_desk.vocabulary_builder",
            "_HUMAN_FIELD_PREFIXES",
            "mapping",
            "2b8c7ad3eb50f13e1bf3de3b0de66a4f2b3c176225b9dedaf2147233951b81ac",
            id="vocabulary-human-field-prefixes",
        ),
        pytest.param(
            "nvda_desk.vocabulary_synonym_audit",
            "ALLOWED_EXTENSIONS",
            "frozenset",
            "9a028204ad70c1bb91df84227be20a27606c79ff3a90496b0095398b1a619e94",
            id="vocabulary-audit-extensions",
        ),
    ],
)
def test_unit4b_governed_process_values_preserve_content_and_reject_caller_mutation(
    module_name: str,
    attribute_name: str,
    frozen_kind: str,
    expected_digest: str,
) -> None:
    import importlib
    from types import MappingProxyType

    value = getattr(importlib.import_module(module_name), attribute_name)
    assert _unit4_policy_digest(value) == expected_digest

    if frozen_kind == "mapping":
        assert isinstance(value, MappingProxyType)
        with pytest.raises(TypeError):
            value["__unit4_mutation__"] = object()
    elif frozen_kind == "tuple":
        assert isinstance(value, tuple)
        with pytest.raises(TypeError):
            value[0] = value[0]
    else:
        assert isinstance(value, frozenset)
        with pytest.raises(AttributeError):
            value.add("__unit4_mutation__")
