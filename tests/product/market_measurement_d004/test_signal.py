"""D004 actual D001/D003 and complete synthetic overnight calendar."""

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 9, 14, tzinfo=UTC)
EVENT, RECEIPT, NOW = T - timedelta(seconds=10), T - timedelta(seconds=5), T + timedelta(seconds=1)
PROVIDER, VARIANT = "foundation-controlled-temporal", "clock_v1"
SAMPLE = "controlled-temporal-sample/1"
D001_BRIEF = "bd023e56cbf27f4e2979587fb9e4deb288be329901fd46c7a78897f9b8b4139d"
D003_BRIEF = "278623c1f97b5faacef1a95304672c92631a14010d5fde71efad4ff817207e1d"
BRIEF = "94ac73562afcbb34af75cd9cd72c7b94783ecb4c4d857beecc7690340d61b495"
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


D004_DEF = f.CalculationDefinitionV1(
    "D004", "D004-OVERNIGHT-TRADING-DATE-1", "K01_TIME",
    "configured session trading date, including overnight attribution",
    ("R023", "R024"), ("D003",), "P_TIME", "date", "exchange_trading_date", AUTHORITY,
)
D004_PARAM = f.CalculationParameterSetV1("mmt-d004-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
D004_POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d004-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def calendar(refused):
    boundaries = tuple(datetime.fromisoformat(s).astimezone(UTC) for s in (
        "2026-10-09T00:00:00+11:00", "2026-10-09T16:00:00+11:00",
        "2026-10-10T06:00:00+11:00", "2026-10-10T16:00:00+11:00",
        "2026-10-11T00:00:00+11:00",
    ))
    return f.CalendarPolicyV1(
        f.VersionRefV1("controlled-overnight", 2 if refused else 1),
        "Australia/Melbourne", boundaries[0], boundaries[-1],
        (f.CalendarIntervalV1(boundaries[0], boundaries[1], "closed", None),
         f.CalendarIntervalV1(boundaries[1], boundaries[2],
                              "closed" if refused else "overnight/1",
                              None if refused else date(2026, 10, 9)),
         f.CalendarIntervalV1(boundaries[2], boundaries[3], "day/1", date(2026, 10, 10)),
         f.CalendarIntervalV1(boundaries[3], boundaries[4], "closed", None)),
    )


def d004_request(predecessor_id, refused):
    return f.TemporalDateRequestV1(
        f.CalculationRequestV1(
            "D004", "NVDA", T, T, D004_DEF.calculation_definition_version,
            f.VersionRefV1(D004_PARAM.context_id, 1), f.VersionRefV1(D004_POLICY.context_id, 1),
            (f.VersionRefV1("controlled-overnight", 2 if refused else 1),),
            tuple(f.RawInputBindingV1(
                MAPS[i].raw_signal_catalogue_id.value, f.VersionRefV1(MAPS[i].mapping_id, 1),
                f.VersionRefV1(UNITS[i].context_id, 1), "NVDA",
            ) for i in (3, 4)),
        ), predecessor_id, calendar(refused),
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d004_signal(tmp_path, refused):
    raw = r.create_owner()
    natives = ("2026-10-10T00:59:50+11:00", "+11:00", "Australia/Melbourne",
               "overnight/1", "controlled-overnight/1")
    projected = []
    for index, mapping in enumerate(MAPS):
        role = ("source_timestamp", "source_timezone", "exchange_iana",
                "session_identity", "calendar_identity")[index]
        container = "time" if index < 3 else "calendar"
        field = ("value", "timezone", "iana", "session", "identity")[index]
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d004-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d004-controlled"),
            source_provider=r.provider_id(PROVIDER),
            native_record={"sample": {"id": SAMPLE}, "value": {"role": role},
                           container: {field: natives[index]}},
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
        assert item.observation_occurrence_id.value == f"d004-{index}"
        assert item.selection_identity == r.RawSelectionIdentityV1((("sample.id", SAMPLE),
                                                                    ("value.role", role)))
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
    request = d004_request(p003.derived_occurrence_id, refused)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d004.sqlite")
    owner = f.create_temporal_date_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=d003.reads, storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    reader = f.create_temporal_date_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    history = dict(derived_signal_id="D004", subject_instrument="NVDA",
                   effective_at_or_before_utc=T, knowledge_at_or_before_utc=T, limit=10)
    if refused:
        assert projected[3].native_value == "overnight/1"
        assert request.calendar_policy.intervals[1].session_id == "closed"
        assert result is None
        assert owner.reads.list_derived_history(**history) == ()
        assert reader.list_derived_history(**history) == ()
        return
    assert type(result) is f.TemporalDateOccurrenceV1
    assert result.request == request and result.definition == D004_DEF
    assert result.parameter_set == D004_PARAM and result.input_selection_policy == D004_POLICY
    assert result.projection_mappings == MAPS[3:] and result.unit_conventions == UNITS[3:]
    assert tuple(line.projection for line in result.raw_input_lineage) == tuple(projected[3:])
    assert result.predecessor == p003 and result.calendar_policy == calendar(False)
    assert result.implementation_brief_sha256 == BRIEF
    assert result.result == date(2026, 10, 9)
    assert result.result != p003.result.date()
    assert result.units == "date" and result.result_shape == "exchange_trading_date"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, T, NOW)
    assert result.derived_occurrence_id.startswith("mmtdate1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**history) == (result,)
