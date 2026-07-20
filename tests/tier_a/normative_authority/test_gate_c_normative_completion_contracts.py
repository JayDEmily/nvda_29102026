from __future__ import annotations

import importlib
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import pytest

_TIME = datetime(2026, 4, 21, 14, 0, tzinfo=timezone.utc)
_FINGERPRINT_A = "a" * 64
_FINGERPRINT_B = "b" * 64


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module: Any, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def _field_names(contract: Any) -> set[str]:
    if hasattr(contract, "model_fields"):
        return set(contract.model_fields)
    if hasattr(contract, "__dataclass_fields__"):
        return set(contract.__dataclass_fields__)
    pytest.fail(f"Required typed contract fields are not inspectable: {contract}")


def _enum_values(enum_type: type[Enum]) -> set[str]:
    return {str(item.value) for item in enum_type}


# C-004 / N-01 — typed options authority before cognition.
def test_c004_options_evidence_contract_preserves_identity_version_time_and_fingerprint() -> None:
    contracts = _require_module("nvda_desk.contracts.options_flow")
    envelope = _require_attr(contracts, "OptionsEvidenceEnvelope")
    required = {
        "evidence_id",
        "source_artifact_id",
        "capture_id",
        "input_schema_version",
        "adapter_policy_version",
        "effective_at_utc",
        "observed_at_utc",
        "captured_at_utc",
        "semantic_fingerprint",
        "completeness_state",
    }
    assert required.issubset(_field_names(envelope))
    assert "options_evidence_ref" in _field_names(contracts.OptionsFlowContextInput)


def test_c004_options_mapper_rejects_generic_mapping_without_typed_options_authority() -> None:
    mapper = _require_module("nvda_desk.cognition.ingress.options_mapper")
    build_options_flow_input = _require_attr(mapper, "build_options_flow_input")
    with pytest.raises((TypeError, ValueError), match="typed|evidence|envelope|authority"):
        build_options_flow_input({"spot_price": 101.0, "front_dte": 1, "next_dte": 5})


# C-005/C-018 / N-02 — exact four-layer financial-calendar model and ownership.
def test_c005_c018_financial_calendar_contract_has_exact_four_semantic_layers() -> None:
    contracts = _require_module("nvda_desk.contracts.reference_data")
    layer = _require_attr(contracts, "FinancialCalendarLayer")
    assert _enum_values(layer) == {
        "market_session_reference",
        "financial_event_reference",
        "operational_calendar_state",
        "derived_runtime_calendar_context",
    }
    bundle = _require_attr(contracts, "FinancialCalendarAuthorityBundle")
    assert {
        "market_session_reference",
        "financial_event_reference",
        "operational_calendar_state",
        "derived_runtime_calendar_context",
    } == _field_names(bundle)


def test_c005_equal_calendar_candidates_coalesce_with_all_lineage() -> None:
    contracts = _require_module("nvda_desk.contracts.reference_data")
    projection = _require_module("nvda_desk.calendar.reference.projection")
    candidate = _require_attr(contracts, "CalendarFactCandidate")
    policy_type = _require_attr(contracts, "CalendarFieldResolutionPolicy")
    layer = _require_attr(contracts, "FinancialCalendarLayer")
    resolve = _require_attr(projection, "resolve_calendar_field")
    candidates = (
        candidate(
            candidate_id="session-a",
            layer=layer.MARKET_SESSION_REFERENCE,
            fact_family="session_open",
            semantic_field="session_open_utc",
            value="2026-04-21T13:30:00Z",
            effective_at_utc=_TIME,
            source_artifact_id="calendar-a",
        ),
        candidate(
            candidate_id="session-b",
            layer=layer.OPERATIONAL_CALENDAR_STATE,
            fact_family="session_open",
            semantic_field="session_open_utc",
            value="2026-04-21T13:30:00Z",
            effective_at_utc=_TIME,
            source_artifact_id="calendar-b",
        ),
    )
    receipt = resolve(
        candidates=candidates,
        policy=policy_type(
            policy_id="session-open-v1",
            semantic_field="session_open_utc",
            mandatory=True,
            authoritative_layer=layer.MARKET_SESSION_REFERENCE,
        ),
    )
    assert receipt.selected_value == "2026-04-21T13:30:00Z"
    assert set(receipt.candidate_ids) == {"session-a", "session-b"}


def test_c005_c018_unequal_or_derived_override_without_explicit_supersession_fails_closed() -> None:
    contracts = _require_module("nvda_desk.contracts.reference_data")
    projection = _require_module("nvda_desk.calendar.reference.projection")
    candidate = _require_attr(contracts, "CalendarFactCandidate")
    policy_type = _require_attr(contracts, "CalendarFieldResolutionPolicy")
    conflict = _require_attr(contracts, "CalendarFieldConflictError")
    layer = _require_attr(contracts, "FinancialCalendarLayer")
    resolve = _require_attr(projection, "resolve_calendar_field")
    candidates = (
        candidate(
            candidate_id="session-source",
            layer=layer.MARKET_SESSION_REFERENCE,
            fact_family="session_close",
            semantic_field="session_close_utc",
            value="2026-04-21T20:00:00Z",
            effective_at_utc=_TIME,
            source_artifact_id="calendar-source",
        ),
        candidate(
            candidate_id="derived-current",
            layer=layer.DERIVED_RUNTIME_CALENDAR_CONTEXT,
            fact_family="session_close",
            semantic_field="session_close_utc",
            value="2026-04-21T19:59:00Z",
            effective_at_utc=_TIME,
            source_artifact_id="runtime-context",
        ),
    )
    with pytest.raises(conflict):
        resolve(
            candidates=candidates,
            policy=policy_type(
                policy_id="session-close-v1",
                semantic_field="session_close_utc",
                mandatory=True,
                authoritative_layer=layer.MARKET_SESSION_REFERENCE,
            ),
        )


# C-008 / N-03 — common prepared envelope plus tagged typed payload.
def test_c008_prepared_envelope_requires_common_identity_version_time_and_fingerprint_lineage() -> (
    None
):
    contracts = _require_module("nvda_desk.contracts.prepared_data")
    envelope = _require_attr(contracts, "PreparedDataEnvelope")
    required = {
        "prepared_id",
        "source_capture_refs",
        "input_schema_versions",
        "preparation_policy_version",
        "derivation_versions",
        "effective_at_utc",
        "input_fingerprint",
        "prepared_fingerprint",
        "validation_state",
        "completeness_state",
        "payload_kind",
        "payload",
    }
    assert required.issubset(_field_names(envelope))


def test_c008_prepared_envelope_rejects_untagged_generic_payload_authority() -> None:
    contracts = _require_module("nvda_desk.contracts.prepared_data")
    envelope = _require_attr(contracts, "PreparedDataEnvelope")
    with pytest.raises((TypeError, ValueError), match="payload|tag|typed|kind|contract"):
        envelope.model_validate(
            {
                "prepared_id": "prepared-1",
                "source_capture_refs": ["capture-1"],
                "input_schema_versions": {"market": "v1"},
                "preparation_policy_version": "prepare-v1",
                "derivation_versions": {"runtime_features": "v1"},
                "effective_at_utc": _TIME,
                "input_fingerprint": _FINGERPRINT_A,
                "prepared_fingerprint": _FINGERPRINT_B,
                "validation_state": "valid",
                "completeness_state": "complete",
                "payload": {"spot_price": 101.0},
            }
        )


# C-011 / N-04 — field-owned canonical resolution and receipt.
def test_c011_equal_field_candidates_coalesce_and_preserve_candidate_provenance() -> None:
    resolution = _require_module("nvda_desk.preparation.field_resolution")
    candidate = _require_attr(resolution, "FieldCandidate")
    policy_type = _require_attr(resolution, "FieldResolutionPolicy")
    resolve = _require_attr(resolution, "resolve_canonical_field")
    receipt = resolve(
        candidates=(
            candidate(
                candidate_id="market-spot",
                source_owner="market",
                semantic_field="spot_price",
                value=101.0,
                source_artifact_id="market-capture",
            ),
            candidate(
                candidate_id="options-spot",
                source_owner="options",
                semantic_field="spot_price",
                value=101.0,
                source_artifact_id="options-capture",
            ),
        ),
        policy=policy_type(
            policy_id="spot-v1",
            semantic_field="spot_price",
            mandatory=True,
        ),
    )
    assert receipt.selected_value == 101.0
    assert set(receipt.candidate_ids) == {"market-spot", "options-spot"}
    assert receipt.resolution_reason == "semantically_equal_coalesced"


def test_c011_unequal_mandatory_candidates_without_field_policy_fail_closed() -> None:
    resolution = _require_module("nvda_desk.preparation.field_resolution")
    candidate = _require_attr(resolution, "FieldCandidate")
    policy_type = _require_attr(resolution, "FieldResolutionPolicy")
    conflict = _require_attr(resolution, "MandatoryFieldConflictError")
    resolve = _require_attr(resolution, "resolve_canonical_field")
    with pytest.raises(conflict):
        resolve(
            candidates=(
                candidate(
                    candidate_id="market-spot",
                    source_owner="market",
                    semantic_field="spot_price",
                    value=100.0,
                    source_artifact_id="market-capture",
                ),
                candidate(
                    candidate_id="options-spot",
                    source_owner="options",
                    semantic_field="spot_price",
                    value=101.0,
                    source_artifact_id="options-capture",
                ),
            ),
            policy=policy_type(
                policy_id="spot-v1",
                semantic_field="spot_price",
                mandatory=True,
            ),
        )


# C-013 / N-05 — one common context plus narrow stage carriers.
def test_c013_stage_bundle_allocates_one_common_context_and_narrow_references() -> None:
    stage_contracts = _require_module("nvda_desk.contracts.stage_inputs")
    options_contracts = _require_module("nvda_desk.contracts.options_flow")
    regime_contracts = _require_module("nvda_desk.contracts.regime")
    temporal_contracts = _require_module("nvda_desk.contracts.temporal")
    common = _require_attr(stage_contracts, "CommonStageContext")
    assert {
        "context_id",
        "prepared_id",
        "prepared_fingerprint",
        "input_schema_versions",
        "preparation_policy_version",
        "temporal_reference_id",
        "completeness_state",
        "resolution_receipt_ids",
    }.issubset(_field_names(common))
    assert "common_context" in _field_names(stage_contracts.StageInputBundle)
    for carrier in (
        temporal_contracts.TemporalContextInput,
        regime_contracts.MarketRegimeContextInput,
        options_contracts.OptionsFlowContextInput,
    ):
        assert "common_context_ref" in _field_names(carrier)
        assert "prepared_payload" not in _field_names(carrier)


def test_c013_stage_bundle_rejects_mismatched_common_context_reference() -> None:
    stage_contracts = _require_module("nvda_desk.contracts.stage_inputs")
    options_contracts = _require_module("nvda_desk.contracts.options_flow")
    regime_contracts = _require_module("nvda_desk.contracts.regime")
    temporal_contracts = _require_module("nvda_desk.contracts.temporal")
    common = _require_attr(stage_contracts, "CommonStageContext")
    context = common(
        context_id="context-1",
        prepared_id="prepared-1",
        prepared_fingerprint=_FINGERPRINT_A,
        input_schema_versions={"market": "v1"},
        preparation_policy_version="prepare-v1",
        temporal_reference_id="session-1",
        completeness_state="complete",
        resolution_receipt_ids=("resolution-1",),
    )
    with pytest.raises((TypeError, ValueError), match="common_context|context.*mismatch|reference"):
        stage_contracts.StageInputBundle(
            common_context=context,
            temporal=temporal_contracts.TemporalContextInput(
                common_context_ref="context-1", source_time_utc=_TIME
            ),
            regime=regime_contracts.MarketRegimeContextInput(
                common_context_ref="context-1",
                nvda_return_pct=0.1,
                nq_return_pct=0.1,
                vix_level=20.0,
            ),
            options_flow=options_contracts.OptionsFlowContextInput(
                common_context_ref="different-context",
                spot_price=101.0,
                front_dte=1,
                next_dte=5,
            ),
        )


# C-024 / N-06 — owner-declared atomic transaction and idempotency boundary.
def _transaction_contracts():
    module = _require_module("nvda_desk.persistence.transactions")
    return (
        _require_attr(module, "TransactionCommand"),
        _require_attr(module, "InMemoryTransactionBoundary"),
        _require_attr(module, "IdempotencyConflictError"),
    )


def test_c024_same_idempotency_key_and_input_returns_original_without_repeating_mutation() -> None:
    command_type, boundary_type, _ = _transaction_contracts()
    boundary = boundary_type(initial_state={"count": 0})
    command = command_type(
        command_type="position_reconciliation",
        consistency_unit_id="position-1",
        command_id="command-1",
        idempotency_key="idem-1",
        input_fingerprint=_FINGERPRINT_A,
        expected_state_version=0,
        policy_version="transaction-v1",
    )

    def mutate(state: dict[str, Any]) -> dict[str, Any]:
        state["count"] += 1
        return {"receipt_id": "receipt-1", "result_id": "result-1"}

    first = boundary.execute(command=command, mutation=mutate)
    second = boundary.execute(command=command, mutation=mutate)
    assert first.receipt_id == second.receipt_id == "receipt-1"
    assert second.duplicate_replay is True
    assert boundary.snapshot_state() == {"count": 1}
    assert len(boundary.list_receipts()) == 1


def test_c024_same_idempotency_key_with_different_input_is_conflict() -> None:
    command_type, boundary_type, conflict = _transaction_contracts()
    boundary = boundary_type(initial_state={"count": 0})
    common = dict(
        command_type="position_reconciliation",
        consistency_unit_id="position-1",
        command_id="command-1",
        idempotency_key="idem-1",
        expected_state_version=0,
        policy_version="transaction-v1",
    )
    boundary.execute(
        command=command_type(input_fingerprint=_FINGERPRINT_A, **common),
        mutation=lambda state: {"receipt_id": "receipt-1", "result_id": "result-1"},
    )
    with pytest.raises(conflict):
        boundary.execute(
            command=command_type(input_fingerprint=_FINGERPRINT_B, **common),
            mutation=lambda state: {"receipt_id": "receipt-2", "result_id": "result-2"},
        )


def test_c024_failed_mutation_rolls_back_state_and_emits_no_success_receipt() -> None:
    command_type, boundary_type, _ = _transaction_contracts()
    boundary = boundary_type(initial_state={"count": 0})
    command = command_type(
        command_type="position_reconciliation",
        consistency_unit_id="position-1",
        command_id="command-1",
        idempotency_key="idem-1",
        input_fingerprint=_FINGERPRINT_A,
        expected_state_version=0,
        policy_version="transaction-v1",
    )

    def fail_after_mutation(state: dict[str, Any]) -> dict[str, Any]:
        state["count"] = 99
        raise RuntimeError("mutation failed")

    with pytest.raises(RuntimeError, match="mutation failed"):
        boundary.execute(command=command, mutation=fail_after_mutation)
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()


# C-026 / N-07 — signal-informed stateful phase model; clock alone is insufficient.
def _phase_contracts():
    module = _require_module("nvda_desk.domain.temporal.intraday_phase")
    return (
        _require_attr(module, "IntradayPhase"),
        _require_attr(module, "IntradayPhaseEvidence"),
        _require_attr(module, "IntradayPhasePolicy"),
        _require_attr(module, "IntradayPhaseEvaluator"),
    )


def test_c026_phase_contract_has_seven_ordered_states_and_required_signal_families() -> None:
    phase, evidence, _, _ = _phase_contracts()
    assert {
        "pre_open",
        "opening_price_discovery",
        "opening_transition",
        "continuous_session",
        "closing_transition",
        "closing_auction",
        "post_close",
        "unresolved",
    }.issubset(_enum_values(phase))
    assert {
        "source_time_utc",
        "session_reference_id",
        "activity_participation_signal",
        "liquidity_signal",
        "price_discovery_signal",
        "market_structure_status",
        "evidence_fingerprint",
    }.issubset(_field_names(evidence))


def test_c026_same_clock_with_different_sustained_signals_cannot_be_forced_to_same_phase() -> None:
    _, evidence, policy_type, evaluator_type = _phase_contracts()
    policy = policy_type(policy_version="phase-v1", minimum_dwell_observations=1)
    evaluator = evaluator_type(policy=policy)
    discovery = evaluator.evaluate(
        evidence=evidence(
            evidence_id="phase-evidence-1",
            source_time_utc=_TIME,
            session_reference_id="session-1",
            activity_participation_signal="unstable_high",
            liquidity_signal="thin_widening",
            price_discovery_signal="unstable",
            market_structure_status="continuous_trading",
            evidence_fingerprint=_FINGERPRINT_A,
        ),
        prior_state=None,
    )
    settled = evaluator.evaluate(
        evidence=evidence(
            evidence_id="phase-evidence-2",
            source_time_utc=_TIME,
            session_reference_id="session-1",
            activity_participation_signal="broad_stable",
            liquidity_signal="stable",
            price_discovery_signal="settled",
            market_structure_status="continuous_trading",
            evidence_fingerprint=_FINGERPRINT_B,
        ),
        prior_state=None,
    )
    assert discovery.phase != settled.phase
    assert discovery.source_time_utc == settled.source_time_utc == _TIME


def test_c026_clock_only_input_is_explicitly_degraded_and_does_not_invent_detailed_phase() -> None:
    _, evidence, policy_type, evaluator_type = _phase_contracts()
    result = evaluator_type(
        policy=policy_type(policy_version="phase-v1", minimum_dwell_observations=1)
    ).evaluate(
        evidence=evidence(
            evidence_id="phase-evidence-clock-only",
            source_time_utc=_TIME,
            session_reference_id="session-1",
            activity_participation_signal=None,
            liquidity_signal=None,
            price_discovery_signal=None,
            market_structure_status="continuous_trading",
            evidence_fingerprint=_FINGERPRINT_A,
        ),
        prior_state=None,
    )
    assert result.phase.value == "unresolved"
    assert result.authority_state == "clock_only_degraded"


# C-036 / N-08 — two mandatory final-risk branches; hard blocks dominate.
def _final_risk_contracts():
    contracts = _require_module("nvda_desk.contracts.risk")
    join = _require_module("nvda_desk.domain.final_risk.terminal_join")
    return (
        _require_attr(contracts, "SerialFinalRiskBranch"),
        _require_attr(contracts, "ParallelRiskFinalRiskBranch"),
        _require_attr(contracts, "FinalRiskJoinPolicy"),
        _require_attr(join, "apply_terminal_join"),
    )


def _serial_branch(serial_type: Any, *, hard_blocks: tuple[str, ...] = ()):
    return serial_type(
        branch_id="serial-1",
        candidate_id="candidate-1",
        execution_expression_id="expression-1",
        semantic_fingerprint=_FINGERPRINT_A,
        permission_state="allow" if not hard_blocks else "blocked",
        hard_blocks=hard_blocks,
        cautions=(),
        policy_version="serial-risk-v1",
    )


def _parallel_branch(parallel_type: Any, *, hard_blocks: tuple[str, ...] = ()):
    return parallel_type(
        branch_id="parallel-1",
        candidate_id="candidate-1",
        packet_id="parallel-packet-1",
        semantic_fingerprint=_FINGERPRINT_B,
        hard_blocks=hard_blocks,
        cautions=(),
        evidence_limitations=(),
        policy_version="parallel-risk-v1",
    )


def test_c036_two_complete_clear_branches_emit_only_capital_assessment_eligibility() -> None:
    serial_type, parallel_type, policy_type, join = _final_risk_contracts()
    receipt = join(
        serial_branch=_serial_branch(serial_type),
        parallel_branch=_parallel_branch(parallel_type),
        policy=policy_type(policy_version="final-join-v1"),
        receipt_id="final-join-1",
    )
    assert receipt.action == "eligible_for_capital_assessment"
    assert receipt.capital_authority_granted is False
    assert receipt.execution_authority_granted is False


def test_c036_any_parallel_or_serial_hard_block_forces_stand_down_and_is_retained() -> None:
    serial_type, parallel_type, policy_type, join = _final_risk_contracts()
    receipt = join(
        serial_branch=_serial_branch(serial_type),
        parallel_branch=_parallel_branch(parallel_type, hard_blocks=("liquidity_hard_block",)),
        policy=policy_type(policy_version="final-join-v1"),
        receipt_id="final-join-1",
    )
    assert receipt.action == "stand_down"
    assert "liquidity_hard_block" in receipt.hard_blocks


def test_c036_missing_branch_cannot_be_reconstructed_or_converted_by_confidence() -> None:
    serial_type, _, policy_type, join = _final_risk_contracts()
    receipt = join(
        serial_branch=_serial_branch(serial_type),
        parallel_branch=None,
        policy=policy_type(policy_version="final-join-v1"),
        receipt_id="final-join-1",
    )
    assert receipt.action == "stand_down"
    assert "missing_parallel_risk_authority" in receipt.missing_authority_reasons
    assert not hasattr(receipt, "confidence_scalar")


# C-046 / N-09 — verified replay envelope and comparison-only subordination.
def test_c046_authoritative_replay_contract_carries_complete_logical_envelope_and_classes() -> None:
    contracts = _require_module("nvda_desk.contracts.replay")
    replay_class = _require_attr(contracts, "ReplayClass")
    authority_status = _require_attr(contracts, "ReplayAuthorityStatus")
    envelope = _require_attr(contracts, "AuthoritativeReplayEnvelope")
    assert _enum_values(replay_class) == {
        "preserved_occurrence_replay",
        "governed_semantic_reexecution",
        "comparison_only",
    }
    assert "non_authoritative_incomplete" in _enum_values(authority_status)
    assert {
        "replay_envelope_id",
        "replay_run_id",
        "replay_class",
        "target_identity",
        "source_artifacts",
        "dataset_identity",
        "contract_versions",
        "policy_versions",
        "executable_meaning",
        "ordered_state_and_receipt_refs",
        "original_output_identity",
        "original_semantic_fingerprint",
    }.issubset(_field_names(envelope))


def test_c046_missing_executable_or_artifact_authority_is_non_authoritative_incomplete() -> None:
    contracts = _require_module("nvda_desk.contracts.replay")
    service_module = _require_module("nvda_desk.analysis.replay.service")
    replay_class = _require_attr(contracts, "ReplayClass")
    envelope_type = _require_attr(contracts, "AuthoritativeReplayEnvelope")
    service_type = _require_attr(service_module, "AuthoritativeReplayService")
    envelope = envelope_type(
        replay_envelope_id="replay-envelope-1",
        replay_run_id="replay-run-1",
        replay_class=replay_class.GOVERNED_SEMANTIC_REEXECUTION,
        target_identity="decision-1",
        source_artifacts=(),
        dataset_identity=None,
        contract_versions={"decision": "v1"},
        policy_versions={"decision": "v1"},
        executable_meaning=None,
        ordered_state_and_receipt_refs=(),
        original_output_identity="output-1",
        original_semantic_fingerprint=_FINGERPRINT_A,
        missing_authority=("source_artifacts", "executable_meaning"),
    )
    assessment = service_type().assess(envelope)
    assert assessment.authority_status.value == "non_authoritative_incomplete"
    assert set(assessment.missing_authority) == {"source_artifacts", "executable_meaning"}
    assert assessment.reconstruction_claimed is False


def test_c046_mapping_comparison_remains_comparison_only_and_cannot_claim_reconstruction() -> None:
    service_module = _require_module("nvda_desk.analysis.replay.service")
    comparison = service_module.ReplayEvaluationService().compare_outputs(
        baseline={"decision_id": "decision-1", "action": "stand_down"},
        candidate={"decision_id": "decision-1", "action": "stand_down"},
    )
    assert comparison.replay_class == "comparison_only"
    assert comparison.authority_status == "non_authoritative_comparison"
    assert comparison.reconstruction_claimed is False
    assert comparison.runtime_authority_promoted is False
