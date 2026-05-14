from __future__ import annotations

import json
from pathlib import Path

import pytest


def test_financial_calendar_vocabulary_terms_are_present() -> None:
    vocab_path = Path("data/vocabulary/canonical_vocabulary.json")
    if not vocab_path.exists():
        pytest.fail(
            "Required vocabulary artefact is not implemented: data/vocabulary/canonical_vocabulary.json"
        )

    vocab = json.loads(vocab_path.read_text(encoding="utf-8"))
    entries = vocab.get("entries", [])
    slugs = {entry["canonical_slug"] for entry in entries}
    aliases = {alias for entry in entries for alias in entry.get("allowed_aliases", [])}

    assert "financial_calendar_crosswalk" in slugs
    assert "financial_calendar_import_record" in slugs
    assert (
        "financial_calendar_reference_bundle" in slugs
        or "financial_calendar_reference_bundle" in aliases
    )
