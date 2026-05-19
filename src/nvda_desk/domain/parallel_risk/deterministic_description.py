"""Deterministic vocabulary-governed description rendering for PRL profiles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nvda_desk.contracts.parallel_risk import (
    ParallelRiskDescriptionTemplateRef,
    ParallelRiskMinuteProfile,
)

_FORBIDDEN_ACTION_TERMS = (
    "buy",
    "sell",
    "fade",
    "chase",
    "hedge",
    "size up",
    "stand down",
    "take the trade",
    "avoid the trade",
    "order",
    "position size",
)


def load_description_template_registry(path: str | Path) -> dict[str, Any]:
    """Load the governed deterministic PRL description-template registry."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def render_parallel_risk_description(
    *,
    profile: ParallelRiskMinuteProfile,
    template_ref: ParallelRiskDescriptionTemplateRef,
    registry: dict[str, Any],
) -> str:
    """Render deterministic risk-state text from an explicit template reference.

    The result describes environmental state-of-play only and is rejected if template output
    contains prohibited action language.
    """

    template = _find_template(registry=registry, template_id=template_ref.template_id)
    _validate_template_refs(template=template, template_ref=template_ref)
    output = template["template"].format(**_template_values(profile))
    _reject_action_language(output)
    return output


def _find_template(*, registry: dict[str, Any], template_id: str) -> dict[str, Any]:
    for template in registry.get("templates", []):
        if template.get("template_id") == template_id:
            return template
    raise ValueError("parallel_risk_description_template_not_found")


def _validate_template_refs(
    *, template: dict[str, Any], template_ref: ParallelRiskDescriptionTemplateRef
) -> None:
    refs = set(template.get("vocabulary_refs", []))
    expected = set(template_ref.vocabulary_dictionary_refs + template_ref.description_vocabulary_refs)
    if expected and not expected <= refs:
        raise ValueError("parallel_risk_description_vocabulary_refs_mismatch")


def _template_values(profile: ParallelRiskMinuteProfile) -> dict[str, Any]:
    sorted_families = sorted(
        profile.risk_family_states,
        key=lambda item: (-item.intensity, item.family),
    )
    return {
        "risk_envelope_state": profile.risk_envelope_state,
        "active_atom_count": len(profile.active_risk_atoms),
        "watched_atom_count": len(profile.watched_risk_atoms),
        "dominant_families": ",".join(item.family for item in sorted_families[:3]) or "none",
        "profile_confidence": profile.uncertainty_summary.get("profile_confidence", "unknown"),
    }


def _reject_action_language(output: str) -> None:
    lowered = output.lower()
    if any(term in lowered for term in _FORBIDDEN_ACTION_TERMS):
        raise ValueError("parallel_risk_description_forbidden_action_language")
