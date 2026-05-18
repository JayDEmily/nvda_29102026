from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.parallel_risk import (
    ParallelRiskDescriptionTemplateRef,
    ParallelRiskMinuteProfile,
)


def test_description_template_ref_is_deterministic_metadata_only() -> None:
    ref = ParallelRiskDescriptionTemplateRef(
        template_id="prl.minute_profile.summary.v1",
        template_registry_ref="data/parallel_risk/description_templates.v1.json",
        vocabulary_dictionary_refs=["data/vocabulary/canonical_vocabulary.json"],
        description_vocabulary_refs=["docs/vocabulary/vocabulary_registry.md#parallel-risk-lane"],
    )

    assert ref.deterministic_template_only is True
    assert ref.free_form_generation_allowed is False
    assert ref.trade_advice_allowed is False
    assert ref.capital_or_order_language_allowed is False


def test_description_template_ref_rejects_free_form_or_trade_advice_authority() -> None:
    with pytest.raises(ValidationError, match="parallel_risk_description_template_ref_must_remain_bounded"):
        ParallelRiskDescriptionTemplateRef(
            template_id="prl.minute_profile.summary.v1",
            template_registry_ref="data/parallel_risk/description_templates.v1.json",
            free_form_generation_allowed=True,
        )


def test_minute_profile_description_fields_remain_references_not_prose() -> None:
    profile = ParallelRiskMinuteProfile(
        packet_id="profile-description-ref",
        symbol="NVDA",
        source_time_utc="2026-05-18T14:30:00Z",
        generated_at_utc="2026-05-18T14:30:01Z",
        description_template_id="prl.minute_profile.summary.v1",
        description_vocabulary_refs=["data/vocabulary/canonical_vocabulary.json"],
    )

    assert profile.description_template_id == "prl.minute_profile.summary.v1"
    assert profile.description_vocabulary_refs == ["data/vocabulary/canonical_vocabulary.json"]
    assert "plain_english" not in ParallelRiskMinuteProfile.model_fields
    assert "freeform_text" not in ParallelRiskMinuteProfile.model_fields
