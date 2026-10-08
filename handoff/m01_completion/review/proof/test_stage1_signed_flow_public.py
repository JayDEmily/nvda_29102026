"""Independent reviewer proof. Runs through the public M01 owner seam.

Authority: accepted brief K08 D016 and D120 and catalogue graph D015->D016,D120.
Data: one exact C100 contract; one quote midpoint (4+6)/2=5;
one trade at 6, size 2, multiplier 100; D015 sign must be +1.
"""

from decimal import Decimal

import stage1_signed_flow_public_fixture as scenario


def test_d016_trade_signed_volume_must_match_d015_trade_truth():
    sign = scenario.owner.materialise(scenario.request("D015"))
    assert sign is not None and sign.result == 1
    occurrence = scenario.owner.materialise(scenario.request("D016"))
    assert occurrence is not None
    assert occurrence.result == Decimal("2")


def test_d120_trade_signed_notional_must_match_d015_trade_truth():
    sign = scenario.owner.materialise(scenario.request("D015"))
    assert sign is not None and sign.result == 1
    occurrence = scenario.owner.materialise(scenario.request("D120"))
    assert occurrence is not None
    assert dict(occurrence.result) == {
        "signed_contracts": Decimal("2"),
        "signed_premium_notional": Decimal("1200"),
    }
