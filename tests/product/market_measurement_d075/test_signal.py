"""D075: two declared public source/return cases; fixed independent logarithm oracle."""

from copy import deepcopy
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

D, BRIEF = "D075", "5cbb863087a2393218818f2e85c0182ad44060509ec1901200f6f670e8d1e377"
SUBJECT = "NVDA"
PROVIDER, VARIANT = "foundation-controlled-underlying", "last_prior_close_v1"
MAP_SPECS = (
    (
        "R037",
        "mmt-r037-underlying",
        ("trade", "last"),
        "price",
        (
            ("instrument.id", ("instrument", "id")),
            ("session.id", ("session", "id")),
            ("adjustment.basis", ("adjustment", "basis")),
            ("price.kind", ("price", "kind")),
        ),
    ),
    (
        "R042",
        "mmt-r042-underlying",
        ("official_close", "value"),
        "price",
        (
            ("instrument.id", ("instrument", "id")),
            ("session.id", ("session", "id")),
            ("adjustment.basis", ("adjustment", "basis")),
            ("price.kind", ("price", "kind")),
        ),
    ),
)
SOURCE_RECORDS = [
    [
        0,
        "NVDA",
        "2026-10-20T12:40:00Z",
        "2026-10-20T12:40:00Z",
        {
            "trade": {"last": "125"},
            "instrument": {"id": "NVDA"},
            "session": {"id": "controlled-20oct12-13Z"},
            "adjustment": {"basis": "controlled_unadjusted/1"},
            "price": {"kind": "current_last"},
        },
    ],
    [
        1,
        "NVDA",
        "2026-10-19T13:00:00Z",
        "2026-10-19T13:00:00Z",
        {
            "official_close": {"value": "100"},
            "instrument": {"id": "NVDA"},
            "session": {"id": "controlled-19oct12-13Z"},
            "adjustment": {"basis": "controlled_unadjusted/1"},
            "price": {"kind": "official_close"},
        },
    ],
]
EXPECTED = Decimal("0.22314355131420975576629509030983450337460108554801")


def dt(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


T, REFERENCE, START, END = map(
    dt,
    (
        "2026-10-20T12:40:00Z",
        "2026-10-19T13:00:00Z",
        "2026-10-19T12:00:00Z",
        "2026-10-20T13:00:00Z",
    ),
)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-underlying-session", 1), START, END, START)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        mid, 1, r.RawSignalCatalogueId(rid), PROVIDER, VARIANT, path, unit, meta
    )
    for rid, mid, path, unit, meta in MAP_SPECS
)
UNIT = f.UnitConventionVersionV1(
    "mmt-underlying-price", 1, "price", "price", Decimal("1"), Decimal("0")
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d075-selection",
    1,
    ("subject_instrument", "instrument.id", "session.id"),
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
PARAM = f.CalculationParameterSetV1("mmt-d075-controlled", 1, "P_WINDOW", SUBJECT, (SUBJECT,))
DEFINITION = f.CalculationDefinitionV1(
    D,
    D + "-LOG-RETURN-1",
    "K03_CHANGE_RETURN",
    "ln(current/reference)",
    ("R037", "R042"),
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
def test_d075_signal(tmp_path, refused):
    raw = r.create_owner()
    records = deepcopy(SOURCE_RECORDS)
    if refused:
        records[0][4]["trade"]["last"] = "-1"
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
                observation_occurrence_id=r.observation_occurrence_id("d075-raw-" + str(index)),
                delivery_artifact_ref=r.delivery_artifact_ref("d075-controlled"),
                source_provider=r.provider_id(PROVIDER),
                native_record=native,
                received_ts_utc=dt(receipt),
                ingestion_sequence=index + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                source_variant=VARIANT,
                subject_instrument=subject,
                native_units="price",
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
        item = projected["d075-raw-" + str(index)]
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
        assert projected["d075-raw-0"].native_value == Decimal("-1")
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
            "d075-raw-" + str(index),
            f.VersionRefV1(MAPS[role].mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1),
            projected["d075-raw-" + str(index)],
            projected["d075-raw-" + str(index)].native_value,
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
