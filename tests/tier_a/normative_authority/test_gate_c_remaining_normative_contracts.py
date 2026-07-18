from __future__ import annotations

import csv
from pathlib import Path

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
