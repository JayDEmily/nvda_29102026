"""Conservative F4 progress reconciliation against accepted catalogue and F3 ledger.

Only two newly established public rows are advanced here. This script does NOT
confer public proof on other D rows or on an entire relationship class.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AUTHORITY = ROOT / "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv"
F3 = ROOT / "handoff/m01_completion/proof/f3_20261009/F3_ALL_EDGES_RECONCILIATION.csv"
OUT = Path(__file__).resolve().parent
NORMATIVE_SHA256 = "63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5"
STAGE1_KERNELS = {f"K{i:02d}" for i in range(1, 9)} | {"K16", "K17"}
F4_BOUNDED_PUBLIC_ROWS = {
    "D145": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_book_ofi_public.py",
        "admitted M00 four-field ordered book; exact raw lineage; "
        "incomplete-field and cutoff refusal",
    ),
    "D151": (
        "RC13",
        "tests/product/derived_signal/test_m01_f4_basket_breadth_public.py",
        "admitted M00 three-member basket; component-specific denominator; "
        "full lineage; missing-member refusal",
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert _sha256(AUTHORITY) == NORMATIVE_SHA256, "Accepted catalogue hash drift"
    with AUTHORITY.open(newline="", encoding="utf-8") as handle:
        catalogue = list(csv.DictReader(handle))
    assert len(catalogue) == 209
    authoritative = {item["derived_id"]: item for item in catalogue}
    assert len(authoritative) == 209
    stage1 = {
        did
        for did, item in authoritative.items()
        if item["kernel_id"].split("_", 1)[0] in STAGE1_KERNELS
    }
    assert len(stage1) == 174

    def closed(did: str, seen: frozenset[str] = frozenset()) -> bool:
        assert did not in seen, "Catalogue D graph must remain acyclic"
        if did not in stage1:
            return False
        return all(
            closed(dep, seen | {did})
            for dep in authoritative[did]["derived_dependencies"].split(";")
            if dep
        )

    closed_rows = {did for did in stage1 if closed(did)}
    deferred = stage1 - closed_rows
    assert (len(closed_rows), len(deferred)) == (144, 30)
    assert set(F4_BOUNDED_PUBLIC_ROWS).issubset(closed_rows)

    with F3.open(newline="", encoding="utf-8") as handle:
        edges = list(csv.DictReader(handle))
    assert len(edges) == 489, "488 dependencies plus D007 zero-edge sentinel"
    ids = [item["f1_edge_id"] for item in edges]
    assert len(set(ids)) == 489
    assert sum(item["source_type"] in {"R", "D"} for item in edges) == 488
    for item in edges:
        did = item["derived_row"]
        if did in F4_BOUNDED_PUBLIC_ROWS:
            expected_class, witness, proof = F4_BOUNDED_PUBLIC_ROWS[did]
            assert item["stage2_boundary"] == "STAGE1_CLOSED"
            assert item["relationship_class"] == expected_class
            assert item["f3c_disposition"] == "F4_OUTSTANDING_RELATIONSHIP_PROOF"
            item["f4_disposition"] = "F4_BOUNDED_PUBLIC_ROW_PROOF"
            item["f4_evidence"] = witness + ": " + proof
        else:
            item["f4_disposition"] = item["f3c_disposition"]
            item["f4_evidence"] = item["evidence_and_scope"]

    statuses = Counter(item["f4_disposition"] for item in edges)
    assert statuses == {
        "F2_ACCEPTED_SCOPED_EVIDENCE": 18,
        "F3A_BOUNDED_PUBLIC_PROOF": 4,
        "F3B_BOUNDED_PUBLIC_PROOF": 7,
        "F4_BOUNDED_PUBLIC_ROW_PROOF": 8,
        "F4_OUTSTANDING_RELATIONSHIP_PROOF": 344,
        "STAGE2_BOUNDARY_DEFERRED": 107,
        "ZERO_EDGE_SENTINEL_NO_DEPENDENCY": 1,
    }, statuses
    csv_target = OUT / "F4_RELATIONSHIP_PROOF_LEDGER.csv"
    columns = [*edges[0].keys()]
    with csv_target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, columns)
        writer.writeheader()
        writer.writerows(edges)
    metadata = {
        "authority_catalogue_sha256": _sha256(AUTHORITY),
        "prior_f3_ledger_sha256": _sha256(F3),
        "stage1_rows": len(stage1),
        "stage1_closed_rows": len(closed_rows),
        "cross_stage_rows": len(deferred),
        "f4_new_bounded_public_rows": sorted(F4_BOUNDED_PUBLIC_ROWS),
        "total_dependency_edges": 488,
        "zero_edge_sentinels": 1,
        "f4_dispositions": dict(sorted(statuses.items())),
        "stage1_f4_candidate_ready": False,
        "stage1_independent_acceptance": False,
        "boundary": (
            "Row-level public witness is not a proof of every member of "
            "RC12/RC13 or all 144 Stage-1-closed rows"
        ),
    }
    (OUT / "F4_PROGRESS_READBACK.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
