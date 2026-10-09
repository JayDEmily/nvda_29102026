"""F4 RC12 public book-rate proof: per-side/level and pre-delete quantity.

Controlled public M00 projections, not a provider-specific integration claim.
Accepted D139/D140 semantics: K08 book operations by side/configured level bucket.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 8, tzinfo=UTC)
FIELDS = ("R001", "R185", "R187", "R188", "R190")
VALUES: tuple[tuple[str, int, int, str, str, Decimal], ...] = (
    ("bid-add", -5, 1, "insert", "bid", Decimal(10)),
    ("ask-add", -4, 2, "insert", "ask", Decimal(7)),
    ("bid-delete", -3, 1, "delete", "bid", Decimal(0)),
    ("ask-cancel", -2, 2, "cancel", "ask", Decimal(0)),
)


def _public_rates(
    *, missing_event_side: bool = False
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, (tag, offset, level, op, side, size) in enumerate(VALUES, 1):
        moment = NOW + timedelta(seconds=offset)
        native = {
            "book": {
                "event_ts": moment.isoformat(),
                "level": level,
                "operation": op,
                "side": side,
                "quantity": size,
            }
        }
        if missing_event_side and tag == "ask-cancel":
            del native["book"]["side"]
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("delivery-" + tag),
                source_provider=raw.provider_id("controlled-rates"),
                native_record=native,
                received_ts_utc=moment,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-rates:smart"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in FIELDS),
                source_variant="smart",
                subject_instrument="NVDA",
                native_units="book_record",
                revision_vintage_native="v1",
            )
        )
    paths = ("event_ts", "level", "operation", "side", "quantity")
    units = ("iso8601", "level", "operation", "side", "contracts")
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            f"f4-book-{rid}",
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-rates",
            "smart",
            ("book", path),
            unit,
        )
        for rid, path, unit in zip(FIELDS, paths, units, strict=True)
    )
    unit_conventions = tuple(
        api.UnitConventionVersionV1(
            f"f4-unit-{rid}",
            1,
            native,
            native,
            Decimal(1),
            Decimal(0),
        )
        for rid, native in zip(FIELDS, units, strict=True)
    )
    params = api.CalculationParameterSetV1(
        "f4-book-rule",
        1,
        "P_RULE",
        (("window_seconds", 10), ("level_bucket_upper_bounds", (1, 3))),
    )
    policy = api.InputSelectionPolicyVersionV1(
        "f4-rate-selection",
        1,
        ("subject_instrument",),
        timedelta(seconds=15),
        timedelta(seconds=15),
        ("true_instant",),
        (),
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(params,),
        input_selection_policies=(policy,),
        unit_conventions=unit_conventions,
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=1),
    )
    request = api.CalculationRequestV1(
        "D139",
        "NVDA",
        NOW,
        NOW,
        "f4-book-rates-v1",
        "f4-book-rule",
        1,
        "f4-rate-selection",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1(f"f4-book-{rid}", 1),
                api.VersionRefV1(f"f4-unit-{rid}", 1),
                "NVDA",
                None,
            )
            for rid in FIELDS
        ),
    )
    return owner, request


def test_d139_public_insert_rate_preserves_exact_side_and_level_buckets() -> None:
    owner, request = _public_rates()
    result = owner.materialise(request)
    assert result is not None
    fields = dict(result.result)
    # Counts/sizes are per 10-second configured window, not a merged count.
    assert dict(fields["by_side_level"]) == {
        ("bid", 1): (Decimal("0.1"), Decimal(1)),
        ("ask", 3): (Decimal("0.1"), Decimal("0.7")),
    }
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {x[0] for x in VALUES}
    assert owner.materialise(request) == result


def test_d140_public_cancel_uses_immediate_pre_delete_size_not_zero() -> None:
    owner, request = _public_rates()
    result = owner.materialise(replace(request, derived_signal_id="D140"))
    assert result is not None
    fields = dict(result.result)
    assert dict(fields["by_side_level"]) == {
        ("bid", 1): (Decimal("0.1"), Decimal(1)),
        ("ask", 3): (Decimal("0.1"), Decimal("0.7")),
    }
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {x[0] for x in VALUES}


def test_d139_d140_refuse_absent_level_buckets_or_missing_native_field() -> None:
    owner, request = _public_rates()
    # A raw-binding omission is not a zero-sized or zero-rate event.
    truncated = replace(request, raw_input_bindings=request.raw_input_bindings[:-1])
    assert owner.materialise(truncated) is None
    missing_owner, missing_request = _public_rates(missing_event_side=True)
    assert missing_owner.materialise(missing_request) is None
    # Policy version mismatches also refuse rather than silently reinterpreting level IDs.
    assert owner.materialise(replace(request, input_selection_policy_version=2)) is None
