#!/usr/bin/env python3
"""Review-only schema check. Never writes an admission or synthesises authority."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from nvda_desk.architecture.schema import SchemaValidationError, validate_instance

prefix = ROOT / "handoff/review/t01_ruff_zero_readmission_20261114"
manifest = json.loads((prefix / "PROPOSED_SUCCESSOR_GENERATIONS.json").read_text())
schema = json.loads((ROOT / "schemas/product_proof_admission.schema.json").read_text())
results = []
for row in manifest["claims"]:
    name = row["claim_id"]
    document = row["proposed_generation_record_REVIEW_ONLY_INCOMPLETE_AUTHORITY"]
    assert document["adequacy_review_ref"] is None
    assert document["admission_authority_ref"] is None
    assert not (ROOT / row["proposed_generation_path"]).exists()
    pointer = json.loads((ROOT / row["admission_path"]).read_text())
    validate_instance(pointer, schema)
    assert pointer["current_generation"] == row["predecessor_pointer"]
    try:
        validate_instance(document, schema)
    except SchemaValidationError:
        incomplete_rejected = True
    else:
        raise AssertionError(f"{name}: incomplete generation was incorrectly accepted")
    temporary = copy.deepcopy(document)
    # These are non-authoritative schema-type sentinels, never persisted.
    temporary["adequacy_review_ref"] = "SCHEMA_ONLY_SENTINEL_NOT_AN_ADEQUACY_REVIEW"
    temporary["admission_authority_ref"] = "SCHEMA_ONLY_SENTINEL_NOT_OWNER_APPROVAL"
    validate_instance(temporary, schema)
    results.append({
        "claim_id": name,
        "active_pointer_schema_valid": True,
        "missing_authority_rejected": incomplete_rejected,
        "hypothetical_nonempty_references_shape_valid": True,
        "new_generation_written": False,
        "review_or_admission_authority_conferred": False,
    })
print(json.dumps({
    "audit": "SCHEMA_ONLY_NON_ADMISSION_PREFLIGHT",
    "claims_verified": len(results),
    "status": "PASS_PRE_ADMISSION_SHAPE_ONLY",
    "actual_owner_admission_authority": "UNVERIFIED_PENDING",
    "proof_executed": False,
    "new_generation_written": False,
    "results": results,
}, indent=2))
