from __future__ import annotations

from pathlib import Path


def test_parallel_risk_description_constraints_reference_governed_vocabulary_sources() -> None:
    text = Path("docs/planning/PRL_RISK_DESCRIPTION_VOCABULARY_CONSTRAINTS.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md",
        "docs/vocabulary/README.md",
        "docs/vocabulary/CONSOLIDATION_WORKFLOW.md",
        "docs/vocabulary/vocabulary_registry.md",
        "data/vocabulary/canonical_vocabulary.json",
    ):
        assert required in text


def test_parallel_risk_description_constraints_exclude_free_form_trade_advice() -> None:
    text = Path("docs/planning/PRL_RISK_DESCRIPTION_VOCABULARY_CONSTRAINTS.md").read_text(
        encoding="utf-8"
    )

    assert "No free-form generative commentary" in text
    assert "must not contain trade advice" in text
    assert "data/parallel_risk/description_templates.v1.json" in text
    assert "Do not implement a renderer" in text
