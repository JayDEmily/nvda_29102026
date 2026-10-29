"""D066: two declared public source/return cases; fixed independent logarithm oracle."""

from copy import deepcopy
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

D, BRIEF = "D066", "39e06e96fd6bc3c8415296995896710ec91964c7c7c5d9e8e49e77e59c866308"
SUBJECT = "NVDA"
PROVIDER, VARIANT = "foundation-controlled-international", "daily_close_v1"
MAP_SPECS = (
    (
        "R270",
        "mmt-r270-international",
        ("index", "value"),
        "index_points",
        (
            ("index.series", ("index", "series")),
            ("index.close_utc", ("index", "close_utc")),
            ("index.adjustment_basis", ("index", "adjustment_basis")),
            ("index.close_kind", ("index", "close_kind")),
        ),
    ),
)
SOURCE_RECORDS = [
    (
        0,
        "NVDA",
        "2026-10-20T13:00:00Z",
        "2026-10-20T13:00:00Z",
        {
            "index": {
                "value": "110",
                "series": "NIKKEI225",
                "close_utc": "2026-10-20T13:00:00Z",
                "adjustment_basis": "controlled_unadjusted/1",
                "close_kind": "controlled_official",
            }
        },
    ),
    (
        0,
        "NVDA",
        "2026-10-19T13:00:00Z",
        "2026-10-19T13:00:00Z",
        {
            "index": {
                "value": "100",
                "series": "NIKKEI225",
                "close_utc": "2026-10-19T13:00:00Z",
                "adjustment_basis": "controlled_unadjusted/1",
                "close_kind": "controlled_official",
            }
        },
    ),
]
EXPECTED = Decimal("0.095310179804324860043952123280765092220605365308644")


def dt(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


T, REFERENCE, START, END = map(
    dt,
    (
        "2026-10-20T13:00:00Z",
        "2026-10-19T13:00:00Z",
        "2026-10-19T13:00:00Z",
        "2026-10-20T13:00:01Z",
    ),
)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-international-r270", 1), START, END, START)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        mid, 1, r.RawSignalCatalogueId(rid), PROVIDER, VARIANT, path, unit, meta
    )
    for rid, mid, path, unit, meta in MAP_SPECS
)
UNIT = f.UnitConventionVersionV1(
    "mmt-r270-index-units", 1, "index_points", "index_points", Decimal("1"), Decimal("0")
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d066-selection",
    1,
    ("subject_instrument", "index.series"),
    timedelta(days=1),
    timedelta(0),
    ("true_instant",),
    (),
    PROVIDER,
    VARIANT,
    PROVIDER + "/" + VARIANT,
    100,
    1000,
)
PARAM = f.CalculationParameterSetV1("mmt-d066-controlled", 1, "P_WINDOW", SUBJECT, (SUBJECT,))
DEFINITION = f.CalculationDefinitionV1(
    D,
    D + "-LOG-RETURN-1",
    "K03_CHANGE_RETURN",
    "ln(current/reference)",
    ("R270",),
    (),
    "P_WINDOW",
    "return",
    "scalar_decimal",
    (
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
            "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
        ),
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
            "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
        ),
    ),
)


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d066_signal(tmp_path, refused):
    raw = r.create_owner()
    records = deepcopy(SOURCE_RECORDS)
    if refused:
        records[1][4]["index"]["adjustment_basis"] = "split_adjusted/1"
    for index, (role, subject, event, receipt, native) in enumerate(records):
        mapping = MAPS[role]
        parent = native
        for part in mapping.native_field_path[:-1]:
            parent = parent[part]
        parent[mapping.native_field_path[-1]] = Decimal(parent[mapping.native_field_path[-1]])
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id("d066-raw-" + str(index)),
                delivery_artifact_ref=r.delivery_artifact_ref("d066-controlled"),
                source_provider=r.provider_id(PROVIDER),
                native_record=native,
                received_ts_utc=dt(receipt),
                ingestion_sequence=index + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                source_variant=VARIANT,
                subject_instrument=subject,
                native_units="index_points",
                source_timestamp_raw=event,
                source_timezone_native="UTC",
            )
        )
    projected = {}
    for role, subject, _, _, _ in records:
        mapping = MAPS[role]
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id,
            mappings=(mapping,),
            subject_instrument=subject,
            received_at_or_before_utc=NOW,
            event_at_or_before_utc=T,
            limit=100,
            cursor=None,
        )
        assert page.next_cursor is None
        projected.update({p.observation_occurrence_id.value: p for p in page.items})
    assert len(projected) == 2
    for index, (role, subject, event, receipt, native) in enumerate(records):
        item = projected["d066-raw-" + str(index)]
        mapping = MAPS[role]
        assert item.received_ts_utc == dt(receipt) and item.source_timestamp_raw == event
        assert (
            item.subject_instrument == subject
            and item.raw_signal_catalogue_id == mapping.raw_signal_catalogue_id
        )
        expected_meta = []
        for key, path in mapping.selection_identity_field_paths:
            value = native
            for part in path:
                value = value[part]
            expected_meta.append((key, value))
        assert item.selection_identity == r.RawSelectionIdentityV1(tuple(expected_meta))
        value = native
        for part in mapping.native_field_path:
            value = value[part]
        assert item.native_value == value
    if refused:
        assert (
            "split_adjusted/1" in dict(projected["d066-raw-1"].selection_identity.values).values()
        )
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "m02.sqlite")
    owner = f.create_window_owner(
        admission=admission,
        raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            D,
            SUBJECT,
            T,
            CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAM.context_id, 1),
            f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            tuple(
                f.RawInputBindingV1(
                    m.raw_signal_catalogue_id.value,
                    f.VersionRefV1(m.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1),
                    SUBJECT,
                )
                for m in MAPS
            ),
        ),
        CONTEXT,
        (),
    )
    result = owner.materialise(request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(
        derived_signal_id=D,
        subject_instrument=SUBJECT,
        effective_at_or_before_utc=T,
        knowledge_at_or_before_utc=CUTOFF,
        limit=10,
    )
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is Decimal and result.result.as_tuple() == EXPECTED.as_tuple()
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAM and result.input_selection_policy == POLICY
    assert result.unit_conventions == (UNIT,) and result.projection_mappings == MAPS
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            MAPS[role].raw_signal_catalogue_id.value,
            "d066-raw-" + str(index),
            f.VersionRefV1(MAPS[role].mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1),
            projected["d066-raw-" + str(index)],
            projected["d066-raw-" + str(index)].native_value,
            dt(event),
        )
        for index, (role, _, event, _, _) in enumerate(records)
    )
    assert result.predecessors == () and result.window_seconds == int(
        (T - REFERENCE).total_seconds()
    )
    assert (
        result.owner_object_id == "M02"
        and result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    )
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == D
    assert result.units == "return" and result.result_shape == "scalar_decimal"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert (
        owner.reads.get_derived_occurrence(result.derived_occurrence_id)
        == reader.get_derived_occurrence(result.derived_occurrence_id)
        == result
    )
    assert reader.list_derived_history(**args) == (result,)
