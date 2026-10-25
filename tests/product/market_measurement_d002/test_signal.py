"""D002 actual D001 source-event age and visible date-only refusal."""

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
BRIEF = "1d7a4621010e87c6fe44254aeb88712ae2d3b61bf6d739a4ef3ef7c8b3a8477f"
META = (("sample.id", ("sample", "id")), ("value.role", ("value", "role")))
MAPS = (
    r.RawSignalProjectionMappingV1(
        "mmt-d002-r001", 1, r.RawSignalCatalogueId("R001"), PROVIDER,
        VARIANT, ("time", "receipt"), "UTC_datetime", META,
    ),
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
    f.UnitConventionVersionV1("mmt-d002-receipt", 1, "UTC_datetime", "UTC_datetime",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d001-temporal", 1, "native_time", "UTC_datetime",
                              Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-d001-zone", 1, "native_timezone", "offset",
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
    "D002", "D002-SOURCE-AGE-1", "K01_TIME",
    "cutoff minus true source event or actual collector receipt", ("R001", "R002"), ("D001",),
    "P_TIME", "seconds", "age_basis_seconds", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d002-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d002-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant", "receipt_only", "date_only"),
    ("NVDA",), PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def d001_request():
    return f.CalculationRequestV1(
        "D001", "NVDA", T, T, D001_DEF.calculation_definition_version,
        f.VersionRefV1(D001_PARAM.context_id, 1), f.VersionRefV1(D001_POLICY.context_id, 1), (),
        tuple(f.RawInputBindingV1(
            MAPS[i].raw_signal_catalogue_id.value, f.VersionRefV1(MAPS[i].mapping_id, 1),
            f.VersionRefV1(UNITS[i].context_id, 1), "NVDA",
        ) for i in (1, 2)),
    )


def d002_request(predecessor_ids):
    return f.TemporalAgeRequestV1(
        f.CalculationRequestV1(
            "D002", "NVDA", T, T, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1), (),
            tuple(f.RawInputBindingV1(
                MAPS[i].raw_signal_catalogue_id.value, f.VersionRefV1(MAPS[i].mapping_id, 1),
                f.VersionRefV1(UNITS[i].context_id, 1), "NVDA",
            ) for i in (0, 1)),
        ), predecessor_ids,
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d002_signal(tmp_path, refused):
    raw = r.create_owner()
    natives = (
        "2026-10-09T13:59:55Z",
        "2026-10-10" if refused else "2026-10-10T00:59:50+11:00",
        "+11:00",
    )
    projected = []
    for index, mapping in enumerate(MAPS):
        role = ("collector_receipt", "source_timestamp", "source_timezone")[index]
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d002-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d002-controlled"),
            source_provider=r.provider_id(PROVIDER),
            native_record={
                "sample": {"id": SAMPLE}, "value": {"role": role},
                "time": {("receipt", "value", "timezone")[index]: natives[index]},
            },
            received_ts_utc=RECEIPT, ingestion_sequence=index + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind=("receipt_only", "date_only" if refused else "true_instant",
                                  "true_instant")[index],
            raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
            source_variant=VARIANT, subject_instrument="NVDA",
            native_units=mapping.native_units,
            source_timestamp_raw=(None, natives[1], "2026-10-09T13:59:50Z")[index],
            source_timezone_native=(None, "+11:00", "UTC")[index],
        ))
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,), subject_instrument="NVDA",
            received_at_or_before_utc=T, event_at_or_before_utc=None, limit=100, cursor=None,
        )
        assert page.next_cursor is None and len(page.items) == 1
        item = page.items[0]
        assert item.native_value == natives[index] and item.received_ts_utc == RECEIPT
        assert item.observation_occurrence_id.value == f"d002-{index}"
        assert item.selection_identity == r.RawSelectionIdentityV1((
            ("sample.id", SAMPLE), ("value.role", role),
        ))
        projected.append(item)
    d001 = f.create_temporal_owner(
        admission=f.OwnerAdmissionV1("M02", D001_BRIEF), raw_projection_reader=raw.reads,
        storage=f.MemoryStorageV1(), utc_now=lambda: NOW,
    )
    predecessor = d001.materialise(d001_request())
    if refused:
        assert predecessor is None
    else:
        assert type(predecessor) is f.TemporalOccurrenceV1
        assert predecessor.result == EVENT
        assert predecessor.raw_input_lineage[0].projection == projected[1]
        assert predecessor.raw_input_lineage[1].projection == projected[2]
    request = d002_request(() if predecessor is None else (predecessor.derived_occurrence_id,))
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d002.sqlite")
    owner = f.create_temporal_age_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=d001.reads, storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    reader = f.create_temporal_age_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    history = dict(
        derived_signal_id="D002", subject_instrument="NVDA",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=T, limit=10,
    )
    if refused:
        assert projected[1].source_temporal_kind == "date_only"
        assert result is None
        assert owner.reads.list_derived_history(**history) == ()
        assert reader.list_derived_history(**history) == ()
        return
    assert type(result) is f.TemporalAgeOccurrenceV1
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.projection_mappings == MAPS[:2] and result.unit_conventions == UNITS[:2]
    assert result.result == f.TemporalAgeV1("source_event", Decimal(10))
    assert result.units == "seconds" and result.result_shape == "age_basis_seconds"
    assert result.implementation_brief_sha256 == BRIEF
    assert tuple(line.projection for line in result.raw_input_lineage) == tuple(projected[:2])
    assert tuple(line.canonical_value for line in result.raw_input_lineage) == natives[:2]
    assert result.predecessors == (predecessor,)
    assert result.request.predecessor_occurrence_ids == (predecessor.derived_occurrence_id,)
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, T, NOW)
    assert result.derived_occurrence_id.startswith("mmtage1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**history) == (result,)
