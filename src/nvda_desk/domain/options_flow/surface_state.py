"""Pure options-surface classification helpers."""

from __future__ import annotations

from nvda_desk.contracts.options_flow import OptionsFlowContextInput, OptionsFlowContextOutput


def classify_surface_state(context: OptionsFlowContextInput) -> OptionsFlowContextOutput:
    """Return one bounded options-flow state from simple surface inputs."""

    reasons: list[str] = []
    missing_fields = set(context.missing_fields)
    if context.spot_price is None:
        missing_fields.add("spot_price")
    if context.front_dte is None:
        missing_fields.add("front_dte")
    if context.next_dte is None:
        missing_fields.add("next_dte")

    term_structure_state = "unknown"
    if context.front_dte is not None and context.next_dte is not None:
        if context.next_dte > context.front_dte > 0:
            term_structure_state = "contango"
            reasons.append("next_dte_gt_front_dte")
        elif context.front_dte > context.next_dte > 0:
            term_structure_state = "backwardation"
            reasons.append("front_dte_gt_next_dte")
        else:
            term_structure_state = "flat"
            reasons.append("term_structure_flat")
    else:
        reasons.append("term_structure_inputs_incomplete")

    gamma_state = "unknown"
    if context.spot_price is not None:
        gamma_state = "active" if context.spot_price > 0 else "inactive"
        reasons.append("spot_price_present")
    else:
        reasons.append("spot_price_missing")

    for field_name in sorted(missing_fields):
        token = f"missing_{field_name}"
        if token not in reasons:
            reasons.append(token)

    return OptionsFlowContextOutput(
        term_structure_state=term_structure_state,
        skew_state="unknown",
        gamma_state=gamma_state,
        reasons=reasons,
    )
