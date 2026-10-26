"""D003 actual public D001 and IANA identity: success and reached refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 9, 14, tzinfo=UTC)
EVENT, RECEIPT, NOW = T - timedelta(seconds=10), T - timedelta(seconds=5), T + timedelta(seconds=1)
PROVIDER, VARIANT = "foundation-controlled-temporal", "clock_v1"
SAMPLE = "controlled-temporal-sample/1"
D001_BRIEF = "bd023e56cbf27f4e2979587fb9e4deb288be329901fd46c7a78897f9b8b4139d"
BRIEF = "278623c1f97b5faacef1a95304672c92631a14010d5fde71efad4ff817207e1d"
META = (("sample.id", ("sample", "id")), ("value.role", ("value", "role")))
MAPS = (
    r.RawSignalProjectionMappingV1("mmt-d001-r002", 1, r.RawSignalCatalogueId("R002"),
                                   PROVIDER, VARIANT, ("time", "value"), "native_time", META),
    r.RawSignalProjectionMappingV1("mmt-d001-r003", 1, r.RawSignalCatalogueId("R003"),
                                   PROVIDER, VARIANT, ("time", "timezone"),
                                   "native_timezone", META),
    r.RawSignalProjectionMappingV1("mmt-d003-r004", 1, r.RawSignalCatalogueId("R004"),
                                   PROVIDER, VARIANT, ("time", "iana"), "IANA_timezone", META),
)
UNITS = (
    f.UnitConventionVersionV1("mmt-d001-temporal", 1, "native_time", "UTC_datetime",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d001-zone", 1, "native_timezone", "offset",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d003-iana", 1, "IANA_timezone", "IANA_timezone",
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
DEFINITION = f.CalculationDefinitionV1(
    "D003", "D003-IANA-LOCAL-1", "K01_TIME",
    "same D001 instant in configured IANA exchange zone", ("R004",), ("D001",),
    "P_TIME", "local_datetime", "aware_iana_datetime", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d003-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
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
            "D003", "NVDA", T, T, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1), (),
            (f.RawInputBindingV1("R004", f.VersionRefV1(MAPS[2].mapping_id, 1),
                                 f.VersionRefV1(UNITS[2].context_id, 1), "NVDA"),),
        ), predecessor_id,
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d003_signal(tmp_path, refused):
    raw = r.create_owner()
    natives = ("2026-10-10T00:59:50+11:00", "+11:00",
               "Unknown/Nowhere" if refused else "Australia/Melbourne")
    projected = []
    for index, mapping in enumerate(MAPS):
        role = ("source_timestamp", "source_timezone", "exchange_iana")[index]
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d003-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d003-controlled"),
            source_provider=r.provider_id(PROVIDER),
            native_record={"sample": {"id": SAMPLE}, "value": {"role": role},
                           "time": {("value", "timezone", "iana")[index]: natives[index]}},
            received_ts_utc=RECEIPT, ingestion_sequence=index + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
            source_variant=VARIANT, subject_instrument="NVDA", native_units=mapping.native_units,
            source_timestamp_raw=(natives[0], "2026-10-09T13:59:50Z",
                                  "2026-10-09T13:59:50Z")[index],
            source_timezone_native=("+11:00", "UTC", "UTC")[index],
        ))
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,), subject_instrument="NVDA",
            received_at_or_before_utc=T, event_at_or_before_utc=None, limit=100, cursor=None,
        )
        assert page.next_cursor is None and len(page.items) == 1
        item = page.items[0]
        assert item.native_value == natives[index] and item.received_ts_utc == RECEIPT
        assert item.observation_occurrence_id.value == f"d003-{index}"
        assert item.selection_identity == r.RawSelectionIdentityV1((("sample.id", SAMPLE),
                                                                    ("value.role", role)))
        projected.append(item)
    d001 = f.create_temporal_owner(
        admission=f.OwnerAdmissionV1("M02", D001_BRIEF), raw_projection_reader=raw.reads,
        storage=f.MemoryStorageV1(), utc_now=lambda: NOW,
    )
    predecessor = d001.materialise(d001_request())
    assert type(predecessor) is f.TemporalOccurrenceV1
    assert predecessor.result == EVENT
    assert tuple(line.projection for line in predecessor.raw_input_lineage) == tuple(projected[:2])
    request = d003_request(predecessor.derived_occurrence_id)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d003.sqlite")
    owner = f.create_temporal_local_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=d001.reads, storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    reader = f.create_temporal_local_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    history = dict(derived_signal_id="D003", subject_instrument="NVDA",
                   effective_at_or_before_utc=T, knowledge_at_or_before_utc=T, limit=10)
    if refused:
        assert projected[2].native_value == "Unknown/Nowhere"
        assert result is None
        assert owner.reads.list_derived_history(**history) == ()
        assert reader.list_derived_history(**history) == ()
        return
    assert type(result) is f.TemporalLocalOccurrenceV1
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.projection_mapping == MAPS[2] and result.unit_convention == UNITS[2]
    assert result.raw_input_lineage.projection == projected[2]
    assert result.raw_input_lineage.canonical_value == "Australia/Melbourne"
    assert result.predecessor == predecessor
    assert result.implementation_brief_sha256 == BRIEF
    assert result.result.isoformat() == "2026-10-10T00:59:50+11:00"
    assert result.result.tzinfo.key == "Australia/Melbourne"
    assert result.result.astimezone(UTC) == predecessor.result
    assert result.units == "local_datetime" and result.result_shape == "aware_iana_datetime"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, T, NOW)
    assert result.derived_occurrence_id.startswith("mmtlocal1:")
    reopened = reader.get_derived_occurrence(result.derived_occurrence_id)
    assert reopened == result and reopened.result.tzinfo.key == "Australia/Melbourne"
    assert reader.list_derived_history(**history) == (result,)
