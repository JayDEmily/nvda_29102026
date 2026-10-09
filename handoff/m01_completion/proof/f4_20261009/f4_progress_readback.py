"""Conservative F4 progress reconciliation against accepted catalogue and F3 ledger.

The original F3 ledger remains immutable historical evidence. Its row-edge IDs are
mechanically rebased by (D row, kind, source ID) onto the authorised F1
D134/D135 R187 correction; no historical acceptance is silently invented.
The new D134/D135/D136 proofs apply only to their bounded public mechanism.
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
NORMATIVE_SHA256 = "8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a"
STAGE1_KERNELS = {f"K{i:02d}" for i in range(1, 9)} | {"K16", "K17"}
F4_BOUNDED_PUBLIC_ROWS = {
    "D134": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_positional_book_class.py",
        "M00 position-shifting operation reconstruction; top-two bid 17; missing operation refusal and exact lineage",
    ),
    "D135": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_positional_book_class.py",
        "M00 independent ask book top-two 13; explicit operations and exact lineage",
    ),
    "D136": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_positional_book_class.py",
        "M00 D134/D135 reconstructed ratio 4/30 with inherited lineage",
    ),
    "D145": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_book_ofi_public.py",
        "admitted M00 four-field ordered book; exact raw lineage; "
        "incomplete-field and cutoff refusal",
    ),
    "D139": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_book_rates_public.py",
        "controlled M00 book event rates by side/level; native event completeness; exact lineage",
    ),
    "D140": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_book_rates_public.py",
        "controlled M00 book quantity rates by side/level; "
        "native event completeness; exact lineage",
    ),
    "D143": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_direct_book_public.py",
        "controlled M00 direct venue concentration; missing native venue refusal",
    ),
    "D144": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_direct_book_public.py",
        "controlled M00 SMART/direct matched-book divergence; incomplete event refusal",
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
        old_edges = list(csv.DictReader(handle))
    assert len(old_edges) == 489, "Historical F3 ledger must remain the original 488+1"
    old_by_identity = {(e["derived_row"], e["source_type"], e["source_id"]): e for e in old_edges}
    assert len(old_by_identity) == 489
    classified = ROOT / "handoff/m01_completion/foundation/F1_CLASSIFIED_EDGE_MAP.csv"
    with classified.open(newline="", encoding="utf-8") as handle:
        canonical_edges = list(csv.DictReader(handle))
    assert len(canonical_edges) == 491, "490 amended dependencies plus D007 sentinel"
    edges = []
    added = []
    for edge in canonical_edges:
        key = (edge["derived_id"], edge["source_type"], edge["source_id"])
        inherited = old_by_identity.get(key)
        if inherited is None:
            assert key in {("D134", "R", "R187"), ("D135", "R", "R187")}, key
            added.append(key)
            item = {
                "f1_edge_id": edge["edge_id"], "derived_row": edge["derived_id"],
                "source_type": edge["source_type"], "source_id": edge["source_id"],
                "relationship_class": edge["relationship_class"],
                "stage2_boundary": edge["stage2_boundary"],
                "f3c_disposition": "F4_OUTSTANDING_RELATIONSHIP_PROOF",
                "evidence_and_scope": "Programme Owner 2026-10-09 R187 amendment; no inherited F3 proof",
            }
        else:
            item = dict(inherited)
            item["f1_edge_id"] = edge["edge_id"]
            assert item["relationship_class"] == edge["relationship_class"]
            assert item["stage2_boundary"] == edge["stage2_boundary"]
        edges.append(item)
    assert len(added) == 2 and len(edges) == 491
    ids = [item["f1_edge_id"] for item in edges]
    assert len(set(ids)) == 491
    assert sum(item["source_type"] in {"R", "D"} for item in edges) == 490
    for item in edges:
        did = item["derived_row"]
        if did in F4_BOUNDED_PUBLIC_ROWS:
            expected_class, witness, proof = F4_BOUNDED_PUBLIC_ROWS[did]
            assert item["stage2_boundary"] == "STAGE1_CLOSED"
            assert item["relationship_class"] == expected_class
            assert item["f3c_disposition"] == "F4_OUTSTANDING_RELATIONSHIP_PROOF"
            item["f4_disposition"] = "F4_BOUNDED_PUBLIC_ROW_PROOF"
            item["f4_evidence"] = witness + ": " + proof
        elif did == "D007" and item["source_type"] == "NONE":
            assert item["f3c_disposition"] == "ZERO_EDGE_SENTINEL_NO_DEPENDENCY"
            item["f4_disposition"] = "F4_ZERO_EDGE_PUBLIC_PROOF"
            item["f4_evidence"] = (
                "tests/product/derived_signal/test_m01_f4_required_field_public.py: "
                "required-field policy and M00 projection with allowed absence, future refusal"
            )
        else:
            item["f4_disposition"] = item["f3c_disposition"]
            item["f4_evidence"] = item["evidence_and_scope"]

    statuses = Counter(item["f4_disposition"] for item in edges)
    assert statuses == {
        "F2_ACCEPTED_SCOPED_EVIDENCE": 18,
        "F3A_BOUNDED_PUBLIC_PROOF": 4,
        "F3B_BOUNDED_PUBLIC_PROOF": 7,
        "F4_BOUNDED_PUBLIC_ROW_PROOF": 45,
        "F4_OUTSTANDING_RELATIONSHIP_PROOF": 309,
        "STAGE2_BOUNDARY_DEFERRED": 107,
        "F4_ZERO_EDGE_PUBLIC_PROOF": 1,
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
        "total_dependency_edges": 490,
        "new_authorised_raw_edges": ["D134/R187", "D135/R187"],
        "zero_edge_sentinels": 1,
        "f4_dispositions": dict(sorted(statuses.items())),
        "unresolved_rc12_public_rows": ["D131", "D137", "D138", "D141", "D142"],
        "historical_three_field_witness": "retained in commit 450b7e6; formerly produced zero",
        "repaired_event_witness": "explicit R187 operation; D134=10, D135=7, D136=3/17",
        "depth_snapshot_vs_event_reconstruction_authority": "AUTHORISATION_RESOLVED_EVENT_DRIVEN",
        "stage1_f4_candidate_ready": False,
        "stage1_independent_acceptance": False,
        "boundary": (
            "Bounded row proofs do not prove all 144 Stage-1-closed rows or 30 cross-stage rows; "
            "F4 outstanding edge classes and public reachability remain unproved"
        ),
    }
    (OUT / "F4_PROGRESS_READBACK.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
