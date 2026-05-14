from __future__ import annotations

import json
from pathlib import Path


def test_required_module_8_parallel_risk_terms_are_present() -> None:
    vocab = json.loads(
        Path("data/vocabulary/canonical_vocabulary.json").read_text(encoding="utf-8")
    )
    entries = {entry["canonical_slug"]: entry for entry in vocab["entries"]}

    expected = {
        "environment_assessment": "ParallelRiskEnvironmentAssessment",
        "candidate_audit": "ParallelRiskCandidateAuditSurface",
        "stage_read_state": "ParallelRiskStageReadRecord",
        "dependency_packet_ids": "DmpV3Lineage.dependencyids",
        "parallel_risk_observation_store": "ParallelRiskObservationStore",
        "write_only_persistence": "ParallelRiskObservationStore.append_observation",
        "append_only_observation_record": "ParallelRiskObservationRecord",
    }

    for slug, contract in expected.items():
        assert slug in entries
        assert entries[slug]["maps_to_contract"] == contract
