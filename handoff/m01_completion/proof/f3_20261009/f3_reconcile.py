"""Independent readback of F3 bounded relationship evidence versus accepted F1 census.

This deliberately marks unproved edges as open; a census is never a proof of behaviour.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
M01 = HERE.parents[1]
F1_PATH = M01 / "foundation" / "F1_CLASSIFIED_EDGE_MAP.csv"
F2_PATH = HERE.parent / "f2_observation_identity_20261009" / "F2_EDGE_RECONCILIATION.csv"
F1_COUNTS_PATH = M01 / "foundation" / "F1_COUNTS.json"
OUT = HERE / "F3_ALL_EDGES_RECONCILIATION.csv"
CLASSES_OUT = HERE / "F3_CLASS_COVERAGE.json"


def rows(p: Path) -> list[dict[str, str]]:
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


f1 = rows(F1_PATH)
f2 = rows(F2_PATH)
counts = json.loads(F1_COUNTS_PATH.read_text(encoding="utf-8"))
actual = {r["edge_id"]: r for r in f1 if r["source_type"] in {"D", "R"}}
assert len(actual) == 488 and len(f1) == 489 and counts["stage1_closed"] == 144
assert counts["cross_stage_direct"] + counts["cross_stage_transitive_only"] == 30
assert len({r["edge_id"] for r in f1}) == 489
assert len(f2) == 18 and len({r["f1_edge_id"] for r in f2}) == 18
f2_keys = {r["f1_edge_id"] for r in f2}
for r in f2:
    a = actual[r["f1_edge_id"]]
    assert (r["derived_row"], r["source_type"], r["source_id"], r["relationship_class"]) == (
        a["derived_id"],
        a["source_type"],
        a["source_id"],
        a["relationship_class"],
    )

f3a = {"D109:D:01", "D109:D:02", "D170:R:01", "D170:D:01"}
f3b = {"D091:R:01", "D121:D:01", "D121:D:02", "D122:D:01", "D122:D:02"}
assert len(f3a | f3b) == 9 and not ((f3a | f3b) & f2_keys)
for i in f3a:
    assert actual[i]["relationship_class"] == "RC10"
for i in f3b:
    assert actual[i]["relationship_class"] == "RC11"

fields = [
    "f1_edge_id",
    "derived_row",
    "source_type",
    "source_id",
    "relationship_class",
    "stage2_boundary",
    "f3c_disposition",
    "evidence_and_scope",
]
summary = Counter()
classes: dict[str, Counter[str]] = {}
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for a in f1:
        eid = a["edge_id"]
        if a["source_type"] == "NONE":
            status = "ZERO_EDGE_SENTINEL_NO_DEPENDENCY"
            evidence = "F1 D007 zero-dependency row; not a public runtime proof"
        elif eid in f3a:
            status = "F3A_BOUNDED_PUBLIC_PROOF"
            evidence = (
                "test_m01_f3_contract_graph.py; test_m01_stage1_predecessor_scope.py "
                "(19 focused tests); D109/D170 contract identity and lineage"
            )
        elif eid in f3b:
            status = "F3B_BOUNDED_PUBLIC_PROOF"
            evidence = (
                "test_m01_f3_grouped_public.py (16 focused tests); D121/D122 grouping "
                "and D091 delta across multiple contracts"
            )
        elif eid in f2_keys:
            status = "F2_ACCEPTED_SCOPED_EVIDENCE"
            evidence = (
                "F2_EDGE_RECONCILIATION.csv; reviewer F2_ACCEPTED; "
                "other class edges still require proof"
            )
        elif a["stage2_boundary"] != "STAGE1_CLOSED":
            status = "STAGE2_BOUNDARY_DEFERRED"
            evidence = (
                "ExecPlan 144 closed/30 cross-stage rows; "
                "own Stage1 kernel proof still required at F4"
            )
        else:
            status = "F4_OUTSTANDING_RELATIONSHIP_PROOF"
            evidence = (
                "Unreconciled at F3; prior kernel tests alone do not establish "
                "this exact public join"
            )
        summary[status] += 1
        classes.setdefault(a["relationship_class"], Counter())[status] += 1
        w.writerow(
            dict(
                f1_edge_id=eid,
                derived_row=a["derived_id"],
                source_type=a["source_type"],
                source_id=a["source_id"],
                relationship_class=a["relationship_class"],
                stage2_boundary=a["stage2_boundary"],
                f3c_disposition=status,
                evidence_and_scope=evidence,
            )
        )
assert sum(summary.values()) == 489
assert summary["F3A_BOUNDED_PUBLIC_PROOF"] == 4
assert summary["F3B_BOUNDED_PUBLIC_PROOF"] == 5
assert summary["F2_ACCEPTED_SCOPED_EVIDENCE"] == 18
assert summary["ZERO_EDGE_SENTINEL_NO_DEPENDENCY"] == 1
assert len(classes) == 21
result = {
    "f1_authoritative_edges": 488,
    "f1_zero_edge_sentinel": 1,
    "stage1_rows": 174,
    "stage1_closed_rows": 144,
    "stage2_deferred_rows": 30,
    "f2_accepted_scoped_edges": 18,
    "f3_a_contract_edges": 4,
    "f3_b_grouped_edges": 5,
    "statuses": dict(sorted(summary.items())),
    "classes": {key: dict(sorted(value.items())) for key, value in sorted(classes.items())},
    "boundary": "Evidence accounting is not proof of all edges; remaining F4 obligations explicit",
}
CLASSES_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("F3c PASS: F1 488 edges + 1 sentinel, F2 18, F3a 4, F3b 5, no overlaps, 21 classes")
print("F3c remaining:", dict(sorted(summary.items())))
