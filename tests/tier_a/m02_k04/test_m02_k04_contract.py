"""Minimum truthful public-seam proof for M02 K04 financial-calendar authority."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest
from tests.support.m02_k04_contract_harness import (
    CLOSED_AUTHORITIES,
    MUTANTS,
    LayerCase,
    ReferenceSubject,
    field_policy,
    production_api,
    production_candidate_payload,
    production_policy_payload,
    production_snapshot_payload,
    snapshot_fingerprint,
    valid_candidate,
    valid_snapshot,
)


def test_reference_has_exact_four_layer_identity() -> None:
    assert {item.value for item in LayerCase} == {
        "market_session_reference",
        "financial_event_reference",
        "operational_calendar_state",
        "derived_runtime_calendar_context",
    }


def test_reference_equal_values_coalesce_with_complete_lineage() -> None:
    first = valid_candidate(candidate_id="session.a", source_artifact_id="source.a")
    second = valid_candidate(
        candidate_id="session.b",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        source_artifact_id="source.b",
    )
    snapshot = valid_snapshot(session_candidates=(first,), operational_candidates=(second,))
    decision = ReferenceSubject().project(snapshot, field_policy())

    assert decision.status == "projected"
    assert decision.selected_fields[0].candidate_ids == ("session.a", "session.b")
    assert decision.selected_fields[0].source_refs == (
        ("source.a", "2026.07.31.1"),
        ("source.b", "2026.07.31.1"),
    )
    assert set(decision.selected_fields[0].layers) == {
        LayerCase.MARKET_SESSION_REFERENCE,
        LayerCase.OPERATIONAL_CALENDAR_STATE,
    }


def test_reference_lawful_operational_supersession_is_explicit() -> None:
    source = valid_candidate(candidate_id="session.source", value="13:30")
    correction = valid_candidate(
        candidate_id="session.correction",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        value="14:30",
        supersedes_candidate_id="session.source",
        supersession_reason="venue_correction",
    )
    decision = ReferenceSubject().project(
        valid_snapshot(session_candidates=(source,), operational_candidates=(correction,)),
        field_policy(),
    )

    assert decision.status == "projected"
    assert decision.selected_fields[0].value == "14:30"
    assert decision.selected_fields[0].candidate_ids == ("session.correction",)


def test_reference_unequal_candidates_without_lawful_supersession_withhold() -> None:
    source = valid_candidate(candidate_id="session.source", value="13:30")
    conflict = valid_candidate(
        candidate_id="session.conflict",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        value="14:30",
    )
    decision = ReferenceSubject().project(
        valid_snapshot(session_candidates=(source,), operational_candidates=(conflict,)),
        field_policy(),
    )

    assert decision.status == "withheld"
    assert decision.selected_fields == ()
    assert decision.unresolved_conflicts == ("session_open_utc",)


def test_reference_derived_value_cannot_override_source_truth() -> None:
    source = valid_candidate(candidate_id="session.source", value="13:30")
    derived = valid_candidate(
        candidate_id="session.derived",
        layer=LayerCase.DERIVED_RUNTIME_CALENDAR_CONTEXT,
        value="14:30",
        supersedes_candidate_id="session.source",
        supersession_reason="runtime_guess",
    )
    decision = ReferenceSubject().project(
        valid_snapshot(session_candidates=(source,), derived_candidates=(derived,)),
        field_policy(),
    )

    assert decision.status == "withheld"
    assert decision.selected_fields == ()


def test_reference_distinguishes_missing_session_from_unknown_events_and_empty_events() -> None:
    subject = ReferenceSubject()
    missing_session = valid_snapshot(session_candidates=(), session_completeness="unknown")
    missing_session = replace(
        missing_session, semantic_fingerprint=snapshot_fingerprint(missing_session)
    )
    unknown_events = valid_snapshot(event_candidates=(), event_completeness="unknown")
    unknown_events = replace(
        unknown_events, semantic_fingerprint=snapshot_fingerprint(unknown_events)
    )
    complete_empty_events = valid_snapshot(event_candidates=(), event_completeness="complete")
    complete_empty_events = replace(
        complete_empty_events,
        semantic_fingerprint=snapshot_fingerprint(complete_empty_events),
    )

    missing = subject.project(missing_session, field_policy())
    unknown = subject.project(unknown_events, field_policy())
    empty = subject.project(complete_empty_events, field_policy())

    assert missing.status == "withheld"
    assert missing.missing_mandatory_authority == ("market_session_reference",)
    assert unknown.status == "degraded"
    assert unknown.degraded_facts == ("financial_event_reference_unknown",)
    assert empty.status == "projected"


def test_reference_projection_identity_is_deterministic_and_foreign_authority_closed() -> None:
    subject = ReferenceSubject()
    first = subject.project(valid_snapshot(), field_policy())
    second = subject.project(valid_snapshot(), field_policy())

    assert first.semantic_fingerprint == second.semantic_fingerprint
    assert first.closed_authority_classes == CLOSED_AUTHORITIES
    assert first.foreign_authority_claimed is False


@pytest.mark.parametrize("mutant_name", tuple(MUTANTS))
def test_each_false_positive_mutant_is_killed(mutant_name: str) -> None:
    subject = MUTANTS[mutant_name]()

    if mutant_name in {"caller_order", "lineage_dropping"}:
        first = valid_candidate(candidate_id="session.a", source_artifact_id="source.a")
        second = valid_candidate(
            candidate_id="session.b",
            layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
            source_artifact_id="source.b",
        )
        reference = ReferenceSubject().project(
            valid_snapshot(session_candidates=(first,), operational_candidates=(second,)),
            field_policy(),
        )
        mutant = subject.project(
            valid_snapshot(session_candidates=(first,), operational_candidates=(second,)),
            field_policy(),
        )
        assert len(reference.selected_fields[0].candidate_ids) == 2
        assert mutant.selected_fields != reference.selected_fields
    elif mutant_name == "derived_override":
        source = valid_candidate(candidate_id="session.source", value="13:30")
        derived = valid_candidate(
            candidate_id="session.derived",
            layer=LayerCase.DERIVED_RUNTIME_CALENDAR_CONTEXT,
            value="14:30",
        )
        snapshot = valid_snapshot(session_candidates=(source,), derived_candidates=(derived,))
        assert ReferenceSubject().project(snapshot, field_policy()).status == "withheld"
        assert subject.project(snapshot, field_policy()).status == "projected"
    elif mutant_name == "missing_session_as_projected":
        snapshot = valid_snapshot(session_candidates=(), session_completeness="unknown")
        snapshot = replace(snapshot, semantic_fingerprint=snapshot_fingerprint(snapshot))
        assert ReferenceSubject().project(snapshot, field_policy()).status == "withheld"
        assert subject.project(snapshot, field_policy()).status == "projected"
    elif mutant_name == "unknown_events_as_empty":
        snapshot = valid_snapshot(event_candidates=(), event_completeness="unknown")
        snapshot = replace(snapshot, semantic_fingerprint=snapshot_fingerprint(snapshot))
        assert ReferenceSubject().project(snapshot, field_policy()).status == "degraded"
        assert subject.project(snapshot, field_policy()).status == "projected"
    else:
        reference = ReferenceSubject().project(valid_snapshot(), field_policy())
        mutant = subject.project(valid_snapshot(), field_policy())
        assert reference.foreign_authority_claimed is False
        assert "capital" in reference.closed_authority_classes
        assert mutant.foreign_authority_claimed is True
        assert "capital" not in mutant.closed_authority_classes


def test_production_exports_exact_frozen_contract_models() -> None:
    api = production_api()
    assert {item.value for item in api["FinancialCalendarLayer"]} == {
        "market_session_reference",
        "financial_event_reference",
        "operational_calendar_state",
        "derived_runtime_calendar_context",
    }
    assert api["CalendarFactCandidate"].model_config.get("frozen") is True
    assert api["FinancialCalendarSnapshot"].model_config.get("frozen") is True
    assert api["CalendarProjection"].model_config.get("frozen") is True
    api["CalendarFactCandidate"].model_validate(production_candidate_payload(valid_candidate()))


def _production_subject(snapshot=None, policy=None):
    api = production_api()
    snapshot_model = api["FinancialCalendarSnapshot"].model_validate(
        production_snapshot_payload(snapshot)
    )
    policy_model = api["CalendarFieldResolutionPolicy"].model_validate(
        production_policy_payload(policy)
    )
    return api, snapshot_model, policy_model, api["CalendarResolver"]()


def test_production_equal_values_coalesce_with_complete_lineage() -> None:
    first = valid_candidate(candidate_id="session.a", source_artifact_id="source.a")
    second = valid_candidate(
        candidate_id="session.b",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        source_artifact_id="source.b",
    )
    api, snapshot, policy, resolver = _production_subject(
        valid_snapshot(session_candidates=(first,), operational_candidates=(second,))
    )
    result = resolver.project(snapshot, policy, projection_id="projection.production.coalesced")
    assert result.status == "projected"
    assert set(result.selected_fields[0].candidate_ids) == {"session.a", "session.b"}
    assert result.closed_authority_classes == CLOSED_AUTHORITIES
    assert api["CalendarProjection"].model_validate(result.model_dump()) == result


def test_production_rejects_derived_override_and_unresolved_conflict() -> None:
    source = valid_candidate(candidate_id="session.source", value="13:30")
    derived = valid_candidate(
        candidate_id="session.derived",
        layer=LayerCase.DERIVED_RUNTIME_CALENDAR_CONTEXT,
        value="14:30",
        supersedes_candidate_id="session.source",
        supersession_reason="runtime_guess",
    )
    _, snapshot, policy, resolver = _production_subject(
        valid_snapshot(session_candidates=(source,), derived_candidates=(derived,))
    )
    result = resolver.project(snapshot, policy, projection_id="projection.derived")
    assert result.status == "withheld"
    assert result.selected_fields == ()
    assert result.unresolved_conflicts == ("session_open_utc",)


def test_production_accepts_only_explicit_lawful_operational_supersession() -> None:
    source = valid_candidate(candidate_id="session.source", value="13:30")
    correction = valid_candidate(
        candidate_id="session.correction",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        value="14:30",
        supersedes_candidate_id="session.source",
        supersession_reason="venue_correction",
    )
    _, snapshot, policy, resolver = _production_subject(
        valid_snapshot(session_candidates=(source,), operational_candidates=(correction,))
    )
    result = resolver.project(snapshot, policy, projection_id="projection.corrected")
    assert result.status == "projected"
    assert result.selected_fields[0].candidate_ids == ("session.correction",)


def test_production_preserves_missing_unknown_and_complete_empty_states() -> None:
    api = production_api()
    resolver = api["CalendarResolver"]()
    policy = api["CalendarFieldResolutionPolicy"].model_validate(production_policy_payload())
    cases = (
        (valid_snapshot(session_candidates=(), session_completeness="unknown"), "withheld"),
        (valid_snapshot(event_candidates=(), event_completeness="unknown"), "degraded"),
        (valid_snapshot(event_candidates=(), event_completeness="complete"), "projected"),
    )
    statuses = []
    for index, (case, expected) in enumerate(cases):
        case = replace(case, semantic_fingerprint=snapshot_fingerprint(case))
        snapshot = api["FinancialCalendarSnapshot"].model_validate(
            production_snapshot_payload(case)
        )
        result = resolver.project(snapshot, policy, projection_id=f"projection.state.{index}")
        statuses.append(result.status)
        assert result.status == expected
    assert statuses == ["withheld", "degraded", "projected"]


def test_production_projection_is_deterministic_and_side_effect_closed() -> None:
    _, snapshot, policy, resolver = _production_subject()
    first = resolver.project(snapshot, policy, projection_id="projection.stable")
    second = resolver.project(snapshot, policy, projection_id="projection.stable")
    assert first.semantic_fingerprint == second.semantic_fingerprint
    assert first.closed_authority_classes == CLOSED_AUTHORITIES
    assert first.foreign_authority_claimed is False


def test_production_rejects_snapshot_fingerprint_forgery() -> None:
    api = production_api()
    payload = production_snapshot_payload()
    payload["semantic_fingerprint"] = "forged"
    with pytest.raises(Exception):
        api["FinancialCalendarSnapshot"].model_validate(payload)


def test_production_revalidates_copied_snapshot_authority() -> None:
    api, snapshot, policy, resolver = _production_subject()
    forged = snapshot.model_copy(update={"semantic_fingerprint": "forged"})
    with pytest.raises(ValueError, match="invalid_calendar_authority"):
        resolver.project(forged, policy, projection_id="projection.forged.snapshot")
    assert api["FinancialCalendarSnapshot"].model_config.get("frozen") is True


def test_production_rejects_candidate_in_wrong_layer_collection() -> None:
    api = production_api()
    payload = production_snapshot_payload()
    payload["operational_calendar_state"] = payload["market_session_reference"]
    payload["market_session_reference"] = []
    with pytest.raises(Exception):
        api["FinancialCalendarSnapshot"].model_validate(payload)


def test_production_snapshot_identity_is_member_order_independent() -> None:
    first = valid_candidate(candidate_id="session.a", source_artifact_id="source.a")
    second = valid_candidate(candidate_id="session.b", source_artifact_id="source.b")
    left = valid_snapshot(session_candidates=(first, second))
    right = valid_snapshot(session_candidates=(second, first))
    assert left.semantic_fingerprint == right.semantic_fingerprint
    api = production_api()
    left_model = api["FinancialCalendarSnapshot"].model_validate(production_snapshot_payload(left))
    right_model = api["FinancialCalendarSnapshot"].model_validate(
        production_snapshot_payload(right)
    )
    assert left_model.semantic_fingerprint == right_model.semantic_fingerprint


def test_production_coalesces_distinct_candidates_sharing_one_source() -> None:
    first = valid_candidate(candidate_id="session.a", source_artifact_id="source.shared")
    second = valid_candidate(
        candidate_id="session.b",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        source_artifact_id="source.shared",
    )
    _, snapshot, policy, resolver = _production_subject(
        valid_snapshot(session_candidates=(first,), operational_candidates=(second,))
    )
    result = resolver.project(snapshot, policy, projection_id="projection.shared.source")
    assert result.selected_fields[0].candidate_ids == ("session.a", "session.b")
    assert result.selected_fields[0].source_refs == (("source.shared", "2026.07.31.1"),)


def test_production_rejects_forged_projection_fingerprint() -> None:
    api, snapshot, policy, resolver = _production_subject()
    result = resolver.project(snapshot, policy, projection_id="projection.valid")
    payload = result.model_dump()
    payload["semantic_fingerprint"] = "forged"
    with pytest.raises(Exception):
        api["CalendarProjection"].model_validate(payload)


def test_production_requires_selected_reference_bundle_identity() -> None:
    api = production_api()
    payload = production_snapshot_payload()
    payload["selected_reference_bundles"] = []
    payload["semantic_fingerprint"] = "forged-for-missing-bundle"
    with pytest.raises(Exception):
        api["FinancialCalendarSnapshot"].model_validate(payload)


def test_production_requires_projection_policy_for_derived_layer() -> None:
    api = production_api()
    derived = valid_candidate(
        candidate_id="derived.context",
        layer=LayerCase.DERIVED_RUNTIME_CALENDAR_CONTEXT,
        semantic_key="session_open_utc",
    )
    case = valid_snapshot(derived_candidates=(derived,))
    payload = production_snapshot_payload(case)
    payload["projection_policy_version"] = None
    with pytest.raises(Exception):
        api["FinancialCalendarSnapshot"].model_validate(payload)


def test_production_projection_preserves_applied_supersession_decision() -> None:
    source = valid_candidate(candidate_id="session.source", value="13:30")
    correction = valid_candidate(
        candidate_id="session.correction",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        value="14:30",
        supersedes_candidate_id="session.source",
        supersession_reason="venue_correction",
        supersession_status="applied",
    )
    _, snapshot, policy, resolver = _production_subject(
        valid_snapshot(session_candidates=(source,), operational_candidates=(correction,))
    )
    result = resolver.project(snapshot, policy, projection_id="projection.supersession")
    assert len(result.applied_supersessions) == 1
    decision = result.applied_supersessions[0]
    assert decision.superseding_candidate_id == "session.correction"
    assert decision.superseded_candidate_id == "session.source"
    assert decision.reason == "venue_correction"
    assert decision.status == "applied"


def test_production_withheld_projection_preserves_prior_supersession_evidence() -> None:
    source = valid_candidate(candidate_id="session.source", value="13:30")
    correction = valid_candidate(
        candidate_id="session.correction",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        value="14:30",
        supersedes_candidate_id="session.source",
        supersession_reason="venue_correction",
        supersession_status="applied",
    )
    case = valid_snapshot(session_candidates=(source,), operational_candidates=(correction,))
    case = replace(case, unresolved_conflicts=("session_open_utc",))
    case = replace(case, semantic_fingerprint=snapshot_fingerprint(case))
    _, snapshot, policy, resolver = _production_subject(case)

    result = resolver.project(snapshot, policy, projection_id="projection.supersession.withheld")

    assert result.status == "withheld"
    assert result.unresolved_conflicts == ("session_open_utc",)
    assert len(result.applied_supersessions) == 1
    assert result.applied_supersessions[0].superseding_candidate_id == "session.correction"


def test_production_preserves_supplied_observation_and_capture_facts() -> None:
    case = valid_candidate(
        observed_at_utc=datetime(2026, 7, 31, 13, 29, tzinfo=UTC),
        capture_id="capture.calendar.session.a",
        captured_at_utc=datetime(2026, 7, 31, 13, 30, tzinfo=UTC),
    )
    api = production_api()
    candidate = api["CalendarFactCandidate"].model_validate(production_candidate_payload(case))

    assert candidate.observed_at_utc == case.observed_at_utc
    assert candidate.capture_id == case.capture_id
    assert candidate.captured_at_utc == case.captured_at_utc


def test_production_rejects_incomplete_capture_identity_pair() -> None:
    api = production_api()
    payload = production_candidate_payload(valid_candidate())
    payload["capture_id"] = "capture.calendar.session.a"
    payload["captured_at_utc"] = None

    with pytest.raises(Exception, match="capture_identity_time_mismatch"):
        api["CalendarFactCandidate"].model_validate(payload)


def test_production_rejects_unrecorded_or_non_applied_supersession() -> None:
    api = production_api()
    source = valid_candidate(candidate_id="session.source", value="13:30")
    correction = valid_candidate(
        candidate_id="session.correction",
        layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
        value="14:30",
        supersedes_candidate_id="session.source",
        supersession_reason="venue_correction",
    )
    snapshot_payload = production_snapshot_payload(
        valid_snapshot(session_candidates=(source,), operational_candidates=(correction,))
    )
    snapshot_payload["applied_supersessions"] = []
    with pytest.raises(Exception, match="applied_supersession_set_mismatch"):
        api["FinancialCalendarSnapshot"].model_validate(snapshot_payload)

    candidate_payload = production_candidate_payload(correction)
    candidate_payload["supersession_status"] = "proposed"
    with pytest.raises(Exception):
        api["CalendarFactCandidate"].model_validate(candidate_payload)


def test_production_projection_declares_and_fingerprints_canonicalisation_version() -> None:
    api, snapshot, policy, resolver = _production_subject()
    result = resolver.project(snapshot, policy, projection_id="projection.canonicalisation")

    assert result.canonicalisation_version == snapshot.canonicalisation_version
    forged = result.model_dump()
    forged["canonicalisation_version"] = "m02-k04-forged"
    with pytest.raises(Exception, match="projection_fingerprint_mismatch"):
        api["CalendarProjection"].model_validate(forged)


def test_semantic_continuity_m02_selected_field_preserves_type_and_unit() -> None:
    first = replace(
        valid_candidate(candidate_id="session.a", source_artifact_id="source.a"),
        value="13:30",
        value_type="local_time",
        unit="America/New_York",
    )
    second = replace(
        valid_candidate(
            candidate_id="session.b",
            layer=LayerCase.OPERATIONAL_CALENDAR_STATE,
            source_artifact_id="source.b",
        ),
        value="13:30",
        value_type="local_time",
        unit="America/New_York",
    )
    _, snapshot, policy, resolver = _production_subject(
        valid_snapshot(session_candidates=(first,), operational_candidates=(second,))
    )

    result = resolver.project(snapshot, policy, projection_id="projection.semantic.typed")

    assert result.status == "projected"
    assert result.selected_fields[0].value_type == "local_time"
    assert result.selected_fields[0].unit == "America/New_York"
