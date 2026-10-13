"""Owner-approved F4 Stage-1 policy consumers, never Stage-2 producers."""

from datetime import datetime
from decimal import Decimal, localcontext
from fractions import Fraction

from . import api


def named(value: object) -> dict[str, object]:
    if type(value) is not tuple:
        raise ValueError("structured named carrier required")
    result: dict[str, object] = {}
    for entry in value:
        if type(entry) is not tuple or len(entry) != 2 or type(entry[0]) is not str:
            raise ValueError("invalid named carrier")
        key, item = entry
        if key in result:
            raise ValueError("duplicate named field")
        result[key] = item
    return result


def number(value: object) -> Fraction:
    if type(value) is not Decimal or not value.is_finite():
        raise ValueError("finite Decimal required")
    return Fraction(value)


def decimal(value: Fraction) -> Decimal:
    """Conservative 28-fractional-place convenience; exact rational is canonical."""
    scaled = value.numerator * 10**28 // value.denominator
    with localcontext() as ctx:
        ctx.prec = max(60, len(str(abs(scaled))) + 2)
        return Decimal(scaled).scaleb(-28)


def one(inputs: dict, identity: str, now: datetime, cutoff: datetime):
    values = inputs.get(identity, ())
    if len(values) != 1:
        raise ValueError("exact unambiguous predecessor required")
    value = values[0]
    if value.effective_at_utc > now or value.received_ts_utc > cutoff:
        raise ValueError("future input")
    return value


def context(contexts: tuple[object, ...], cls):
    values = [value for value in contexts if type(value) is cls]
    if len(values) != 1:
        raise ValueError("exact versioned context required")
    return values[0]


def ref(value) -> tuple[str, int]:
    return value.context_id, value.version


def limit_price(raw, derived, params, contexts, now, cutoff):
    candidate = context(contexts, api.CandidateStructureContextV1)
    order = context(contexts, api.OrderIntentContextV1)
    if params["execution_edge_definition"] != "EXECUTION_EDGE_CURRENCY_V1":
        raise ValueError("execution definition")
    cost_input = one(derived, "D133", now, cutoff)
    cost = named(cost_input.value)
    edge = named(one(derived, "D177", now, cutoff).value)
    currency = params["risk_currency"]
    if not currency or cost["currency"] != currency or edge["currency"] != currency:
        raise ValueError("currency mismatch")
    if edge["utility_domain"] != "net_currency" or not edge["utility_definition_ref"]:
        raise ValueError("untransformed net currency utility required")
    if edge["execution_reference_id"] != cost_input.occurrence_id:
        raise ValueError("execution reference mismatch")
    for carrier in (cost, edge):
        if (carrier["candidate_ref"] != ref(candidate)
                or carrier["as_of_utc"] != now or carrier["knowledge_cutoff_utc"] != cutoff):
            raise ValueError("frozen candidate/time mismatch")
    if cost["convention_ref"] != edge["convention_ref"] or not cost["convention_ref"]:
        raise ValueError("convention mismatch")
    contract = cost["contract_identity"]
    if contract not in candidate.leg_contract_identities:
        raise ValueError("unknown leg")
    leg = candidate.leg_contract_identities.index(contract)
    if candidate.leg_sides[leg] != order.side:
        raise ValueError("leg-side mismatch")
    size = number(order.intended_size)
    if cost["order_intent_ref"] != ref(order) or number(cost["intended_size"]) != size:
        raise ValueError("order reference/size mismatch")
    if abs(number(candidate.leg_quantities[leg])) != size:
        raise ValueError("candidate leg size mismatch")
    multiplier = number(cost["multiplier"])
    bid = number(one(raw, "R034", now, cutoff).value)
    ask = number(one(raw, "R035", now, cutoff).value)
    # Depth remains a required declared fact, even though the authorised price
    # boundary is quote/urgency-based and invents no depth-price estimator.
    for identity in ("R189", "R190"):
        if number(one(raw, identity, now, cutoff).value) < 0:
            raise ValueError("negative depth")
    midpoint = (bid + ask) / 2
    if not 0 <= bid <= ask or midpoint <= 0 or size <= 0 or multiplier <= 0:
        raise ValueError("invalid premium basis")
    if cost["side"] != order.side or number(cost["decision_midpoint"]) != midpoint:
        raise ValueError("execution side/midpoint mismatch")
    sign = 1 if order.side == "buy" else -1
    slippage = sign * (number(cost["expected_fill_price"]) - midpoint)
    quantity = size * multiplier
    if (slippage < 0 or number(cost["signed_slippage_per_unit"]) != slippage
            or number(cost["expected_slippage_currency"]) != quantity * slippage
            or number(cost["slippage_bps"]) != 10000 * slippage / midpoint):
        raise ValueError("inconsistent execution components")
    weights: dict[str, Fraction] = {}
    for entry in params["leg_headroom_weights"]:
        identity, amount = entry.split("|")
        if identity in weights:
            raise ValueError("duplicate allocation")
        weights[identity] = number(Decimal(amount))
    if (set(weights) != set(candidate.leg_contract_identities)
            or sum(weights.values()) != 1 or min(weights.values()) < 0
            or not params["allocation_version"]):
        raise ValueError("invalid full-candidate allocation")
    caps: dict[str, Fraction] = {}
    for entry in params["urgency_cost_caps"]:
        urgency, amount = entry.split("|")
        if urgency in caps:
            raise ValueError("ambiguous urgency")
        caps[urgency] = number(Decimal(amount))
    urgency_cap = caps[order.urgency]
    headroom = weights[contract] * (
        number(edge["net_currency_utility"]) - number(params["minimum_retained_edge_currency"])
    )
    allowed = min(slippage, slippage + headroom / quantity, urgency_cap)
    if allowed < 0 or urgency_cap < 0:
        raise ValueError("retained edge infeasible")
    price = min(ask, midpoint + allowed) if sign == 1 else max(bid, midpoint - allowed)
    # Buy floors, sell ceilings, so rounding cannot spend excess edge.
    output = decimal(price) if sign == 1 else -decimal(-price)
    if quantity * (sign * (number(output) - midpoint) - slippage) > headroom:
        raise ValueError("persisted price exceeds retained edge")
    return output
