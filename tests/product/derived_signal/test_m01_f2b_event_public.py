"""F2b authority-derived red proofs: real M00 mapping, isolated event revisions.

The controlled field paths are proof schema only; no live provider is asserted.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 4, tzinfo=UTC)
EVENT = "macro-A"


def _identity(event: str) -> raw.RawSelectionIdentityV1:
    return raw.RawSelectionIdentityV1((("event_id", event),))


def _feature() -> api.ScoreFeatureV1:
    return api.ScoreFeatureV1(
        signal_id="R289",
        extractor="component",
        extractor_arguments=(),
        transform="identity",
        transform_scale=None,
        orientation=1,
        weight=Decimal("1"),
        clip_min=None,
        clip_max=None,
        baseline_values=(),
    )


def _fixture(
    observations: tuple[tuple[str, str, int, str, Decimal | str], ...],
    *,
    provider: str = "controlled-a",
    variant: str = "event-calendar",
    importance_feature: api.ScoreFeatureV1 | None = None,
    importance_provider: str | None = None,
    ambiguous_revision: bool = False,
) -> tuple[
    api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1, raw.RawSignalOccurrenceOwnerV1
]:
    """Observation tuple: (R id, event id, receipt seconds, observation id, value)."""
    m00 = raw.create_owner()
    for sequence, (rid, event_id, seconds, observation_id, value) in enumerate(observations, 1):
        native = {
            "event": {
                "id": event_id,
                "scheduled": value if rid == "R284" else NOW.isoformat(),
                "importance": value if rid == "R289" else Decimal("0"),
            }
        }
        obs = raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id(observation_id),
            delivery_artifact_ref=raw.delivery_artifact_ref("deliver-" + observation_id),
            source_provider=raw.provider_id(
                importance_provider or provider if rid == "R289" else provider
            ),
            native_record=native,
            received_ts_utc=NOW + timedelta(seconds=seconds),
            ingestion_sequence=1 if ambiguous_revision and rid == "R284" else sequence,
            ingestion_sequence_scope=raw.ingestion_sequence_scope(
                (importance_provider or provider if rid == "R289" else provider) + ":" + variant
            ),
            source_temporal_kind="receipt_only",
            raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
            source_variant=variant,
            subject_instrument="NVDA",
            native_units="native_event",
            revision_vintage_native=f"v{sequence}",
        )
        m00.commands.admit_raw_observation_occurrence(obs)

    mappings = (
        raw.RawSignalProjectionMappingV1(
            mapping_id="controlled:R284",
            version=1,
            raw_signal_catalogue_id=raw.RawSignalCatalogueId("R284"),
            source_provider=provider,
            source_variant=variant,
            native_field_path=("event", "scheduled"),
            native_units="utc_iso8601",
            selection_identity_field_paths=(("event_id", ("event", "id")),),
        ),
        raw.RawSignalProjectionMappingV1(
            mapping_id="controlled:R289",
            version=1,
            raw_signal_catalogue_id=raw.RawSignalCatalogueId("R289"),
            source_provider=importance_provider or provider,
            source_variant=variant,
            native_field_path=("event", "importance"),
            native_units="score",
            selection_identity_field_paths=(("event_id", ("event", "id")),),
        ),
    )
    units = tuple(
        api.UnitConventionVersionV1(
            context_id="unit:" + name,
            version=1,
            native_units=name,
            canonical_units=name,
            scale=Decimal(1),
            offset=Decimal(0),
        )
        for name in ("utc_iso8601", "score")
    )
    score = api.CalculationParameterSetV1(
        context_id="score-event",
        version=1,
        profile="P_SCORE",
        parameters=(("intercept", Decimal("0.1")),),
        score_features=(importance_feature or _feature(),),
    )
    rule = api.CalculationParameterSetV1(
        context_id="event-rule",
        version=1,
        profile="P_RULE",
        parameters=(
            ("pre_window_seconds", Decimal("120")),
            ("post_window_seconds", Decimal("120")),
            ("importance_threshold", Decimal("0.7")),
        ),
    )
    time = api.CalculationParameterSetV1(
        context_id="event-time",
        version=1,
        profile="P_TIME",
        parameters=(("selection_mode", "exact"),),
    )
    policy = api.InputSelectionPolicyVersionV1(
        context_id="events-visible",
        version=1,
        join_keys=("subject_instrument",),
        maximum_staleness=timedelta(hours=1),
        maximum_skew=timedelta(hours=1),
        temporal_basis_permissions=("receipt_only",),
        basket_membership=(),
    )
    child = api.InputSelectionPolicyVersionV1(
        context_id="one-event",
        version=1,
        join_keys=("event_id",),
        maximum_staleness=timedelta(hours=1),
        maximum_skew=timedelta(hours=1),
        temporal_basis_permissions=("receipt_only",),
        basket_membership=(),
    )
    bindings = tuple(
        api.RawInputBindingV1(
            raw_id,
            api.VersionRefV1("controlled:" + raw_id, 1),
            api.VersionRefV1("unit:" + unit, 1),
            "NVDA",
        )
        for raw_id, unit in (("R284", "utc_iso8601"), ("R289", "score"))
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(score, rule, time),
        input_selection_policies=(policy, child),
        unit_conventions=units,
        contexts=(),
        utc_now=lambda: NOW + timedelta(hours=1),
    )
    request = api.CalculationRequestV1(
        derived_signal_id="D065",
        subject_instrument="NVDA",
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        calculation_definition_version="calc-f2b",
        parameter_set_id="event-rule",
        parameter_set_version=1,
        input_selection_policy_id="events-visible",
        input_selection_policy_version=1,
        context_refs=(),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "score-event", 1),
            api.ParameterProfileRefV1("P_TIME", "event-time", 1),
        ),
        raw_input_bindings=bindings,
        predecessor_selection_policy_refs=(("D064", api.VersionRefV1("one-event", 1)),),
    )
    return owner, request, m00


def _obs(
    rid: str, event: str, receipt: int, tag: str, value: Decimal | str
) -> tuple[str, str, int, str, Decimal | str]:
    return rid, event, receipt, tag, value


def _base() -> tuple[tuple[str, str, int, str, Decimal | str], ...]:
    return (
        _obs("R284", EVENT, -30, "schedule-a-1", (NOW + timedelta(seconds=70)).isoformat()),
        _obs("R289", EVENT, -20, "importance-a-1", Decimal("0.8")),
    )


def _request_at(
    req: api.CalculationRequestV1, *, cutoff: int = 0, at: int = 0
) -> api.CalculationRequestV1:
    return replace(
        req,
        as_of_utc=NOW + timedelta(seconds=at),
        knowledge_cutoff_utc=NOW + timedelta(seconds=cutoff),
    )


def test_d064_raw_score_uses_native_projection_and_exact_lineage() -> None:
    owner, request, _ = _fixture(_base())
    result = owner.materialise(
        replace(
            request,
            derived_signal_id="D064",
            parameter_set_id="score-event",
            input_selection_policy_id="one-event",
            raw_input_bindings=(
                replace(request.raw_input_bindings[1], selection_identity=_identity(EVENT)),
            ),
        )
    )
    assert result is not None
    assert result.result == Decimal("0.9")
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {"importance-a-1"}
    assert (
        result.selection_identity is not None
        and result.selection_identity.value_for("event_id") == EVENT
    )


def test_d065_same_event_competing_identity_and_lineage() -> None:
    other = (
        _obs("R284", "macro-B", -15, "schedule-b-1", (NOW + timedelta(seconds=40)).isoformat()),
        _obs("R289", "macro-B", -10, "importance-b-1", Decimal("0.2")),
    )
    owner, request, _ = _fixture((*_base(), *other))
    result = owner.materialise(request)
    assert result is not None and result.result is False  # B is nearer than A.
    assert {
        x.observation_occurrence_id for x in result.raw_input_lineage if x.raw_signal_id == "R284"
    } == {"schedule-a-1", "schedule-b-1"}  # Both revisions determined nearest selection.
    assert {
        x.observation_occurrence_id for x in result.raw_input_lineage if x.raw_signal_id == "R289"
    } == {"importance-b-1"}
    assert len(result.predecessor_occurrence_ids) >= 1
    assert owner.materialise(request) == result


def test_d065_revision_and_knowledge_cutoff_do_not_look_ahead() -> None:
    revisions = (
        _obs("R284", EVENT, 30, "schedule-a-2", (NOW + timedelta(seconds=300)).isoformat()),
        _obs("R289", EVENT, 40, "importance-a-2", Decimal("0.1")),
    )
    owner, request, _ = _fixture((*_base(), *revisions))
    earlier = owner.materialise(request)
    assert earlier is not None and earlier.result is True
    later = owner.materialise(_request_at(request, cutoff=45, at=45))
    assert later is not None and later.result is False
    assert {
        x.observation_occurrence_id for x in earlier.raw_input_lineage if x.raw_signal_id == "R289"
    } == {"importance-a-1"}
    # Scheduled revision moved outside window: TRUE becomes FALSE without
    # consulting importance (so the new R289 is correctly absent from lineage).
    assert not any(x.raw_signal_id == "R289" for x in later.raw_input_lineage)
    assert {
        x.observation_occurrence_id for x in later.raw_input_lineage if x.raw_signal_id == "R284"
    } == {"schedule-a-2"}
    assert earlier.derived_occurrence_id != later.derived_occurrence_id


def test_d065_missing_importance_is_absence_not_false() -> None:
    owner, request, _ = _fixture((_base()[0],))
    assert owner.materialise(request) is None


def test_d065_ambiguous_or_missing_event_identity_is_refused() -> None:
    owner, request, _ = _fixture(_base())
    assert owner.materialise(replace(request, predecessor_selection_policy_refs=())) is None
    bad = replace(request.raw_input_bindings[0], selection_identity=_identity("nonexistent"))
    assert (
        owner.materialise(replace(request, raw_input_bindings=(bad, request.raw_input_bindings[1])))
        is None
    )


def test_d064_refuses_undeclared_or_unavailable_score_extraction() -> None:
    rogue = replace(_feature(), signal_id="R284")
    owner, request, _ = _fixture(_base(), importance_feature=rogue)
    score_request = replace(
        request,
        derived_signal_id="D064",
        parameter_set_id="score-event",
        input_selection_policy_id="one-event",
        raw_input_bindings=(
            replace(request.raw_input_bindings[1], selection_identity=_identity(EVENT)),
        ),
    )
    assert owner.materialise(score_request) is None


def test_d065_new_importance_revision_changes_applicability_with_same_event() -> None:
    owner, request, _ = _fixture(
        (
            *_base(),
            _obs("R289", EVENT, 30, "importance-a-2", Decimal("0.2")),
        )
    )
    before = owner.materialise(request)
    after = owner.materialise(_request_at(request, cutoff=35, at=35))
    assert before is not None and before.result is True
    assert after is not None and after.result is False
    assert {
        v.observation_occurrence_id for v in after.raw_input_lineage if v.raw_signal_id == "R289"
    } == {"importance-a-2"}
    assert after.predecessor_occurrence_ids
    assert before.derived_occurrence_id != after.derived_occurrence_id


def test_d065_same_event_id_different_provider_is_not_equivalent() -> None:
    owner, request, _ = _fixture(_base(), importance_provider="controlled-b")
    assert owner.materialise(request) is None


def test_d065_event_outside_window_returns_actual_false_without_score() -> None:
    event = _obs("R284", EVENT, -30, "schedule-far", (NOW + timedelta(hours=4)).isoformat())
    owner, request, _ = _fixture((event,))
    result = owner.materialise(request)
    assert result is not None and result.result is False
    assert {
        v.observation_occurrence_id for v in result.raw_input_lineage if v.raw_signal_id == "R284"
    } == {"schedule-far"}
    assert not any(v.raw_signal_id == "R289" for v in result.raw_input_lineage)


def test_d065_invalid_timestamp_or_duplicate_revision_fails_closed() -> None:
    invalid = _obs("R284", EVENT, -30, "invalid-time", "not-a-time")
    owner, request, _ = _fixture((invalid, _base()[1]))
    assert owner.materialise(request) is None
    # A same-knowledge-instant, same sequence ambiguity cannot be inferred
    # from UUID lexical ordering. The exact ambiguity is exercised separately
    # in a kernel-level proof using the same canonical M00 projection metadata.


def test_d065_incompatible_r289_mapping_version_fails_closed() -> None:
    owner, request, _ = _fixture(_base())
    bindings = (
        request.raw_input_bindings[0],
        replace(
            request.raw_input_bindings[1],
            projection_mapping_ref=api.VersionRefV1("controlled:R289", 2),
        ),
    )
    assert owner.materialise(replace(request, raw_input_bindings=bindings)) is None


def test_d064_missing_feature_does_not_implicitly_convert_category() -> None:
    owner, request, _ = _fixture((_base()[0], _obs("R289", EVENT, -20, "category-a", "high")))
    score_request = replace(
        request,
        derived_signal_id="D064",
        parameter_set_id="score-event",
        input_selection_policy_id="one-event",
        raw_input_bindings=(
            replace(request.raw_input_bindings[1], selection_identity=_identity(EVENT)),
        ),
    )
    assert owner.materialise(score_request) is None


def test_d065_true_after_event_when_no_upcoming_d062_exists() -> None:
    observations = (
        _obs("R284", EVENT, -30, "schedule-past", (NOW - timedelta(seconds=45)).isoformat()),
        _obs("R289", EVENT, -20, "importance-past", Decimal("0.85")),
    )
    owner, request, _ = _fixture(observations)
    result = owner.materialise(request)
    assert result is not None and result.result is True
    assert result.predecessor_occurrence_ids
    assert {r.raw_signal_id for r in result.raw_input_lineage} == {"R284", "R289"}


def test_d065_competing_events_at_identical_instants_are_ambiguous() -> None:
    observations = (
        _obs("R284", EVENT, -30, "same-time-a", (NOW + timedelta(seconds=50)).isoformat()),
        _obs("R284", "macro-B", -20, "same-time-b", (NOW + timedelta(seconds=50)).isoformat()),
        _obs("R289", EVENT, -15, "importance-a", Decimal("0.9")),
        _obs("R289", "macro-B", -10, "importance-b", Decimal("0.2")),
    )
    owner, request, _ = _fixture(observations)
    assert owner.materialise(request) is None


def test_d065_equal_receipt_and_ingestion_revision_precedence_refuses() -> None:
    observations = (
        _obs("R284", EVENT, -30, "dup-schedule-1", (NOW + timedelta(seconds=60)).isoformat()),
        _obs("R284", EVENT, -30, "dup-schedule-2", (NOW + timedelta(seconds=80)).isoformat()),
        _obs("R289", EVENT, -20, "importance-a", Decimal("0.9")),
    )
    owner, request, _ = _fixture(observations, ambiguous_revision=True)
    assert owner.materialise(request) is None


def test_d064_applies_configured_k07_orientation_weight_and_clipping() -> None:
    feature = replace(
        _feature(),
        orientation=-1,
        weight=Decimal("0.5"),
        clip_max=Decimal("0.5"),
    )
    owner, request, _ = _fixture(_base(), importance_feature=feature)
    score_request = replace(
        request,
        derived_signal_id="D064",
        parameter_set_id="score-event",
        input_selection_policy_id="one-event",
        raw_input_bindings=(
            replace(request.raw_input_bindings[1], selection_identity=_identity(EVENT)),
        ),
    )
    result = owner.materialise(score_request)
    assert result is not None and result.result == Decimal("-0.15")


def test_d065_equal_distance_tie_prefers_earlier_event() -> None:
    observations = (
        _obs("R284", "early", -30, "event-early", (NOW - timedelta(seconds=60)).isoformat()),
        _obs("R289", "early", -20, "importance-early", Decimal("0.85")),
        _obs("R284", "late", -10, "event-late", (NOW + timedelta(seconds=60)).isoformat()),
        _obs("R289", "late", -5, "importance-late", Decimal("0.1")),
    )
    owner, request, _ = _fixture(observations)
    result = owner.materialise(request)
    assert result is not None and result.result is True
    assert result.selection_identity is not None
    assert result.selection_identity.value_for("event_id") == "early"
    assert {
        r.observation_occurrence_id for r in result.raw_input_lineage if r.raw_signal_id == "R284"
    } == {"event-early", "event-late"}
    assert {
        r.observation_occurrence_id for r in result.raw_input_lineage if r.raw_signal_id == "R289"
    } == {"importance-early"}


def test_d064_uses_explicit_component_coefficients_from_native_r289() -> None:
    feature = replace(
        _feature(),
        extractor="weighted_component_sum",
        extractor_arguments=(
            "impact",
            Decimal("0.7"),
            "historical_sensitivity",
            Decimal("0.3"),
        ),
    )
    native_fields = {"impact": Decimal("0.6"), "historical_sensitivity": Decimal("0.4")}
    owner, request, _ = _fixture(
        (_base()[0], _obs("R289", EVENT, -20, "structured-importance", native_fields)),
        importance_feature=feature,
    )
    score_request = replace(
        request,
        derived_signal_id="D064",
        parameter_set_id="score-event",
        input_selection_policy_id="one-event",
        raw_input_bindings=(
            replace(request.raw_input_bindings[1], selection_identity=_identity(EVENT)),
        ),
    )
    score = owner.materialise(score_request)
    assert score is not None and score.result == Decimal("0.64")
    assert {r.observation_occurrence_id for r in score.raw_input_lineage} == {
        "structured-importance"
    }
