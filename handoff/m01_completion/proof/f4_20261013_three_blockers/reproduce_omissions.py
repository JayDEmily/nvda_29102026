"""Evidence probes of inherited code, not acceptance tests or a new risk model.

Run from repository root with PYTHONPATH=src. Python 3.12 observations are
diagnostic only; project acceptance requires its declared Python 3.13.5.
"""

import json
import platform
from datetime import UTC, datetime
from decimal import Decimal as D

from nvda_desk.derived_signal_calculation_truth import _stage1, api

AT = datetime(2026, 10, 13, 7, tzinfo=UTC)


def evaluate(did, derived, params, raw=None, contexts=()):
    def value(key, datum):
        return (_stage1.KernelValueV1(datum, key + "-probe", AT, AT, "NVDA", "derived"),)

    result = _stage1.evaluate_stage1_kernel(
        did,
        raw_inputs={k: value(k, v) for k, v in (raw or {}).items()},
        derived_inputs={k: value(k, v) for k, v in derived.items()},
        parameter_set=api.CalculationParameterSetV1("probe-" + did, 1, "P_RULE", params),
        contexts=contexts,
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )
    return None if result is None else result.value


out = {"python": platform.python_version(), "classification": "DIAGNOSTIC_NOT_ACCEPTANCE"}
quotes = {"R034": D(4), "R035": D(6), "R189": D(5), "R190": D(8)}
price_params = (("allowed_execution_cost_per_unit", D("0.5")), ("side", "buy"))
out["D178_predecessor_nonuse"] = [
    {"D133": cost, "D177": edge, "observed": evaluate("D178", {"D133": cost, "D177": edge}, price_params, quotes)}
    for cost, edge in ((D(4), D(2)), (D(400), D(-200)))
]
out["D178_typed_sell_ignored"] = evaluate(
    "D178", {"D133": D(4), "D177": D(2)}, price_params, quotes,
    (api.OrderIntentContextV1("sell-intent", 1, "sell", D(2), "normal"),),
)
exposures = {"D181": D(15), "D182": D(12), "D183": D(13), "D184": D(14)}
bands = (("target_bands", ("delta|0|10", "gamma|0|10", "vega|0|10", "theta|0|10")),)
out["D189_limit_nonuse"] = [
    {"D175": limit, "observed": evaluate("D189", {**exposures, "D175": limit}, bands)}
    for limit in (D(0), D(100000))
]
decision = {
    "D187": False, "D188": (("expected_currency_PnL", D(10)),),
    "D189": (("delta", D(-10)), ("gamma", D(0)), ("vega", D(0)), ("theta", D(0))),
    "D190": D(0), "D191": D(5),
}
out["D192_hedge_without_risk_value"] = evaluate(
    "D192", {**decision, "D175": D(100000)},
    (("mandatory_hedge_on_risk", True),),
)
out["D175_structured_stress_matrix_not_consumed"] = evaluate(
    "D175",
    {"D162": (("CVaR_currency", D(80)),), "D174": (("candidate", "A"), ("scenario_pnl", (D(-5), D(-70))))},
    (("selection_mode", "exact"),),
    {"R205": D(100), "R206": D(50), "R209": D(90), "R208": D(60)},
)
print(json.dumps(out, indent=2, default=str))
