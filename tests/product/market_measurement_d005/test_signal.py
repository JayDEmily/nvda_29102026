"""D005 actual D003 with a separate versioned phase schedule."""

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
BRIEF = "07c01c3e34a1f93f4f004d67d01a05efe353eeeb9b26e6bb4165b1a8702383bb"
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


D005_DEF = f.CalculationDefinitionV1(
    "D005", "D005-ORDERED-SESSION-PHASE-1", "K01_TIME",
    "configured half-open ordered nonoverlapping local session phase",
    ("R023", "R024"), ("D003",), "P_TIME", "category", "session_phase", AUTHORITY,
)
D005_PARAM = f.CalculationParameterSetV1("mmt-d005-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
D005_POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d005-selection", 1, ("subject_instrument", "sample.id"),
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


def phases(refused):
    bounds = tuple(datetime.fromisoformat(s).astimezone(UTC) for s in (
        "2026-10-10T00:00:00+11:00", "2026-10-10T06:00:00+11:00",
        "2026-10-10T16:00:00+11:00",
    ))
    intervals = (f.PhaseIntervalV1(bounds[1], bounds[2], "day"),)
    if not refused:
        intervals = (f.PhaseIntervalV1(bounds[0], bounds[1], "overnight"), *intervals)
    return f.PhasePolicyV1(
        f.VersionRefV1("controlled-phases", 2 if refused else 1),
        f.VersionRefV1("controlled-overnight", 1), "Australia/Melbourne", intervals,
    )


def d005_request(predecessor_id, refused):
    return f.TemporalPhaseRequestV1(
        f.CalculationRequestV1(
            "D005", "NVDA", T, T, D005_DEF.calculation_definition_version,
            f.VersionRefV1(D005_PARAM.context_id, 1), f.VersionRefV1(D005_POLICY.context_id, 1),
            (f.VersionRefV1("controlled-overnight", 1),
             f.VersionRefV1("controlled-phases", 2 if refused else 1)),
            tuple(f.RawInputBindingV1(
                MAPS[i].raw_signal_catalogue_id.value, f.VersionRefV1(MAPS[i].mapping_id, 1),
                f.VersionRefV1(UNITS[i].context_id, 1), "NVDA",
            ) for i in (3, 4)),
        ), predecessor_id, calendar(), phases(refused),
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d005_signal(tmp_path, refused):
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
            observation_occurrence_id=r.observation_occurrence_id(f"d005-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d005-controlled"),
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
        assert item.observation_occurrence_id.value == f"d005-{index}"
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
    request = d005_request(p003.derived_occurrence_id, refused)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d005.sqlite")
    owner = f.create_temporal_phase_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=d003.reads, storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    reader = f.create_temporal_phase_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    history = dict(derived_signal_id="D005", subject_instrument="NVDA",
                   effective_at_or_before_utc=T, knowledge_at_or_before_utc=T, limit=10)
    if refused:
        assert tuple(item.native_value for item in projected[3:]) == (
            "overnight/1", "controlled-overnight/1",
        )
        assert request.phase_policy.intervals == (
            f.PhaseIntervalV1(
                datetime.fromisoformat("2026-10-10T06:00:00+11:00").astimezone(UTC),
                datetime.fromisoformat("2026-10-10T16:00:00+11:00").astimezone(UTC), "day",
            ),
        )
        assert result is None
        assert owner.reads.list_derived_history(**history) == ()
        assert reader.list_derived_history(**history) == ()
        return
    assert type(result) is f.TemporalPhaseOccurrenceV1
    assert result.request == request and result.definition == D005_DEF
    assert result.parameter_set == D005_PARAM and result.input_selection_policy == D005_POLICY
    assert result.projection_mappings == MAPS[3:] and result.unit_conventions == UNITS[3:]
    assert tuple(line.projection for line in result.raw_input_lineage) == tuple(projected[3:])
    assert result.predecessor == p003 and result.calendar_policy == calendar()
    assert result.phase_policy == phases(False)
    assert result.implementation_brief_sha256 == BRIEF
    assert result.result == "overnight"
    assert result.units == "category" and result.result_shape == "session_phase"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, T, NOW)
    assert result.derived_occurrence_id.startswith("mmtphase1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**history) == (result,)
