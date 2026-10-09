"""F4 RC20: complete co-referenced M00 macro vintages and knowledge cutoffs."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 1, 0, tzinfo=UTC)
FIELDS = ("R280", "R281", "R282")
ROWS = (
    ("v1", -8, "2026-09-01", "2026-09-30", "2026-10-08"),
    ("v2", -2, "2026-10-01", "2026-10-31", "2026-10-09"),
)


def macro_owner(
    *, include_second: bool = True, omit_latest: str | None = None,
    future_latest: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, (tag, offset, start, end, updated) in enumerate(
        ROWS if include_second else ROWS[:1], 1
    ):
        received = NOW + timedelta(seconds=2) if tag == "v2" and future_latest else (
            NOW + timedelta(seconds=offset)
        )
        data = dict(zip(FIELDS, (start, end, updated), strict=True))
        if tag == "v2" and omit_latest is not None:
            del data[omit_latest]
        m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("vintage-" + tag),
            delivery_artifact_ref=raw.delivery_artifact_ref("vintage-" + tag),
            source_provider=raw.provider_id("controlled-macro-revisions"),
            native_record={"vintage": data}, received_ts_utc=received,
            ingestion_sequence=seq,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("macro:vintages"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=received.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in FIELDS),
            source_variant="macro-revision", subject_instrument="NVDA",
            native_units="macro_vintage", revision_vintage_native=tag,
        ))
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(raw.RawSignalProjectionMappingV1(
            "vintage-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
            "controlled-macro-revisions", "macro-revision", ("vintage", rid),
            "macro_vintage",
        ) for rid in FIELDS),
        parameter_sets=(api.CalculationParameterSetV1(
            "vintage-time", 1, "P_TIME", (("exchange_timezone", "UTC"),),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "vintage-selection", 1, ("subject_instrument",), timedelta(seconds=30),
            timedelta(seconds=30), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "vintage-unit", 1, "macro_vintage", "macro_vintage", Decimal(1), Decimal(0),
        ),),
        contexts=(), utc_now=lambda: NOW + timedelta(seconds=1),
    )
    req = api.CalculationRequestV1(
        "D009", "NVDA", NOW, NOW, "macro-revision", "vintage-time", 1,
        "vintage-selection", 1, (), raw_input_bindings=tuple(api.RawInputBindingV1(
            rid, api.VersionRefV1("vintage-map-" + rid, 1),
            api.VersionRefV1("vintage-unit", 1), "NVDA", None,
        ) for rid in FIELDS),
    )
    return owner, req


def test_rc20_public_latest_known_macro_vintage_lineage_and_idempotency() -> None:
    owner, req = macro_owner()
    out = owner.materialise(req)
    assert out is not None
    assert out.result == (
        ("status", "latest_known_at_cutoff"),
        ("realtime_start", "2026-10-01"),
        ("realtime_end", "2026-10-31"),
        ("last_updated", "2026-10-09"),
        ("cutoff", NOW),
    )
    assert {x.raw_signal_id for x in out.raw_input_lineage} == set(FIELDS)
    assert {x.observation_occurrence_id for x in out.raw_input_lineage} == {
        "vintage-v1", "vintage-v2",
    }
    assert owner.materialise(req) == out


def test_rc20_public_initial_and_future_revision_exclusion() -> None:
    owner, req = macro_owner(include_second=False)
    initial = owner.materialise(req)
    assert initial is not None
    assert initial.result[0] == ("status", "initial")
    owner, req = macro_owner(future_latest=True)
    visible = owner.materialise(req)
    assert visible is not None
    assert visible.result[0] == ("status", "initial")
    assert {x.observation_occurrence_id for x in visible.raw_input_lineage} == {"vintage-v1"}


def test_rc20_public_incomplete_latest_native_vintage_must_fail_closed() -> None:
    # A newer event cannot be silently elided merely because R282 was missing.
    # Otherwise the prior vintage masquerades as the current complete state.
    owner, req = macro_owner(omit_latest="R282")
    assert owner.materialise(req) is None
