"""F2 proof-before-production: admitted M00 observation lineage, not derived IDs.

Authority: accepted brief K08 D015/D016/D120, K02 D017, K08 D065;
F1 accepted census RC07/RC08/RC09/RC01 and reviewer signed-flow witness.
"""

from __future__ import annotations

import importlib.util
from dataclasses import replace
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

ROOT = Path(__file__).resolve().parents[3]
PROOF = Path(__file__).with_name("native_signed_flow_fixture.py")
SPEC = importlib.util.spec_from_file_location("f2_original_reviewer_fixture", PROOF)
assert SPEC is not None and SPEC.loader is not None
reviewer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reviewer)


def _raw_point(
    rid: str, value: object, oid: str, at: datetime, *, contract: Any = None
) -> raw.ProjectedRawValueV1:
    original = reviewer.points[rid]
    return replace(
        original,
        native_value=value,
        observation_occurrence_id=raw.observation_occurrence_id(oid),
        source_timestamp_raw=at.isoformat(),
        received_ts_utc=at,
        selection_identity=reviewer.IDENT if contract is None else contract,
    )


def _owner(points: dict[str, tuple[raw.ProjectedRawValueV1, ...]]) -> Any:
    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            return raw.ProjectedRawHistoryPageV1(
                items=points.get(raw_signal_catalogue_id.value, ()), next_cursor=None
            )

        def project_raw_value(self, *args: object, **kwargs: object) -> None:
            return None

    return api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=reviewer.models,
        parameter_sets=reviewer.params,
        input_selection_policies=(reviewer.selection,),
        unit_conventions=reviewer.units,
        contexts=(),
        utc_now=lambda: reviewer.NOW + timedelta(minutes=1),
    )


def _request(did: str, instant: datetime) -> api.CalculationRequestV1:
    return replace(reviewer.request(did), as_of_utc=instant, knowledge_cutoff_utc=instant)


def _two_trade_points(
    *, second_size: Decimal = Decimal("3"), second_price: Decimal = Decimal("4")
) -> dict[str, tuple[raw.ProjectedRawValueV1, ...]]:
    t1, t2 = reviewer.NOW, reviewer.NOW + timedelta(seconds=5)
    values: dict[str, tuple[raw.ProjectedRawValueV1, ...]] = {}
    for rid in reviewer.raw_values:
        if rid in ("R034", "R035"):
            values[rid] = (_raw_point(rid, reviewer.raw_values[rid], "quote-C100", t1),)
        else:
            a = _raw_point(rid, reviewer.raw_values[rid], "trade-buy-C100", t1)
            b_value = {"R120": second_price, "R121": second_size}.get(rid, reviewer.raw_values[rid])
            b = _raw_point(rid, b_value, "trade-sell-C100", t2)
            values[rid] = (a, b)
    return values


def _raw_ids(occ: api.DerivedSignalOccurrenceV1, rid: str) -> set[str]:
    return {v.observation_occurrence_id for v in occ.raw_input_lineage if v.raw_signal_id == rid}


def test_reviewer_canonical_trade_sign_volume_and_notional_public() -> None:
    for did, expected in (
        ("D011", Decimal("5")),
        ("D015", 1),
        ("D016", Decimal("2")),
    ):
        occurrence = reviewer.owner.materialise(reviewer.request(did))
        assert occurrence is not None and occurrence.result == expected
    notional = reviewer.owner.materialise(reviewer.request("D120"))
    assert notional is not None
    assert dict(notional.result) == {
        "signed_contracts": Decimal("2"),
        "signed_premium_notional": Decimal("1200"),
    }
    assert _raw_ids(notional, "R120") == {str(reviewer.points["R120"].observation_occurrence_id)}
    assert notional.predecessor_occurrence_ids


def test_two_opposing_trades_have_distinct_exact_lineage_and_stable_retry() -> None:
    points = _two_trade_points()
    owner = _owner(points)
    t1, t2 = reviewer.NOW, reviewer.NOW + timedelta(seconds=5)
    buy = owner.materialise(_request("D015", t1))
    sell = owner.materialise(_request("D015", t2))
    assert buy is not None and buy.result == 1
    assert sell is not None and sell.result == -1
    assert buy.derived_occurrence_id != sell.derived_occurrence_id
    for did, expected in (
        ("D016", Decimal("-1")),
        ("D120", (("signed_contracts", Decimal("-1")), ("signed_premium_notional", Decimal("0")))),
    ):
        request = _request(did, t2)
        result = owner.materialise(request)
        assert result is not None and result.result == expected
        assert {buy.derived_occurrence_id, sell.derived_occurrence_id} <= set(
            result.predecessor_occurrence_ids
        )
        assert _raw_ids(result, "R121") == {"trade-buy-C100", "trade-sell-C100"}
        assert owner.materialise(request) == result
        assert all(x.derived_occurrence_id != "trade-buy-C100" for x in (buy, sell))
    changed = owner.materialise(
        replace(_request("D016", t2), knowledge_cutoff_utc=t2 + timedelta(seconds=1))
    )
    assert changed is not None
    assert changed.supersedes_derived_occurrence_id is not None


def test_ambiguous_or_missing_trade_sign_must_refuse_not_look_like_zero() -> None:
    points = _two_trade_points(second_price=Decimal("5"))
    owner = _owner(points)
    t1, t2 = reviewer.NOW, reviewer.NOW + timedelta(seconds=5)
    assert owner.materialise(_request("D015", t1)) is not None
    at_midpoint = owner.materialise(_request("D015", t2))
    assert at_midpoint is not None  # Tick test can be decisive; this is tested separately.
    # An unmatched earlier trade has no prior D015 record; do not discard its size.
    fresh = _owner(_two_trade_points())
    assert fresh.materialise(_request("D016", t2)) is None
    assert fresh.materialise(_request("D120", t2)) is None


def test_d017_only_pairs_trade_fields_from_same_m00_native_record() -> None:
    points = _two_trade_points(second_price=Decimal("4"), second_size=Decimal("3"))
    owner = _owner(points)
    t2 = reviewer.NOW + timedelta(seconds=5)
    computed = owner.materialise(_request("D017", t2))
    assert computed is not None
    assert computed.result == Decimal("24") / Decimal("5")
    assert _raw_ids(computed, "R120") == _raw_ids(computed, "R121")
    broken = dict(points)
    broken["R121"] = (points["R121"][0],)
    assert _owner(broken).materialise(_request("D017", t2)) is None


def test_original_reviewer_fixture_separate_contract_mismatch_is_not_accepted() -> None:
    points = {rid: (value,) for rid, value in reviewer.points.items()}
    wrong = raw.RawSelectionIdentityV1(
        values=tuple((k, "C200" if k == "contract_id" else v) for k, v in reviewer.IDENT.values)
    )
    points["R121"] = (_raw_point("R121", Decimal("2"), "wrong-C200", reviewer.NOW, contract=wrong),)
    assert _owner(points).materialise(_request("D016", reviewer.NOW)) is None
    assert _owner(points).materialise(_request("D120", reviewer.NOW)) is None


def test_no_sign_or_ambiguous_native_trade_refuses_instead_of_zero() -> None:
    at = reviewer.NOW
    # Quote midpoint = 5 and no different prior trade: D015 is explicitly unknown.
    points = {rid: (value,) for rid, value in reviewer.points.items()}
    points["R120"] = (_raw_point("R120", Decimal("5"), "obs-trade-C100", at),)
    owner = _owner(points)
    sign = owner.materialise(_request("D015", at))
    assert sign is not None and sign.result == 0
    assert owner.materialise(_request("D016", at)) is None
    assert owner.materialise(_request("D120", at)) is None

    # Two independent native trades have the same event/receipt instant;
    # neither sign-to-trade pairing may be made by opaque-ID ordering.
    collisions = _two_trade_points()
    for rid in ("R120", "R121", "R015", "R016", "R126", "R127"):
        collisions[rid] = (
            collisions[rid][0],
            replace(
                collisions[rid][1],
                source_timestamp_raw=at.isoformat(),
                received_ts_utc=at,
            ),
        )
    assert _owner(collisions).materialise(_request("D016", at)) is None
    assert _owner(collisions).materialise(_request("D120", at)) is None


def test_d015_lineage_does_not_relabel_an_earlier_trade_when_latest_size_is_missing() -> None:
    points = _two_trade_points()
    points["R121"] = points["R121"][:1]
    # New D015 knows latest trade B, but the only size belongs to trade A.
    # Do not attach B's sign to A by overlapping historical lineage.
    owner = _owner(points)
    t2 = reviewer.NOW + timedelta(seconds=5)
    assert owner.materialise(_request("D015", t2)) is not None
    assert owner.materialise(_request("D016", t2)) is None
    assert owner.materialise(_request("D120", t2)) is None


def test_native_trade_cutoff_excludes_future_trade_and_history_is_append_only() -> None:
    owner = _owner(_two_trade_points())
    t1, t2 = reviewer.NOW, reviewer.NOW + timedelta(seconds=5)
    past = owner.materialise(_request("D016", t1))
    assert past is not None and past.result == Decimal("2")
    assert _raw_ids(past, "R121") == {"trade-buy-C100"}
    owner.materialise(_request("D015", t2))
    current = owner.materialise(_request("D016", t2))
    assert current is not None and current.result == Decimal("-1")
    assert current.supersedes_derived_occurrence_id == past.derived_occurrence_id
    assert owner.materialise(_request("D016", t1)) == past


def test_second_exact_contract_is_not_associated_with_first_contract_sign() -> None:
    c200 = raw.RawSelectionIdentityV1(
        values=tuple((k, "C200" if k == "contract_id" else v) for k, v in reviewer.IDENT.values)
    )
    points = {
        rid: (
            _raw_point(
                rid,
                value,
                "quote-C200" if rid in ("R034", "R035") else "trade-C200",
                reviewer.NOW,
                contract=c200,
            ),
        )
        for rid, value in reviewer.raw_values.items()
    }
    bindings = tuple(replace(binding, selection_identity=c200) for binding in reviewer.bindings)

    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            rid = raw_signal_catalogue_id.value
            return raw.ProjectedRawHistoryPageV1(items=points.get(rid, ()), next_cursor=None)

        def project_raw_value(self, *args: object, **kwargs: object) -> None:
            return None

    owner = api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=reviewer.models,
        parameter_sets=reviewer.params,
        input_selection_policies=(reviewer.selection,),
        unit_conventions=reviewer.units,
        contexts=(),
        utc_now=lambda: reviewer.NOW,
    )
    request = replace(reviewer.request("D120"), raw_input_bindings=bindings)
    result = owner.materialise(request)
    assert result is not None and dict(result.result) == {
        "signed_contracts": Decimal("2"),
        "signed_premium_notional": Decimal("1200"),
    }
    assert _raw_ids(result, "R120") == {"trade-C200"}
    assert "trade-C100" not in _raw_ids(result, "R120")


def test_incompatible_trade_mapping_or_cutoff_refuses() -> None:
    at = reviewer.NOW
    points = {rid: (value,) for rid, value in reviewer.points.items()}
    points["R121"] = (replace(points["R121"][0], projection_mapping_version=2),)
    assert _owner(points).materialise(_request("D016", at)) is None
    assert _owner(points).materialise(_request("D120", at)) is None
    points = {rid: (value,) for rid, value in reviewer.points.items()}
    points["R121"] = (replace(points["R121"][0], received_ts_utc=at + timedelta(seconds=5)),)
    assert _owner(points).materialise(_request("D016", at)) is None
    assert _owner(points).materialise(_request("D120", at)) is None
