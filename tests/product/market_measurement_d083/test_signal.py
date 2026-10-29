"""D083: complete three-member current/prior source basket and sample dispersion."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
PRIOR = datetime(2026, 10, 19, 13, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
MEMBERS = ("NVDA", "QQQ", "SMH")
VALUES = (("110", "100"), ("100", "100"), ("100", "110"))
PROVIDER, VARIANT = "foundation-controlled-underlying", "last_prior_close_v1"
BRIEF = "463d126955fa20959ca81b1bb8792fd63750176b78ced7b7dc432d3326923af4"
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
META = (
    ("instrument.id", ("instrument", "id")),
    ("session.id", ("session", "id")),
    ("adjustment.basis", ("adjustment", "basis")),
    ("price.kind", ("price", "kind")),
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + raw.lower() + "-underlying", 1, r.RawSignalCatalogueId(raw),
        PROVIDER, VARIANT, path, "price", META,
    ) for raw, path in (
        ("R037", ("trade", "last")), ("R042", ("official_close", "value")),
    )
)
UNIT = f.UnitConventionVersionV1(
    "mmt-underlying-price", 1, "price", "price", Decimal("1"), Decimal("0")
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-underlying-session", 1),
    datetime(2026, 10, 19, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 19, 12, tzinfo=UTC),
)
DEFINITION = f.CalculationDefinitionV1(
    "D083", "D083-CROSS-SECTION-DISPERSION-1", "K04_STANDARDISE_RANK",
    "sample_sd(log(current/prior) for all three members)", ("R037", "R042"), (),
    "P_CROSS_SECTION", "return_dispersion", "scalar_decimal", AUTHORITY,
)
PARAM = f.CalculationParameterSetV1(
    "mmt-d083-controlled", 1, "P_CROSS_SECTION", "TECH_SEMI_DISPERSION", MEMBERS
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d083-selection", 1, ("subject_instrument", "instrument.id", "session.id"),
    timedelta(days=1), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def _utc(value):
    return value.isoformat().replace("+00:00", "Z")


def _request():
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D083", "TECH_SEMI_DISPERSION", T, CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAM.context_id, 1),
            f.VersionRefV1(POLICY.context_id, 1), (CONTEXT.ref,),
            tuple(
                f.RawInputBindingV1(
                    mapping.raw_signal_catalogue_id.value,
                    f.VersionRefV1(mapping.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1), member,
                ) for member in MEMBERS for mapping in MAPS
            ),
        ), CONTEXT, (),
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d083_signal(tmp_path, refused):
    raw = r.create_owner()
    projected = {}
    for j, member in enumerate(MEMBERS):
        for role, mapping in enumerate(MAPS):
            if refused and (member, role) == ("SMH", 1):
                continue
            anchor = T if role == 0 else PRIOR
            price = Decimal(VALUES[j][role])
            session = "controlled-20oct12-13Z" if role == 0 else "controlled-19oct12-13Z"
            kind = "current_last" if role == 0 else "official_close"
            native = {
                "trade": {"last": price} if role == 0 else {},
                "official_close": {"value": price} if role == 1 else {},
                "instrument": {"id": member},
                "session": {"id": session},
                "adjustment": {"basis": "controlled_unadjusted/1"},
                "price": {"kind": kind},
            }
            identity = f"d083-{member.lower()}-{role}"
            raw.commands.admit_raw_observation_occurrence(
                r.RawObservationOccurrenceV1(
                    concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=r.observation_occurrence_id(identity),
                    delivery_artifact_ref=r.delivery_artifact_ref("d083-controlled"),
                    source_provider=r.provider_id(PROVIDER), native_record=native,
                    received_ts_utc=anchor, ingestion_sequence=j * 2 + role + 1,
                    ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                    source_temporal_kind="true_instant",
                    raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                    source_variant=VARIANT, subject_instrument=member,
                    native_units="price", source_timestamp_raw=_utc(anchor),
                    source_timezone_native="UTC",
                )
            )
            page = raw.reads.list_projected_raw_history(
                mapping.raw_signal_catalogue_id, mappings=(mapping,),
                subject_instrument=member, received_at_or_before_utc=CUTOFF,
                event_at_or_before_utc=T, limit=100, cursor=None,
            )
            assert page.next_cursor is None and len(page.items) == 1
            item = page.items[0]
            assert item.observation_occurrence_id.value == identity
            assert item.native_value == price and item.received_ts_utc == anchor
            assert item.selection_identity == r.RawSelectionIdentityV1((
                ("instrument.id", member), ("session.id", session),
                ("adjustment.basis", "controlled_unadjusted/1"), ("price.kind", kind),
            ))
            projected[(member, role)] = item
    assert len(projected) == (5 if refused else 6)
    assert all((member, 0) in projected for member in MEMBERS)
    assert all((member, 1) in projected for member in MEMBERS if member != "SMH")
    request = _request()
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d083.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(
        derived_signal_id="D083", subject_instrument="TECH_SEMI_DISPERSION",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10,
    )
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is Decimal
    assert result.result.as_tuple() == Decimal(
        "0.095310179804324860043952123280765092220605365308644"
    ).as_tuple()
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAM and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.projection_mappings == MAPS and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            MAPS[role].raw_signal_catalogue_id.value,
            projected[(member, role)].observation_occurrence_id.value,
            f.VersionRefV1(MAPS[role].mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), projected[(member, role)],
            Decimal(VALUES[j][role]), T if role == 0 else PRIOR,
        ) for j, member in enumerate(MEMBERS) for role in (0, 1)
    )
    assert result.predecessors == () and result.window_seconds == 85200
    assert result.units == "return_dispersion" and result.result_shape == "scalar_decimal"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
