"""D094: exact contract five-minute model IV change and reached C2 reference refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
C1, C2 = "controlled-nvda-c110-20261023", "controlled-nvda-p110-20261023"
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
BRIEF = "93e7054fd91487f6a8fe2fa1b2118ed82e35b0094c4950841fbb174b1c41b6f5"
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
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r111-option", 1, r.RawSignalCatalogueId("R111"),
    PROVIDER, VARIANT, ("model", "iv"), "annualised_decimal_volatility", META,
)
UNIT = f.UnitConventionVersionV1(
    "mmt-option-iv", 1, "annualised_decimal_volatility",
    "annualised_decimal_volatility", Decimal("1"), Decimal("0"),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-iv-window", 1),
    T - timedelta(seconds=600), datetime(2026, 10, 20, 13, tzinfo=UTC),
    T - timedelta(seconds=600),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d094-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=600), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D094", "D094-OPTION-IV-CHANGE-5M-1", "K03_CHANGE_RETURN",
    "100*(current_iv-reference_iv)", ("R111",), (), "P_WINDOW",
    "volatility_points", "exact_ratio", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d094-controlled", 1, "P_WINDOW", C1, (C1,))


def request():
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D094", C1, T, CUTOFF, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            (f.RawInputBindingV1(
                "R111", f.VersionRefV1(MAPPING.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1), C1,
            ),),
        ), CONTEXT, (),
    )


def native(contract, value):
    return {
        "contract": {"id": contract, "multiplier": "100"},
        "underlying": {"id": "NVDA"}, "expiry": {"date": "2026-10-23"},
        "strike": {"key": "110"}, "option": {"right": "P" if contract == C2 else "C"},
        "currency": {"code": "USD"}, "instrument": {"kind": "option"},
        "model": {"convention": "controlled-model/1", "iv": value},
        "value": {"role": "model_iv"},
    }


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d094_signal(tmp_path, refused):
    raw = r.create_owner()
    observations = (
        (C1, 0, Decimal("0.53")), (C1, 120, Decimal("0.90")),
        (C2 if refused else C1, 300, Decimal("0.50")),
        (C2 if refused else C1, 360, Decimal("0.48")),
    )
    projected = {}
    for seq, (contract, lag, value) in enumerate(observations, start=1):
        event = T - timedelta(seconds=lag)
        identity = f"d094-{seq}"
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            delivery_artifact_ref=r.delivery_artifact_ref("d094-controlled"),
            source_provider=r.provider_id(PROVIDER), native_record=native(contract, value),
            received_ts_utc=event, ingestion_sequence=seq,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(r.RawSignalCatalogueId("R111"),),
            source_variant=VARIANT, subject_instrument=contract,
            native_units="annualised_decimal_volatility",
            source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
            source_timezone_native="UTC",
        ))
        page = raw.reads.list_projected_raw_history(
            r.RawSignalCatalogueId("R111"), mappings=(MAPPING,),
            subject_instrument=contract, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert page.next_cursor is None
        matching = [item for item in page.items if item.observation_occurrence_id.value == identity]
        assert len(matching) == 1
        item = matching[0]
        assert item.native_value == value and item.received_ts_utc == event
        assert item.selection_identity == r.RawSelectionIdentityV1((
            ("contract.id", contract), ("underlying.id", "NVDA"),
            ("expiry.date", "2026-10-23"), ("strike.key", "110"),
            ("option.right", "P" if contract == C2 else "C"),
            ("currency.code", "USD"), ("contract.multiplier", "100"),
            ("instrument.kind", "option"), ("model.convention", "controlled-model/1"),
            ("value.role", "model_iv"),
        ))
        projected[lag] = item
    assert len(projected) == 4
    assert [projected[lag].native_value for lag in (0, 120, 300, 360)] == [
        Decimal(".53"), Decimal(".90"), Decimal(".50"), Decimal(".48")
    ]
    if refused:
        assert all(projected[lag].selection_identity.values[0] == ("contract.id", C2)
                   for lag in (300, 360))
        assert all(projected[lag].selection_identity.values[0] == ("contract.id", C1)
                   for lag in (0, 120))
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d094.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    own_request = request()
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D094", subject_instrument=C1,
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == f.ExactRatioV1(3, 1) and type(result.result) is f.ExactRatioV1
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.projection_mappings == (MAPPING,) and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            "R111", projected[lag].observation_occurrence_id.value,
            f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
            projected[lag], Decimal(".53" if lag == 0 else ".50"),
            T - timedelta(seconds=lag),
        ) for lag in (0, 300)
    )
    assert result.predecessors == () and result.window_seconds == 300
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.units == "volatility_points" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
