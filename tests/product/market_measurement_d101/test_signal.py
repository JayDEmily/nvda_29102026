"""D101 complete native delta four-contract smile and missing P50 delta refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
E1 = "2026-10-23"
TAGS = ("C25", "P25", "C50", "P50")
MEMBERS = tuple(f"controlled-skew-{E1}-{tag}" for tag in TAGS)
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
BRIEF = "e2ce7083301088d963c64d427811aa0938c141d7805e7aee18359ae7b5ee4ba8"
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
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw), PROVIDER, VARIANT,
    path, unit, META,
) for raw, path, unit in (
    ("R111", ("model", "iv"), "annualised_decimal_volatility"),
    ("R112", ("model", "delta"), "delta_fraction"),
))
UNITS = (
    f.UnitConventionVersionV1("mmt-option-iv", 1, "annualised_decimal_volatility",
                              "annualised_decimal_volatility", Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-option-delta", 1, "delta_fraction", "delta_fraction",
                              Decimal(1), Decimal(0)),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC), datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d101-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D101", "D101-SMILE-CURVATURE-1", "K02_ALGEBRA",
    "100*(put25_iv+call25_iv-2*(call50_iv+put50_iv)/2)",
    ("R111", "R112"), (), "P_BASIC", "volatility_points", "exact_ratio", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d101-controlled", 1, "P_BASIC", "NVDA_SMILE_E1", MEMBERS,
)
VALUES = {"C25": (Decimal(".20"), Decimal(".25")),
          "P25": (Decimal(".30"), Decimal("-.25")),
          "C50": (Decimal(".22"), Decimal(".50")),
          "P50": (Decimal(".26"), Decimal("-.50"))}
STRIKES = {"C25": "120", "P25": "100", "C50": "110", "P50": "110"}


def request():
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D101", "NVDA_SMILE_E1", T, CUTOFF, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,), tuple(f.RawInputBindingV1(
                mapping.raw_signal_catalogue_id.value, f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(UNITS[role].context_id, 1), member,
            ) for member in MEMBERS for role, mapping in enumerate(MAPS)),
        ), CONTEXT, (),
    )


@pytest.mark.parametrize("missing", (False, True), ids=("success", "refusal"))
def test_d101_signal(tmp_path, missing):
    raw = r.create_owner()
    projected = {}
    for member_index, (tag, member) in enumerate(zip(TAGS, MEMBERS, strict=True)):
        for role, mapping in enumerate(MAPS):
            if missing and tag == "P50" and role == 1:
                continue
            value = VALUES[tag][role]
            native = {
                "contract": {"id": member, "multiplier": "100"},
                "underlying": {"id": "NVDA"}, "expiry": {"date": E1},
                "strike": {"key": STRIKES[tag]}, "option": {"right": tag[0]},
                "currency": {"code": "USD"}, "instrument": {"kind": "option"},
                "model": {"convention": "controlled-model/1",
                          "iv" if role == 0 else "delta": value},
                "value": {"role": "model_iv" if role == 0 else "model_delta"},
            }
            identity = f"d101-{member_index}-{role}"
            raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("d101-controlled"),
                source_provider=r.provider_id(PROVIDER), native_record=native,
                received_ts_utc=T, ingestion_sequence=member_index * 2 + role + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                source_variant=VARIANT, subject_instrument=member,
                native_units=mapping.native_units,
                source_timestamp_raw="2026-10-20T12:40:00Z", source_timezone_native="UTC",
            ))
            page = raw.reads.list_projected_raw_history(
                mapping.raw_signal_catalogue_id, mappings=(mapping,),
                subject_instrument=member, received_at_or_before_utc=CUTOFF,
                event_at_or_before_utc=T, limit=100, cursor=None,
            )
            assert page.next_cursor is None and len(page.items) == 1
            item = page.items[0]
            assert item.observation_occurrence_id.value == identity
            assert item.native_value == value and item.received_ts_utc == T
            assert item.selection_identity == r.RawSelectionIdentityV1((
                ("contract.id", member), ("underlying.id", "NVDA"),
                ("expiry.date", E1), ("strike.key", STRIKES[tag]),
                ("option.right", tag[0]), ("currency.code", "USD"),
                ("contract.multiplier", "100"), ("instrument.kind", "option"),
                ("model.convention", "controlled-model/1"),
                ("value.role", "model_iv" if role == 0 else "model_delta"),
            ))
            projected[(tag, role)] = item
    assert len(projected) == (7 if missing else 8)
    assert all(projected[(tag, 1)].native_value == VALUES[tag][1]
               for tag in TAGS if (tag, 1) in projected)
    assert ("P50", 0) in projected and (("P50", 1) in projected) is not missing
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d101.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    own_request = request()
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D101", subject_instrument="NVDA_SMILE_E1",
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if missing:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.projection_mappings == MAPS and result.unit_conventions == UNITS
    assert result.raw_input_lineage == tuple(f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value,
        projected[(tag, role)].observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNITS[role].context_id, 1),
        projected[(tag, role)], VALUES[tag][role], T,
    ) for tag in TAGS for role, mapping in enumerate(MAPS))
    assert result.result == f.ExactRatioV1(2, 1)
    assert result.predecessors == () and result.window_seconds == 0
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.units == "volatility_points" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
