"""Reconcile F2's scoped edge evidence against the frozen F1 catalogue census.

Run from any directory with Python 3.13+: python <this script path>.
This is an evidence verifier, not a new source of domain authority.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
M01 = HERE.parents[1]
F1 = M01 / "foundation" / "F1_CLASSIFIED_EDGE_MAP.csv"
F2 = HERE.parent / "f2_observation_identity_20261009" / "F2_EDGE_RECONCILIATION.csv"
EXPECTED = HERE / "F2_CENSUS_READBACK.json"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


f1 = read(F1)
f2 = read(F2)
f1_edges = {row["edge_id"]: row for row in f1 if row["source_type"] in ("R", "D")}
f2_ids = [row["f1_edge_id"] for row in f2]
assert len(f1_edges) == 488, f"Unexpected F1 dependency-edge count: {len(f1_edges)}"
assert len(f2) == 18 and len(set(f2_ids)) == 18, "F2 evidence missing/duplicated"
assert not (set(f2_ids) - set(f1_edges)), "F2 evidence contains non-authoritative edge"
for entry in f2:
    authority = f1_edges[entry["f1_edge_id"]]
    keys = ("derived_row", "source_type", "source_id", "relationship_class")
    actual = tuple(entry[k] for k in keys)
    expected = tuple(authority[k] for k in ("derived_id", "source_type", "source_id", "relationship_class"))
    assert actual == expected, (entry["f1_edge_id"], actual, expected)
    assert entry["f2_observed_status"].startswith("SUPPORTED_FOR_"), entry
result = json.loads(EXPECTED.read_text(encoding="utf-8"))
assert result["authoritative_f1_edges"] == len(f1_edges)
assert result["f2_scoped_edges"] == len(f2)
assert result["f2_counts_by_class"] == dict(sorted(Counter(r["relationship_class"] for r in f2).items()))
print("PASS: F1 488 authoritative edges; all 18 F2 IDs uniquely resolve and classes/status agree")
print("Scope: RC01, RC07, RC08, RC09, RC21; no assertion of whole-F1 class acceptance")
