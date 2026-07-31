"""Minimum truthful public-seam proof for M07 K12 coefficient/modifier authority."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal

import pytest

from tests.support.m07_k12_contract_harness import (
    CLOSED_AUTHORITIES,
    MUTANTS,
    ModifierCase,
    ReferenceSubject,
    conflict_bundle,
    production_api,
    valid_bundle,
    valid_facts,
)


def _result(decision, coefficient_id: str = "posture.exposure_scale"):
    return next(
        item for item in decision.coefficient_results if item.coefficient_id == coefficient_id
    )


def test_reference_distinguishes_missing_bundle_from_valid_no_modifier_bundle() -> None:
    facts = valid_facts()
    rejected = ReferenceSubject().resolve(None, facts)
    no_op = ReferenceSubject().resolve(valid_bundle(modifiers=()), facts)

    assert rejected.status == "rejected"
    assert rejected.reason == "bundle_authority_missing"
    assert rejected.semantic_fingerprint is None
    assert ReferenceSubject.build_receipt(
        rejected,
        receipt_id="receipt-rejected",
        application_id="application-rejected",
        emitted_at_utc=datetime(2026, 7, 31, 3, 1, tzinfo=UTC),
    ) is None

    assert no_op.status == "no_modifier_members"
    assert _result(no_op).effective == Decimal("0.60")
    receipt = ReferenceSubject.build_receipt(
        no_op,
        receipt_id="receipt-no-op",
        application_id="application-no-op",
        emitted_at_utc=datetime(2026, 7, 31, 3, 1, tzinfo=UTC),
    )
    assert receipt is not None
    assert receipt.no_op_class == "no_modifier_members"


def test_reference_preserves_valid_no_applicable_modifiers_as_distinct_no_op() -> None:
    decision = ReferenceSubject().resolve(
        valid_bundle(),
        valid_facts(facts={"stress": False, "volatility": False, "kill": False}),
    )

    assert decision.status == "no_applicable_modifiers"
    assert decision.applied_modifiers == ()
    assert decision.skipped_modifiers == (
        ("stress_add", "not_applicable"),
        ("volatility_multiply", "not_applicable"),
    )
    assert _result(decision).effective == Decimal("0.60")


def test_reference_uses_authority_precedence_then_clamps_after_algebra() -> None:
    bundle = valid_bundle()
    decision = ReferenceSubject().resolve(
        bundle,
        valid_facts(),
        caller_modifier_order=("volatility_multiply", "stress_add"),
    )

    assert decision.status == "applied"
    assert decision.applied_modifiers == ("stress_add", "volatility_multiply")
    result = _result(decision)
    assert result.pre_clamp_candidate == Decimal("2.20")
    assert result.effective == Decimal("1.00")
    assert result.bound_disposition == "clamped_upper"


def test_reference_fails_closed_on_missing_fact_and_unresolved_conflict() -> None:
    missing_fact = ReferenceSubject().resolve(
        valid_bundle(),
        valid_facts(facts={"stress": True}),
    )
    conflict = ReferenceSubject().resolve(conflict_bundle(), valid_facts())

    assert missing_fact.status == "rejected"
    assert missing_fact.reason == "missing_applicability_fact"
    assert conflict.status == "rejected"
    assert conflict.reason == "unresolved_modifier_conflict"


def test_reference_hard_kill_dominates_weaker_effects() -> None:
    kill = ModifierCase(
        modifier_id="hard_kill",
        modifier_version="1.0.0",
        target="posture.exposure_scale",
        fact_ref="kill",
        precedence=100,
        operator="set",
        operand=Decimal("0"),
        kill_switch=True,
    )
    bundle = valid_bundle(modifiers=(*valid_bundle().modifiers, kill))
    facts = valid_facts(facts={"stress": True, "volatility": True, "kill": True})

    decision = ReferenceSubject().resolve(bundle, facts)

    assert decision.status == "applied"
    assert decision.applied_modifiers == ("hard_kill",)
    assert decision.skipped_modifiers == (
        ("stress_add", "dominated_by_kill_switch"),
        ("volatility_multiply", "dominated_by_kill_switch"),
    )
    assert _result(decision).effective == Decimal("0")


def test_reference_fingerprint_is_deterministic_and_receipt_cannot_claim_foreign_effects() -> None:
    subject = ReferenceSubject()
    decision_a = subject.resolve(valid_bundle(), valid_facts())
    decision_b = subject.resolve(valid_bundle(), valid_facts())
    receipt_a = subject.build_receipt(
        decision_a,
        receipt_id="receipt-a",
        application_id="application-a",
        emitted_at_utc=datetime(2026, 7, 31, 3, 1, tzinfo=UTC),
    )
    receipt_b = subject.build_receipt(
        decision_b,
        receipt_id="receipt-b",
        application_id="application-b",
        emitted_at_utc=datetime(2026, 7, 31, 3, 2, tzinfo=UTC),
    )

    assert decision_a.semantic_fingerprint == decision_b.semantic_fingerprint
    assert receipt_a is not None and receipt_b is not None
    assert receipt_a.source_decision_fingerprint == receipt_b.source_decision_fingerprint
    assert receipt_a.external_mutation_proven is False
    assert receipt_a.closed_authority_classes == CLOSED_AUTHORITIES


@pytest.mark.parametrize("mutant_name", tuple(MUTANTS))
def test_each_false_positive_mutant_is_killed(mutant_name: str) -> None:
    subject = MUTANTS[mutant_name]()
    facts = valid_facts()

    if mutant_name == "caller_order":
        reference = ReferenceSubject().resolve(
            valid_bundle(),
            facts,
            caller_modifier_order=("volatility_multiply", "stress_add"),
        )
        mutant = subject.resolve(
            valid_bundle(),
            facts,
            caller_modifier_order=("volatility_multiply", "stress_add"),
        )
        assert _result(reference).pre_clamp_candidate == Decimal("2.20")
        assert _result(mutant).pre_clamp_candidate != Decimal("2.20")
    elif mutant_name == "missing_bundle_as_empty":
        reference = ReferenceSubject().resolve(None, facts)
        mutant = subject.resolve(None, facts)
        assert reference.status == "rejected"
        assert mutant.status != "rejected"
    elif mutant_name == "clamp_before_algebra":
        reference = ReferenceSubject().resolve(valid_bundle(), facts)
        mutant = subject.resolve(valid_bundle(), facts)
        assert _result(reference).pre_clamp_candidate == Decimal("2.20")
        assert _result(mutant).pre_clamp_candidate != Decimal("2.20")
    elif mutant_name == "arbitrary_conflict_tie":
        reference = ReferenceSubject().resolve(conflict_bundle(), facts)
        mutant = subject.resolve(conflict_bundle(), facts)
        assert reference.reason == "unresolved_modifier_conflict"
        assert mutant.status == "applied"
    else:
        decision = ReferenceSubject().resolve(valid_bundle(), facts)
        reference_receipt = ReferenceSubject.build_receipt(
            decision,
            receipt_id="receipt-reference",
            application_id="application-reference",
            emitted_at_utc=datetime(2026, 7, 31, 3, 1, tzinfo=UTC),
        )
        mutant_receipt = subject.build_receipt(
            decision,
            receipt_id="receipt-mutant",
            application_id="application-mutant",
            emitted_at_utc=datetime(2026, 7, 31, 3, 1, tzinfo=UTC),
        )
        assert reference_receipt is not None and mutant_receipt is not None
        assert reference_receipt.external_mutation_proven is False
        assert mutant_receipt.external_mutation_proven is True


def _production_payloads():
    api = production_api()
    bundle = api["PolicyBundle"].model_validate(
        {
            "bundle_id": "m07.posture.coefficients",
            "bundle_version": "2026.07.31.1",
            "schema_version": "1.0.0",
            "authority_id": "m07.k12",
            "authority_version": "1.0.0",
            "effective_version_selector": "promoted:2026.07.31.1",
            "resolution_law_version": "k12.v1",
            "promotion_lineage": "workbook://coefficient-authority/2026.07.31.1",
            "owner_stage": "posture",
            "coefficients": [
                {
                    "coefficient_id": "posture.exposure_scale",
                    "coefficient_version": "1.0.0",
                    "owner_stage": "posture",
                    "value_type": "decimal",
                    "units": "ratio",
                    "baseline_value": "0.60",
                    "hard_lower_bound": "0.00",
                    "hard_upper_bound": "1.00",
                    "surface_class": "mutable_runtime_surface",
                    "transform_family": "bounded_decimal_algebra",
                    "runtime_mutability_class": "runtime_mutable",
                    "promotion_lineage": "workbook://posture.exposure_scale/1.0.0",
                }
            ],
            "modifiers": [
                {
                    "modifier_id": "stress_add",
                    "modifier_version": "1.0.0",
                    "owner_stage": "posture",
                    "target_coefficient_ids": ["posture.exposure_scale"],
                    "applicability_fact_refs": ["stress"],
                    "precedence_rank": 10,
                    "transform_operator": "add",
                    "operand": "0.50",
                    "combination_law": "authority_ordered",
                    "conflict_modifier_ids": [],
                    "veto_modifier_ids": [],
                    "kill_switch": False,
                    "restrictive_only": False,
                    "promotion_lineage": "workbook://stress_add/1.0.0",
                },
                {
                    "modifier_id": "volatility_multiply",
                    "modifier_version": "1.0.0",
                    "owner_stage": "posture",
                    "target_coefficient_ids": ["posture.exposure_scale"],
                    "applicability_fact_refs": ["volatility"],
                    "precedence_rank": 20,
                    "transform_operator": "multiply",
                    "operand": "2.00",
                    "combination_law": "authority_ordered",
                    "conflict_modifier_ids": [],
                    "veto_modifier_ids": [],
                    "kill_switch": False,
                    "restrictive_only": False,
                    "promotion_lineage": "workbook://volatility_multiply/1.0.0",
                },
            ],
        }
    )
    input_state = {
        "context_id": "state::posture::20260731T030000Z",
        "context_version": "1.0.0",
        "effective_at_utc": datetime(2026, 7, 31, 3, 0, tzinfo=UTC),
        "fingerprint": "facts-sha256-001",
        "facts": {"stress": True, "volatility": True},
    }
    return api, bundle, input_state


def test_production_public_api_exposes_exact_k12_contracts() -> None:
    api = production_api()

    assert api["PolicyBundle"].__name__ == "PolicyBundle"
    assert api["ModifierDecision"].__name__ == "ModifierDecision"
    assert api["ModifierApplicationReceipt"].__name__ == "ModifierApplicationReceipt"


def test_production_public_seam_distinguishes_missing_bundle_and_valid_no_op() -> None:
    api, bundle, input_state = _production_payloads()
    missing = api["resolve_k12"](
        bundle=None,
        owner_stage="posture",
        input_state=input_state,
    )
    no_op = api["resolve_k12"](
        bundle=bundle.model_copy(update={"modifiers": ()}),
        owner_stage="posture",
        input_state=input_state,
    )

    assert isinstance(missing, api["ModifierDecision"])
    assert missing.status == "rejected"
    assert missing.rejection_reasons == ("bundle_authority_missing",)
    assert api["build_k12_receipt"](
        decision=missing,
        receipt_id="receipt-rejected",
        application_id="application-rejected",
        emitted_at_utc=datetime(2026, 7, 31, 3, 1, tzinfo=UTC),
    ) is None

    assert no_op.status == "no_modifier_members"
    assert no_op.coefficient_results[0].effective_value == Decimal("0.60")


def test_production_public_seam_applies_authority_order_and_post_algebra_bounds() -> None:
    api, bundle, input_state = _production_payloads()
    reversed_bundle = bundle.model_copy(update={"modifiers": tuple(reversed(bundle.modifiers))})
    decision = api["resolve_k12"](
        bundle=reversed_bundle,
        owner_stage="posture",
        input_state=input_state,
    )

    assert isinstance(decision, api["ModifierDecision"])
    assert decision.status == "applied"
    assert tuple(item.modifier_id for item in decision.applied_modifiers) == (
        "stress_add",
        "volatility_multiply",
    )
    result = decision.coefficient_results[0]
    assert result.pre_clamp_candidate == Decimal("2.20")
    assert result.effective_value == Decimal("1.00")
    assert result.bound_disposition == "clamped_upper"


def test_production_public_seam_hard_kill_dominates_weaker_effects() -> None:
    api, bundle, input_state = _production_payloads()
    kill = bundle.modifiers[0].model_copy(
        update={
            "modifier_id": "hard_kill",
            "modifier_version": "1.0.0",
            "applicability_fact_refs": ("kill",),
            "precedence_rank": 100,
            "transform_operator": "set",
            "operand": Decimal("0"),
            "kill_switch": True,
            "restrictive_only": True,
            "promotion_lineage": "workbook://hard_kill/1.0.0",
        }
    )
    decision = api["resolve_k12"](
        bundle=bundle.model_copy(update={"modifiers": (*bundle.modifiers, kill)}),
        owner_stage="posture",
        input_state={**input_state, "facts": {"stress": True, "volatility": True, "kill": True}},
    )

    assert decision.status == "applied"
    assert tuple(item.modifier_id for item in decision.applied_modifiers) == ("hard_kill",)
    assert tuple((item.modifier_id, item.reason) for item in decision.skipped_modifiers) == (
        ("stress_add", "dominated_by_kill_switch"),
        ("volatility_multiply", "dominated_by_kill_switch"),
    )
    assert decision.coefficient_results[0].effective_value == Decimal("0")


def test_production_public_seam_rejects_missing_fact_and_equal_precedence_conflict() -> None:
    api, bundle, input_state = _production_payloads()
    missing_fact = api["resolve_k12"](
        bundle=bundle,
        owner_stage="posture",
        input_state={**input_state, "facts": {"stress": True}},
    )
    conflict_modifiers = tuple(
        modifier.model_copy(
            update={
                "precedence_rank": 10,
                "conflict_modifier_ids": (
                    "volatility_multiply" if modifier.modifier_id == "stress_add" else "stress_add",
                ),
            }
        )
        for modifier in bundle.modifiers
    )
    conflict = api["resolve_k12"](
        bundle=bundle.model_copy(update={"modifiers": conflict_modifiers}),
        owner_stage="posture",
        input_state=input_state,
    )

    assert missing_fact.status == "rejected"
    assert missing_fact.rejection_reasons == ("missing_applicability_fact:volatility",)
    assert conflict.status == "rejected"
    assert conflict.rejection_reasons == (
        "unresolved_modifier_conflict:stress_add:volatility_multiply",
    )


def test_production_receipt_preserves_decision_lineage_without_foreign_authority() -> None:
    api, bundle, input_state = _production_payloads()
    decision_a = api["resolve_k12"](
        bundle=bundle,
        owner_stage="posture",
        input_state=input_state,
    )
    decision_b = api["resolve_k12"](
        bundle=bundle,
        owner_stage="posture",
        input_state=input_state,
    )
    receipt = api["build_k12_receipt"](
        decision=decision_a,
        receipt_id="receipt-001",
        application_id="application-001",
        emitted_at_utc=datetime(2026, 7, 31, 3, 1, tzinfo=UTC),
    )

    assert decision_a.semantic_fingerprint == decision_b.semantic_fingerprint
    assert isinstance(receipt, api["ModifierApplicationReceipt"])
    assert receipt.source_decision_id == decision_a.decision_id
    assert receipt.source_decision_fingerprint == decision_a.semantic_fingerprint
    assert receipt.external_mutation_proven is False
    assert tuple(receipt.closed_authority_classes) == CLOSED_AUTHORITIES
    assert receipt.emitted_at_utc == datetime(2026, 7, 31, 3, 1, tzinfo=UTC)


def test_production_public_seam_rejects_non_utc_input_state_time() -> None:
    api, bundle, input_state = _production_payloads()
    non_utc = datetime(2026, 7, 31, 13, 0, tzinfo=UTC).astimezone(
        timezone(timedelta(hours=10))
    )
    decision = api["resolve_k12"](
        bundle=bundle,
        owner_stage="posture",
        input_state={**input_state, "effective_at_utc": non_utc},
    )

    assert decision.status == "rejected"
    assert decision.rejection_reasons == ("input_state_time_must_be_utc",)
