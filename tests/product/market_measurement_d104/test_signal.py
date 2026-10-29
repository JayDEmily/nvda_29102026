"""D104 genuine skew producers at two anchors, and wrong-expiry prior refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
A, CUTOFF, NOW = T - timedelta(seconds=300), T + timedelta(seconds=1), T + timedelta(seconds=2)
E1, E2 = "2026-10-23", "2026-10-30"
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
BRIEF = "a4a08441eddcc44ec5def45ccce81f9a1f5e426fa08c43e6691ef67b77658cc9"
BRIEFS = {"D099": "ab854fdd6a9a34c431c977fa973e392592be1e0d21854f4c95324852ed4f95a7",
          "D100": "15e3f6d0ea1568d4661d9695915c29b708c19197bbcfb111e42ddaae498fcd9d"}
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
    "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
    PROVIDER, VARIANT, path, unit, META,
) for raw, path, unit in (
    ("R111", ("model", "iv"), "annualised_decimal_volatility"),
    ("R112", ("model", "delta"), "delta_fraction"),
    ("R015", ("contract", "right"), "option_right"),
))
UNITS = tuple(f.UnitConventionVersionV1(name, 1, unit, unit, Decimal(1), Decimal(0))
              for name, unit in (
                  ("mmt-option-iv", "annualised_decimal_volatility"),
                  ("mmt-option-delta", "delta_fraction"),
                  ("mmt-option-right", "option_right"),
              ))
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC), datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
TAGS = {"D099": ("C25", "P25"), "D100": ("C10", "P10")}
STRIKES = {"C25": "120", "P25": "100", "C10": "130", "P10": "90"}
DELTA = {"C25": Decimal(".25"), "P25": Decimal("-.25"),
         "C10": Decimal(".10"), "P10": Decimal("-.10")}
IV = {("D099", A): (Decimal(".20"), Decimal(".28")),
      ("D099", T): (Decimal(".20"), Decimal(".30")),
      ("D100", A): (Decimal(".25"), Decimal(".37")),
      ("D100", T): (Decimal(".25"), Decimal(".40"))}
MEMBERS = tuple(f"controlled-skew-{E1}-{tag}" for tag in ("C25", "P25", "C10", "P10"))
PARAMETER = f.CalculationParameterSetV1("mmt-d104-controlled", 1, "P_WINDOW",
                                        "NVDA_SKEW_E1", MEMBERS)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d104-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=300), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D104", "D104-SKEW-ROTATION-5M-1", "K03_CHANGE_RETURN",
    "(D100_current-D099_current)-(D100_prior-D099_prior)",
    (), ("D099", "D100"), "P_WINDOW", "volatility_points", "exact_ratio", AUTHORITY,
)


def source_fact(raw, signal, expiry, anchor, tag, role, sequence):
    contract = f"controlled-skew-{expiry}-{tag}"
    side = tag[0]
    value = (IV[(signal, anchor)][0 if side == "C" else 1], DELTA[tag], side)[role]
    native = {
        "contract": {"id": contract, "multiplier": "100"},
        "underlying": {"id": "NVDA"}, "expiry": {"date": expiry},
        "strike": {"key": STRIKES[tag]}, "option": {"right": side},
        "currency": {"code": "USD"}, "instrument": {"kind": "option"},
        "model": {"convention": "controlled-model/1"},
        "value": {"role": ("model_iv", "model_delta", "option_right")[role]},
    }
    if role == 0:
        native["model"]["iv"] = value
    elif role == 1:
        native["model"]["delta"] = value
    else:
        native["contract"]["right"] = value
    mapping = MAPS[role]
    ident = f"d104-{sequence}"
    raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
        concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=r.observation_occurrence_id(ident),
        delivery_artifact_ref=r.delivery_artifact_ref("d104-controlled"),
        source_provider=r.provider_id(PROVIDER), native_record=native,
        received_ts_utc=anchor, ingestion_sequence=sequence,
        ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
        source_variant=VARIANT, subject_instrument=contract,
        native_units=mapping.native_units,
        source_timestamp_raw=anchor.isoformat().replace("+00:00", "Z"),
        source_timezone_native="UTC",
    ))
    page = raw.reads.list_projected_raw_history(
        mapping.raw_signal_catalogue_id, mappings=(mapping,),
        subject_instrument=contract, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    assert page.next_cursor is None
    matches = [x for x in page.items if x.observation_occurrence_id.value == ident]
    assert len(matches) == 1
    item = matches[0]
    assert item.native_value == value and item.received_ts_utc == anchor
    assert item.selection_identity == r.RawSelectionIdentityV1((
        ("contract.id", contract), ("underlying.id", "NVDA"),
        ("expiry.date", expiry), ("strike.key", STRIKES[tag]),
        ("option.right", side), ("currency.code", "USD"),
        ("contract.multiplier", "100"), ("instrument.kind", "option"),
        ("model.convention", "controlled-model/1"),
        ("value.role", ("model_iv", "model_delta", "option_right")[role]),
    ))
    return item


def producer_request(signal, expiry, anchor):
    key = "E1" if expiry == E1 else "E2"
    members = tuple(f"controlled-skew-{expiry}-{tag}" for tag in TAGS[signal])
    definition = f.CalculationDefinitionV1(
        signal, signal + "-NATIVE-DELTA-SKEW-1", "K02_ALGEBRA",
        "100*(put_iv-call_iv)", ("R111", "R112", "R015"), (),
        "P_BASIC", "volatility_points", "option_skew", AUTHORITY,
    )
    parameter = f.CalculationParameterSetV1(f"mmt-{signal.lower()}-{key}-controlled", 1,
                                            "P_BASIC", f"NVDA_SKEW_{expiry}", members)
    policy = f.InputSelectionPolicyVersionV1(
        f"mmt-{signal.lower()}-{key}-selection", 1,
        ("subject_instrument", "contract.id", "underlying.id", "expiry.date",
         "strike.key", "option.right", "currency.code", "contract.multiplier",
         "model.convention"), timedelta(seconds=60), timedelta(0),
        ("true_instant",), members, PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
    )
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        signal, f"NVDA_SKEW_{expiry}", anchor, CUTOFF,
        definition.calculation_definition_version,
        f.VersionRefV1(parameter.context_id, 1), f.VersionRefV1(policy.context_id, 1),
        (CONTEXT.ref,), tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(UNITS[role].context_id, 1), member,
        ) for member in members for role, mapping in enumerate(MAPS)),
    ), CONTEXT, ())


class ActualReads:
    def __init__(self, readers):
        self.readers = readers

    def get_derived_occurrence(self, derived_occurrence_id):
        found = tuple(p for reader in self.readers
                      if (p := reader.get_derived_occurrence(derived_occurrence_id)) is not None)
        assert len(found) <= 1
        return found[0] if found else None

    def list_derived_history(self, **kwargs):
        facts = tuple(p for reader in self.readers for p in reader.list_derived_history(**kwargs))
        ordered = sorted(facts, key=lambda x: (x.effective_as_of_utc,
                                               x.calculated_at_utc,
                                               x.derived_occurrence_id), reverse=True)
        return tuple(ordered[:kwargs["limit"]])


def request(parents):
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D104", "NVDA_SKEW_E1", T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), (),
    ), CONTEXT, tuple(p.derived_occurrence_id for p in parents))


@pytest.mark.parametrize("wrong_expiry", (False, True), ids=("success", "refusal"))
def test_d104_signal(tmp_path, wrong_expiry):
    raw = r.create_owner()
    projected = {}
    producer_specs = (("D099", E1, A), ("D100", E2 if wrong_expiry else E1, A),
                      ("D099", E1, T), ("D100", E1, T))
    for signal, expiry, anchor in producer_specs:
        for tag in TAGS[signal]:
            for role in range(3):
                projected[(signal, expiry, anchor, tag, role)] = source_fact(
                    raw, signal, expiry, anchor, tag, role, len(projected) + 1,
                )
    assert len(projected) == 24
    assert all(item.native_value == (IV[(signal, anchor)][0 if tag[0] == "C" else 1],
                                     DELTA[tag], tag[0])[role]
               for (signal, _expiry, anchor, tag, role), item in projected.items())
    parents = []
    readers = []
    for signal, expiry, anchor in producer_specs:
        owner = f.create_window_owner(
            admission=f.OwnerAdmissionV1("M02", BRIEFS[signal]),
            raw_projection_reader=raw.reads, storage=f.MemoryStorageV1(), utc_now=lambda: NOW,
        )
        parent = owner.materialise(producer_request(signal, expiry, anchor))
        assert type(parent) is f.WindowMeasurementOccurrenceV1
        expected = {("D099", A): 8, ("D100", A): 12,
                    ("D099", T): 10, ("D100", T): 15}[(signal, anchor)]
        assert parent.result.value == f.ExactRatioV1(expected, 1)
        assert len(parent.raw_input_lineage) == 4
        assert len(parent.result.native_right_lineage) == 2
        assert [x.projection.native_value for x in parent.result.native_right_lineage] == ["C", "P"]
        assert owner.reads.get_derived_occurrence(parent.derived_occurrence_id) == parent
        parents.append(parent)
        readers.append(owner.reads)
    assert tuple(p.derived_signal_id for p in parents) == ("D099", "D100", "D099", "D100")
    assert tuple(p.effective_as_of_utc for p in parents) == (A, A, T, T)
    assert parents[1].request.calculation.subject_instrument == (
        f"NVDA_SKEW_{E2}" if wrong_expiry else f"NVDA_SKEW_{E1}")
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d104.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=ActualReads(readers), storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    own_request = request(tuple(parents))
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D104", subject_instrument="NVDA_SKEW_E1",
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if wrong_expiry:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == f.ExactRatioV1(1, 1)
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.predecessors == tuple(parents) and result.window_seconds == 300
    assert result.raw_input_lineage == tuple(line for p in parents for line in p.raw_input_lineage)
    assert result.projection_mappings == MAPS and result.unit_conventions == UNITS
    assert result.units == "volatility_points" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    persisted = reader.get_derived_occurrence(result.derived_occurrence_id)
    assert persisted == result
    assert tuple(x.result.native_right_lineage for x in persisted.predecessors) == tuple(
        p.result.native_right_lineage for p in parents)
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
