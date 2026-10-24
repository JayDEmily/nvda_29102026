"""D099: public native right/delta/IV matched skew and contradictory-side refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
A, CUTOFF, NOW = T - timedelta(seconds=300), T + timedelta(seconds=1), T + timedelta(seconds=2)
E1 = "2026-10-23"
C25, P25 = (f"controlled-skew-{E1}-{tag}" for tag in ("C25", "P25"))
SUBJECT = "NVDA_SKEW_2026-10-23"
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
BRIEF = "ab854fdd6a9a34c431c977fa973e392592be1e0d21854f4c95324852ed4f95a7"
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
    ("model.convention", ("model", "convention")),
    ("value.role", ("value", "role")),
)
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
    PROVIDER, VARIANT, path, native_unit, META,
) for raw, path, native_unit in (
    ("R111", ("model", "iv"), "annualised_decimal_volatility"),
    ("R112", ("model", "delta"), "delta_fraction"),
    ("R015", ("contract", "right"), "option_right"),
))
UNITS = (
    f.UnitConventionVersionV1("mmt-option-iv", 1, "annualised_decimal_volatility",
                              "annualised_decimal_volatility", Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-option-delta", 1, "delta_fraction",
                              "delta_fraction", Decimal(1), Decimal(0)),
    f.UnitConventionVersionV1("mmt-option-right", 1, "option_right",
                              "option_right", Decimal(1), Decimal(0)),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC), datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d099-E1-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), (C25, P25),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D099", "D099-NATIVE-DELTA-SKEW-1", "K02_ALGEBRA", "100*(put_iv-call_iv)",
    ("R111", "R112", "R015"), (), "P_BASIC", "volatility_points", "option_skew", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d099-E1-controlled", 1, "P_BASIC", SUBJECT, (C25, P25)
)


def request():
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D099", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,), tuple(
                f.RawInputBindingV1(
                    mapping.raw_signal_catalogue_id.value,
                    f.VersionRefV1(mapping.mapping_id, 1),
                    f.VersionRefV1(UNITS[role].context_id, 1), contract,
                ) for contract in (C25, P25) for role, mapping in enumerate(MAPS)
            ),
        ), CONTEXT, (),
    )


def native(contract, tag, role, number, refused):
    right = "C" if tag == "C25" else "P"
    record = {
        "contract": {"id": contract, "multiplier": "100"},
        "underlying": {"id": "NVDA"}, "expiry": {"date": E1},
        "strike": {"key": "120" if tag == "C25" else "100"},
        "option": {"right": right}, "currency": {"code": "USD"},
        "instrument": {"kind": "option"}, "model": {"convention": "controlled-model/1"},
        "value": {"role": ("model_iv", "model_delta", "option_right")[role]},
    }
    if role == 0:
        record["model"]["iv"] = number
    elif role == 1:
        record["model"]["delta"] = number
    else:
        record["contract"]["right"] = "C" if refused and tag == "P25" else right
    return record


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d099_signal(tmp_path, refused):
    raw = r.create_owner()
    values = {"C25": (Decimal(".20"), Decimal(".25"), "C"),
              "P25": (Decimal(".30"), Decimal("-.25"), "C" if refused else "P")}
    projected = {}
    for member_index, (tag, contract) in enumerate((("C25", C25), ("P25", P25))):
        for role, mapping in enumerate(MAPS):
            number = values[tag][role]
            identity = f"d099-{member_index}-{role}"
            raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("d099-controlled"),
                source_provider=r.provider_id(PROVIDER),
                native_record=native(contract, tag, role, number, refused),
                received_ts_utc=T, ingestion_sequence=member_index * 3 + role + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                source_variant=VARIANT, subject_instrument=contract,
                native_units=mapping.native_units,
                source_timestamp_raw="2026-10-20T12:40:00Z", source_timezone_native="UTC",
            ))
            page = raw.reads.list_projected_raw_history(
                mapping.raw_signal_catalogue_id, mappings=(mapping,),
                subject_instrument=contract, received_at_or_before_utc=CUTOFF,
                event_at_or_before_utc=T, limit=100, cursor=None,
            )
            assert page.next_cursor is None and len(page.items) == 1
            item = page.items[0]
            assert item.observation_occurrence_id.value == identity
            assert item.native_value == number and item.received_ts_utc == T
            assert item.selection_identity == r.RawSelectionIdentityV1((
                ("contract.id", contract), ("underlying.id", "NVDA"),
                ("expiry.date", E1), ("strike.key", "120" if tag == "C25" else "100"),
                ("option.right", "C" if tag == "C25" else "P"),
                ("currency.code", "USD"), ("contract.multiplier", "100"),
                ("instrument.kind", "option"), ("model.convention", "controlled-model/1"),
                ("value.role", ("model_iv", "model_delta", "option_right")[role]),
            ))
            projected[(tag, role)] = item
    assert len(projected) == 6
    assert projected[("C25", 1)].native_value == Decimal(".25")
    assert projected[("P25", 1)].native_value == Decimal("-.25")
    assert projected[("C25", 2)].native_value == "C"
    assert projected[("P25", 2)].native_value == ("C" if refused else "P")
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d099.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    own_request = request()
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D099", subject_instrument=SUBJECT,
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.projection_mappings == MAPS and result.unit_conventions == UNITS
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            mapping.raw_signal_catalogue_id.value,
            projected[(tag, role)].observation_occurrence_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNITS[role].context_id, 1),
            projected[(tag, role)], values[tag][role], T,
        ) for tag in ("C25", "P25") for role, mapping in enumerate(MAPS[:2])
    )
    expected_rights = tuple(f.OptionRightLineageV1(
        "R015", projected[(tag, 2)].observation_occurrence_id.value,
        f.VersionRefV1(MAPS[2].mapping_id, 1), MAPS[2],
        projected[(tag, 2)], values[tag][2], values[tag][2], "option_right", T,
    ) for tag in ("C25", "P25"))
    assert result.result == f.OptionSkewV1(f.ExactRatioV1(10, 1), expected_rights)
    assert result.predecessors == () and result.window_seconds == 0
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.units == "volatility_points" and result.result_shape == "option_skew"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    persisted = reader.get_derived_occurrence(result.derived_occurrence_id)
    assert persisted == result and type(persisted.result) is f.OptionSkewV1
    assert persisted.result.native_right_lineage == expected_rights
    assert [x.projection.native_value for x in persisted.result.native_right_lineage] == ["C", "P"]
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
