"""D131: actual public midpoint and typed positional book, two controlled cases."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT = "controlled-nvda-c110-20261023"
OPTION_PROVIDER, OPTION_VARIANT = "foundation-controlled-options", "option_snapshot_v1"
BOOK_PROVIDER, BOOK_VARIANT = "foundation-controlled-smart-book", "positional_v1"
BOOK_GENERATION = "controlled-smart-book-generation/1"
OPTION_BRIEF = "103777a517401fcb08099acb6fe7c915286499819c1f8f71da50c4bf71cc8468"
BOOK_BRIEF = "c095187484e295c35e1c27906480a0793d81d76091fac21fc9002ac6c521302c"
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
OPTION_META = (
    ("contract.id", ("contract", "id")), ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")), ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")), ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("model.convention", ("model", "convention")), ("value.role", ("value", "role")),
)
OPTION_MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
    OPTION_PROVIDER, OPTION_VARIANT, ("quote", field), "USD_per_share", OPTION_META,
) for raw, field in (("R034", "bid"), ("R035", "ask")))
OPTION_UNIT = f.UnitConventionVersionV1(
    "mmt-option-price", 1, "USD_per_share", "USD_per_share", Decimal(1), Decimal(0),
)
OPTION_CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
OPTION_DEFINITION = f.CalculationDefinitionV1(
    "D087", "D087-OPTION-SCALAR-1", "K02_ALGEBRA", "(bid+ask)/2",
    ("R034", "R035"), (), "P_BASIC", "option_premium", "exact_ratio", AUTHORITY,
)
OPTION_POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d087-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), (),
    OPTION_PROVIDER, OPTION_VARIANT, OPTION_PROVIDER + "/" + OPTION_VARIANT, 100, 1000,
)
BOOK_ROLES = (
    ("R185", "position", "book_position"), ("R187", "operation", "book_operation"),
    ("R188", "side", "book_side"), ("R189", "price", "USD_per_share"),
    ("R190", "size", "contracts"),
)
BOOK_IDENTITY = (("generation.id", ("generation", "id")),
                 ("event.id", ("event", "id")), ("contract.id", ("contract", "id")))
BOOK_MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d131-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), BOOK_PROVIDER,
    BOOK_VARIANT, ("book", field), units, BOOK_IDENTITY,
) for raw, field, units in BOOK_ROLES)
BOOK_UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d131-" + raw.lower() + "-unit", 1, units, units, Decimal(1), Decimal(0),
) for raw, _, units in BOOK_ROLES)
BOOK_DEFINITION = f.CalculationDefinitionV1(
    "D131", "D131-POSITIONAL-OPTION-DEPTH-BAND-1", "K02_ALGEBRA",
    "sum(standing size where abs(price - actual D087 midpoint) <= band)",
    tuple(raw for raw, _, _ in BOOK_ROLES), ("D087",), "P_BASIC", "contracts",
    "scalar_decimal", AUTHORITY,
)
BOOK_PARAMETER = f.CalculationParameterSetV1(
    "mmt-d131-half-dollar", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
BOOK_SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d131-smart-positional", 1), BOOK_PROVIDER, BOOK_VARIANT,
    BOOK_GENERATION, T - timedelta(seconds=10), 100,
)


def admit(raw, identity, provider, variant, record, ids, stamp, sequence,
          source_stamp=None):
    raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
        concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=r.observation_occurrence_id(identity),
        delivery_artifact_ref=r.delivery_artifact_ref("d131-controlled"),
        source_provider=r.provider_id(provider), native_record=record,
        received_ts_utc=stamp, ingestion_sequence=sequence,
        ingestion_sequence_scope=r.ingestion_sequence_scope(provider + "/" + variant),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(raw_id) for raw_id in ids),
        source_variant=variant, subject_instrument=SUBJECT, native_units="mixed_book_roles",
        source_timestamp_raw=(source_stamp or stamp).isoformat().replace("+00:00", "Z"),
        source_timezone_native="UTC",
    ))


def option_parent(raw, tmp_path):
    for role, (mapping, amount) in enumerate(zip(
        OPTION_MAPS, (Decimal("99"), Decimal("101")), strict=True,
    )):
        record = {
            "quote": {"bid" if role == 0 else "ask": amount},
            "contract": {"id": SUBJECT, "multiplier": "100"},
            "underlying": {"id": "NVDA"}, "expiry": {"date": "2026-10-23"},
            "strike": {"key": "110"}, "option": {"right": "C"},
            "currency": {"code": "USD"}, "instrument": {"kind": "option"},
            "model": {"convention": "controlled-model/1"},
            "value": {"role": "option_bid" if role == 0 else "option_ask"},
        }
        admit(raw, f"d131-option-{role}", OPTION_PROVIDER, OPTION_VARIANT, record,
              (mapping.raw_signal_catalogue_id.value,), T, role + 1)
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert len(page.items) == 1 and page.items[0].native_value == amount
    parameter = f.CalculationParameterSetV1(
        "mmt-d087-c1-controlled", 1, "P_BASIC", SUBJECT, (SUBJECT,),
    )
    request = f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D087", SUBJECT, T, CUTOFF, OPTION_DEFINITION.calculation_definition_version,
        f.VersionRefV1(parameter.context_id, 1), f.VersionRefV1(OPTION_POLICY.context_id, 1),
        (OPTION_CONTEXT.ref,), tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(OPTION_UNIT.context_id, 1), SUBJECT,
        ) for mapping in OPTION_MAPS),
    ), OPTION_CONTEXT, ())
    path = str(tmp_path / "d087.sqlite")
    owner = f.create_window_owner(
        admission=f.OwnerAdmissionV1("M02", OPTION_BRIEF), raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    parent = owner.materialise(request)
    assert type(parent) is f.WindowMeasurementOccurrenceV1
    assert parent.result == f.ExactRatioV1(100, 1)
    reader = f.create_window_reader(
        admission=f.OwnerAdmissionV1("M02", OPTION_BRIEF),
        storage=f.SQLiteReadStorageV1(path),
    )
    assert reader.get_derived_occurrence(parent.derived_occurrence_id) == parent
    return parent, reader


def event(raw, name, position, operation, side, price, size, seconds, sequence,
          source_seconds=None):
    fields = ("R187",) if operation == 317 else tuple(raw_id for raw_id, _, _ in BOOK_ROLES)
    record = {
        "generation": {"id": BOOK_GENERATION}, "event": {"id": name},
        "contract": {"id": SUBJECT}, "book": {"operation": operation},
    }
    if operation != 317:
        record["book"].update(position=position, side=side, price=price, size=size)
    stamp = T - timedelta(seconds=seconds)
    admit(raw, "d131-" + name, BOOK_PROVIDER, BOOK_VARIANT, record,
          fields, stamp, sequence,
          T - timedelta(seconds=source_seconds) if source_seconds is not None else None)
    selected = []
    for mapping in BOOK_MAPS:
        if mapping.raw_signal_catalogue_id.value not in fields:
            continue
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        projection = next(item for item in page.items
                          if item.observation_occurrence_id.value == "d131-" + name)
        assert projection.native_field_path == mapping.native_field_path
        assert projection.selection_identity.value_for("event.id") == name
        selected.append(projection)
    assert len(selected) == len(fields)
    return selected


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d131_signal(tmp_path, refused):
    raw = r.create_owner()
    parent, predecessor_reader = option_parent(raw, tmp_path)
    observed = []
    observed.extend(event(raw, "bid-near", 0, 0, 0, Decimal("99.8"),
                          Decimal("5"), 3, 1))
    observed.extend(event(raw, "ask-near", 0, 0, 1, Decimal("100.2"),
                          Decimal("3"), 2, 2))
    observed.extend(event(raw, "bid-far", 1, 0, 0, Decimal("99"),
                          Decimal("7"), 1, 3, source_seconds=4))
    if refused:
        reset = event(raw, "reset", None, 317, None, None, None, 0, 4)
        assert len(reset) == 1 and reset[0].native_value == 317
        observed.extend(reset)
    assert len(observed) == (16 if refused else 15)
    request = f.BookDepthRequestV1(f.CalculationRequestV1(
        "D131", SUBJECT, T, CUTOFF, BOOK_DEFINITION.calculation_definition_version,
        f.VersionRefV1(BOOK_PARAMETER.context_id, 1), BOOK_SELECTION.ref,
        (BOOK_SELECTION.ref,), tuple(f.RawInputBindingV1(
            raw_id, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (raw_id, _, _), mapping, unit in zip(
            BOOK_ROLES, BOOK_MAPS, BOOK_UNITS, strict=True)),
    ), BOOK_SELECTION, parent.derived_occurrence_id, Decimal("0.5"))
    admission = f.OwnerAdmissionV1("M02", BOOK_BRIEF)
    path = str(tmp_path / "d131.sqlite")
    owner = f.create_book_depth_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=predecessor_reader, storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    occurrence = owner.materialise(request)
    reader = f.create_book_depth_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    query = dict(derived_signal_id="D131", subject_instrument=SUBJECT,
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF,
                 limit=10)
    if refused:
        assert occurrence is None
        assert reader.list_derived_history(**query) == ()
        return
    assert type(occurrence) is f.BookDepthOccurrenceV1
    assert occurrence.result == Decimal("8")
    assert occurrence.standing_rows == (
        f.BookRowV1(0, 0, Decimal("99.8"), Decimal("5")),
        f.BookRowV1(0, 1, Decimal("99"), Decimal("7")),
        f.BookRowV1(1, 0, Decimal("100.2"), Decimal("3")),
    )
    assert occurrence.owner_object_id == "M02" and occurrence.owner_namespace.endswith(
        "/book-depth/v1")
    assert occurrence.implementation_brief_sha256 == BOOK_BRIEF
    assert occurrence.definition == BOOK_DEFINITION
    assert occurrence.parameter_set == BOOK_PARAMETER
    assert occurrence.request == request and occurrence.predecessor == parent
    assert occurrence.unit_conventions == BOOK_UNITS
    assert occurrence.projection_mappings == BOOK_MAPS
    assert occurrence.units == "contracts" and occurrence.result_shape == "scalar_decimal"
    assert (occurrence.effective_as_of_utc, occurrence.knowledge_cutoff_utc,
            occurrence.calculated_at_utc) == (T, CUTOFF, NOW)
    assert len(occurrence.raw_input_lineage) == 15
    assert tuple(line.observation_occurrence_id for line in
                 occurrence.raw_input_lineage[::5]) == (
        "d131-bid-near", "d131-ask-near", "d131-bid-far",
    )  # receipt order differs from native source-event timestamp order
    assert {line.observation_occurrence_id for line in occurrence.raw_input_lineage} == {
        "d131-bid-near", "d131-ask-near", "d131-bid-far",
    }
    for line in occurrence.raw_input_lineage:
        projection = next(item for item in observed
                          if item.observation_occurrence_id.value == line.observation_occurrence_id
                          and item.raw_signal_catalogue_id.value == line.raw_signal_id)
        assert line.projection == projection
        assert line.canonical_value == projection.native_value
        assert type(line.canonical_value) is (int if line.raw_signal_id in
                                                ("R185", "R187", "R188") else Decimal)
    assert reader.get_derived_occurrence(occurrence.derived_occurrence_id) == occurrence
    assert reader.list_derived_history(**query) == (occurrence,)
