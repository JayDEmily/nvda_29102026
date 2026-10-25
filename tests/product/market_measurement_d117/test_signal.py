"""D117 twenty-session receipt baseline and historically late required sample."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
C1 = "controlled-nvda-c110-20261023"
PROVIDER, VARIANT = "foundation-controlled-option-volume", "retained_realtime_counter_v1"
BRIEF = "b1ac74fb86cd171f3d4a431713cadeab9864a98b755a84016809aa8654120b33"
AUTHORITY = tuple(f.AuthorityArtifactRefV1(*x) for x in (
    ("handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
     "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c"),
    ("handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
     "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549"),
    ("handoff/m01_completion/authority/D117_OWNER_APPROVED_RAW_VOLUME_HISTORY_AMENDMENT_20261016.md",
     "7dab0973a7bafcdb284185f492fd37a4ad58d0e9e1246e6f37c3fa893e8023df"),
    ("handoff/m01_completion/authority/D117_OWNER_APPROVED_EXACT_CONTRACT_BASELINE_20261016.md",
     "b5b310413b9f2ded2d87e6b84994f531bb9aba2dd679c463deb48d0e54f7546b"),
))
META = (
    ("contract.id", ("contract", "id")), ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")), ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")), ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("calendar.id", ("calendar", "id")),
    ("calendar.version", ("calendar", "version")),
    ("session.id", ("session", "id")),
    ("stream.id", ("stream", "id")),
    ("stream.generation", ("stream", "generation")),
    ("source.mode", ("source", "mode")),
    ("counter.basis", ("counter", "basis")),
    ("counter.complete_from_open", ("counter", "complete_from_open")),
    ("value.role", ("value", "role")),
)
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r041-option-session-volume", 1, r.RawSignalCatalogueId("R041"), PROVIDER,
    VARIANT, ("session", "volume"), "contracts", META,
)
UNIT = f.UnitConventionVersionV1("mmt-option-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
DATES = tuple(datetime(2026, 9, 29, 12, tzinfo=UTC) + timedelta(days=i) for i in range(22))
CONTEXT = f.BaselineWindowContextV1(
    f.VersionRefV1("controlled-option-volume-calendar", 1), DATES[-1],
    DATES[-1] + timedelta(hours=1), DATES[0],
    tuple(f.SessionFrameV1(f.VersionRefV1("controlled-option-volume-" + day.strftime("%Y%m%d"), 1),
                           "controlled_option_regular", day, day + timedelta(hours=1))
          for day in DATES), 20, 2400,
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d117-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "calendar.id",
     "calendar.version", "session.id", "stream.id", "stream.generation",
     "source.mode", "counter.basis", "counter.complete_from_open"),
    timedelta(days=30), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D117", "D117-EXACT-CONTRACT-20SESSION-RECEIPT-1", "K04_STANDARDISE_RANK",
    "(current-mean(prior20))/sample_sd(prior20)", ("R041",), (), "P_BASELINE",
    "z_score", "scalar_decimal", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d117-controlled", 1, "P_BASELINE", C1, (C1,))


def request():
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D117", C1, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), (f.RawInputBindingV1(
            "R041", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), C1,
        ),),
    ), CONTEXT, ())


def native(day, volume):
    date = day.strftime("%Y%m%d")
    return {
        "contract": {"id": C1, "multiplier": "100"},
        "underlying": {"id": "NVDA"}, "expiry": {"date": "2026-10-23"},
        "strike": {"key": "110"}, "option": {"right": "C"},
        "currency": {"code": "USD"}, "instrument": {"kind": "option"},
        "calendar": {"id": "controlled-option-volume-calendar", "version": "1"},
        "session": {"id": f"controlled-option-volume-{date}/1", "volume": volume},
        "stream": {"id": "controlled-option-stream/1",
                   "generation": f"controlled-session-{date}/1"},
        "source": {"mode": "controlled_real_time"},
        "counter": {"basis": "cumulative_contracts_in_named_session",
                    "complete_from_open": "true"},
        "value": {"role": "reported_session_volume"},
    }


def lookup(obj, path):
    for key in path:
        obj = obj[key]
    return obj


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d117_signal(tmp_path, refused):
    raw = r.create_owner()
    expected = {}
    for index, day in enumerate(DATES):
        minute = day + timedelta(minutes=40)
        volume = Decimal(999 if index == 0 else 25 if index == 21 else
                         10 if (index - 1) % 2 == 0 else 20)
        event = minute if index == 21 else minute - timedelta(seconds=1)
        if index == 2:  # 1 October: source event outside its own receipt interval.
            event = day + timedelta(minutes=38, seconds=30)
        receipt = minute if index == 21 else minute - timedelta(seconds=1)
        if refused and index == 1:  # 30 September: globally visible, historically late.
            receipt = minute + timedelta(seconds=1)
        stamp = event.isoformat().replace("+00:00", "Z")
        identity = f"d117-{index}"
        obj = native(day, volume)
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            delivery_artifact_ref=r.delivery_artifact_ref("d117-controlled"),
            source_provider=r.provider_id(PROVIDER), native_record=obj,
            received_ts_utc=receipt, ingestion_sequence=index + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(r.RawSignalCatalogueId("R041"),),
            source_variant=VARIANT, subject_instrument=C1, native_units="contracts",
            source_timestamp_raw=stamp, source_timezone_native="UTC",
        ))
        expected[identity] = (volume, event, receipt, obj)
    actual = {}
    cursor = None
    pages = 0
    while True:
        page = raw.reads.list_projected_raw_history(
            r.RawSignalCatalogueId("R041"), mappings=(MAPPING,), subject_instrument=C1,
            received_at_or_before_utc=CUTOFF, event_at_or_before_utc=T,
            limit=100, cursor=cursor,
        )
        pages += 1
        for item in page.items:
            identity = item.observation_occurrence_id.value
            value, event, receipt, obj = expected[identity]
            assert item.native_value == value
            assert item.received_ts_utc == receipt
            assert item.source_timestamp_raw == event.isoformat().replace("+00:00", "Z")
            assert item.selection_identity == r.RawSelectionIdentityV1(tuple(
                (key, lookup(obj, path)) for key, path in META
            ))
            actual[identity] = item
        cursor = page.next_cursor
        if cursor is None:
            break
        assert pages < 1000
    assert pages == 1 and len(actual) == 22 and set(actual) == set(expected)
    october1 = expected["d117-2"]
    assert october1[1] == DATES[2] + timedelta(minutes=38, seconds=30)
    assert october1[2] == DATES[2] + timedelta(minutes=39, seconds=59)
    assert october1[1] < DATES[2] + timedelta(minutes=39) < october1[2]
    september30 = expected["d117-1"]
    assert september30[1] == DATES[1] + timedelta(minutes=39, seconds=59)
    assert september30[2] == DATES[1] + timedelta(minutes=40, seconds=1 if refused else -1)
    assert september30[2] <= CUTOFF
    assert expected["d117-0"][0] == 999
    assert tuple(expected[f"d117-{i}"][0] for i in range(1, 21)) == (
        Decimal(10), Decimal(20)) * 10
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d117.sqlite")
    owner = f.create_window_owner(admission=admission, raw_projection_reader=raw.reads,
                                  storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW)
    own_request = request()
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D117", subject_instrument=C1,
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=30)
    if refused:
        assert september30[2] > DATES[1] + timedelta(minutes=40)
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == Decimal("1.9493588689617927813676826399799200598505167800675")
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.projection_mappings == (MAPPING,) and result.unit_conventions == (UNIT,)
    order = (21, *range(1, 21))
    assert result.raw_input_lineage == tuple(f.RawInputLineageV1(
        "R041", actual[f"d117-{i}"].observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        actual[f"d117-{i}"], expected[f"d117-{i}"][0], expected[f"d117-{i}"][1],
    ) for i in order)
    assert "d117-0" not in tuple(x.observation_occurrence_id for x in result.raw_input_lineage)
    assert result.predecessors == () and result.window_seconds == 2400
    assert result.units == "z_score" and result.result_shape == "scalar_decimal"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
