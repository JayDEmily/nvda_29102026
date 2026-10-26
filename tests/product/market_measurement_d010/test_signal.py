"""D010 actual delivered-live R005 and controlled open/liquid state."""

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 9, 14, tzinfo=UTC)
EVENT, RECEIPT, NOW = T - timedelta(seconds=10), T - timedelta(seconds=5), T + timedelta(seconds=1)
PROVIDER, VARIANT = "foundation-controlled-temporal", "clock_v1"
SAMPLE = "controlled-temporal-sample/1"
D001_BRIEF = "8eead9ba80813cd82244ce076af7a18fdef121474c0dd15a346aee814e892a98"
D003_BRIEF = "278623c1f97b5faacef1a95304672c92631a14010d5fde71efad4ff817207e1d"
BRIEF = "74d13a1058d4ecb89235c1789d54db1956f0857280665b064e666e8d5341f587"
META = (("sample.id", ("sample", "id")), ("value.role", ("value", "role")))
MAPS = (
    r.RawSignalProjectionMappingV1("mmt-d001-r002", 1, r.RawSignalCatalogueId("R002"),
                                   PROVIDER, VARIANT, ("time", "value"), "native_time", META),
    r.RawSignalProjectionMappingV1("mmt-d001-r003", 1, r.RawSignalCatalogueId("R003"),
                                   PROVIDER, VARIANT, ("time", "timezone"),
                                   "native_timezone", META),
    r.RawSignalProjectionMappingV1("mmt-d003-r004", 1, r.RawSignalCatalogueId("R004"),
                                   PROVIDER, VARIANT, ("time", "iana"), "IANA_timezone", META),
    r.RawSignalProjectionMappingV1("mmt-d004-r023", 1, r.RawSignalCatalogueId("R023"),
                                   PROVIDER, VARIANT, ("calendar", "session"),
                                   "session_identity", META),
    r.RawSignalProjectionMappingV1("mmt-d004-r024", 1, r.RawSignalCatalogueId("R024"),
                                   PROVIDER, VARIANT, ("calendar", "identity"),
                                   "calendar_identity", META),
    r.RawSignalProjectionMappingV1("mmt-d010-r005", 1, r.RawSignalCatalogueId("R005"),
                                   PROVIDER, VARIANT, ("market", "delivered_mode"),
                                   "marketDataType_enum", (*META,
                                       ("requested.mode", ("requested", "mode")),
                                       ("generation.id", ("generation", "id")))),
)
UNITS = (
    f.UnitConventionVersionV1("mmt-d001-temporal", 1, "native_time", "UTC_datetime",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d001-zone", 1, "native_timezone", "offset",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d003-iana", 1, "IANA_timezone", "IANA_timezone",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d004-session", 1, "session_identity", "session_identity",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d004-calendar", 1, "calendar_identity", "calendar_identity",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d010-mode", 1, "marketDataType_enum", "delivered_mode",
                              Decimal(1), Decimal(0)),
)
AUTHORITY = (
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
)
D001_DEF = f.CalculationDefinitionV1(
    "D001", "D001-TRUE-INSTANT-UTC-1", "K01_TIME",
    "same true instant converted to aware UTC", ("R002", "R003"), (),
    "P_TIME", "UTC_datetime", "aware_utc_datetime", AUTHORITY,
)
D001_PARAM = f.CalculationParameterSetV1("mmt-d001-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
D001_POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d001-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
D003_DEF = f.CalculationDefinitionV1(
    "D003", "D003-IANA-LOCAL-1", "K01_TIME",
    "same D001 instant in configured IANA exchange zone", ("R004",), ("D001",),
    "P_TIME", "local_datetime", "aware_iana_datetime", AUTHORITY,
)
D003_PARAM = f.CalculationParameterSetV1("mmt-d003-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
D003_POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d003-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def d001_request():
    return f.CalculationRequestV1(
        "D001", "NVDA", T, T, D001_DEF.calculation_definition_version,
        f.VersionRefV1(D001_PARAM.context_id, 1), f.VersionRefV1(D001_POLICY.context_id, 1), (),
        tuple(f.RawInputBindingV1(MAPS[i].raw_signal_catalogue_id.value,
                                  f.VersionRefV1(MAPS[i].mapping_id, 1),
                                  f.VersionRefV1(UNITS[i].context_id, 1), "NVDA") for i in (0, 1)),
    )


def d003_request(predecessor_id):
    return f.TemporalLocalRequestV1(
        f.CalculationRequestV1(
            "D003", "NVDA", T, T, D003_DEF.calculation_definition_version,
            f.VersionRefV1(D003_PARAM.context_id, 1), f.VersionRefV1(D003_POLICY.context_id, 1), (),
            (f.RawInputBindingV1("R004", f.VersionRefV1(MAPS[2].mapping_id, 1),
                                 f.VersionRefV1(UNITS[2].context_id, 1), "NVDA"),),
        ), predecessor_id,
    )


D010_MAPS = (MAPS[5], MAPS[3], MAPS[4])
D010_UNITS = (UNITS[5], UNITS[3], UNITS[4])
DEFINITION = f.CalculationDefinitionV1(
    "D010", "D010-LIVE-OPEN-LIQUID-1", "K01_TIME",
    "eligible live source AND known open calendar AND configured liquid phase",
    ("R005", "R023", "R024"), ("D003",), "P_TIME", "boolean", "market_open", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d010-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d010-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
def calendar():
    boundaries = tuple(datetime.fromisoformat(s).astimezone(UTC) for s in (
        "2026-10-09T00:00:00+11:00", "2026-10-09T16:00:00+11:00",
        "2026-10-10T06:00:00+11:00", "2026-10-10T16:00:00+11:00",
        "2026-10-11T00:00:00+11:00",
    ))
    return f.CalendarPolicyV1(
        f.VersionRefV1("controlled-overnight", 1), "Australia/Melbourne",
        boundaries[0], boundaries[-1],
        (f.CalendarIntervalV1(boundaries[0], boundaries[1], "closed", None),
         f.CalendarIntervalV1(boundaries[1], boundaries[2],
                              "overnight/1", date(2026, 10, 9)),
         f.CalendarIntervalV1(boundaries[2], boundaries[3], "day/1", date(2026, 10, 10)),
         f.CalendarIntervalV1(boundaries[3], boundaries[4], "closed", None)),
    )


def phases():
    bounds = tuple(datetime.fromisoformat(s).astimezone(UTC) for s in (
        "2026-10-10T00:00:00+11:00", "2026-10-10T06:00:00+11:00",
        "2026-10-10T16:00:00+11:00",
    ))
    intervals = (f.PhaseIntervalV1(bounds[0], bounds[1], "overnight"),
                 f.PhaseIntervalV1(bounds[1], bounds[2], "day"))
    return f.PhasePolicyV1(
        f.VersionRefV1("controlled-phases", 1),
        f.VersionRefV1("controlled-overnight", 1), "Australia/Melbourne", intervals,
    )


def market_state(refused):
    return f.MarketStatePolicyV1(
        f.VersionRefV1("controlled-market-state", 2 if refused else 1),
        f.VersionRefV1("controlled-overnight", 1),
        () if refused else (date(2026, 10, 10),), (),
    )


def mode_policy():
    return f.DeliveredModePolicyV1(
        f.VersionRefV1("controlled-delivered-mode", 1), "live", 1, "controlled-stream/1",
    )


def d010_request(predecessor_id, refused):
    return f.MarketOpenRequestV1(
        f.CalculationRequestV1(
            "D010", "NVDA", T, T, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
            (f.VersionRefV1("controlled-delivered-mode", 1),
             f.VersionRefV1("controlled-overnight", 1),
             f.VersionRefV1("controlled-phases", 1),
             f.VersionRefV1("controlled-market-state", 2 if refused else 1)),
            tuple(f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value, f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1(u.context_id, 1), "NVDA",
            ) for m, u in zip(D010_MAPS, D010_UNITS, strict=True)),
        ), predecessor_id, mode_policy(), calendar(), phases(), market_state(refused),
        ("overnight",),
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d010_signal(tmp_path, refused):
    raw = r.create_owner()
    natives = ("2026-10-10T00:59:50+11:00", "+11:00", "Australia/Melbourne",
               "overnight/1", "controlled-overnight/1", 1)
    roles = ("source_timestamp", "source_timezone", "exchange_iana",
             "session_identity", "calendar_identity", "delivered_market_mode")
    projected = []
    for index, mapping in enumerate(MAPS):
        if index < 3:
            container, field = "time", ("value", "timezone", "iana")[index]
        elif index < 5:
            container, field = "calendar", ("session", "identity")[index - 3]
        else:
            container, field = "market", "delivered_mode"
        native_record = {"sample": {"id": SAMPLE}, "value": {"role": roles[index]},
                         container: {field: natives[index]}}
        if index == 5:
            native_record.update(requested={"mode": "live"},
                                 generation={"id": "controlled-stream/1"})
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d010-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d010-controlled"),
            source_provider=r.provider_id(PROVIDER), native_record=native_record,
            received_ts_utc=RECEIPT, ingestion_sequence=index + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
            source_variant=VARIANT, subject_instrument="NVDA", native_units=mapping.native_units,
            source_timestamp_raw=natives[0] if index == 0 else "2026-10-09T13:59:50Z",
            source_timezone_native="+11:00" if index == 0 else "UTC",
        ))
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,), subject_instrument="NVDA",
            received_at_or_before_utc=T, event_at_or_before_utc=None, limit=100, cursor=None,
        )
        assert page.next_cursor is None and len(page.items) == 1
        item = page.items[0]
        assert item.native_value == natives[index] and item.received_ts_utc == RECEIPT
        assert item.observation_occurrence_id.value == f"d010-{index}"
        assert item.selection_identity.value_for("sample.id") == SAMPLE
        assert item.selection_identity.value_for("value.role") == roles[index]
        if index == 5:
            assert type(item.native_value) is int
            assert item.selection_identity.value_for("requested.mode") == "live"
            assert item.selection_identity.value_for("generation.id") == "controlled-stream/1"
        projected.append(item)
    d001 = f.create_temporal_owner(
        admission=f.OwnerAdmissionV1("M02", D001_BRIEF), raw_projection_reader=raw.reads,
        storage=f.MemoryStorageV1(), utc_now=lambda: NOW,
    )
    p001 = d001.materialise(d001_request())
    assert type(p001) is f.TemporalOccurrenceV1 and p001.result == EVENT
    assert tuple(line.projection for line in p001.raw_input_lineage) == tuple(projected[:2])
    d003 = f.create_temporal_local_owner(
        admission=f.OwnerAdmissionV1("M02", D003_BRIEF), raw_projection_reader=raw.reads,
        predecessor_reader=d001.reads, storage=f.MemoryStorageV1(), utc_now=lambda: NOW,
    )
    p003 = d003.materialise(d003_request(p001.derived_occurrence_id))
    assert type(p003) is f.TemporalLocalOccurrenceV1
    assert p003.result.isoformat() == "2026-10-10T00:59:50+11:00"
    assert p003.raw_input_lineage.projection == projected[2] and p003.predecessor == p001
    request = d010_request(p003.derived_occurrence_id, refused)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d010.sqlite")
    owner = f.create_market_open_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=d003.reads, storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    reader = f.create_market_open_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    history = dict(derived_signal_id="D010", subject_instrument="NVDA",
                   effective_at_or_before_utc=T, knowledge_at_or_before_utc=T, limit=10)
    if refused:
        assert projected[5].native_value == 1 and projected[3].native_value == "overnight/1"
        assert request.market_state_policy.open_dates == ()
        assert result is None
        assert owner.reads.list_derived_history(**history) == ()
        assert reader.list_derived_history(**history) == ()
        return
    assert type(result) is f.MarketOpenOccurrenceV1
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.projection_mappings == D010_MAPS and result.unit_conventions == D010_UNITS
    assert result.delivered_mode_lineage.projection == projected[5]
    assert result.delivered_mode_lineage.canonical_value == 1
    assert tuple(line.projection for line in result.calendar_lineage) == tuple(projected[3:5])
    assert result.predecessor == p003
    assert result.mode_policy == mode_policy() and result.calendar_policy == calendar()
    assert result.phase_policy == phases() and result.market_state_policy == market_state(False)
    assert result.liquid_phases == ("overnight",)
    assert result.implementation_brief_sha256 == BRIEF
    assert result.result is True and result.units == "boolean"
    assert result.result_shape == "market_open"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, T, NOW)
    assert result.derived_occurrence_id.startswith("mmtopen1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**history) == (result,)
