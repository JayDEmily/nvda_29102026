"""Independent F2 review: a later quote must not reclassify an old trade.

Authority: accepted M01 brief §5 K08 D015-D016-D120 (contemporaneous
trade/quote matching and per-trade signed sums), §8.1 and §11 temporal law.
This uses the M01 public materialise seam with a separately assembled typed
M00 projection history; no worker owner/point creation helper is called.
"""
from __future__ import annotations

import importlib.util
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

BASE = Path(__file__).with_name("stage1_signed_flow_public_fixture.py")
spec = importlib.util.spec_from_file_location("f2_prior_independent_reviewer", BASE)
assert spec is not None and spec.loader is not None
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)


def _point(rid: str, value: Decimal, oid: str, at):
    return replace(
        original.points[rid],
        observation_occurrence_id=raw.observation_occurrence_id(oid),
        native_value=value,
        source_timestamp_raw=at.isoformat(),
        received_ts_utc=at,
    )


def test_later_quote_does_not_reclassify_earlier_sell_or_erase_signed_flow():
    t0 = original.NOW
    t5 = t0 + timedelta(seconds=5)
    t10 = t0 + timedelta(seconds=10)
    events = {}
    # Two actual trades: first buy (price 6, size 2), second sell
    # (price 4, size 3). Their contemporaneous quote midpoint is 5.
    for rid, value in original.raw_values.items():
        if rid in ("R034", "R035"):
            events[rid] = (_point(rid, value, "quote-at-trades", t0),)
        else:
            other_value = {
                "R120": Decimal("4"), "R121": Decimal("3")
            }.get(rid, value)
            events[rid] = (
                _point(rid, value, "trade-buy", t0),
                _point(rid, other_value, "trade-sell", t5),
            )
    # At t10 only the quote changes; no trade occurs. Its midpoint is 3,
    # so using this later quote would misclassify the old price-4 sell as a buy.
    events["R034"] += (_point("R034", Decimal("2"), "quote-after-trades", t10),)
    events["R035"] += (_point("R035", Decimal("4"), "quote-after-trades", t10),)

    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id, **kwargs):
            return raw.ProjectedRawHistoryPageV1(
                items=events.get(raw_signal_catalogue_id.value, ()), next_cursor=None
            )

        def project_raw_value(self, *args, **kwargs):
            return None

    owner = api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=original.models,
        parameter_sets=original.params,
        input_selection_policies=(original.selection,),
        unit_conventions=(original.unit,),
        contexts=(),
        utc_now=lambda: t10 + timedelta(seconds=1),
    )

    def calculate(did, at):
        req = replace(original.request(did), as_of_utc=at, knowledge_cutoff_utc=at)
        return owner.materialise(req)

    buy = calculate("D015", t0)
    sell = calculate("D015", t5)
    later = calculate("D015", t10)
    signed_volume = calculate("D016", t10)
    signed_flow = calculate("D120", t10)
    print("D015 at buy time:", None if buy is None else buy.result)
    print("D015 at sell time:", None if sell is None else sell.result)
    print("D015 after quote-only update:", None if later is None else later.result)
    print("D016 after quote-only update:", None if signed_volume is None else signed_volume.result)
    print("D120 after quote-only update:", None if signed_flow is None else signed_flow.result)
    assert buy is not None and buy.result == 1
    assert sell is not None and sell.result == -1
    # No later quote may turn the already-classified sell into a buy.
    assert later is None or later.result != 1
    # Both observed, known-sign trades remain within the selected 60s window.
    assert signed_volume is not None and signed_volume.result == Decimal("-1")
    assert signed_flow is not None and dict(signed_flow.result) == {
        "signed_contracts": Decimal("-1"),
        "signed_premium_notional": Decimal("0"),
    }
