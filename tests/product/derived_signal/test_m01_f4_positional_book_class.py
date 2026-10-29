"""F4 proof-first class witnesses for positional event-driven order-book semantics.

The retained 3-field historical red witness lives in
`test_m01_f4_depth_snapshot_authority.py`; it is not valid positive input once
R187 becomes a mandatory dependency. These witnesses use explicit operations.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.derived_signal_calculation_truth._stage1 import (
    BookEventV1,
    _book_final_state,
    reconstruct_book,
)
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 10, tzinfo=UTC)
FIELDS = ("R185", "R187", "R188", "R190")


def event(
    tag: str,
    second: int,
    position: int,
    op: str,
    side: str,
    size: int,
    venue: str = "SMART",
    sequence: int = 0,
) -> BookEventV1:
    return BookEventV1(
        tag,
        NOW + timedelta(seconds=second),
        position,
        op,
        side,
        Decimal(0),
        Decimal(size),
        venue,
        sequence,
    )


def test_book_insert_shifts_levels_update_and_delete_reindexes_each_side_and_source() -> None:
    events = (
        event("b0", -8, 0, "insert", "bid", 10),
        event("b1", -7, 1, "insert", "bid", 5),
        event("a0", -6, 0, "insert", "ask", 9),
        event("other", -5, 0, "insert", "bid", 100, "DIRECT"),
        event("push", -4, 0, "insert", "bid", 7),
    )
    state = _book_final_state(tuple(reversed(events)))
    assert state is not None
    assert [state[("SMART", "bid", i)][1] for i in range(3)] == list(map(Decimal, (7, 10, 5)))
    assert state[("SMART", "ask", 0)][1] == Decimal(9)
    assert state[("DIRECT", "bid", 0)][1] == Decimal(100)
    assert sum((state[("SMART", "bid", i)][1] for i in (0, 1)), Decimal(0)) == Decimal(17)
    updated = _book_final_state(
        (*events, event("upd", -3, 1, "update", "bid", 11), event("del", -2, 0, "delete", "bid", 0))
    )
    assert updated is not None
    assert [updated[("SMART", "bid", i)][1] for i in range(2)] == list(map(Decimal, (11, 5)))
    mutations = reconstruct_book(
        (*events, event("upd", -3, 1, "update", "bid", 11), event("del", -2, 0, "delete", "bid", 0))
    )
    assert [m.event.occurrence_id for m in mutations] == [e.occurrence_id for e in events] + [
        "upd",
        "del",
    ]
    assert mutations[-2].prior_size == Decimal(10)
    assert mutations[-2].restored_size == Decimal(1)
    assert mutations[-1].removed_size == Decimal(7)


@pytest.mark.parametrize(
    "bad",
    [
        (event("bad-update", 0, 0, "update", "bid", 2),),
        (event("bad-delete", 0, 0, "delete", "bid", 0),),
        (event("bad-gap", 0, 3, "insert", "bid", 2),),
        (event("bad-side", 0, 0, "insert", "unknown", 2),),
        (event("bad-op", 0, 0, "replace", "bid", 2),),
    ],
)
def test_unestablished_or_unsupported_book_state_fails_closed(bad: tuple[BookEventV1, ...]) -> None:
    assert _book_final_state(bad) is None


def public_book(
    rows: tuple[tuple[str, int, int, str, str, int], ...],
    *,
    provider: str = "controlled-positional",
    missing: str | None = None,
    depth: int = 2,
    decoy_instrument: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    units = ("level", "operation", "side", "contracts")
    names = ("position", "operation", "side", "quantity")
    if decoy_instrument:
        rows = (*rows, ("amd-book", -3, 0, "insert", "bid", 500))
    for n, (tag, offset, position, operation, side, size) in enumerate(rows, 1):
        moment = NOW + timedelta(seconds=offset)
        record = {
            "position": position,
            "operation": operation,
            "side": side,
            "quantity": Decimal(size),
        }
        if tag == missing:
            record.pop("operation")
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("positional-" + tag),
                source_provider=raw.provider_id(provider),
                native_record=record,
                received_ts_utc=moment,
                ingestion_sequence=n,
                ingestion_sequence_scope=raw.ingestion_sequence_scope(provider + ":book"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(k) for k in FIELDS),
                source_variant="book",
                subject_instrument="AMD" if tag == "amd-book" else "NVDA",
                native_units="book_event",
                revision_vintage_native="v1",
            )
        )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "position-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            provider,
            "book",
            (name,),
            unit,
        )
        for rid, name, unit in zip(FIELDS, names, units, strict=True)
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "position-basic", 1, "P_BASIC", (("depth_levels", depth),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "position-policy",
                1,
                ("subject_instrument",),
                timedelta(seconds=30),
                timedelta(seconds=30),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1(
                "position-unit-" + rid, 1, unit, unit, Decimal(1), Decimal(0)
            )
            for rid, unit in zip(FIELDS, units, strict=True)
        ),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=1),
    )
    request = api.CalculationRequestV1(
        "D134",
        "NVDA",
        NOW,
        NOW,
        "f4-position",
        "position-basic",
        1,
        "position-policy",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("position-map-" + rid, 1),
                api.VersionRefV1("position-unit-" + rid, 1),
                "NVDA",
                None,
            )
            for rid in FIELDS
        ),
    )
    return owner, request


ROWS = (
    ("bid-first", -8, 0, "insert", "bid", 10),
    ("bid-second", -7, 1, "insert", "bid", 5),
    ("ask-first", -6, 0, "insert", "ask", 9),
    ("bid-shift", -5, 0, "insert", "bid", 7),
    ("ask-second", -4, 1, "insert", "ask", 4),
)


def test_public_d134_d135_d136_shifted_depth_results_and_exact_lineage() -> None:
    owner, request = public_book(ROWS)
    bid = owner.materialise(request)
    ask = owner.materialise(replace(request, derived_signal_id="D135"))
    ratio = owner.materialise(replace(request, derived_signal_id="D136"))
    assert bid is not None and bid.result == Decimal(17)
    assert ask is not None and ask.result == Decimal(13)
    assert ratio is not None and ratio.result == Decimal(4) / Decimal(30)
    assert {x.observation_occurrence_id for x in bid.raw_input_lineage} == {row[0] for row in ROWS}
    assert {x.raw_signal_id for x in bid.raw_input_lineage} == set(FIELDS)
    assert owner.materialise(request) == bid


def test_public_book_missing_operation_and_temporal_cutoff_refuse_or_recalculate() -> None:
    owner, request = public_book(ROWS, missing="bid-shift")
    assert owner.materialise(request) is None
    good, req = public_book(ROWS)
    historical = replace(
        req, as_of_utc=NOW - timedelta(seconds=6), knowledge_cutoff_utc=NOW - timedelta(seconds=6)
    )
    old = good.materialise(historical)
    assert old is not None and old.result == Decimal(15)
    latest = good.materialise(req)
    assert latest is not None and latest.result == Decimal(17)
    assert old.derived_occurrence_id != latest.derived_occurrence_id
    assert {v.observation_occurrence_id for v in old.raw_input_lineage} == {
        "bid-first",
        "bid-second",
        "ask-first",
    }
    assert {v.observation_occurrence_id for v in latest.raw_input_lineage} == {
        row[0] for row in ROWS
    }


def test_public_depth_limits_choose_exact_final_levels_and_exclude_other_instruments() -> None:
    owner_one, request_one = public_book(ROWS, depth=1, decoy_instrument=True)
    bid_one = owner_one.materialise(request_one)
    ask_one = owner_one.materialise(replace(request_one, derived_signal_id="D135"))
    ratio_one = owner_one.materialise(replace(request_one, derived_signal_id="D136"))
    assert bid_one is not None and bid_one.result == Decimal(7)
    assert ask_one is not None and ask_one.result == Decimal(9)
    assert ratio_one is not None and ratio_one.result == Decimal(-1) / Decimal(8)
    assert {r.observation_occurrence_id for r in bid_one.raw_input_lineage} == {r[0] for r in ROWS}
    owner_three, request_three = public_book(ROWS, depth=3)
    bid_three = owner_three.materialise(request_three)
    ask_three = owner_three.materialise(replace(request_three, derived_signal_id="D135"))
    ratio_three = owner_three.materialise(replace(request_three, derived_signal_id="D136"))
    assert bid_three is not None and bid_three.result == Decimal(22)
    assert ask_three is not None and ask_three.result == Decimal(13)
    assert ratio_three is not None and ratio_three.result == Decimal(9) / Decimal(35)
