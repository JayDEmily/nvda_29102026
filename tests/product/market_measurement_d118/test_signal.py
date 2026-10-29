"""D118 exact four-contract call/put volume basket and missing P10 refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT = "NVDA_ACTIVITY_E1"
TAGS = ("C25", "C10", "P25", "P10")
MEMBERS = tuple(f"controlled-skew-2026-10-23-{tag}" for tag in TAGS)
STRIKES = ("120", "130", "100", "90")
AMOUNTS = (Decimal(7), Decimal(5), Decimal(1), Decimal(3))
PROVIDER, VARIANT = "foundation-controlled-option-activity", "member_volume_v1"
BRIEF = "64e2717a7065a043ef65d3130b12cedd78733083eaf83bacb3e48be6d95434d1"
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
    ("source.mode", ("source", "mode")),
    ("session.id", ("session", "id")),
    ("counter.generation", ("counter", "generation")),
    ("counter.basis", ("counter", "basis")),
    ("value.role", ("value", "role")),
)
MAPS = (
    r.RawSignalProjectionMappingV1(
        "mmt-r049-member-call-volume", 1, r.RawSignalCatalogueId("R049"),
        PROVIDER, VARIANT, ("activity", "call_volume"), "contracts", META,
    ),
    r.RawSignalProjectionMappingV1(
        "mmt-r050-member-put-volume", 1, r.RawSignalCatalogueId("R050"),
        PROVIDER, VARIANT, ("activity", "put_volume"), "contracts", META,
    ),
)
UNIT = f.UnitConventionVersionV1("mmt-option-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1), datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC), datetime(2026, 10, 20, 12, tzinfo=UTC),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d118-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "source.mode",
     "session.id", "counter.generation", "counter.basis"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D118", "D118-CALL-PUT-VOLUME-BASKET-1", "K02_ALGEBRA",
    "sum(call_member_volume)/sum(put_member_volume)", ("R049", "R050"), (),
    "P_BASIC", "ratio", "exact_ratio", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d118-controlled", 1, "P_BASIC", SUBJECT, MEMBERS)


def request():
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D118", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), tuple(f.RawInputBindingV1(
            MAPS[index // 2].raw_signal_catalogue_id.value,
            f.VersionRefV1(MAPS[index // 2].mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), member,
        ) for index, member in enumerate(MEMBERS)),
    ), CONTEXT, ())


def native(index):
    member, amount = MEMBERS[index], AMOUNTS[index]
    call = index < 2
    return {
        "contract": {"id": member, "multiplier": "100"},
        "underlying": {"id": "NVDA"}, "expiry": {"date": "2026-10-23"},
        "strike": {"key": STRIKES[index]}, "option": {"right": "C" if call else "P"},
        "currency": {"code": "USD"}, "instrument": {"kind": "option"},
        "source": {"mode": "controlled_real_time"},
        "session": {"id": "controlled-option-20oct12-13Z"},
        "counter": {"generation": "controlled-counter-20261020/1",
                    "basis": "per_contract_cumulative_session"},
        "value": {"role": "call_volume" if call else "put_volume"},
        "activity": {"call_volume" if call else "put_volume": amount},
    }


def lookup(obj, path):
    for key in path:
        obj = obj[key]
    return obj


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d118_signal(tmp_path, refused):
    raw = r.create_owner()
    expected = {}
    for index, member in enumerate(MEMBERS):
        if refused and index == 3:
            continue
        mapping = MAPS[index // 2]
        obj = native(index)
        identity = f"d118-{index}"
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            delivery_artifact_ref=r.delivery_artifact_ref("d118-controlled"),
            source_provider=r.provider_id(PROVIDER), native_record=obj,
            received_ts_utc=T, ingestion_sequence=index + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
            source_variant=VARIANT, subject_instrument=member, native_units="contracts",
            source_timestamp_raw="2026-10-20T12:40:00Z", source_timezone_native="UTC",
        ))
        expected[index] = obj
    projected = {}
    for index, member in enumerate(MEMBERS):
        mapping = MAPS[index // 2]
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,), subject_instrument=member,
            received_at_or_before_utc=CUTOFF, event_at_or_before_utc=T, limit=100,
            cursor=None,
        )
        assert page.next_cursor is None
        if index not in expected:
            assert page.items == ()
            continue
        assert len(page.items) == 1
        item = page.items[0]
        obj = expected[index]
        assert item.observation_occurrence_id.value == f"d118-{index}"
        assert item.native_value == AMOUNTS[index] and item.received_ts_utc == T
        assert item.source_timestamp_raw == "2026-10-20T12:40:00Z"
        assert item.selection_identity == r.RawSelectionIdentityV1(tuple(
            (key, lookup(obj, path)) for key, path in META
        ))
        projected[index] = item
    assert len(projected) == (3 if refused else 4)
    assert tuple(int(STRIKES[i]) for i in range(4)) == (120, 130, 100, 90)
    assert all(90 <= int(x) <= 130 for x in STRIKES)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d118.sqlite")
    owner = f.create_window_owner(admission=admission, raw_projection_reader=raw.reads,
                                  storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW)
    own_request = request()
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D118", subject_instrument=SUBJECT,
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if refused:
        assert set(projected) == {0, 1, 2}
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == f.ExactRatioV1(3, 1)
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.projection_mappings == MAPS and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(f.RawInputLineageV1(
        MAPS[index // 2].raw_signal_catalogue_id.value,
        projected[index].observation_occurrence_id.value,
        f.VersionRefV1(MAPS[index // 2].mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        projected[index], AMOUNTS[index], T,
    ) for index in range(4))
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
