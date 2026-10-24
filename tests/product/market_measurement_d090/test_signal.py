"""D090: bounded log-moneyness and selected negative-spot refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
C1 = "controlled-nvda-c110-20261023"
C2 = "controlled-nvda-p110-20261023"
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
BRIEF = "5f3f5938be58e677cd56e1a733f7a1959d6f1c64ef70d7fca5ac53af7f0514a6"
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
    ("contract.id", ("contract", "id")),
    ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")),
    ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")),
    ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("model.convention", ("model", "convention")),
    ("value.role", ("value", "role")),
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
        PROVIDER, VARIANT, path, "USD_per_share", META,
    ) for raw, path in (("R014", ("contract", "strike")), ("R118", ("model", "underlying_price")))
)
UNIT = f.UnitConventionVersionV1(
    "mmt-option-price", 1, "USD_per_share", "USD_per_share", Decimal("1"), Decimal("0")
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
DEFINITION = f.CalculationDefinitionV1(
    "D090", "D090-OPTION-SCALAR-1", "K02_ALGEBRA", "ln(strike/spot)",
    ("R014", "R118"), (), "P_BASIC", "dimensionless", "scalar_decimal", AUTHORITY,
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d090-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def parameter(contract):
    return f.CalculationParameterSetV1("mmt-d090-controlled", 1, "P_BASIC", contract, (contract,))


def request(contract):
    param = parameter(contract)
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D090", contract, T, CUTOFF, DEFINITION.calculation_definition_version,
            f.VersionRefV1(param.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            tuple(
                f.RawInputBindingV1(
                    mapping.raw_signal_catalogue_id.value,
                    f.VersionRefV1(mapping.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1), contract,
                ) for mapping in MAPS
            ),
        ), CONTEXT, (),
    )


def native(contract, role, price):
    return {
        "contract": {
            "id": contract, "multiplier": "100",
            **({"strike": price} if role == 0 else {}),
        },
        "underlying": {"id": "NVDA"}, "expiry": {"date": "2026-10-23"},
        "strike": {"key": "110"},
        "option": {"right": "C" if contract == C1 else "P"},
        "currency": {"code": "USD"}, "instrument": {"kind": "option"},
        "model": {
            "convention": "controlled-model/1",
            **({"underlying_price": price} if role else {}),
        },
        "value": {"role": "option_strike" if role == 0 else "model_underlying_price"},
    }


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d090_signal(tmp_path, refused):
    raw = r.create_owner()
    amounts = (Decimal("110"), Decimal("-1")) if refused else (Decimal("110"), Decimal("100"))
    projected = []
    for role, mapping in enumerate(MAPS):
        identity = f"d090-c1-{role}"
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("d090-controlled"),
                source_provider=r.provider_id(PROVIDER),
                native_record=native(C1, role, amounts[role]),
                received_ts_utc=T, ingestion_sequence=role + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                source_variant=VARIANT, subject_instrument=C1, native_units="USD_per_share",
                source_timestamp_raw="2026-10-20T12:40:00Z", source_timezone_native="UTC",
            )
        )
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,), subject_instrument=C1,
            received_at_or_before_utc=CUTOFF, event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert page.next_cursor is None and len(page.items) == 1
        item = page.items[0]
        assert item.observation_occurrence_id.value == identity
        assert item.native_value == amounts[role] and item.received_ts_utc == T
        assert item.selection_identity == r.RawSelectionIdentityV1((
            ("contract.id", C1), ("underlying.id", "NVDA"),
            ("expiry.date", "2026-10-23"), ("strike.key", "110"),
            ("option.right", "C"), ("currency.code", "USD"),
            ("contract.multiplier", "100"), ("instrument.kind", "option"),
            ("model.convention", "controlled-model/1"),
            ("value.role", "option_strike" if role == 0 else "model_underlying_price"),
        ))
        projected.append(item)
    assert len(projected) == 2
    if refused:
        assert projected[1].native_value == Decimal("-1")
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d090.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    own_request = request(C1)
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(
        derived_signal_id="D090", subject_instrument=C1,
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10,
    )
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is Decimal
    assert result.result == Decimal("0.095310179804324860043952123280765092220605365308644")
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == parameter(C1) and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.projection_mappings == MAPS and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            mapping.raw_signal_catalogue_id.value, projected[i].observation_occurrence_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
            projected[i], amounts[i], T,
        ) for i, mapping in enumerate(MAPS)
    )
    assert result.predecessors == () and result.window_seconds == 0
    assert result.units == "dimensionless" and result.result_shape == "scalar_decimal"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
