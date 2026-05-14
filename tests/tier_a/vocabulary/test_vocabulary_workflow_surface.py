from __future__ import annotations

from pathlib import Path

import pytest


def test_vocabulary_workflow_document_is_present() -> None:
    workflow_path = Path("docs/vocabulary/CONSOLIDATION_WORKFLOW.md")
    if not workflow_path.exists():
        pytest.fail(
            "Required workflow document is not implemented: docs/vocabulary/CONSOLIDATION_WORKFLOW.md"
        )
    workflow = workflow_path.read_text(encoding="utf-8")
    assert "enrich_existing" in workflow
    assert "add_new" in workflow
    assert "alias_only" in workflow
    assert "quarantine" in workflow
    assert "candidate" "_audit" in workflow.replace("-", "_")
    assert "llm pass" in workflow.casefold()
