from __future__ import annotations

import importlib
from typing import Iterable


def reference_status(
    *,
    replay_class: str,
    complete: bool,
    result_present: bool,
    fingerprint_match: bool,
    reasons_match: bool,
    executable_match: bool,
) -> str:
    if replay_class == "comparison_only":
        return "comparison_only"
    if replay_class == "preserved_occurrence_replay":
        return "authoritative_match" if complete else "non_authoritative_incomplete"
    if replay_class != "governed_semantic_reexecution":
        raise ValueError("unsupported_replay_class")
    if not complete or not result_present:
        return "non_authoritative_incomplete"
    if fingerprint_match and reasons_match and executable_match:
        return "authoritative_match"
    return "semantic_mismatch"


def canonical_reasons(values: Iterable[str]) -> tuple[str, ...]:
    result = tuple(str(value).strip() for value in values)
    if any(not value for value in result):
        raise ValueError("reason_must_be_nonempty")
    if len(set(result)) != len(result):
        raise ValueError("reasons_must_be_unique")
    return result


def production_api():
    module = importlib.import_module("nvda_desk.m12_evidence_replay")
    names = (
        "ReplayMaterial",
        "ReplayEnvelope",
        "ReplayAssessment",
        "ReviewProjection",
        "EvidenceReplayService",
    )
    return {name: getattr(module, name) for name in names}
