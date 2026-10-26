"""D124 exact strike/expiry OI shares and HHI with missing contract refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT = "NVDA_OI_CONCENTRATION_E1"
TAGS = ("100-C", "105-C", "100-P", "105-P")
MEMBERS = tuple(f"controlled-oi-E1-{tag}" for tag in TAGS)
STRIKES = ("100", "105", "100", "105")
AMOUNTS = (Decimal(20), Decimal(6), Decimal(10), Decimal(4))
PROVIDER, VARIANT = "foundation-controlled-option-activity", "member_oi_concentration_v1"
BRIEF = "de019a62f030ebe9380a53072ec20dad64493531f43d0b7c8910ae1d8bd719a1"
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
    ("official.period_id", ("official", "period_id")),
    ("official.revision_id", ("official", "revision_id")),
    ("value.role", ("value", "role")),
)
MAPS = (
    r.RawSignalProjectionMappingV1(
        "mmt-r047-member-call-oi", 1, r.RawSignalCatalogueId("R047"),
        PROVIDER, VARIANT, ("oi", "call"), "contracts", META,
    ),
    r.RawSignalProjectionMappingV1(
        "mmt-r048-member-put-oi", 1, r.RawSignalCatalogueId("R048"),
        PROVIDER, VARIANT, ("oi", "put"), "contracts", META,
    ),
)
UNIT = f.UnitConventionVersionV1("mmt-option-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1), datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC), datetime(2026, 10, 20, 12, tzinfo=UTC),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d124-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "source.mode",
     "official.period_id", "official.revision_id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D124", "D124-STRIKE-EXPIRY-OI-HHI-1", "K08_RULE_BUCKET_POLICY",
    "strike_expiry shares and sum of squared shares", ("R047", "R048"), (),
    "P_BASIC", "concentration", "strike_expiry_hhi", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d124-controlled", 1, "P_BASIC", SUBJECT, MEMBERS)


def request():
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D124", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
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
        "official": {"period_id": "controlled-oi-period-20261020/1",
                     "revision_id": "controlled-oi-revision/1"},
        "value": {"role": "call_oi" if call else "put_oi"},
        "oi": {"call" if call else "put": amount},
    }


def lookup(obj, path):
    for key in path:
        obj = obj[key]
    return obj


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d124_signal(tmp_path, refused):
    raw = r.create_owner()
    expected = {}
    for index, member in enumerate(MEMBERS):
        if refused and index == 3:
            continue
        mapping = MAPS[index // 2]
        obj = native(index)
        identity = f"d124-{index}"
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            delivery_artifact_ref=r.delivery_artifact_ref("d124-controlled"),
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
        assert item.observation_occurrence_id.value == f"d124-{index}"
        assert item.native_value == AMOUNTS[index] and item.received_ts_utc == T
        assert item.source_timestamp_raw == "2026-10-20T12:40:00Z"
        assert item.selection_identity == r.RawSelectionIdentityV1(tuple(
            (key, lookup(obj, path)) for key, path in META
        ))
        projected[index] = item
    assert len(projected) == (3 if refused else 4)
    assert tuple(int(STRIKES[i]) for i in range(4)) == (100, 105, 100, 105)
    assert all(90 <= int(x) <= 130 for x in STRIKES)
    assert all(item.selection_identity.value_for("official.period_id") ==
               "controlled-oi-period-20261020/1" for item in projected.values())
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d124.sqlite")
    owner = f.create_window_owner(admission=admission, raw_projection_reader=raw.reads,
                                  storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW)
    own_request = request()
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D124", subject_instrument=SUBJECT,
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if refused:
        assert set(projected) == {0, 1, 2}
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == f.OIConcentrationV1(
        (("2026-10-23", "100"), ("2026-10-23", "105")),
        (f.ExactRatioV1(3, 4), f.ExactRatioV1(1, 4)), f.ExactRatioV1(5, 8),
    )
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
    assert result.units == "concentration" and result.result_shape == "strike_expiry_hhi"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
