from __future__ import annotations

import pytest

from nvda_desk.contracts.parallel_risk import (
    ParallelRiskDescriptionTemplateRef,
    ParallelRiskMinuteProfile,
    RiskFamilyState,
)
from nvda_desk.domain.parallel_risk.deterministic_description import (
    load_description_template_registry,
    render_parallel_risk_description,
)


def _profile() -> ParallelRiskMinuteProfile:
    return ParallelRiskMinuteProfile(
        packet_id="profile-description",
        symbol="NVDA",
        source_time_utc="2026-05-18T14:30:00Z",
        generated_at_utc="2026-05-18T14:30:01Z",
        risk_envelope_state="caution",
        risk_family_states=[
            RiskFamilyState(
                family="calendar_event",
                state="observe",
                intensity=0.4,
                confidence=0.8,
                dominant_atoms=["event_proximity:earnings"],
            ),
            RiskFamilyState(
                family="market_volatility_context",
                state="caution",
                intensity=0.7,
                confidence=0.6,
                dominant_atoms=["envelope:market_volatility_context:vix_elevated"],
            ),
        ],
        uncertainty_summary={"profile_confidence": 0.62},
    )


def _template_ref() -> ParallelRiskDescriptionTemplateRef:
    return ParallelRiskDescriptionTemplateRef(
        template_id="prl.minute_profile.summary.v1",
        template_registry_ref="data/parallel_risk/description_templates.v1.json",
        vocabulary_dictionary_refs=["data/vocabulary/canonical_vocabulary.json"],
        description_vocabulary_refs=["docs/vocabulary/vocabulary_registry.md#parallel-risk-lane"],
    )


def test_description_template_registry_loads_and_renders_deterministically() -> None:
    registry = load_description_template_registry(
        "data/parallel_risk/description_templates.v1.json"
    )

    output = render_parallel_risk_description(
        profile=_profile(), template_ref=_template_ref(), registry=registry
    )

    assert output == (
        "Parallel Risk Lane state-of-play: envelope=caution; active_atoms=0; "
        "watched_atoms=0; dominant_families=market_volatility_context,calendar_event; "
        "confidence=0.62. This is environmental risk description only."
    )
    for forbidden in ("buy", "sell", "fade", "chase", "hedge", "size up", "take the trade"):
        assert forbidden not in output


def test_description_renderer_rejects_unknown_template_id() -> None:
    registry = load_description_template_registry(
        "data/parallel_risk/description_templates.v1.json"
    )
    ref = _template_ref().model_copy(update={"template_id": "missing.template"})

    with pytest.raises(ValueError, match="parallel_risk_description_template_not_found"):
        render_parallel_risk_description(profile=_profile(), template_ref=ref, registry=registry)


def test_description_renderer_rejects_action_language_in_template_output() -> None:
    registry = {
        "templates": [
            {
                "template_id": "bad.template",
                "template": "buy because envelope={risk_envelope_state}",
                "vocabulary_refs": [
                    "data/vocabulary/canonical_vocabulary.json",
                    "docs/vocabulary/vocabulary_registry.md#parallel-risk-lane",
                ],
            }
        ]
    }
    ref = _template_ref().model_copy(update={"template_id": "bad.template"})

    with pytest.raises(ValueError, match="parallel_risk_description_forbidden_action_language"):
        render_parallel_risk_description(profile=_profile(), template_ref=ref, registry=registry)
