"""F2a proof first: quote chosen for a trade cannot arrive after that trade.

Public-seam propositions are derived from accepted brief K08 D015/D016/D120,
§8.1 temporally compatible input selection and §11 no-look-ahead.
"""

from __future__ import annotations

import importlib.util
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

_REVIEW = (
    Path(__file__).resolve().parents[3]
    / "handoff/m01_completion/review/proof/stage1_signed_flow_public_fixture.py"
)
_spec = importlib.util.spec_from_file_location("f2a_authority_reviewer_fixture", _REVIEW)
assert _spec is not None and _spec.loader is not None
fixture = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fixture)


def _point(rid: str, val: Decimal, oid: str, at):
    return replace(
        fixture.points[rid],
        native_value=val,
        observation_occurrence_id=raw.observation_occurrence_id(oid),
        source_timestamp_raw=at.isoformat(),
        received_ts_utc=at,
    )


def _owner(events):
    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id, **kwargs):
            return raw.ProjectedRawHistoryPageV1(
                items=events.get(raw_signal_catalogue_id.value, ()), next_cursor=None
            )

        def project_raw_value(self, *args, **kwargs):
            return None

    return api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=fixture.models,
        parameter_sets=fixture.params,
        input_selection_policies=(fixture.selection,),
        unit_conventions=(fixture.unit,),
        contexts=(),
        utc_now=lambda: fixture.NOW + timedelta(seconds=20),
    )


def _calc(owner, did, at, *, cutoff=None):
    return owner.materialise(
        replace(
            fixture.request(did),
            as_of_utc=at,
            knowledge_cutoff_utc=at if cutoff is None else cutoff,
        )
    )


def _trades_and_quotes(*, later_bid=Decimal("2"), later_ask=Decimal("4"), first_quote_delay=0):
    t0 = fixture.NOW
    t5 = t0 + timedelta(seconds=5)
    t10 = t0 + timedelta(seconds=10)
    events = {}
    for rid, value in fixture.raw_values.items():
        if rid in {"R034", "R035"}:
            events[rid] = (
                _point(rid, value, "quote-before", t0 + timedelta(seconds=first_quote_delay)),
            )
        else:
            second = {"R120": Decimal("4"), "R121": Decimal("3")}.get(rid, value)
            events[rid] = (
                _point(rid, value, "trade-buy", t0),
                _point(rid, second, "trade-sell", t5),
            )
    events["R034"] += (_point("R034", later_bid, "quote-after", t10),)
    events["R035"] += (_point("R035", later_ask, "quote-after", t10),)
    return events, t0, t5, t10


def _ids(occ, rid):
    return {v.observation_occurrence_id for v in occ.raw_input_lineage if v.raw_signal_id == rid}


def test_quote_only_update_preserves_trade_sign_aggregates_and_quote_lineage():
    events, t0, t5, t10 = _trades_and_quotes()
    owner = _owner(events)
    before_buy = _calc(owner, "D015", t0)
    before_sell = _calc(owner, "D015", t5)
    after = _calc(owner, "D015", t10)
    assert before_buy is not None and before_buy.result == 1
    assert before_sell is not None and before_sell.result == -1
    assert after is not None and after.result == -1
    assert "quote-before" in _ids(after, "R034")
    assert "quote-after" not in _ids(after, "R034")
    for did, expected in (
        ("D016", Decimal("-1")),
        ("D120", (("signed_contracts", Decimal("-1")), ("signed_premium_notional", Decimal("0")))),
    ):
        result = _calc(owner, did, t10)
        assert result is not None and result.result == expected
        assert {before_buy.derived_occurrence_id, after.derived_occurrence_id} <= set(
            result.predecessor_occurrence_ids
        )
        assert _calc(owner, did, t10) == result


def test_different_later_midpoint_cannot_override_trade_time_midpoint():
    events, _t0, t5, t10 = _trades_and_quotes(later_bid=Decimal("8"), later_ask=Decimal("10"))
    owner = _owner(events)
    assert _calc(owner, "D015", t5).result == -1
    after = _calc(owner, "D015", t10)
    assert after is not None and after.result == -1
    assert "quote-after" not in _ids(after, "R035")


def test_only_post_trade_quote_must_not_classify_old_trade():
    events, _t0, t5, t10 = _trades_and_quotes(first_quote_delay=7)
    owner = _owner(events)
    # A quote at t7 and one at t10 both postdate the trade at t5.
    assert _calc(owner, "D015", t5, cutoff=t10) is None
    assert _calc(owner, "D015", t10) is None
