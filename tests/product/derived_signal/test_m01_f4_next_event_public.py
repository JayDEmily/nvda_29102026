"""F4 RC01: D062 public event countdown from M00 native future schedule records."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 1, tzinfo=UTC)
CLOCK = NOW - timedelta(seconds=5)
FIELDS = ("R001", "R002", "R003", "R284")


def event_owner(
    *, omit: str | None = None, targets: tuple[int, ...] = (300, 120, -30),
    future_received: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    native_clock = {"R001": "macro", "R002": CLOCK.isoformat(), "R003": "UTC"}
    m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
        concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw.observation_occurrence_id("rc01-clock"),
        delivery_artifact_ref=raw.delivery_artifact_ref("rc01-clock"),
        source_provider=raw.provider_id("controlled-clock"),
        native_record={"clock": native_clock},
        received_ts_utc=CLOCK,
        ingestion_sequence=1,
        ingestion_sequence_scope=raw.ingestion_sequence_scope("rc01:clock"),
        source_temporal_kind="true_instant",
        source_timestamp_raw=CLOCK.isoformat(),
        source_timezone_native="UTC",
        raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in FIELDS[:3]),
        source_variant="clock", subject_instrument="NVDA",
        native_units="native_time", revision_vintage_native="v1",
    ))
    for i, seconds in enumerate(targets):
        time = NOW + timedelta(seconds=seconds)
        observed = NOW + timedelta(seconds=3) if future_received else CLOCK
        m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id(f"rc01-event-{seconds}"),
            delivery_artifact_ref=raw.delivery_artifact_ref(f"rc01-event-{seconds}"),
            source_provider=raw.provider_id("controlled-calendar"),
            native_record={"event": {"target": time.isoformat()}},
            received_ts_utc=observed,
            ingestion_sequence=i + 1,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("rc01:calendar"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=observed.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=(raw.RawSignalCatalogueId("R284"),),
            source_variant="calendar", subject_instrument="NVDA",
            native_units="utc_iso8601", revision_vintage_native="v1",
        ))
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(raw.RawSignalProjectionMappingV1(
            "event-map-"+rid, 1, raw.RawSignalCatalogueId(rid),
            "controlled-calendar" if rid == "R284" else "controlled-clock",
            "calendar" if rid == "R284" else "clock",
            ("event", "target") if rid == "R284" else ("clock", rid),
            "utc_iso8601" if rid == "R284" else "native_time",
        ) for rid in FIELDS),
        parameter_sets=(api.CalculationParameterSetV1(
            "event-time", 1, "P_TIME", (("exchange_timezone", "UTC"),),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "event-select", 1, ("subject_instrument",), timedelta(seconds=30),
            timedelta(seconds=30), ("true_instant",), (),
        ),),
        unit_conventions=tuple(api.UnitConventionVersionV1(
            "event-unit-" + rid, 1, "utc_iso8601" if rid == "R284" else "native_time",
            "utc_iso8601" if rid == "R284" else "native_time", Decimal(1), Decimal(0),
        ) for rid in FIELDS),
        contexts=(), utc_now=lambda: NOW + timedelta(seconds=1),
    )
    req = api.CalculationRequestV1(
        "D062", "NVDA", NOW, NOW, "event-countdown", "event-time", 1,
        "event-select", 1, (), raw_input_bindings=tuple(api.RawInputBindingV1(
            rid, api.VersionRefV1("event-map-"+rid, 1),
            api.VersionRefV1("event-unit-"+rid, 1), "NVDA", None,
        ) for rid in FIELDS if rid != omit),
    )
    return owner, req


def test_rc01_public_next_future_event_earliest_result_lineage_and_retry() -> None:
    owner, req = event_owner()
    out = owner.materialise(req)
    assert out is not None
    assert out.result == (("seconds", Decimal(120)), ("minutes", Decimal(2)))
    # D001 declares R002/R003; R001 is not an input to either D001 or D062.
    assert {r.raw_signal_id for r in out.raw_input_lineage} == {"R002", "R003", "R284"}
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        "rc01-clock", "rc01-event-300", "rc01-event-120", "rc01-event--30",
    }
    assert len(out.predecessor_occurrence_ids) == 1
    d001 = owner.reads.get_derived_occurrence(out.predecessor_occurrence_ids[0])
    assert d001 is not None and d001.derived_signal_id == "D001"
    assert d001.result == CLOCK
    assert owner.materialise(req) == out


def test_rc01_public_event_countdown_refuses_absent_or_past_only_schedule() -> None:
    owner, req = event_owner(targets=(-30, -10))
    assert owner.materialise(req) is None
    owner, req = event_owner(omit="R284", targets=(120,))
    assert owner.materialise(req) is None


def test_rc01_public_event_countdown_refuses_future_received_schedule() -> None:
    owner, req = event_owner(targets=(120,), future_received=True)
    assert owner.materialise(req) is None
