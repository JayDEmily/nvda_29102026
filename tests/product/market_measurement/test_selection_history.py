"""FND-P04: complete quiescent public history, eligibility, ties and cursor refusal."""

from dataclasses import replace
from datetime import timedelta
from decimal import Decimal

import pytest
from _support import ASOF, configuration, foundation, mapping, observation, request

from nvda_desk.raw_signal_occurrence_truth import api as raw_api


def test_latest_eligible_history_and_ambiguity():
    raw = raw_api.create_owner()
    raw.commands.admit_raw_observation_occurrence(observation("ask", sequence=0))
    # A fixed complete population before enumeration; no live/concurrent snapshot claim.
    for index in range(1, 103):
        raw.commands.admit_raw_observation_occurrence(
            observation(
                "bid",
                identity=f"history-{index}",
                sequence=index,
                event=ASOF - timedelta(seconds=3 if index < 101 else 2),
                value=Decimal("100") if index < 102 else 999.0,
            )
        )
    raw.commands.admit_raw_observation_occurrence(
        observation(
            "bid",
            identity="late-after",
            sequence=103,
            event=ASOF - timedelta(seconds=1),
            receipt=ASOF + timedelta(microseconds=1),
            value=Decimal("999"),
        )
    )
    calls = []

    class CountingReader:
        def list_projected_raw_history(self, rid, **kwargs):
            calls.append((rid, kwargs))
            return raw.reads.list_projected_raw_history(rid, **kwargs)

    f = foundation()
    o = f.create_owner(**configuration(f, CountingReader()))
    result = o.materialise(request(f))
    assert result.result == Decimal("101")
    assert result.raw_input_lineage[0].observation_occurrence_id == "history-101"
    bid_calls = [kwargs for rid, kwargs in calls if rid == raw_api.RawSignalCatalogueId("R034")]
    assert len(bid_calls) == 2 and bid_calls[0]["cursor"] is None
    assert bid_calls[1]["cursor"] == "100"
    for kwargs in bid_calls:
        assert kwargs["mappings"] == (mapping("bid"),)
        assert kwargs["limit"] == 100 and kwargs["subject_instrument"] == "NVDA"
        assert kwargs["event_at_or_before_utc"] == kwargs["received_at_or_before_utc"] == ASOF
    # A late but cutoff-eligible arrival becomes the newest eligible event.
    raw.commands.admit_raw_observation_occurrence(
        observation(
            "bid",
            identity="late-before",
            sequence=104,
            event=ASOF - timedelta(seconds=1),
            receipt=ASOF,
            value=Decimal("104"),
        )
    )
    assert o.materialise(request(f)).result == Decimal("103")


@pytest.mark.parametrize(
    "mode",
    ["reverse", "duplicate", "conflict", "repeat", "invalid", "empty", "cap", "wrong-carrier"],
)
def test_history_enumeration_and_cursor_discriminators(mode):
    raw = raw_api.create_owner()
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))

    class Reader:
        calls = 0

        def list_projected_raw_history(self, rid, **kwargs):
            page = raw.reads.list_projected_raw_history(rid, **(kwargs | {"cursor": None}))
            if rid.value == "R035":
                return page
            self.calls += 1
            item = page.items[0]
            if mode == "reverse":
                older = replace(
                    item,
                    observation_occurrence_id=raw_api.observation_occurrence_id("older"),
                    source_timestamp_raw="2026-10-16T00:59:57Z",
                    native_value=Decimal("90"),
                )
                return raw_api.ProjectedRawHistoryPageV1((item, older), None)
            if mode == "duplicate":
                return raw_api.ProjectedRawHistoryPageV1((item, item), None)
            if mode == "conflict":
                other = replace(
                    item,
                    observation_occurrence_id=raw_api.observation_occurrence_id("equal-rank"),
                    native_value=Decimal("99"),
                )
                return raw_api.ProjectedRawHistoryPageV1((item, other), None)
            if mode == "repeat":
                return raw_api.ProjectedRawHistoryPageV1(page.items, "1")
            if mode == "invalid":
                return raw_api.ProjectedRawHistoryPageV1(page.items, 1)
            if mode == "empty":
                return raw_api.ProjectedRawHistoryPageV1((), "1")
            if mode == "cap":
                return raw_api.ProjectedRawHistoryPageV1(page.items, str(self.calls))
            return (item,)

    reader = Reader()
    f = foundation()
    o = f.create_owner(**configuration(f, reader))
    result = o.materialise(request(f))
    if mode in {"reverse", "duplicate"}:
        assert result.result == Decimal("101")
    else:
        assert result is None
    assert reader.calls <= 1000


@pytest.mark.parametrize(
    "field,value",
    [
        ("projection_mapping_version", 2),
        ("projection_mapping_id", "wrong"),
        ("raw_signal_catalogue_id", raw_api.RawSignalCatalogueId("R035")),
        ("native_field_path", ("quote", "ask")),
        ("selection_identity", raw_api.RawSelectionIdentityV1((("x", "y"),))),
        ("received_ts_utc", ASOF.replace(tzinfo=None)),
    ],
)
def test_projection_metadata_is_independently_checked(field, value):
    raw = raw_api.create_owner()
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))

    class Reader:
        def list_projected_raw_history(self, rid, **kwargs):
            page = raw.reads.list_projected_raw_history(rid, **kwargs)
            if rid.value == "R034":
                return replace(page, items=(replace(page.items[0], **{field: value}),))
            return page

    f = foundation()
    assert f.create_owner(**configuration(f, Reader())).materialise(request(f)) is None
