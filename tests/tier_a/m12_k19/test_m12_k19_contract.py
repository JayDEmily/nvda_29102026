from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from nvda_desk.m10_execution_gateway.contracts import semantic_fingerprint
from tests.support.m12_k19_contract_harness import (
    canonical_reasons,
    production_api,
    reference_status,
)


def test_reference_replay_classes_are_closed_and_fail_closed():
    assert reference_status(replay_class="comparison_only", complete=True, result_present=True, fingerprint_match=True, reasons_match=True, executable_match=True) == "comparison_only"
    assert reference_status(replay_class="preserved_occurrence_replay", complete=True, result_present=False, fingerprint_match=False, reasons_match=False, executable_match=False) == "authoritative_match"
    assert reference_status(replay_class="preserved_occurrence_replay", complete=False, result_present=False, fingerprint_match=False, reasons_match=False, executable_match=False) == "non_authoritative_incomplete"
    with pytest.raises(ValueError):
        reference_status(replay_class="future_replay", complete=True, result_present=True, fingerprint_match=True, reasons_match=True, executable_match=True)


def test_reference_governed_reexecution_requires_complete_exact_result():
    assert reference_status(replay_class="governed_semantic_reexecution", complete=True, result_present=True, fingerprint_match=True, reasons_match=True, executable_match=True) == "authoritative_match"
    for kwargs in (
        dict(complete=False, result_present=True, fingerprint_match=True, reasons_match=True, executable_match=True),
        dict(complete=True, result_present=False, fingerprint_match=True, reasons_match=True, executable_match=True),
        dict(complete=True, result_present=True, fingerprint_match=False, reasons_match=True, executable_match=True),
        dict(complete=True, result_present=True, fingerprint_match=True, reasons_match=False, executable_match=True),
        dict(complete=True, result_present=True, fingerprint_match=True, reasons_match=True, executable_match=False),
    ):
        expected = "non_authoritative_incomplete" if not kwargs["complete"] or not kwargs["result_present"] else "semantic_mismatch"
        assert reference_status(replay_class="governed_semantic_reexecution", **kwargs) == expected


def test_reference_reason_order_is_semantic_and_duplicates_fail():
    assert canonical_reasons(("blocked", "missing_input")) == ("blocked", "missing_input")
    assert canonical_reasons(("missing_input", "blocked")) != ("blocked", "missing_input")
    with pytest.raises(ValueError): canonical_reasons(("blocked", "blocked"))
    with pytest.raises(ValueError): canonical_reasons(("",))


def _material(api, *, material_id_seed="packet", sequence=0, owner="M04", occurrence="packet-occurrence:1", fp_seed="packet-content"):
    service = api["EvidenceReplayService"]()
    return service.build_material(
        owner_module=owner,
        contract_name="DMPV3Packet",
        contract_version="3.0.0",
        occurrence_id=occurrence,
        content_fingerprint=semantic_fingerprint({"seed": fp_seed}),
        sequence=sequence,
        material_time_utc=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
        material_label=material_id_seed,
    )


def _envelope(api, *, replay_class="governed_semantic_reexecution", missing=(), unverifiable=(), contradictions=(), materials=None, reasons=("stand_down",), executable=("m09.capital.v1",)):
    service = api["EvidenceReplayService"]()
    mats = tuple(materials or (_material(api),))
    return service.build_envelope(
        replay_run_id="replay-run:1",
        replay_class=replay_class,
        target_id="capital-decision:1",
        original_output_id="capital-decision:1",
        original_output_occurrence_id="decision-occurrence:1",
        original_output_fingerprint=semantic_fingerprint({"result": "stand_down"}),
        original_reasons=reasons,
        materials=mats,
        executable_versions=executable,
        missing_material=missing,
        unverifiable_material=unverifiable,
        contradictions=contradictions,
    )


def test_production_exports_frozen_closed_contracts():
    api = production_api()
    for name in ("ReplayMaterial", "ReplayEnvelope", "ReplayAssessment", "ReviewProjection"):
        assert api[name].model_config.get("frozen") is True
        assert api[name].model_config.get("extra") == "forbid"


def test_production_material_identity_and_contract_are_deterministic():
    api = production_api(); first = _material(api); second = _material(api)
    assert first == second
    assert first.material_id.startswith("replay-material:")
    assert first.verified is True and first.retrievable is True


def test_production_envelope_requires_unique_strict_material_order_and_verified_hashes():
    api = production_api(); first = _material(api, sequence=0); second = _material(api, sequence=1, occurrence="packet-occurrence:2", fp_seed="two")
    envelope = _envelope(api, materials=(first, second))
    assert envelope.material_ids == (first.material_id, second.material_id)
    with pytest.raises(ValueError): _envelope(api, materials=(second, first))
    with pytest.raises(ValueError): _envelope(api, materials=(first, first))
    with pytest.raises(ValidationError): api["ReplayMaterial"].model_validate({"content_fingerprint":"bad"})


def test_production_comparison_only_never_promotes_to_authoritative():
    api = production_api(); service = api["EvidenceReplayService"](); envelope = _envelope(api, replay_class="comparison_only", executable=())
    assessment = service.assess(envelope)
    assert assessment.authority_status == "comparison_only"
    assert assessment.runtime_authority_promoted is False
    assert assessment.live_side_effects_performed is False


def test_production_incomplete_governed_replay_cannot_match():
    api = production_api(); service = api["EvidenceReplayService"](); envelope = _envelope(api, missing=("policy_snapshot",))
    assessment = service.assess(
        envelope,
        reproduced_output_id="reproduced:1",
        reproduced_output_fingerprint=envelope.original_output_fingerprint,
        reproduced_reasons=envelope.original_reasons,
        executable_versions=envelope.executable_versions,
    )
    assert assessment.authority_status == "non_authoritative_incomplete"
    assert assessment.missing_material == ("policy_snapshot",)


def test_production_governed_reexecution_exact_match_is_authoritative_only_when_isolated():
    api = production_api(); service = api["EvidenceReplayService"](); envelope = _envelope(api)
    assessment = service.assess(
        envelope,
        reproduced_output_id="reproduced:1",
        reproduced_output_fingerprint=envelope.original_output_fingerprint,
        reproduced_reasons=envelope.original_reasons,
        executable_versions=envelope.executable_versions,
    )
    assert assessment.authority_status == "authoritative_match"
    assert assessment.exact_matches == ("semantic_fingerprint", "reasons_constraints", "executable_versions")
    with pytest.raises(ValueError, match="live_side_effect"):
        service.assess(envelope, reproduced_output_id="x", reproduced_output_fingerprint=envelope.original_output_fingerprint, reproduced_reasons=envelope.original_reasons, executable_versions=envelope.executable_versions, live_side_effects=("order_submitted",))


def test_production_mismatch_is_not_normalised_away():
    api = production_api(); service = api["EvidenceReplayService"](); envelope = _envelope(api)
    assessment = service.assess(
        envelope,
        reproduced_output_id="reproduced:2",
        reproduced_output_fingerprint=semantic_fingerprint({"result": "eligible"}),
        reproduced_reasons=("eligible",),
        executable_versions=envelope.executable_versions,
    )
    assert assessment.authority_status == "semantic_mismatch"
    assert assessment.mismatches == ("semantic_fingerprint", "reasons_constraints")


def test_production_preserved_occurrence_requires_exact_occurrence_material():
    api = production_api(); service = api["EvidenceReplayService"](); envelope = _envelope(api, replay_class="preserved_occurrence_replay", executable=())
    incomplete = service.assess(envelope)
    assert incomplete.authority_status == "non_authoritative_incomplete"
    material = _material(api, occurrence="decision-occurrence:1", owner="M09", fp_seed="decision")
    complete = _envelope(api, replay_class="preserved_occurrence_replay", executable=(), materials=(material,))
    assert service.assess(complete).authority_status == "authoritative_match"


def test_production_revalidates_forged_nested_material_and_envelope_copies():
    api = production_api(); service = api["EvidenceReplayService"](); material = _material(api)
    forged = material.model_copy(update={"content_fingerprint": "0" * 64})
    envelope = _envelope(api, materials=(forged,))
    with pytest.raises(ValueError): service.assess(envelope)


def test_production_review_projection_is_detached_and_exactly_bound():
    api = production_api(); service = api["EvidenceReplayService"](); envelope = _envelope(api)
    assessment = service.assess(envelope, reproduced_output_id="reproduced:1", reproduced_output_fingerprint=envelope.original_output_fingerprint, reproduced_reasons=envelope.original_reasons, executable_versions=envelope.executable_versions)
    projection = service.project(envelope=envelope, assessment=assessment)
    assert projection.envelope_id == envelope.envelope_id
    assert projection.assessment_id == assessment.assessment_id
    assert projection.runtime_authority_promoted is False
    assert projection.live_side_effects_performed is False
    with pytest.raises(ValueError): service.project(envelope=envelope, assessment=assessment.model_copy(update={"envelope_id":"other"}))


def test_production_future_replay_and_executable_versions_fail_closed():
    api = production_api(); service = api["EvidenceReplayService"]()
    with pytest.raises(ValueError): _envelope(api, replay_class="future_replay")
    envelope = _envelope(api)
    assessment = service.assess(envelope, reproduced_output_id="x", reproduced_output_fingerprint=envelope.original_output_fingerprint, reproduced_reasons=envelope.original_reasons, executable_versions=("current.latest",))
    assert assessment.authority_status == "semantic_mismatch"
    assert "executable_versions" in assessment.mismatches


def test_production_semantic_identity_excludes_replay_transport_identity_but_not_domain_result():
    api = production_api(); first = _envelope(api)
    service = api["EvidenceReplayService"]()
    second = service.build_envelope(
        replay_run_id="replay-run:2",
        replay_class=first.replay_class,
        target_id=first.target_id,
        original_output_id=first.original_output_id,
        original_output_occurrence_id=first.original_output_occurrence_id,
        original_output_fingerprint=first.original_output_fingerprint,
        original_reasons=first.original_reasons,
        materials=first.materials,
        executable_versions=first.executable_versions,
    )
    assert first.semantic_domain_fingerprint == second.semantic_domain_fingerprint
    changed = _envelope(api, reasons=("different",))
    assert first.semantic_domain_fingerprint != changed.semantic_domain_fingerprint
