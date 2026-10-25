"""D103 complete two-contract/two-anchor IV shift and missing prior put refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
A, CUTOFF, NOW = T - timedelta(seconds=300), T + timedelta(seconds=1), T + timedelta(seconds=2)
C25, P25 = (f"controlled-skew-2026-10-23-{tag}" for tag in ("C25", "P25"))
MEMBERS = (C25, P25)
BRIEF = "8fe8a0081907ca543c7bb94765cedac48cfcc2335d724384c3d9dfe77bbef45d"
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
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
    ("contract.id", ("contract", "id")), ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")), ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")), ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("model.convention", ("model", "convention")), ("value.role", ("value", "role")),
)
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r111-option", 1, r.RawSignalCatalogueId("R111"), PROVIDER, VARIANT,
    ("model", "iv"), "annualised_decimal_volatility", META,
)
UNIT = f.UnitConventionVersionV1("mmt-option-iv", 1, "annualised_decimal_volatility",
                                 "annualised_decimal_volatility", Decimal(1), Decimal(0))
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC), datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d103-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=300), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D103", "D103-MATCHED-SURFACE-SHIFT-5M-1", "K03_CHANGE_RETURN",
    "100*mean(member_iv_current-member_iv_reference)", ("R111",), (),
    "P_WINDOW", "volatility_points", "exact_ratio", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d103-controlled", 1, "P_WINDOW", "NVDA_SURFACE_E1", MEMBERS,
)
VALUES = {("C25", T): Decimal(".20"), ("P25", T): Decimal(".35"),
          ("C25", A): Decimal(".10"), ("P25", A): Decimal(".20")}


def request():
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D103", "NVDA_SURFACE_E1", T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), tuple(f.RawInputBindingV1(
            "R111", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), member,
        ) for member in MEMBERS),
    ), CONTEXT, ())


@pytest.mark.parametrize("missing", (False, True), ids=("success", "refusal"))
def test_d103_signal(tmp_path, missing):
    raw = r.create_owner()
    projected = {}
    for anchor in (T, A):
        for tag, member in (("C25", C25), ("P25", P25)):
            if missing and tag == "P25" and anchor == A:
                continue
            value = VALUES[(tag, anchor)]
            identity = f"d103-{tag}-{int(anchor == A)}"
            native = {
                "contract": {"id": member, "multiplier": "100"},
                "underlying": {"id": "NVDA"}, "expiry": {"date": "2026-10-23"},
                "strike": {"key": "120" if tag == "C25" else "100"},
                "option": {"right": tag[0]}, "currency": {"code": "USD"},
                "instrument": {"kind": "option"},
                "model": {"convention": "controlled-model/1", "iv": value},
                "value": {"role": "model_iv"},
            }
            raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("d103-controlled"),
                source_provider=r.provider_id(PROVIDER), native_record=native,
                received_ts_utc=anchor, ingestion_sequence=len(projected) + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(r.RawSignalCatalogueId("R111"),),
                source_variant=VARIANT, subject_instrument=member,
                native_units="annualised_decimal_volatility",
                source_timestamp_raw=anchor.isoformat().replace("+00:00", "Z"),
                source_timezone_native="UTC",
            ))
            page = raw.reads.list_projected_raw_history(
                r.RawSignalCatalogueId("R111"), mappings=(MAPPING,),
                subject_instrument=member, received_at_or_before_utc=CUTOFF,
                event_at_or_before_utc=T, limit=100, cursor=None,
            )
            assert page.next_cursor is None
            matches = [x for x in page.items if x.observation_occurrence_id.value == identity]
            assert len(matches) == 1
            item = matches[0]
            assert item.native_value == value and item.received_ts_utc == anchor
            assert item.selection_identity == r.RawSelectionIdentityV1((
                ("contract.id", member), ("underlying.id", "NVDA"),
                ("expiry.date", "2026-10-23"),
                ("strike.key", "120" if tag == "C25" else "100"),
                ("option.right", tag[0]), ("currency.code", "USD"),
                ("contract.multiplier", "100"), ("instrument.kind", "option"),
                ("model.convention", "controlled-model/1"), ("value.role", "model_iv"),
            ))
            projected[(tag, anchor)] = item
    assert len(projected) == (3 if missing else 4)
    assert all(projected[k].native_value == VALUES[k] for k in projected)
    assert (("P25", A) in projected) is not missing
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d103.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    own_request = request()
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D103", subject_instrument="NVDA_SURFACE_E1",
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if missing:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == f.ExactRatioV1(25, 2)
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.projection_mappings == (MAPPING,) and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(f.RawInputLineageV1(
        "R111", projected[(tag, anchor)].observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        projected[(tag, anchor)], VALUES[(tag, anchor)], anchor,
    ) for anchor in (T, A) for tag in ("C25", "P25"))
    assert result.predecessors == () and result.window_seconds == 300
    assert result.units == "volatility_points" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
