"""D116 exact CALL volume/OI and selected-zero-denominator refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
C1, C2 = "controlled-nvda-c110-20261023", "controlled-nvda-p110-20261023"
PROVIDER, VARIANT = "foundation-controlled-option-activity", "volume_oi_v1"
BRIEF = "4aff69cb6d28b19bb9d0490bae077036c59eda5923e8bd305cfa4e7549b447df"
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
BASE_META = (
    ("contract.id", ("contract", "id")), ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")), ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")), ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("value.role", ("value", "role")), ("source.mode", ("source", "mode")),
)
VOLUME_META = (*BASE_META,
    ("session.id", ("session", "id")),
    ("counter.generation", ("counter", "generation")),
    ("counter.basis", ("counter", "basis")),
)
OI_META = (*BASE_META, ("official.period_id", ("official", "period_id")))
MAPS = (
    r.RawSignalProjectionMappingV1("mmt-r041-option-volume", 1, r.RawSignalCatalogueId("R041"),
                                   PROVIDER, VARIANT, ("activity", "cumulative_volume"),
                                   "contracts", VOLUME_META),
    r.RawSignalProjectionMappingV1("mmt-r047-option-oi", 1, r.RawSignalCatalogueId("R047"),
                                   PROVIDER, VARIANT, ("oi", "call"), "contracts", OI_META),
    r.RawSignalProjectionMappingV1("mmt-r048-option-oi", 1, r.RawSignalCatalogueId("R048"),
                                   PROVIDER, VARIANT, ("oi", "put"), "contracts", OI_META),
)
UNIT = f.UnitConventionVersionV1("mmt-option-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-option-session", 1),
                            datetime(2026, 10, 20, 12, tzinfo=UTC),
                            datetime(2026, 10, 20, 13, tzinfo=UTC),
                            datetime(2026, 10, 20, 12, tzinfo=UTC))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d116-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "source.mode"),
    timedelta(seconds=60), timedelta(seconds=1), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D116", "D116-OPTION-VOLUME-OI-1", "K02_ALGEBRA", "volume/applicable_open_interest",
    ("R041", "R047", "R048"), (), "P_BASIC", "ratio", "exact_ratio", AUTHORITY,
)


def parameter(contract):
    return f.CalculationParameterSetV1(
        "mmt-d116-c1-controlled" if contract == C1 else "mmt-d116-c2-controlled", 1,
        "P_BASIC", contract, (contract,),
    )


def request(contract):
    param = parameter(contract)
    applicable = MAPS[:2] if contract == C1 else (MAPS[0], MAPS[2])
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D116", contract, T, CUTOFF, DEFINITION.calculation_definition_version,
            f.VersionRefV1(param.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,), tuple(f.RawInputBindingV1(
                mapping.raw_signal_catalogue_id.value, f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1), contract,
            ) for mapping in applicable),
        ), CONTEXT, (),
    )


def native(contract, role, amount):
    result = {
        "contract": {"id": contract, "multiplier": "100"},
        "underlying": {"id": "NVDA"}, "expiry": {"date": "2026-10-23"},
        "strike": {"key": "110"}, "option": {"right": "C" if contract == C1 else "P"},
        "currency": {"code": "USD"}, "instrument": {"kind": "option"},
        "value": {"role": "reported_session_volume" if role == 0 else
                  "call_open_interest" if role == 1 else "put_open_interest"},
        "source": {"mode": "controlled_real_time" if role == 0 else
                   "controlled_official_snapshot"},
    }
    if role == 0:
        result.update(activity={"cumulative_volume": amount},
                      session={"id": "controlled-option-20oct12-13Z"},
                      counter={"generation": "controlled-counter-20261020/1",
                               "basis": "cumulative_contracts"})
    else:
        result.update(oi={"call" if role == 1 else "put": amount},
                      official={"period_id": "controlled-OI-20261020/1"})
    return result


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d116_signal(tmp_path, refused):
    raw = r.create_owner()
    latest = Decimal(0 if refused else 20)
    facts = ((0, Decimal(30), T), (1, Decimal(10), T - timedelta(seconds=1)),
             (1, latest, T))
    projected = []
    for index, (role, amount, when) in enumerate(facts):
        mapping = MAPS[role]
        stamp = when.isoformat().replace("+00:00", "Z")
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d116-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d116-controlled"),
            source_provider=r.provider_id(PROVIDER), native_record=native(C1, role, amount),
            received_ts_utc=when, ingestion_sequence=index + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,), source_variant=VARIANT,
            subject_instrument=C1, native_units="contracts", source_timestamp_raw=stamp,
            source_timezone_native="UTC",
        ))
    for role, expected in ((0, ((Decimal(30), T, "d116-0"),)),
                           (1, ((Decimal(10), T-timedelta(seconds=1), "d116-1"),
                                (latest, T, "d116-2")))):
        page = raw.reads.list_projected_raw_history(
            MAPS[role].raw_signal_catalogue_id, mappings=(MAPS[role],),
            subject_instrument=C1, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert page.next_cursor is None and len(page.items) == len(expected)
        by_id = {x.observation_occurrence_id.value: x for x in page.items}
        for amount, when, identity in expected:
            item = by_id[identity]
            assert item.native_value == amount and item.received_ts_utc == when
            assert item.source_timestamp_raw == when.isoformat().replace("+00:00", "Z")
            assert item.selection_identity == r.RawSelectionIdentityV1(tuple(
                (key, str(value)) for key, path in MAPS[role].selection_identity_field_paths
                for value in (lookup(native(C1, role, amount), path),)
            ))
        projected.append(by_id)
    assert raw.reads.list_projected_raw_history(
        MAPS[2].raw_signal_catalogue_id, mappings=(MAPS[2],), subject_instrument=C1,
        received_at_or_before_utc=CUTOFF, event_at_or_before_utc=T, limit=100,
        cursor=None,
    ).items == ()
    assert (projected[1]["d116-1"].native_value > latest) if refused else (Decimal(10) < latest)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d116.sqlite")
    owner = f.create_window_owner(admission=admission, raw_projection_reader=raw.reads,
                                  storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW)
    own_request = request(C1)
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D116", subject_instrument=C1,
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == f.ExactRatioV1(3, 2)
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == parameter(C1) and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.projection_mappings == MAPS[:2] and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(f.RawInputLineageV1(
        MAPS[role].raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(MAPS[role].mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, amount, T,
    ) for role, item, amount in ((0, projected[0]["d116-0"], Decimal(30)),
                               (1, projected[1]["d116-2"], Decimal(20))))
    assert result.predecessors == () and result.window_seconds == 0
    assert result.units == "ratio" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)


def lookup(value, path):
    for key in path:
        value = value[key]
    return value
