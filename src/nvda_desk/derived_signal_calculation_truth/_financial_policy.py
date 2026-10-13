"""Owner-approved F4 Stage-1 policy consumers, never Stage-2 producers."""

from datetime import datetime
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import pairwise

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
        if (
            carrier["candidate_ref"] != ref(candidate)
            or carrier["as_of_utc"] != now
            or carrier["knowledge_cutoff_utc"] != cutoff
        ):
            raise ValueError("frozen candidate/time mismatch")
    if cost["convention_ref"] != edge["convention_ref"] or not cost["convention_ref"]:
        raise ValueError("convention mismatch")
    contract = cost["contract_identity"]
    if contract not in candidate.leg_contract_identities:
        raise ValueError("unknown leg")
    for identity in ("R034", "R035", "R189", "R190"):
        quote_metadata = dict(one(raw, identity, now, cutoff).metadata)
        if quote_metadata.get("contract_id") != contract:
            raise ValueError("quote/depth contract mismatch")
        if identity in {"R034", "R035"} and (
            quote_metadata.get("currency") != currency
            or quote_metadata.get("unit_convention_ref") != cost["convention_ref"]
        ):
            raise ValueError("premium currency/convention mismatch")
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
    if (
        slippage < 0
        or number(cost["signed_slippage_per_unit"]) != slippage
        or number(cost["expected_slippage_currency"]) != quantity * slippage
        or number(cost["slippage_bps"]) != 10000 * slippage / midpoint
    ):
        raise ValueError("inconsistent execution components")
    weights: dict[str, Fraction] = {}
    for entry in params["leg_headroom_weights"]:
        identity, amount = entry.split("|")
        if identity in weights:
            raise ValueError("duplicate allocation")
        weights[identity] = number(Decimal(amount))
    if (
        set(weights) != set(candidate.leg_contract_identities)
        or sum(weights.values()) != 1
        or min(weights.values()) < 0
        or not params["allocation_version"]
    ):
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


GREEKS = ("delta", "gamma", "vega", "theta")
GREEK_UNITS = ("shares", "shares_per_currency", "currency_per_volatility_point", "currency_per_day")
DEFINITION_KEYS = (
    "risk_definition_id",
    "risk_definition_version",
    "risk_currency",
    "risk_price_shock",
    "risk_volatility_points_shock",
    "risk_horizon_days",
)
REFERENCE_KEYS = (
    "currency",
    "candidate_ref",
    "scope_ref",
    "scenario_grid_ref",
    "model_ref",
    "option_convention_ref",
    "as_of_utc",
    "knowledge_cutoff_utc",
)
SCOPE_KEYS = (
    "account_identity",
    "sleeve_identity",
    "position_source_refs",
    "live_position_ref",
    "membership_definition_ref",
    "risk_definition_parameter_ref",
)


def exact(value: object) -> Fraction:
    if (
        type(value) is not tuple
        or len(value) != 2
        or type(value[0]) is not int
        or type(value[1]) is not int
        or value[1] <= 0
    ):
        raise ValueError("canonical rational required")
    result = Fraction(*value)
    if (result.numerator, result.denominator) != value:
        raise ValueError("rational not in lowest terms")
    return result


def pair(value: Fraction) -> tuple[int, int]:
    return value.numerator, value.denominator


def vector(value):
    fields = named(value)
    if tuple(fields) != GREEKS:
        raise ValueError("ordered complete four-Greek vector required")
    return tuple(number(fields[key]) for key in GREEKS)


def packed_vector(values):
    return tuple((key, decimal(value)) for key, value in zip(GREEKS, values, strict=True))


def coefficients(params):
    if (
        params["risk_definition_id"] != "GREEK_SHOCK_ENVELOPE_V1"
        or params["risk_definition_version"] != "D175-REFERENCE-20261013-01"
    ):
        raise ValueError("unadmitted monetary convention")
    s, v, t = (
        number(params[key])
        for key in ("risk_price_shock", "risk_volatility_points_shock", "risk_horizon_days")
    )
    if min(s, v, t) <= 0 or not params["risk_currency"]:
        raise ValueError("explicit positive shocks/currency required")
    return s, s * s / 2, v, t


def envelope(values, weights):
    return sum((abs(x) * w for x, w in zip(values, weights, strict=True)), Fraction(0))


def risk_context(contexts, params):
    scope = context(contexts, api.RiskScopeContextV1)
    candidate = context(contexts, api.CandidateStructureContextV1)
    if ref(candidate) != ref(scope.candidate_structure_ref):
        raise ValueError("candidate scope mismatch")
    definitions = [
        value
        for value in contexts
        if type(value) is api.CalculationParameterSetV1
        and ref(value) == ref(scope.risk_definition_parameter_ref)
    ]
    memberships = [
        value
        for value in contexts
        if type(value) is api.CalculationParameterSetV1
        and ref(value) == ref(scope.membership_definition_ref)
    ]
    if len(definitions) != 1 or len(memberships) != 1:
        raise ValueError("exact risk/membership definitions required")
    definition = dict(definitions[0].parameters)
    if any(params[key] != definition[key] for key in DEFINITION_KEYS):
        raise ValueError("risk convention changed")
    if scope.currency_code != params["risk_currency"]:
        raise ValueError("risk currency mismatch")
    membership = dict(memberships[0].parameters)
    if (
        membership["account_identity"] != scope.account_identity
        or membership["sleeve_identity"] != scope.sleeve_identity
    ):
        raise ValueError("membership scope mismatch")
    members = membership["complete_members"]
    if type(members) is not tuple or not members:
        raise ValueError("explicit complete managed sleeve required")
    contracts, quantities, sources = [], [], []
    for member in members:
        contract, amount, source = member.split("|")
        if not contract or not source:
            raise ValueError("membership identity missing")
        contracts.append(contract)
        quantities.append(number(Decimal(amount)))
        sources.append(source)
    if (
        len(set(contracts)) != len(contracts)
        or len(set(sources)) != len(sources)
        or tuple(sources) != scope.position_membership_source_refs
        or tuple(contracts) != candidate.leg_contract_identities
    ):
        raise ValueError("complete sleeve/source mismatch")
    signed = tuple(
        abs(number(q)) * (1 if side == "buy" else -1)
        for q, side in zip(candidate.leg_quantities, candidate.leg_sides, strict=True)
    )
    if tuple(quantities) != signed:
        raise ValueError("candidate quantity mismatch")
    if scope.scope_mode == "live_sleeve":
        live = context(contexts, api.LivePositionContextV1)
        if (
            ref(live) != ref(scope.live_position_ref)
            or live.leg_contract_identities != tuple(contracts)
            or tuple(number(q) for q in live.signed_quantities) != signed
            or live.m00_occurrence_refs != tuple(sources)
        ):
            raise ValueError("live sleeve membership mismatch")
    return scope, candidate


def risk_budget(raw, derived, params, contexts, now, cutoff):
    weights = coefficients(params)
    scope, candidate = risk_context(contexts, params)
    if params["limit_policy_definition"] != "REFERENCE_CALIBRATED_ENVELOPE_V1":
        raise ValueError("unadmitted limit policy")
    account = []
    for identity in ("R205", "R206", "R209", "R208"):
        value = one(raw, identity, now, cutoff)
        meta = dict(value.metadata)
        if (
            value.subject_instrument != scope.account_subject_identity
            or meta["account_identity"] != scope.account_identity
            or meta["currency"] != scope.currency_code
            or meta["canonical_units"] != scope.currency_code
        ):
            raise ValueError("account/currency/unit mismatch")
        account.append(number(value.value))
    n, a, e, m = account
    capital = number(candidate.risk_capital_currency)
    if n <= 0 or m < 0 or not 0 < capital <= n:
        raise ValueError("invalid capital basis")
    matrix_input = one(derived, "D174", now, cutoff)
    matrix = named(matrix_input.value)
    tail_input = one(derived, "D162", now, cutoff)
    tail = named(tail_input.value)
    if any(matrix[key] != tail[key] for key in REFERENCE_KEYS):
        raise ValueError("incompatible tail and matrix")
    if (
        matrix["currency"] != scope.currency_code
        or matrix["candidate_ref"] != ref(candidate)
        or matrix["scope_ref"] != ref(scope)
        or matrix["as_of_utc"] != now
        or matrix["knowledge_cutoff_utc"] != cutoff
        or tail["d174_occurrence_id"] != matrix_input.occurrence_id
        or matrix["position_source_refs"] != scope.position_membership_source_refs
    ):
        raise ValueError("frozen reference mismatch")
    if not 0 < number(tail["confidence"]) < 1:
        raise ValueError("CVaR confidence invalid")
    pnl, probabilities = named(matrix["gross_scenario_PnL"]), named(matrix["scenario_weights"])
    if (
        not pnl
        or tuple(pnl) != tuple(probabilities)
        or tuple(pnl) != tail["scenario_ids"]
        or any(number(p) < 0 for p in probabilities.values())
        or sum(number(p) for p in probabilities.values()) != 1
    ):
        raise ValueError("exact full weighted grid required")
    if (
        tuple(named(matrix["greek_units"]).items()) != tuple(zip(GREEKS, GREEK_UNITS, strict=True))
        or not matrix["d168_occurrence_id"]
    ):
        raise ValueError("retained Greek unit/occurrence evidence required")
    current = vector(matrix["reference_greeks"])
    usage = envelope(current, weights)
    signed_cvar = number(tail["CVaR_currency"])
    c, w = max(Fraction(0), signed_cvar), max(Fraction(0), max(-number(v) for v in pnl.values()))
    if usage == 0 and (c > 0 or w > 0):
        raise ValueError("positive nonlinear loss in zero Greek coordinate")
    capacity = max(Fraction(0), min(a, e, n - m))
    bases = {
        "capital": capital,
        "tail": capital,
        "stress": capital,
        "concentration": n,
        "liquidity": capacity,
    }
    limits, records, thresholds = {}, [], []
    for name, basis in bases.items():
        active, fraction = params[name + "_active"], number(params[name + "_fraction"])
        if type(active) is not bool or not 0 <= fraction <= 1:
            raise ValueError("explicit activation/fraction required")
        if name in {"capital", "concentration", "liquidity"} and not active:
            raise ValueError("mandatory active ceiling missing")
        native = fraction * basis
        measurement = c if name == "tail" else w if name == "stress" else usage
        fields = [
            ("native_threshold_exact", pair(native)),
            ("measurement_exact", pair(measurement)),
        ]
        thresholds.append((name, pair(native)))
        if not active:
            status = "inactive_by_policy"
        elif name in {"tail", "stress"} and measurement == 0:
            status = "nonbinding_zero_measurement"
        else:
            status = "active_finite"
            ceiling = usage * native / measurement if name in {"tail", "stress"} else native
            limits[name] = ceiling
            fields.append(("envelope_ceiling_exact", pair(ceiling)))
        records.append((name, (("status", status), *fields)))
    maximum = min(limits.values())
    output = dict(
        definition="REFERENCE_CALIBRATED_ENVELOPE_V1",
        maximum_currency_exact=pair(maximum),
        maximum_currency=decimal(maximum),
        maximum_percent_risk_capital_exact=pair(100 * maximum / capital),
        maximum_percent_risk_capital=decimal(100 * maximum / capital),
        decimal_rounding="floor_28_fractional_places",
        reference_greeks=matrix["reference_greeks"],
        greek_units=matrix["greek_units"],
        reference_envelope_currency_exact=pair(usage),
        reference_envelope_currency=decimal(usage),
        native_thresholds=tuple(thresholds),
        native_measurements=(
            ("signed_CVaR_exact", pair(signed_cvar)),
            ("CVaR_usage_exact", pair(c)),
            ("stress_usage_exact", pair(w)),
        ),
        active_limit_records=tuple(records),
        binding_limits=tuple(k for k, v in limits.items() if v == maximum),
        risk_capital_currency=candidate.risk_capital_currency,
        account_identity=scope.account_identity,
        sleeve_identity=scope.sleeve_identity,
        position_source_refs=scope.position_membership_source_refs,
        live_position_ref=() if scope.live_position_ref is None else ref(scope.live_position_ref),
        membership_definition_ref=ref(scope.membership_definition_ref),
        risk_definition_parameter_ref=ref(scope.risk_definition_parameter_ref),
        d174_occurrence_id=matrix_input.occurrence_id,
        d162_occurrence_id=tail_input.occurrence_id,
        d168_occurrence_id=matrix["d168_occurrence_id"],
        confidence=tail["confidence"],
        scenario_ids=tuple(pnl),
    )
    output.update({key: matrix[key] for key in REFERENCE_KEYS})
    output.update({key: params[key] for key in DEFINITION_KEYS})
    return tuple(output.items())


def validate_budget(value, params, now, cutoff):
    b = named(value)
    if (
        b["definition"] != "REFERENCE_CALIBRATED_ENVELOPE_V1"
        or any(b[key] != params[key] for key in DEFINITION_KEYS)
        or b["currency"] != params["risk_currency"]
        or b["as_of_utc"] != now
        or b["knowledge_cutoff_utc"] != cutoff
    ):
        raise ValueError("risk definition/currency/time mismatch")
    weights, current = coefficients(params), vector(b["reference_greeks"])
    if envelope(current, weights) != exact(b["reference_envelope_currency_exact"]):
        raise ValueError("reference risk mismatch")
    maximum = exact(b["maximum_currency_exact"])
    if maximum < 0 or b["maximum_currency"] != decimal(maximum):
        raise ValueError("invalid exact ceiling")
    limits = {}
    for key, record in named(b["active_limit_records"]).items():
        fields = named(record)
        if fields["status"] == "active_finite":
            limits[key] = exact(fields["envelope_ceiling_exact"])
        elif fields["status"] not in {"inactive_by_policy", "nonbinding_zero_measurement"}:
            raise ValueError("unadmitted limit status")
    if (
        not {"capital", "concentration", "liquidity"} <= limits.keys()
        or min(limits.values()) != maximum
    ):
        raise ValueError("inconsistent active ceilings")
    return b, current, weights, maximum


def hedge_adjustment(derived, params, contexts, now, cutoff):
    scope, _ = risk_context(contexts, params)
    live = context(contexts, api.LivePositionContextV1)
    budget_input = one(derived, "D175", now, cutoff)
    b, reference, weights, maximum = validate_budget(budget_input.value, params, now, cutoff)
    if (
        b["scope_ref"] != ref(scope)
        or b["live_position_ref"] != ref(live)
        or b["position_source_refs"] != scope.position_membership_source_refs
    ):
        raise ValueError("live risk scope mismatch")
    current = []
    for identity, unit in zip(("D181", "D182", "D183", "D184"), GREEK_UNITS, strict=True):
        value = one(derived, identity, now, cutoff)
        meta = dict(value.metadata)
        position_ref_matches = meta.get("position_context_ref") == ref(live) or api.VersionRefV1(
            live.context_id, live.version
        ) in meta.get("parameter_context_refs", ())
        if (
            meta.get("canonical_risk_unit", meta.get("units")) != unit
            or not position_ref_matches
            or set(meta["position_source_refs"]) != set(live.m00_occurrence_refs)
        ):
            raise ValueError("live exposure units/source mismatch")
        current.append(number(value.value))
    if tuple(current) != reference:
        raise ValueError("changed reference needs revaluation")
    bands = {}
    for entry in params["target_bands"]:
        key, low, high = entry.split("|")
        lo, hi = number(Decimal(low)), number(Decimal(high))
        if key in bands or key not in GREEKS or lo > hi:
            raise ValueError("ambiguous/reversed band")
        bands[key] = lo, hi
    if set(bands) != set(GREEKS):
        raise ValueError("four independently defined bands required")
    adjustment = tuple(
        Fraction(0) if bands[key][0] <= x <= bands[key][1] else sum(bands[key]) / 2 - x
        for key, x in zip(GREEKS, current, strict=True)
    )
    initial_risk, adjustment_risk = envelope(current, weights), envelope(adjustment, weights)
    cap = min(Fraction(1), maximum / adjustment_risk) if adjustment_risk else Fraction(1)
    points = sorted(
        {
            Fraction(0),
            cap,
            *(-x / h for x, h in zip(current, adjustment, strict=True) if h and 0 < -x / h < cap),
        }
    )

    def residual(z):
        return envelope(tuple(x + z * h for x, h in zip(current, adjustment, strict=True)), weights)

    feasible = [Fraction(0)]
    for left, right in pairwise(points):
        low, high = residual(left), residual(right)
        if high <= initial_risk:
            feasible.append(right)
        elif low <= initial_risk and high > low:
            feasible.append(left + (initial_risk - low) * (right - left) / (high - low))
    fraction = decimal(max(feasible))
    persisted = packed_vector(tuple(number(fraction) * x for x in adjustment))
    permitted = vector(persisted)
    used, remaining = (
        envelope(permitted, weights),
        envelope(tuple(x + h for x, h in zip(current, permitted, strict=True)), weights),
    )
    if used > maximum or remaining > initial_risk:
        raise ValueError("persisted clipping failed readback")
    output = dict(
        adjustment=persisted,
        unclipped_adjustment=packed_vector(adjustment),
        current_exposure=packed_vector(current),
        clipping_fraction=fraction,
        current_risk_currency_exact=pair(initial_risk),
        current_risk_currency=decimal(initial_risk),
        adjustment_risk_currency_exact=pair(used),
        adjustment_risk_currency=decimal(used),
        residual_risk_currency_exact=pair(remaining),
        residual_risk_currency=decimal(remaining),
        risk_limit_currency_exact=pair(maximum),
        risk_limit_currency=decimal(maximum),
        d175_occurrence_id=budget_input.occurrence_id,
        post_adjustment_native_loss_status="requires_revaluation",
    )
    output.update({key: b[key] for key in (*REFERENCE_KEYS, *DEFINITION_KEYS, *SCOPE_KEYS)})
    return tuple(output.items())


def action_decision(derived, params, now, cutoff):
    inputs = {
        identity: one(derived, identity, now, cutoff)
        for identity in ("D187", "D188", "D189", "D190", "D191", "D175")
    }
    b, current, weights, maximum = validate_budget(inputs["D175"].value, params, now, cutoff)
    h = named(inputs["D189"].value)
    if any(b[key] != h[key] for key in (*REFERENCE_KEYS, *DEFINITION_KEYS, *SCOPE_KEYS)):
        raise ValueError("hedge/budget reference mismatch")
    permitted = vector(h["adjustment"])
    initial = envelope(current, weights)
    used = envelope(permitted, weights)
    remaining = envelope(tuple(x + h for x, h in zip(current, permitted, strict=True)), weights)
    if (
        h["d175_occurrence_id"] != inputs["D175"].occurrence_id
        or vector(h["current_exposure"]) != current
        or exact(h["current_risk_currency_exact"]) != initial
        or exact(h["risk_limit_currency_exact"]) != maximum
        or exact(h["adjustment_risk_currency_exact"]) != used
        or used > maximum
        or exact(h["residual_risk_currency_exact"]) != remaining
        or remaining > initial
    ):
        raise ValueError("tampered computed risk evidence")
    invalidation, modify = number(inputs["D187"].value), number(inputs["D190"].value)
    if (
        dict(inputs["D187"].metadata)["units"] != params["invalidation_domain"]
        or params["invalidation_domain"] != "score"
        or dict(inputs["D190"].metadata)["utility_domain"] != params["utility_domain"]
    ):
        raise ValueError("invalidation/modification domain mismatch")
    hold = named(inputs["D188"].value)
    if (
        hold["currency"] != params["risk_currency"]
        or dict(inputs["D191"].metadata)["currency"] != params["risk_currency"]
    ):
        raise ValueError("exit/hold currency mismatch")
    hold_value, exit_value = number(hold["expected_currency_PnL"]), number(inputs["D191"].value)
    exit_enabled, hedge_enabled = (
        params["mandatory_exit_on_invalidation"],
        params["mandatory_hedge_on_risk"],
    )
    if type(exit_enabled) is not bool or type(hedge_enabled) is not bool:
        raise ValueError("explicit policy activation required")
    invalidation_threshold = number(params["invalidation_threshold"])
    modify_minimum, exit_margin = (
        number(params["modify_minimum"]),
        number(params["exit_margin_currency"]),
    )
    if exit_enabled and invalidation >= invalidation_threshold:
        return "exit"
    if hedge_enabled and initial > maximum and any(permitted):
        return "hedge"
    if modify > modify_minimum:
        return "modify"
    if exit_value > hold_value + exit_margin:
        return "exit"
    return "hold"
