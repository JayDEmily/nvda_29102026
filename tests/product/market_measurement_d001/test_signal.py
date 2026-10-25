"""D001 controlled UTC true-instant conversion and reached date-only refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 9, 14, tzinfo=UTC)
EVENT = T - timedelta(seconds=10)
RECEIPT = T - timedelta(seconds=5)
NOW = T + timedelta(seconds=1)
PROVIDER, VARIANT = "foundation-controlled-temporal", "clock_v1"
BRIEF = "bd023e56cbf27f4e2979587fb9e4deb288be329901fd46c7a78897f9b8b4139d"
META = (("sample.id", ("sample", "id")), ("value.role", ("value", "role")))
MAPS = (
    r.RawSignalProjectionMappingV1(
        "mmt-d001-r002", 1, r.RawSignalCatalogueId("R002"), PROVIDER,
        VARIANT, ("time", "value"), "native_time", META,
    ),
    r.RawSignalProjectionMappingV1(
        "mmt-d001-r003", 1, r.RawSignalCatalogueId("R003"), PROVIDER,
        VARIANT, ("time", "timezone"), "native_timezone", META,
    ),
)
UNITS = (
    f.UnitConventionVersionV1(
        "mmt-d001-temporal", 1, "native_time", "UTC_datetime", Decimal(1), Decimal(0),
    ),
    f.UnitConventionVersionV1(
        "mmt-d001-zone", 1, "native_timezone", "offset", Decimal(1), Decimal(0),
    ),
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
DEFINITION = f.CalculationDefinitionV1(
    "D001", "D001-TRUE-INSTANT-UTC-1", "K01_TIME",
    "same true instant converted to aware UTC", ("R002", "R003"), (),
    "P_TIME", "UTC_datetime", "aware_utc_datetime", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d001-controlled", 1, "P_TIME", "NVDA", ("NVDA",),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d001-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def request() -> f.CalculationRequestV1:
    return f.CalculationRequestV1(
        "D001", "NVDA", T, T, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1), (),
        tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value,
            f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), "NVDA",
        ) for mapping, unit in zip(MAPS, UNITS, strict=True)),
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d001_signal(tmp_path, refused):
    source = r.create_owner()
    raw_values = ("2026-10-10" if refused else "2026-10-10T00:59:50+11:00", "+11:00")
    projected = []
    for index, (mapping, native) in enumerate(zip(MAPS, raw_values, strict=True)):
        role = ("source_timestamp", "source_timezone")[index]
        source.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d001-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d001-controlled"),
            source_provider=r.provider_id(PROVIDER),
            native_record={
                "sample": {"id": "controlled-temporal-sample/1"},
                "value": {"role": role},
                "time": {"value" if index == 0 else "timezone": native},
            },
            received_ts_utc=RECEIPT, ingestion_sequence=index + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="date_only" if index == 0 and refused else "true_instant",
            raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
            source_variant=VARIANT, subject_instrument="NVDA",
            native_units=mapping.native_units,
            source_timestamp_raw=raw_values[0] if index == 0 else "2026-10-09T13:59:50Z",
            source_timezone_native="+11:00" if index == 0 else "UTC",
        ))
        page = source.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument="NVDA", received_at_or_before_utc=T,
            event_at_or_before_utc=None, limit=100, cursor=None,
        )
        assert page.next_cursor is None and len(page.items) == 1
        item = page.items[0]
        assert item.observation_occurrence_id.value == f"d001-{index}"
        assert item.native_value == native and item.received_ts_utc == RECEIPT
        assert item.selection_identity == r.RawSelectionIdentityV1((
            ("sample.id", "controlled-temporal-sample/1"),
            ("value.role", role),
        ))
        projected.append(item)
    assert len(projected) == 2
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d001.sqlite")
    owner = f.create_temporal_owner(
        admission=admission, raw_projection_reader=source.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    calc = request()
    result = owner.materialise(calc)
    reader = f.create_temporal_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    history = dict(
        derived_signal_id="D001", subject_instrument="NVDA",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=T, limit=10,
    )
    if refused:
        assert projected[0].source_temporal_kind == "date_only"
        assert result is None
        assert owner.reads.list_derived_history(**history) == ()
        assert reader.list_derived_history(**history) == ()
        return
    assert type(result) is f.TemporalOccurrenceV1
    assert result.request == calc and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.projection_mappings == MAPS and result.unit_conventions == UNITS
    assert result.result == EVENT and result.units == "UTC_datetime"
    assert result.result_shape == "aware_utc_datetime"
    assert result.implementation_brief_sha256 == BRIEF
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, T, NOW)
    assert result.predecessor_occurrence_ids == ()
    assert tuple(line.projection for line in result.raw_input_lineage) == tuple(projected)
    assert tuple(line.canonical_value for line in result.raw_input_lineage) == raw_values
    assert tuple(line.raw_signal_id for line in result.raw_input_lineage) == ("R002", "R003")
    assert all(line.event_time_utc == EVENT for line in result.raw_input_lineage)
    assert result.derived_occurrence_id.startswith("mmttemporal1:")
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**history) == (result,)
