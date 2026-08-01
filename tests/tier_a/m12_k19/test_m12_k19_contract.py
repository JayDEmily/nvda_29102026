from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from tests.support.m12_k19_contract_harness import (
    canonical_reasons,
    production_api,
    reference_status,
)

from nvda_desk.contracts.replay import ReplayPacketLineage
from nvda_desk.contracts.review import ReviewPacket
from nvda_desk.m10_execution_gateway.contracts import semantic_fingerprint


def test_reference_replay_classes_are_closed_and_fail_closed():
    assert (
        reference_status(
            replay_class="comparison_only",
            complete=True,
            result_present=True,
            fingerprint_match=True,
            reasons_match=True,
            executable_match=True,
        )
        == "comparison_only"
    )
    assert (
        reference_status(
            replay_class="preserved_occurrence_replay",
            complete=True,
            result_present=False,
            fingerprint_match=False,
            reasons_match=False,
            executable_match=False,
        )
        == "authoritative_match"
    )
    assert (
        reference_status(
            replay_class="preserved_occurrence_replay",
            complete=False,
            result_present=False,
            fingerprint_match=False,
            reasons_match=False,
            executable_match=False,
        )
        == "non_authoritative_incomplete"
    )
    with pytest.raises(ValueError):
        reference_status(
            replay_class="future_replay",
            complete=True,
            result_present=True,
            fingerprint_match=True,
            reasons_match=True,
            executable_match=True,
        )


def test_reference_governed_reexecution_requires_complete_exact_result():
    assert (
        reference_status(
            replay_class="governed_semantic_reexecution",
            complete=True,
            result_present=True,
            fingerprint_match=True,
            reasons_match=True,
            executable_match=True,
        )
        == "authoritative_match"
    )
    for kwargs in (
        dict(
            complete=False,
            result_present=True,
            fingerprint_match=True,
            reasons_match=True,
            executable_match=True,
        ),
        dict(
            complete=True,
            result_present=False,
            fingerprint_match=True,
            reasons_match=True,
            executable_match=True,
        ),
        dict(
            complete=True,
            result_present=True,
            fingerprint_match=False,
            reasons_match=True,
            executable_match=True,
        ),
        dict(
            complete=True,
            result_present=True,
            fingerprint_match=True,
            reasons_match=False,
            executable_match=True,
        ),
        dict(
            complete=True,
            result_present=True,
            fingerprint_match=True,
            reasons_match=True,
            executable_match=False,
        ),
    ):
        expected = (
            "non_authoritative_incomplete"
            if not kwargs["complete"] or not kwargs["result_present"]
            else "semantic_mismatch"
        )
        assert reference_status(replay_class="governed_semantic_reexecution", **kwargs) == expected


def test_reference_reason_order_is_semantic_and_duplicates_fail():
    assert canonical_reasons(("blocked", "missing_input")) == ("blocked", "missing_input")
    assert canonical_reasons(("missing_input", "blocked")) != ("blocked", "missing_input")
    with pytest.raises(ValueError):
        canonical_reasons(("blocked", "blocked"))
    with pytest.raises(ValueError):
        canonical_reasons(("",))


def _packet_content(seed: str = "packet-content") -> ReplayPacketLineage:
    return ReplayPacketLineage(packet_ids=[f"packet:{seed}"], replay_run_id="source-run:1")


def _output_content(summary: str = "stand_down") -> ReviewPacket:
    return ReviewPacket(packet_id="capital-decision:1", summary=summary, sections=[summary])


def _material(
    api,
    *,
    material_id_seed="packet",
    sequence=0,
    owner="M04",
    occurrence="packet-occurrence:1",
    fp_seed="packet-content",
    content=None,
    material_time_utc=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
    contract_version="1.0.0",
):
    service = api["EvidenceReplayService"]()
    return service.build_material(
        owner_module=owner,
        contract_version=contract_version,
        occurrence_id=occurrence,
        content=content or _packet_content(fp_seed),
        sequence=sequence,
        material_time_utc=material_time_utc,
        material_label=material_id_seed,
    )


def _envelope(
    api,
    *,
    replay_class="governed_semantic_reexecution",
    missing=(),
    unverifiable=(),
    contradictions=(),
    materials=None,
    reasons=("stand_down",),
    executable=("m09.capital.v1",),
    replay_run_id="replay-run:1",
):
    service = api["EvidenceReplayService"]()
    output_content = _output_content(reasons[0] if reasons else "stand_down")
    output_fp = semantic_fingerprint(output_content.model_dump(mode="python"))
    mats = tuple(
        materials
        or (
            _material(api, sequence=0),
            _material(
                api,
                material_id_seed="original-output",
                sequence=1,
                owner="M09",
                occurrence="decision-occurrence:1",
                content=output_content,
            ),
        )
    )
    return service.build_envelope(
        replay_run_id=replay_run_id,
        replay_class=replay_class,
        target_id="capital-decision:1",
        original_output_id="capital-decision:1",
        original_output_occurrence_id="decision-occurrence:1",
        original_output_fingerprint=output_fp,
        original_reasons=reasons,
        materials=mats,
        executable_versions=executable,
        missing_material=missing,
        unverifiable_material=unverifiable,
        contradictions=contradictions,
    )


def _exact_assessment(api, envelope):
    return api["EvidenceReplayService"]().assess(
        envelope,
        reproduced_output_id="reproduced:1",
        reproduced_output_fingerprint=envelope.original_output_fingerprint,
        reproduced_reasons=envelope.original_reasons,
        executable_versions=envelope.executable_versions,
    )


def _recomputed_material(api, material, **updates):
    payload = material.model_dump(mode="python")
    payload.update(updates)
    payload.pop("material_id", None)
    payload.pop("semantic_fingerprint", None)
    fingerprint = semantic_fingerprint(payload)
    payload["material_id"] = f"replay-material:{fingerprint[:24]}"
    payload["semantic_fingerprint"] = fingerprint
    return api["ReplayMaterial"].model_validate(payload)


def _recomputed_assessment(api, assessment, **updates):
    payload = assessment.model_dump(mode="python")
    payload.update(updates)
    payload.pop("assessment_id", None)
    payload.pop("semantic_fingerprint", None)
    fingerprint = semantic_fingerprint(payload)
    payload["assessment_id"] = f"replay-assessment:{fingerprint[:24]}"
    payload["semantic_fingerprint"] = fingerprint
    return api["ReplayAssessment"].model_validate(payload)


def _recomputed_projection(api, projection, **updates):
    payload = projection.model_dump(mode="python")
    payload.update(updates)
    payload.pop("projection_id", None)
    payload.pop("semantic_fingerprint", None)
    fingerprint = semantic_fingerprint(payload)
    payload["projection_id"] = f"review-projection:{fingerprint[:24]}"
    payload["semantic_fingerprint"] = fingerprint
    return api["ReviewProjection"].model_validate(payload)


def test_production_exports_frozen_closed_contracts():
    api = production_api()
    for name in ("ReplayMaterial", "ReplayEnvelope", "ReplayAssessment", "ReviewProjection"):
        assert api[name].model_config.get("frozen") is True
        assert api[name].model_config.get("extra") == "forbid"


def test_production_material_identity_and_contract_are_deterministic():
    api = production_api()
    first = _material(api)
    second = _material(api)
    assert first == second
    assert first.material_id.startswith("replay-material:")
    assert first.verified is True and first.retrievable is True
    assert first.contract_path == "nvda_desk.contracts.replay:ReplayPacketLineage"
    assert first.content_snapshot == _packet_content().model_dump(mode="python")


def test_production_material_requires_embedded_typed_content_not_a_caller_hash():
    api = production_api()
    service = api["EvidenceReplayService"]()
    with pytest.raises(TypeError):
        service.build_material(
            owner_module="M04",
            contract_version="1.0.0",
            occurrence_id="packet-occurrence:1",
            content_fingerprint=semantic_fingerprint({"seed": "detached"}),
            sequence=0,
            material_label="packet",
        )


def test_production_material_revalidates_embedded_content_and_fingerprint():
    api = production_api()
    material = _material(api)
    with pytest.raises(ValueError, match="content"):
        _recomputed_material(
            api,
            material,
            content_snapshot={**material.content_snapshot, "unexpected": "foreign"},
            content_fingerprint=semantic_fingerprint(
                {**material.content_snapshot, "unexpected": "foreign"}
            ),
        )
    with pytest.raises(ValueError, match="fingerprint"):
        _recomputed_material(
            api,
            material,
            content_snapshot=_packet_content("changed").model_dump(mode="python"),
        )


def test_production_envelope_requires_unique_strict_material_order_and_verified_hashes():
    api = production_api()
    first = _material(api, sequence=0)
    second = _material(api, sequence=1, occurrence="packet-occurrence:2", fp_seed="two")
    output = _material(
        api, sequence=2, owner="M09", occurrence="decision-occurrence:1", content=_output_content()
    )
    envelope = _envelope(api, materials=(first, second, output))
    assert envelope.material_ids == (first.material_id, second.material_id, output.material_id)
    with pytest.raises(ValueError):
        _envelope(api, materials=(second, first, output))
    with pytest.raises(ValueError):
        _envelope(api, materials=(first, first, output))
    with pytest.raises(ValidationError):
        api["ReplayMaterial"].model_validate({"content_fingerprint": "bad"})


def test_production_material_rejects_non_utc_and_unknown_owner():
    api = production_api()
    with pytest.raises(ValueError, match="utc"):
        _material(api, material_time_utc=datetime(2026, 8, 1, 1, 0))
    with pytest.raises(ValueError, match="owner_module"):
        _material(api, owner="M99")


def test_production_envelope_requires_exact_original_output_material_binding():
    api = production_api()
    packet = _material(api)
    envelope = _envelope(api, materials=(packet,))
    assessment = _exact_assessment(api, envelope)
    assert assessment.authority_status == "non_authoritative_incomplete"
    assert "original_output_occurrence" in assessment.missing_material


def test_production_comparison_only_never_promotes_to_authoritative():
    api = production_api()
    service = api["EvidenceReplayService"]()
    envelope = _envelope(api, replay_class="comparison_only", executable=())
    assessment = service.assess(envelope)
    assert assessment.authority_status == "comparison_only"
    assert assessment.runtime_authority_promoted is False
    assert assessment.live_side_effects_performed is False
    with pytest.raises(ValueError, match="comparison_only"):
        service.assess(
            envelope,
            reproduced_output_id="x",
            reproduced_output_fingerprint=envelope.original_output_fingerprint,
        )


def test_production_incomplete_governed_replay_cannot_match():
    api = production_api()
    envelope = _envelope(api, missing=("policy_snapshot",))
    assessment = _exact_assessment(api, envelope)
    assert assessment.authority_status == "non_authoritative_incomplete"
    assert assessment.missing_material == ("policy_snapshot",)


def test_production_governed_reexecution_exact_match_is_authoritative_only_when_isolated():
    api = production_api()
    service = api["EvidenceReplayService"]()
    envelope = _envelope(api)
    assessment = _exact_assessment(api, envelope)
    assert assessment.authority_status == "authoritative_match"
    assert assessment.exact_matches == (
        "semantic_fingerprint",
        "reasons_constraints",
        "executable_versions",
    )
    with pytest.raises(ValueError, match="live_side_effect"):
        service.assess(
            envelope,
            reproduced_output_id="x",
            reproduced_output_fingerprint=envelope.original_output_fingerprint,
            reproduced_reasons=envelope.original_reasons,
            executable_versions=envelope.executable_versions,
            live_side_effects=("order_submitted",),
        )
    with pytest.raises(ValueError, match="isolated"):
        service.assess(
            envelope,
            reproduced_output_id="x",
            reproduced_output_fingerprint=envelope.original_output_fingerprint,
            reproduced_reasons=envelope.original_reasons,
            executable_versions=envelope.executable_versions,
            isolated_execution=False,
        )


def test_production_mismatch_is_not_normalised_away():
    api = production_api()
    service = api["EvidenceReplayService"]()
    envelope = _envelope(api)
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
    api = production_api()
    service = api["EvidenceReplayService"]()
    packet = _material(api)
    incomplete = _envelope(
        api, replay_class="preserved_occurrence_replay", executable=(), materials=(packet,)
    )
    assert service.assess(incomplete).authority_status == "non_authoritative_incomplete"
    complete = _envelope(api, replay_class="preserved_occurrence_replay", executable=())
    assert service.assess(complete).authority_status == "authoritative_match"


def test_production_revalidates_forged_nested_material_and_envelope_copies():
    api = production_api()
    service = api["EvidenceReplayService"]()
    envelope = _envelope(api)
    forged_material = envelope.materials[0].model_copy(update={"content_fingerprint": "0" * 64})
    forged_envelope = envelope.model_copy(
        update={"materials": (forged_material,) + envelope.materials[1:]}
    )
    with pytest.raises(ValueError):
        service.assess(forged_envelope)


def test_production_authoritative_assessment_requires_reproduced_output_evidence():
    api = production_api()
    envelope = _envelope(api)
    assessment = _exact_assessment(api, envelope)
    with pytest.raises(ValueError, match="authoritative_match"):
        _recomputed_assessment(
            api,
            assessment,
            reproduced_output_id=None,
            reproduced_output_fingerprint=None,
        )


def test_production_review_projection_is_detached_and_exactly_bound():
    api = production_api()
    service = api["EvidenceReplayService"]()
    envelope = _envelope(api)
    assessment = _exact_assessment(api, envelope)
    projection = service.project(envelope=envelope, assessment=assessment)
    assert projection.envelope_id == envelope.envelope_id
    assert projection.assessment_id == assessment.assessment_id
    assert projection.runtime_authority_promoted is False
    assert projection.live_side_effects_performed is False
    with pytest.raises(ValueError):
        service.project(
            envelope=envelope, assessment=assessment.model_copy(update={"envelope_id": "other"})
        )
    forged = assessment.model_copy(update={"authority_status": "comparison_only"})
    with pytest.raises(ValueError):
        service.project(envelope=envelope, assessment=forged)


def test_production_review_projection_rejects_recomputed_status_evidence_contradiction():
    api = production_api()
    service = api["EvidenceReplayService"]()
    envelope = _envelope(api)
    projection = service.project(envelope=envelope, assessment=_exact_assessment(api, envelope))
    with pytest.raises(ValueError, match="projection_status"):
        _recomputed_projection(api, projection, authority_status="comparison_only")


def test_production_future_replay_and_executable_versions_fail_closed():
    api = production_api()
    service = api["EvidenceReplayService"]()
    with pytest.raises(ValueError):
        _envelope(api, replay_class="future_replay")
    with pytest.raises(ValueError, match="executable_versions"):
        _envelope(api, executable=())
    with pytest.raises(ValueError, match="executable_versions"):
        _envelope(api, executable=("m09.capital.v1", "m09.capital.v1"))
    envelope = _envelope(api)
    assessment = service.assess(
        envelope,
        reproduced_output_id="x",
        reproduced_output_fingerprint=envelope.original_output_fingerprint,
        reproduced_reasons=envelope.original_reasons,
        executable_versions=("current.latest",),
    )
    assert assessment.authority_status == "semantic_mismatch"
    assert "executable_versions" in assessment.mismatches


def test_production_semantic_identity_excludes_replay_transport_identity_but_not_domain_result():
    api = production_api()
    first = _envelope(api)
    second = _envelope(api, replay_run_id="replay-run:2")
    assert first.semantic_domain_fingerprint == second.semantic_domain_fingerprint
    assert first.semantic_fingerprint != second.semantic_fingerprint
    changed = _envelope(api, reasons=("different",))
    assert first.semantic_domain_fingerprint != changed.semantic_domain_fingerprint


def test_production_missing_unverifiable_and_contradiction_sets_are_unique_nonblank():
    api = production_api()
    for kwargs in (
        {"missing": ("x", "x")},
        {"unverifiable": ("",)},
        {"contradictions": ("x", "x")},
    ):
        with pytest.raises(ValueError):
            _envelope(api, **kwargs)
