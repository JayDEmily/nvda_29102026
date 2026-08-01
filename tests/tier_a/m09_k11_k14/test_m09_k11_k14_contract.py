"""M09 K11/K14 proof for final-risk join and bounded fresh-capital authority."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from tests.support.m09_k11_k14_contract_harness import (
    CAPITAL_POLICY_VERSION,
    JOIN_POLICY_VERSION,
    MUTANTS,
    CapitalPolicy,
    CapitalStateCase,
    JoinPolicy,
    ModifierReceipt,
    ParallelBranch,
    SerialBranch,
    evaluate_reference,
    production_api,
    production_modifier_receipt,
    production_parallel_assessment,
    production_serial_candidate,
    validate_result_law,
)


def test_reference_clear_branches_authorise_bounded_target() -> None:
    serial, parallel = SerialBranch(), ParallelBranch()
    result = evaluate_reference(serial, parallel, ModifierReceipt(), CapitalStateCase())
    validate_result_law(result, serial, parallel, ModifierReceipt(), CapitalStateCase())
    assert result.final_action == "eligible_for_capital_assessment"
    assert result.capital_action == "continue"
    assert result.authorised_pct == Decimal("10.00")
    assert result.authorised_notional == Decimal("10000.00")


def test_reference_hard_block_unknown_and_missing_branch_fail_closed() -> None:
    for parallel in (
        replace(ParallelBranch(), state="block", hard_blocks=("event_halt",)),
        replace(ParallelBranch(), state="unknown", unknowns=("volatility",)),
        None,
    ):
        result = evaluate_reference(SerialBranch(), parallel, ModifierReceipt(), CapitalStateCase())
        assert result.final_action == "stand_down"
        assert result.capital_action == "block"
        assert result.authorised_pct == 0


def test_reference_prepared_lineage_must_match_exactly() -> None:
    parallel = replace(ParallelBranch(), prepared_id="prepared.other")
    result = evaluate_reference(SerialBranch(), parallel, ModifierReceipt(), CapitalStateCase())
    assert result.final_action == "stand_down"
    assert "prepared_lineage_conflict" in result.reasons


def test_reference_caution_reduces_only_by_explicit_policy() -> None:
    parallel = replace(ParallelBranch(), state="caution", cautions=("elevated_volatility",))
    result = evaluate_reference(SerialBranch(), parallel, ModifierReceipt(), CapitalStateCase())
    assert result.final_action == "eligible_for_capital_assessment"
    assert result.capital_action == "reduce"
    assert result.authorised_pct == Decimal("5.00")


def test_reference_hard_max_and_capital_state_max_both_bind() -> None:
    policy = CapitalPolicy(target_pct=Decimal("20"), hard_max_pct=Decimal("12"))
    capital = CapitalStateCase(max_fresh_deployable_pct=Decimal("8"))
    result = evaluate_reference(SerialBranch(), ParallelBranch(), ModifierReceipt(), capital, capital_policy=policy)
    assert result.authorised_pct == Decimal("8.00")
    assert result.capital_action == "reduce"


def test_reference_m07_kill_switch_blocks_but_posture_scale_does_not_size() -> None:
    blocked = evaluate_reference(
        SerialBranch(), ParallelBranch(), replace(ModifierReceipt(), kill_switches=("hard_kill",)), CapitalStateCase()
    )
    clear = evaluate_reference(
        SerialBranch(), ParallelBranch(), replace(ModifierReceipt(), posture_scale=Decimal("0.01")), CapitalStateCase()
    )
    assert blocked.capital_action == "block"
    assert clear.authorised_pct == Decimal("10.00")


def test_reference_zero_available_capital_is_no_trade_with_zero_authority() -> None:
    result = evaluate_reference(
        SerialBranch(), ParallelBranch(), ModifierReceipt(),
        CapitalStateCase(available_capital=Decimal("0")),
    )
    assert result.capital_action == "no_trade"
    assert result.authorised_pct == 0
    assert result.authorised_notional == 0


def test_reference_invalid_capital_state_and_policy_domains_fail_closed() -> None:
    invalid_states = (
        CapitalStateCase(reserved_capital=Decimal("-1")),
        CapitalStateCase(max_fresh_deployable_pct=Decimal("101")),
    )
    for capital in invalid_states:
        result = evaluate_reference(SerialBranch(), ParallelBranch(), ModifierReceipt(), capital)
        assert result.capital_action == "block"
        assert "invalid_capital_state" in result.reasons

    invalid_policies = (
        CapitalPolicy(target_pct=Decimal("101"), hard_max_pct=Decimal("100")),
        CapitalPolicy(caution_multiplier=Decimal("1.01")),
        CapitalPolicy(caution_multiplier=Decimal("-0.01")),
    )
    for policy in invalid_policies:
        result = evaluate_reference(
            SerialBranch(),
            replace(ParallelBranch(), state="caution", cautions=("caution",)),
            ModifierReceipt(),
            CapitalStateCase(),
            capital_policy=policy,
        )
        assert result.capital_action == "block"
        assert "invalid_or_unsupported_capital_policy" in result.reasons


def test_reference_semantic_identity_ignores_emission_time() -> None:
    args = (SerialBranch(), ParallelBranch(), ModifierReceipt(), CapitalStateCase())
    first = evaluate_reference(*args, emitted_at_utc=datetime(2026, 8, 1, 1, tzinfo=UTC))
    second = evaluate_reference(*args, emitted_at_utc=datetime(2026, 8, 2, 1, tzinfo=UTC))
    assert first == second


@pytest.mark.parametrize("mutant_name", sorted(MUTANTS))
def test_each_false_positive_mutant_is_killed(mutant_name: str) -> None:
    serial = SerialBranch()
    parallel = ParallelBranch()
    modifier = ModifierReceipt()
    capital = CapitalStateCase()
    join_policy = JoinPolicy()
    capital_policy = CapitalPolicy()
    if mutant_name == "missing_branch_pass":
        parallel = None
    elif mutant_name == "confidence_overrides_block":
        parallel = replace(parallel, state="block", hard_blocks=("hard",))
    elif mutant_name == "lineage_mismatch_pass":
        parallel = replace(parallel, prepared_fingerprint="f" * 64)
    elif mutant_name == "ignores_hard_maximum":
        capital_policy = replace(capital_policy, target_pct=Decimal("20"), hard_max_pct=Decimal("5"))
    elif mutant_name == "accepts_future_policy":
        join_policy = replace(join_policy, version="m09.future.join.v999")
        capital_policy = replace(capital_policy, version="m09.future.capital.v999")

    result = MUTANTS[mutant_name](serial, parallel, modifier, capital, join_policy, capital_policy)
    with pytest.raises(ValueError, match="m09_reference_law_mismatch"):
        validate_result_law(result, serial, parallel, modifier, capital, join_policy, capital_policy)


# Production-facing assertions below are intentionally exact red at C-PROOF until
# the canonical nvda_desk.m09_capital_authority package exists.


def _production_inputs():
    api = production_api()
    parallel = production_parallel_assessment(vix_level=20.0)
    serial = production_serial_candidate(
        prepared_id=parallel.prepared_id,
        prepared_fingerprint=parallel.prepared_fingerprint,
    )
    modifier = production_modifier_receipt()
    join_policy = api["FinalRiskJoinPolicy"](policy_version=JOIN_POLICY_VERSION, cautions_prohibit=False)
    capital_policy = api["CapitalDeploymentPolicy"](
        policy_version=CAPITAL_POLICY_VERSION,
        target_pct=Decimal("10"),
        hard_max_pct=Decimal("15"),
        caution_multiplier=Decimal("0.5"),
        rounding_quantum=Decimal("0.01"),
    )
    capital = api["CapitalState"].create(
        state_id="capital.state.001",
        account_id="account.001",
        state_version=1,
        effective_at_utc=datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
        available_capital=Decimal("100000"),
        reserved_capital=Decimal("10000"),
        max_fresh_deployable_pct=Decimal("12"),
        source_authority_ref="capital.snapshot.authority.v1",
    )
    return api, serial, parallel, modifier, join_policy, capital_policy, capital


def test_production_exports_frozen_contracts_and_owner_service() -> None:
    api = production_api()
    for name in ("FinalRiskDecision", "CapitalState", "CapitalDeploymentDecision", "CapitalDeploymentReceipt"):
        assert api[name].model_config.get("frozen") is True
        assert api[name].model_config.get("extra") == "forbid"
    assert api["CapitalAuthorityService"]


def test_production_k11_joins_exact_owner_products() -> None:
    api, serial, parallel, _, join_policy, _, _ = _production_inputs()
    result = api["CapitalAuthorityService"]().join_final_risk(serial, parallel, join_policy)
    assert isinstance(result, api["FinalRiskDecision"])
    assert result.action == "eligible_for_capital_assessment"
    assert result.serial_candidate_id == serial.candidate_id
    assert result.parallel_assessment_id == parallel.assessment_id
    assert result.capital_authority_granted is False
    assert result.execution_authority_granted is False


def test_production_k11_fail_closed_on_block_and_lineage_conflict() -> None:
    api, serial, parallel, _, join_policy, _, _ = _production_inputs()
    blocked = production_parallel_assessment(vix_level=55.0)
    blocked_serial = production_serial_candidate(
        prepared_id=blocked.prepared_id,
        prepared_fingerprint=blocked.prepared_fingerprint,
    )
    result = api["CapitalAuthorityService"]().join_final_risk(blocked_serial, blocked, join_policy)
    assert result.action == "stand_down"
    forged = parallel.model_copy(update={"prepared_id": "prepared.other"})
    with pytest.raises(ValueError, match="parallel_risk_assessment_contract_invalid"):
        api["CapitalAuthorityService"]().join_final_risk(serial, forged, join_policy)


def test_production_k14_is_bounded_and_does_not_use_m07_coefficient_as_percentage() -> None:
    api, serial, parallel, modifier, join_policy, capital_policy, capital = _production_inputs()
    service = api["CapitalAuthorityService"]()
    final = service.join_final_risk(serial, parallel, join_policy)
    decision = service.evaluate_capital(final, capital, modifier, capital_policy)
    assert isinstance(decision, api["CapitalDeploymentDecision"])
    assert decision.action == "continue"
    assert decision.authorised_pct == Decimal("10.00")
    assert decision.authorised_notional == Decimal("10000.00")
    assert decision.placement_authority_granted is False
    zero_capital = api["CapitalState"].create(
        state_id="capital.state.zero",
        account_id="account.001",
        state_version=2,
        effective_at_utc=datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
        available_capital=Decimal("0"),
        reserved_capital=Decimal("0"),
        max_fresh_deployable_pct=Decimal("12"),
        source_authority_ref="capital.snapshot.authority.v1",
    )
    zero = service.evaluate_capital(final, zero_capital, modifier, capital_policy)
    assert zero.action == "no_trade"
    assert zero.authorised_pct == 0
    assert zero.authorised_notional == 0


def test_production_k14_kill_switch_and_ineligible_join_zero_authority() -> None:
    api, serial, parallel, _, join_policy, capital_policy, capital = _production_inputs()
    service = api["CapitalAuthorityService"]()
    final = service.join_final_risk(serial, parallel, join_policy)
    killed = service.evaluate_capital(final, capital, production_modifier_receipt(kill_switch=True), capital_policy)
    assert killed.action == "block"
    assert killed.authorised_pct == 0
    blocked_parallel = production_parallel_assessment(vix_level=55.0)
    blocked_serial = production_serial_candidate(
        prepared_id=blocked_parallel.prepared_id,
        prepared_fingerprint=blocked_parallel.prepared_fingerprint,
    )
    blocked_final = service.join_final_risk(blocked_serial, blocked_parallel, join_policy)
    blocked = service.evaluate_capital(blocked_final, capital, production_modifier_receipt(), capital_policy)
    assert blocked.action == "block"
    assert blocked.authorised_notional == 0


def test_production_receipt_is_deterministic_and_complete() -> None:
    api, serial, parallel, modifier, join_policy, capital_policy, capital = _production_inputs()
    service = api["CapitalAuthorityService"]()
    final = service.join_final_risk(serial, parallel, join_policy)
    decision = service.evaluate_capital(final, capital, modifier, capital_policy)
    first = service.build_receipt(decision, final, capital, modifier, capital_policy, emitted_at_utc=datetime(2026, 8, 1, 1, tzinfo=UTC))
    second = service.build_receipt(decision, final, capital, modifier, capital_policy, emitted_at_utc=datetime(2026, 8, 2, 1, tzinfo=UTC))
    assert isinstance(first, api["CapitalDeploymentReceipt"])
    assert first.receipt_id == second.receipt_id
    assert first.decision_fingerprint == decision.semantic_fingerprint
    assert first.durable_commit_proven is False
    assert first.broker_authority_granted is False


def test_production_rejects_unsupported_policy_versions_and_forged_copies() -> None:
    api, serial, parallel, modifier, join_policy, capital_policy, capital = _production_inputs()
    service = api["CapitalAuthorityService"]()
    with pytest.raises(ValueError, match="unsupported_final_risk_join_policy"):
        service.join_final_risk(serial, parallel, join_policy.model_copy(update={"policy_version": "m09.future.v999"}))
    final = service.join_final_risk(serial, parallel, join_policy)
    with pytest.raises(ValueError, match="unsupported_capital_policy"):
        service.evaluate_capital(final, capital, modifier, capital_policy.model_copy(update={"policy_version": "m09.future.v999"}))
    forged = capital.model_copy(update={"available_capital": Decimal("999999")})
    with pytest.raises(ValueError, match="capital_state_contract_invalid"):
        service.evaluate_capital(final, forged, modifier, capital_policy)
    with pytest.raises(ValueError):
        api["CapitalState"].create(
            state_id="capital.invalid", account_id="account.001", state_version=1,
            effective_at_utc=datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
            available_capital=Decimal("100"), reserved_capital=Decimal("-1"),
            max_fresh_deployable_pct=Decimal("10"), source_authority_ref="authority.v1",
        )
    with pytest.raises(ValueError):
        api["CapitalDeploymentPolicy"](
            policy_version=CAPITAL_POLICY_VERSION, target_pct=Decimal("10"),
            hard_max_pct=Decimal("15"), caution_multiplier=Decimal("1.01"),
            rounding_quantum=Decimal("0.01"),
        )


def _refingerprint_final(api, payload: dict):
    from nvda_desk.m09_capital_authority.contracts import semantic_fingerprint

    material = dict(payload)
    material.pop("final_decision_id", None)
    material.pop("semantic_fingerprint", None)
    fp = semantic_fingerprint(material)
    return api["FinalRiskDecision"].model_validate(
        {**material, "final_decision_id": f"final-risk.{fp[:20]}", "semantic_fingerprint": fp}
    )


def _refingerprint_capital_decision(api, payload: dict):
    from nvda_desk.m09_capital_authority.contracts import semantic_fingerprint

    material = dict(payload)
    material.pop("decision_id", None)
    material.pop("semantic_fingerprint", None)
    fp = semantic_fingerprint(material)
    return api["CapitalDeploymentDecision"].model_validate(
        {**material, "decision_id": f"capital-decision.{fp[:20]}", "semantic_fingerprint": fp}
    )


def test_production_policy_values_are_bound_into_semantic_identity() -> None:
    api, _, _, modifier, _, capital_policy, capital = _production_inputs()
    caution_parallel = production_parallel_assessment(vix_level=35.0)
    caution_serial = production_serial_candidate(
        prepared_id=caution_parallel.prepared_id,
        prepared_fingerprint=caution_parallel.prepared_fingerprint,
    )
    service = api["CapitalAuthorityService"]()
    permissive = api["FinalRiskJoinPolicy"](
        policy_version=JOIN_POLICY_VERSION,
        cautions_prohibit=False,
    )
    prohibiting = api["FinalRiskJoinPolicy"](
        policy_version=JOIN_POLICY_VERSION,
        cautions_prohibit=True,
    )
    eligible = service.join_final_risk(caution_serial, caution_parallel, permissive)
    blocked = service.join_final_risk(caution_serial, caution_parallel, prohibiting)
    assert eligible.action == "eligible_for_capital_assessment"
    assert blocked.action == "stand_down"
    assert eligible.join_policy_fingerprint != blocked.join_policy_fingerprint
    assert eligible.final_decision_id != blocked.final_decision_id

    reduced = service.evaluate_capital(eligible, capital, modifier, capital_policy)
    altered_policy = api["CapitalDeploymentPolicy"](
        policy_version=CAPITAL_POLICY_VERSION,
        target_pct=Decimal("10"),
        hard_max_pct=Decimal("15"),
        caution_multiplier=Decimal("0.25"),
        rounding_quantum=Decimal("0.01"),
    )
    more_reduced = service.evaluate_capital(eligible, capital, modifier, altered_policy)
    assert reduced.authorised_pct == Decimal("5.00")
    assert more_reduced.authorised_pct == Decimal("2.50")
    assert reduced.capital_policy_fingerprint != more_reduced.capital_policy_fingerprint
    assert reduced.decision_id != more_reduced.decision_id


def test_production_final_decision_rejects_contradictory_parallel_state() -> None:
    api, serial, parallel, _, join_policy, _, _ = _production_inputs()
    final = api["CapitalAuthorityService"]().join_final_risk(serial, parallel, join_policy)
    forged = final.model_dump(mode="python")
    forged["parallel_state"] = "block"
    with pytest.raises(ValueError, match="parallel_block_state_requires_hard_block"):
        _refingerprint_final(api, forged)


def test_production_receipt_recomputes_decision_against_exact_inputs() -> None:
    api, serial, parallel, modifier, join_policy, capital_policy, capital = _production_inputs()
    service = api["CapitalAuthorityService"]()
    final = service.join_final_risk(serial, parallel, join_policy)
    decision = service.evaluate_capital(final, capital, modifier, capital_policy)
    forged_payload = decision.model_dump(mode="python")
    forged_payload.update(
        {
            "action": "reduce",
            "authorised_pct": Decimal("9.00"),
            "authorised_notional": Decimal("9000.00"),
            "reasons": ("forged_but_fingerprinted",),
        }
    )
    forged = _refingerprint_capital_decision(api, forged_payload)
    with pytest.raises(ValueError, match="capital_receipt_decision_input_mismatch"):
        service.build_receipt(
            forged,
            final,
            capital,
            modifier,
            capital_policy,
            emitted_at_utc=datetime(2026, 8, 1, 1, tzinfo=UTC),
        )


def test_production_receipt_preserves_exact_branch_and_policy_lineage() -> None:
    api, serial, parallel, modifier, join_policy, capital_policy, capital = _production_inputs()
    service = api["CapitalAuthorityService"]()
    final = service.join_final_risk(serial, parallel, join_policy)
    decision = service.evaluate_capital(final, capital, modifier, capital_policy)
    receipt = service.build_receipt(
        decision,
        final,
        capital,
        modifier,
        capital_policy,
        emitted_at_utc=datetime(2026, 8, 1, 1, tzinfo=UTC),
    )
    assert receipt.serial_result_id == serial.serial_result_id
    assert receipt.serial_candidate_id == serial.candidate_id
    assert receipt.serial_candidate_fingerprint == serial.semantic_fingerprint
    assert receipt.parallel_assessment_id == parallel.assessment_id
    assert receipt.parallel_assessment_fingerprint == parallel.semantic_fingerprint
    assert receipt.capital_policy_fingerprint == capital_policy.policy_fingerprint
    assert receipt.execution_authority_granted is False


def test_production_revalidates_forged_final_and_decision_copies() -> None:
    api, serial, parallel, modifier, join_policy, capital_policy, capital = _production_inputs()
    service = api["CapitalAuthorityService"]()
    final = service.join_final_risk(serial, parallel, join_policy)
    forged_final = final.model_copy(update={"action": "stand_down"})
    with pytest.raises(ValueError, match="final_risk_decision_contract_invalid"):
        service.evaluate_capital(forged_final, capital, modifier, capital_policy)

    decision = service.evaluate_capital(final, capital, modifier, capital_policy)
    forged_decision = decision.model_copy(update={"authorised_notional": Decimal("1")})
    with pytest.raises(ValueError, match="capital_deployment_decision_contract_invalid"):
        service.build_receipt(
            forged_decision,
            final,
            capital,
            modifier,
            capital_policy,
            emitted_at_utc=datetime(2026, 8, 1, 1, tzinfo=UTC),
        )
