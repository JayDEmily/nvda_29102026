"""D088: direct C1 quote matched to actual public D087 or wrong C2 parent."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
C1, C2 = "controlled-nvda-c110-20261023", "controlled-nvda-p110-20261023"
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
PARENT_BRIEF = "103777a517401fcb08099acb6fe7c915286499819c1f8f71da50c4bf71cc8468"
BRIEF = "23129ece93db232f4258187a6aef130f74652814512d49cd4db2127fd4a23cfb"
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
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
        PROVIDER, VARIANT, path, "USD_per_share", META,
    ) for raw, path in (("R034", ("quote", "bid")), ("R035", ("quote", "ask")))
)
UNIT = f.UnitConventionVersionV1(
    "mmt-option-price", 1, "USD_per_share", "USD_per_share", Decimal("1"), Decimal("0")
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC), datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
POLICY_D087 = f.InputSelectionPolicyVersionV1(
    "mmt-d087-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), (), PROVIDER, VARIANT,
    PROVIDER + "/" + VARIANT, 100, 1000,
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d088-selection", 1, POLICY_D087.join_keys, POLICY_D087.maximum_staleness,
    POLICY_D087.maximum_skew, POLICY_D087.temporal_basis_permissions, (), PROVIDER,
    VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEF_PARENT = f.CalculationDefinitionV1(
    "D087", "D087-OPTION-SCALAR-1", "K02_ALGEBRA", "(bid+ask)/2",
    ("R034", "R035"), (), "P_BASIC", "option_premium", "exact_ratio", AUTHORITY,
)
DEFINITION = f.CalculationDefinitionV1(
    "D088", "D088-OPTION-SCALAR-1", "K02_ALGEBRA", "100*(ask-bid)/mid",
    ("R034", "R035"), ("D087",), "P_BASIC", "percent", "exact_ratio", AUTHORITY,
)
PARAM = f.CalculationParameterSetV1("mmt-d088-controlled", 1, "P_BASIC", C1, (C1,))


def parent_param(contract):
    tag = "c1" if contract == C1 else "c2"
    return f.CalculationParameterSetV1(
        f"mmt-d087-{tag}-controlled", 1, "P_BASIC", contract, (contract,)
    )


def request(identity, contract, parent_id=()):
    param = parent_param(contract) if identity == "D087" else PARAM
    definition = DEF_PARENT if identity == "D087" else DEFINITION
    policy = POLICY_D087 if identity == "D087" else POLICY
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            identity, contract if identity == "D087" else C1, T, CUTOFF,
            definition.calculation_definition_version,
            f.VersionRefV1(param.context_id, 1), f.VersionRefV1(policy.context_id, 1),
            (CONTEXT.ref,),
            tuple(
                f.RawInputBindingV1(
                    mapping.raw_signal_catalogue_id.value,
                    f.VersionRefV1(mapping.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1), contract if identity == "D087" else C1,
                ) for mapping in MAPS
            ),
        ), CONTEXT, parent_id,
    )


def native(contract, role, price):
    return {
        "quote": {"bid" if role == 0 else "ask": price},
        "contract": {"id": contract, "multiplier": "100"},
        "underlying": {"id": "NVDA"}, "expiry": {"date": "2026-10-23"},
        "strike": {"key": "110"}, "option": {"right": "C" if contract == C1 else "P"},
        "currency": {"code": "USD"}, "instrument": {"kind": "option"},
        "model": {"convention": "controlled-model/1"},
        "value": {"role": "option_bid" if role == 0 else "option_ask"},
    }


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d088_signal(tmp_path, refused):
    raw = r.create_owner()
    projected = {}
    contracts = (C1, C2) if refused else (C1,)
    for contract_index, contract in enumerate(contracts):
        for role, mapping in enumerate(MAPS):
            amount = Decimal("2" if role == 0 else "4")
            identity = f"d088-{contract_index}-{role}"
            raw.commands.admit_raw_observation_occurrence(
                r.RawObservationOccurrenceV1(
                    concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=r.observation_occurrence_id(identity),
                    delivery_artifact_ref=r.delivery_artifact_ref("d088-controlled"),
                    source_provider=r.provider_id(PROVIDER),
                    native_record=native(contract, role, amount), received_ts_utc=T,
                    ingestion_sequence=contract_index * 2 + role + 1,
                    ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                    source_temporal_kind="true_instant",
                    raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                    source_variant=VARIANT, subject_instrument=contract,
                    native_units="USD_per_share", source_timestamp_raw="2026-10-20T12:40:00Z",
                    source_timezone_native="UTC",
                )
            )
            page = raw.reads.list_projected_raw_history(
                mapping.raw_signal_catalogue_id, mappings=(mapping,),
                subject_instrument=contract, received_at_or_before_utc=CUTOFF,
                event_at_or_before_utc=T, limit=100, cursor=None,
            )
            assert page.next_cursor is None and len(page.items) == 1
            item = page.items[0]
            assert item.observation_occurrence_id.value == identity
            assert item.native_value == amount and item.received_ts_utc == T
            assert item.selection_identity == r.RawSelectionIdentityV1((
                ("contract.id", contract), ("underlying.id", "NVDA"),
                ("expiry.date", "2026-10-23"), ("strike.key", "110"),
                ("option.right", "C" if contract == C1 else "P"),
                ("currency.code", "USD"), ("contract.multiplier", "100"),
                ("instrument.kind", "option"),
                ("model.convention", "controlled-model/1"),
                ("value.role", "option_bid" if role == 0 else "option_ask"),
            ))
            projected[(contract, role)] = item
    assert len(projected) == (4 if refused else 2)
    parent_contract = C2 if refused else C1
    parent_admission = f.OwnerAdmissionV1("M02", PARENT_BRIEF)
    parent_path = str(tmp_path / "parent.sqlite")
    parent_owner = f.create_window_owner(
        admission=parent_admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(parent_path, True), utc_now=lambda: NOW,
    )
    parent_request = request("D087", parent_contract)
    parent = parent_owner.materialise(parent_request)
    assert type(parent) is f.WindowMeasurementOccurrenceV1
    assert parent.result == f.ExactRatioV1(3, 1)
    assert parent.request == parent_request and parent.definition == DEF_PARENT
    assert parent.parameter_set == parent_param(parent_contract)
    assert parent.input_selection_policy == POLICY_D087
    assert parent.implementation_brief_sha256 == PARENT_BRIEF
    assert parent.projection_mappings == MAPS and parent.unit_conventions == (UNIT,)
    assert parent.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            mapping.raw_signal_catalogue_id.value,
            projected[(parent_contract, i)].observation_occurrence_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
            projected[(parent_contract, i)], Decimal("2" if i == 0 else "4"), T,
        ) for i, mapping in enumerate(MAPS)
    )
    parent_reader = f.create_window_reader(
        admission=parent_admission, storage=f.SQLiteReadStorageV1(parent_path)
    )
    assert parent_reader.get_derived_occurrence(parent.derived_occurrence_id) == parent
    if refused:
        assert parent.request.calculation.subject_instrument == C2
        assert all((C1, i) in projected for i in (0, 1))
    own_request = request("D088", C1, (parent.derived_occurrence_id,))
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d088.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=parent_reader, storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(
        derived_signal_id="D088", subject_instrument=C1,
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10,
    )
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is f.ExactRatioV1 and result.result == f.ExactRatioV1(200, 3)
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAM and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.projection_mappings == MAPS and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            mapping.raw_signal_catalogue_id.value,
            projected[(C1, i)].observation_occurrence_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
            projected[(C1, i)], Decimal("2" if i == 0 else "4"), T,
        ) for i, mapping in enumerate(MAPS)
    )
    assert result.predecessors == (parent,) and result.window_seconds == 0
    assert result.predecessors[0].raw_input_lineage == result.raw_input_lineage
    assert result.units == "percent" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
