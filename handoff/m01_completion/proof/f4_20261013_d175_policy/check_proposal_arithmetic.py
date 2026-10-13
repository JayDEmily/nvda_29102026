"""Arithmetic checks of a proposal, NOT a production policy implementation.

Uses exact rational numbers for published example calculations only. It neither
imports product code nor reads account data nor supplies an executable D175 path.
"""

import json
from fractions import Fraction as F
from itertools import product

cases = []
base = {"N": F(10000), "K": F(10000), "A": F(3000), "E": F(2500), "M": F(1000), "G": F(1000), "C": F(200), "W": F(400)}
fractions = {"capital": F(1, 10), "tail": F(3, 100), "stress": F(6, 100), "concentration": F(1, 5), "liquidity": F(1, 2)}
examples = [
    ("positive_and_equality", {}, {}, True, F(1000)),
    ("tail_breach", {}, {"tail": F(1, 100)}, True, F(500)),
    ("stress_breach", {}, {"stress": F(2, 100)}, True, F(500)),
    ("concentration_breach", {}, {"concentration": F(4, 100)}, True, F(400)),
    ("liquidity_breach", {"A": F(400)}, {}, True, F(200)),
    ("negative_available_zero_capacity", {"A": F(-10)}, {}, True, F(0)),
    ("maintenance_exceeds_NLV", {"M": F(12000)}, {}, True, F(0)),
    ("zero_native_losses_nonbinding", {"C": F(0), "W": F(0)}, {}, True, F(1000)),
    ("tail_explicitly_inactive", {}, {"tail": F(1, 100)}, False, F(1000)),
    ("zero_usage_zero_native_losses", {"G": F(0), "C": F(0), "W": F(0)}, {}, True, F(1000)),
]
for name, changes, fraction_changes, tail_active, expected in examples:
    a = base | changes
    f = fractions | fraction_changes
    limits = {
        "capital": f["capital"] * a["K"],
        "concentration": f["concentration"] * a["N"],
        "liquidity": f["liquidity"] * max(F(0), min(a["A"], a["E"], a["N"] - a["M"])),
    }
    if tail_active and a["C"] > 0:
        limits["tail"] = a["G"] * f["tail"] * a["K"] / a["C"]
    if a["W"] > 0:
        limits["stress"] = a["G"] * f["stress"] * a["K"] / a["W"]
    budget = min(limits.values())
    assert budget == expected, name
    breach = a["G"] > budget
    native_breach = (
        a["G"] > limits["capital"] or a["G"] > limits["concentration"] or a["G"] > limits["liquidity"]
        or (tail_active and a["C"] > f["tail"] * a["K"])
        or a["W"] > f["stress"] * a["K"]
    )
    assert breach == native_breach, name
    cases.append({"case": name, "limits": limits, "maximum_currency": budget, "maximum_percent": 100*budget/a["K"], "breach": breach, "native_constraint_breach": native_breach})

# Tail-breach clipping witness: exact lambda and both envelope inequalities.
g0, h_risk, b = F(1000), F(1000), F(500)
lam = b / h_risk
assert lam == F(1, 2)
assert lam*h_risk <= b and g0-lam*h_risk <= g0
cases.append({"case": "indicative_clip_only", "lambda": lam, "adjustment_delta": -lam*h_risk, "residual_envelope": g0-lam*h_risk, "post_adjustment_native_losses": "REQUIRES_REVALUATION_NOT_CHECKED"})

# Exact degeneracy predicate, not a fabricated epsilon conversion.
assert F(0) == 0 and (F(400) > 0)
cases.append({"case": "zero_envelope_positive_nonlinear_loss", "G": 0, "W": 400, "expected": "REFUSE_ZERO_COORDINATE", "classification": "PROPOSED_CONTRACT_CASE_NOT_PRODUCT_TEST"})

sweep_count = 0
for g,c,w,ft,fs,ta in product((F(1),F(10),F(1000)), (F(0),F(1),F(200),F(400)), (F(0),F(1),F(400)), (F(0),F(1,100),F(3,100)), (F(0),F(2,100),F(6,100)), (False,True)):
    values = [F(1000),F(2000),F(1250)]
    if ta and c>0:
        values.append(g*ft*F(10000)/c)
    if w>0:
        values.append(g*fs*F(10000)/w)
    exact_budget = min(values)
    direct = g>1000 or g>2000 or g>1250 or (ta and c>ft*10000) or w>fs*10000
    assert (g>exact_budget)==direct
    sweep_count += 1
print(json.dumps({"classification": "PROPOSED_EXAMPLE_ARITHMETIC_ONLY", "exact_breach_equivalence_sweep_points":sweep_count, "cases": cases}, indent=2, default=str))
