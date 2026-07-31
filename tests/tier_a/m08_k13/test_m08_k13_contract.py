"""Minimum truthful public-seam proof for M08 K13 playbook catalogue authority."""

from __future__ import annotations

from dataclasses import replace

import pytest

from tests.support.m08_k13_contract_harness import (
    CLOSED_AUTHORITIES,
    MUTANTS,
    ReferenceSubject,
    production_api,
    production_catalogue_payload,
    production_context_payload,
    production_definition_payload,
    production_posture_payload,
    valid_catalogue,
    valid_context,
    valid_definition,
    valid_posture,
)


def _families(decision) -> tuple[str, ...]:
    return tuple(item.candidate_family_id for item in decision.eligible_candidates)


def test_reference_distinguishes_missing_catalogue_from_valid_disabled_catalogue() -> None:
    subject = ReferenceSubject()
    missing = subject.resolve(None, valid_posture(), valid_context())
    disabled = subject.resolve(
        valid_catalogue(definitions=(valid_definition(enabled=False),)),
        valid_posture(),
        valid_context(),
    )

    assert missing.status == "rejected"
    assert missing.reason == "catalogue_authority_missing"
    assert missing.semantic_fingerprint is None
    assert disabled.status == "stand_down_no_candidate_families"
    assert disabled.reason == "no_enabled_candidate_families"
    assert disabled.semantic_fingerprint is not None
    assert disabled.skipped_definitions == (("playbook.breakout", "disabled"),)


def test_reference_distinguishes_posture_block_from_no_eligible_candidates() -> None:
    subject = ReferenceSubject()
    blocked = subject.resolve(valid_catalogue(), valid_posture(status="blocked"), valid_context())
    none_eligible = subject.resolve(
        valid_catalogue(),
        valid_posture(),
        valid_context(facts={"breakout_ready": False, "reversion_ready": False}),
    )

    assert blocked.status == "stand_down_posture_blocked"
    assert blocked.reason == "posture_blocked"
    assert blocked.eligible_candidates == ()
    assert none_eligible.status == "stand_down_no_eligible_candidates"
    assert none_eligible.reason == "no_eligible_candidates"
    assert len(none_eligible.ineligible_definitions) == 2


def test_reference_uses_authority_priority_not_catalogue_or_caller_order() -> None:
    catalogue = valid_catalogue()
    reversed_catalogue = valid_catalogue(
        definitions=tuple(reversed(catalogue.definitions))
    )
    decision = ReferenceSubject().resolve(
        reversed_catalogue,
        valid_posture(),
        valid_context(),
        caller_candidate_order=("family.breakout", "family.reversion"),
    )

    assert reversed_catalogue.catalogue_fingerprint == catalogue.catalogue_fingerprint
    assert _families(decision) == ("family.reversion", "family.breakout")
    assert decision.eligibility_lead is not None
    assert decision.eligibility_lead.candidate_family_id == "family.reversion"


def test_reference_uses_explicit_identity_version_tie_break() -> None:
    zulu = valid_definition(
        playbook_id="playbook.zulu",
        candidate_family_id="family.zulu",
        setup_variant_id="variant.zulu",
        selection_priority=10,
        fact_ref="momentum_ready",
    )
    alpha = valid_definition(
        playbook_id="playbook.alpha",
        candidate_family_id="family.alpha",
        setup_variant_id="variant.alpha",
        selection_priority=10,
        fact_ref="momentum_ready",
    )
    decision = ReferenceSubject().resolve(
        valid_catalogue(definitions=(zulu, alpha)),
        valid_posture(),
        valid_context(),
    )

    assert _families(decision) == ("family.alpha", "family.zulu")


def test_reference_rejects_missing_required_fact_and_catalogue_fingerprint_mismatch() -> None:
    subject = ReferenceSubject()
    missing_fact = subject.resolve(
        valid_catalogue(),
        valid_posture(),
        valid_context(facts={"breakout_ready": True}),
    )
    invalid_catalogue = subject.resolve(
        replace(valid_catalogue(), catalogue_fingerprint="wrong"),
        valid_posture(),
        valid_context(),
    )
    invalid_fact_context = valid_context()
    invalid_fact_context = replace(
        invalid_fact_context,
        facts={
            **invalid_fact_context.facts,
            "reversion_ready": replace(
                invalid_fact_context.facts["reversion_ready"], owner_id=""
            ),
        },
    )
    invalid_fact = subject.resolve(
        valid_catalogue(), valid_posture(), invalid_fact_context
    )

    assert missing_fact.status == "rejected"
    assert missing_fact.reason == "missing_required_fact"
    assert invalid_catalogue.status == "rejected"
    assert invalid_catalogue.reason == "catalogue_fingerprint_mismatch"
    assert invalid_fact.status == "rejected"
    assert invalid_fact.reason == "invalid_required_fact_authority"


def test_reference_fingerprint_and_lifecycle_carriage_are_deterministic_and_closed() -> None:
    subject = ReferenceSubject()
    first = subject.resolve(valid_catalogue(), valid_posture(), valid_context())
    second = subject.resolve(valid_catalogue(), valid_posture(), valid_context())

    assert first.semantic_fingerprint == second.semantic_fingerprint
    assert first.eligibility_lead is not None
    assert dict(first.eligibility_lead.lifecycle_intent) == {
        "handoff_schema": "m05.expression.v1",
        "horizon_class": "intraday",
    }
    assert first.closed_authority_classes == CLOSED_AUTHORITIES
    assert first.foreign_authority_claimed is False


@pytest.mark.parametrize("mutant_name", tuple(MUTANTS))
def test_each_false_positive_mutant_is_killed(mutant_name: str) -> None:
    subject = MUTANTS[mutant_name]()

    if mutant_name == "caller_order":
        reference = ReferenceSubject().resolve(
            valid_catalogue(),
            valid_posture(),
            valid_context(),
            caller_candidate_order=("family.breakout", "family.reversion"),
        )
        mutant = subject.resolve(
            valid_catalogue(),
            valid_posture(),
            valid_context(),
            caller_candidate_order=("family.breakout", "family.reversion"),
        )
        assert _families(reference) == ("family.reversion", "family.breakout")
        assert _families(mutant) != _families(reference)
    elif mutant_name == "missing_catalogue_as_empty":
        reference = ReferenceSubject().resolve(None, valid_posture(), valid_context())
        mutant = subject.resolve(None, valid_posture(), valid_context())
        assert reference.status == "rejected"
        assert mutant.status != "rejected"
    elif mutant_name == "posture_block_ignored":
        reference = ReferenceSubject().resolve(
            valid_catalogue(), valid_posture(status="blocked"), valid_context()
        )
        mutant = subject.resolve(
            valid_catalogue(), valid_posture(status="blocked"), valid_context()
        )
        assert reference.status == "stand_down_posture_blocked"
        assert mutant.status == "eligible"
    elif mutant_name == "catalogue_order_tie":
        zulu = valid_definition(
            playbook_id="playbook.zulu",
            candidate_family_id="family.zulu",
            setup_variant_id="variant.zulu",
            selection_priority=10,
            fact_ref="momentum_ready",
        )
        alpha = valid_definition(
            playbook_id="playbook.alpha",
            candidate_family_id="family.alpha",
            setup_variant_id="variant.alpha",
            selection_priority=10,
            fact_ref="momentum_ready",
        )
        catalogue = valid_catalogue(definitions=(zulu, alpha))
        reference = ReferenceSubject().resolve(catalogue, valid_posture(), valid_context())
        mutant = subject.resolve(catalogue, valid_posture(), valid_context())
        assert _families(reference) == ("family.alpha", "family.zulu")
        assert _families(mutant) != _families(reference)
    else:
        reference = ReferenceSubject().resolve(valid_catalogue(), valid_posture(), valid_context())
        mutant = subject.resolve(valid_catalogue(), valid_posture(), valid_context())
        assert reference.foreign_authority_claimed is False
        assert "capital" in reference.closed_authority_classes
        assert mutant.foreign_authority_claimed is True
        assert "capital" not in mutant.closed_authority_classes


def _production_subjects(*, definitions=None):
    api = production_api()
    definition_payloads = (
        [production_definition_payload(item) for item in definitions]
        if definitions is not None
        else production_catalogue_payload()["definitions"]
    )
    catalogue_payload = production_catalogue_payload(definitions=definitions)
    catalogue_payload["definitions"] = definition_payloads
    catalogue = api["PlaybookCatalogue"].model_validate(catalogue_payload)
    resolver = api["EligibilityResolver"]()
    return api, catalogue, resolver


def test_production_exports_exact_frozen_contract_models() -> None:
    api = production_api()
    assert api["PlaybookDefinition"].model_config.get("frozen") is True
    assert api["PlaybookCatalogue"].model_config.get("frozen") is True
    assert api["EligibilityDecision"].model_config.get("frozen") is True
    api["PlaybookDefinition"].model_validate(production_definition_payload())


def test_production_rejects_missing_catalogue_authority() -> None:
    api = production_api()
    decision = api["EligibilityResolver"]().resolve(
        None,
        production_posture_payload(),
        production_context_payload(),
        decision_id="decision-missing",
    )
    assert decision.status == "rejected"
    assert decision.reason == "catalogue_authority_missing"
    assert decision.semantic_fingerprint is None


def test_production_preserves_three_lawful_stand_down_states() -> None:
    disabled = (valid_definition(enabled=False),)
    _, disabled_catalogue, disabled_resolver = _production_subjects(definitions=disabled)
    no_family = disabled_resolver.resolve(
        disabled_catalogue,
        production_posture_payload(),
        production_context_payload(),
        decision_id="decision-disabled",
    )
    _, catalogue, resolver = _production_subjects()
    blocked = resolver.resolve(
        catalogue,
        production_posture_payload(status="blocked"),
        production_context_payload(),
        decision_id="decision-blocked",
    )
    no_eligible = resolver.resolve(
        catalogue,
        production_posture_payload(),
        production_context_payload(
            facts={"breakout_ready": False, "reversion_ready": False}
        ),
        decision_id="decision-none",
    )
    assert no_family.status == "stand_down_no_candidate_families"
    assert blocked.status == "stand_down_posture_blocked"
    assert no_eligible.status == "stand_down_no_eligible_candidates"


def test_production_uses_authority_priority_and_identity_tie_break() -> None:
    zulu = valid_definition(
        playbook_id="playbook.zulu",
        candidate_family_id="family.zulu",
        setup_variant_id="variant.zulu",
        selection_priority=10,
        fact_ref="momentum_ready",
    )
    alpha = valid_definition(
        playbook_id="playbook.alpha",
        candidate_family_id="family.alpha",
        setup_variant_id="variant.alpha",
        selection_priority=10,
        fact_ref="momentum_ready",
    )
    _, catalogue, resolver = _production_subjects(definitions=(zulu, alpha))
    decision = resolver.resolve(
        catalogue,
        production_posture_payload(),
        production_context_payload(),
        decision_id="decision-tie",
        caller_candidate_order=("family.zulu", "family.alpha"),
    )
    assert tuple(item.candidate_family_id for item in decision.eligible_candidates) == (
        "family.alpha",
        "family.zulu",
    )
    assert decision.eligibility_lead.candidate_family_id == "family.alpha"


def test_production_decision_fingerprint_is_deterministic_and_occurrence_independent() -> None:
    _, catalogue, resolver = _production_subjects()
    first = resolver.resolve(
        catalogue,
        production_posture_payload(),
        production_context_payload(),
        decision_id="decision-a",
    )
    second = resolver.resolve(
        catalogue,
        production_posture_payload(),
        production_context_payload(),
        decision_id="decision-b",
    )
    assert first.semantic_fingerprint == second.semantic_fingerprint


def test_production_rejects_missing_required_fact_and_bad_catalogue_fingerprint() -> None:
    api, catalogue, resolver = _production_subjects()
    missing = resolver.resolve(
        catalogue,
        production_posture_payload(),
        production_context_payload(facts={"breakout_ready": True}),
        decision_id="decision-missing-fact",
    )
    invalid_fact_context = production_context_payload()
    invalid_fact_context["facts"]["reversion_ready"]["owner_id"] = ""
    invalid_fact = resolver.resolve(
        catalogue,
        production_posture_payload(),
        invalid_fact_context,
        decision_id="decision-invalid-fact",
    )
    bad_payload = production_catalogue_payload()
    bad_payload["catalogue_fingerprint"] = "wrong"
    with pytest.raises(ValueError, match="catalogue_fingerprint"):
        api["PlaybookCatalogue"].model_validate(bad_payload)
    assert missing.status == "rejected"
    assert missing.reason == "missing_required_fact"
    assert invalid_fact.status == "rejected"
    assert invalid_fact.reason == "invalid_required_fact_authority"


def test_production_carries_lifecycle_metadata_without_foreign_authority() -> None:
    _, catalogue, resolver = _production_subjects()
    decision = resolver.resolve(
        catalogue,
        production_posture_payload(),
        production_context_payload(),
        decision_id="decision-authority",
    )
    assert decision.status == "eligible"
    assert decision.eligibility_lead.lifecycle_intent == {
        "handoff_schema": "m05.expression.v1",
        "horizon_class": "intraday",
    }
    assert tuple(decision.closed_authority_classes) == CLOSED_AUTHORITIES
    assert decision.foreign_authority_claimed is False
