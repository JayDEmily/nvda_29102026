#!/usr/bin/env python3
"""Evidence-only F1 authority graph census. Never writes or imports production code.

Source of truth: exact hash-bound CSV, not this script or output CSV.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv"
OUT = Path(__file__).resolve().parent
CAT_SHA = "8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a"
STAGE_RE = re.compile(r"^K(?:0[1-8]|16|17)_")
D_RE = re.compile(r"^D\d{3}$")
R_RE = re.compile(r"^R\d{3}$")

def split(value: str) -> list[str]:
    return [v.strip() for v in value.split(";") if v.strip()]

def calculate() -> tuple[list[dict[str, str]],list[dict[str, str]],dict]:
    if hashlib.sha256(CAT.read_bytes()).hexdigest() != CAT_SHA:
        raise SystemExit("BLOCKED: companion catalogue hash mismatch")
    with CAT.open(newline="", encoding="utf-8-sig") as handle:
        items = list(csv.DictReader(handle))
    ids = [r["derived_id"] for r in items]
    if len(items) != 209 or len(set(ids)) != 209:
        raise SystemExit("BLOCKED: noncanonical catalogue IDs/row multiplicity")
    row_by_id = {r["derived_id"]: r for r in items}
    if set(ids) != {f"D{i:03d}" for i in range(1, 210)}:
        raise SystemExit("BLOCKED: D001–D209 canonical set mismatch")
    for r in items:
        for d in split(r["derived_dependencies"]):
            if not D_RE.fullmatch(d) or d not in row_by_id:
                raise SystemExit(f"BLOCKED: broken D edge {r['derived_id']}->{d}")
        for raw in split(r["raw_dependencies"]):
            if not R_RE.fullmatch(raw):
                raise SystemExit(f"BLOCKED: malformed R edge {r['derived_id']}->{raw}")
    stage = [r for r in items if STAGE_RE.match(r["kernel_id"])]
    if len(stage) != 174:
        raise SystemExit(f"BLOCKED: stage1 row count {len(stage)} !=174")
    memo: dict[str,set[str]]={}
    def stage2_ancestors(d: str, stack: frozenset[str] = frozenset()) -> set[str]:
        if d in stack: raise SystemExit(f"BLOCKED: dependency cycle at {d}")
        if d in memo: return memo[d]
        out = {d} if not STAGE_RE.match(row_by_id[d]["kernel_id"]) else set()
        for pred in split(row_by_id[d]["derived_dependencies"]):
            out |= stage2_ancestors(pred,stack|{d})
        memo[d] = out
        return out
    result_rows=[]
    result_edges=[]
    for r in stage:
        did=r["derived_id"]
        rdeps=split(r["raw_dependencies"])
        ddeps=split(r["derived_dependencies"])
        direct_s2=[d for d in ddeps if not STAGE_RE.match(row_by_id[d]["kernel_id"])]
        ancestors=stage2_ancestors(did)
        state="CROSS_STAGE_DIRECT" if direct_s2 else "CROSS_STAGE_TRANSITIVE" if ancestors else "STAGE1_CLOSED"
        entry=dict(derived_id=did,workbook_row=r["workbook_row"],signal_name=r["derived_signal"],
            kernel_id=r["kernel_id"],parameter_profiles=r["parameter_profiles"],
            typed_contexts=r["typed_contexts"],parameter_window=r["parameter_window"],
            raw_dependencies=r["raw_dependencies"],derived_dependencies=r["derived_dependencies"],
            raw_count=str(len(rdeps)),derived_count=str(len(ddeps)),
            stage2_boundary=state,direct_stage2_predecessors=";".join(direct_s2),
            transitive_stage2_ancestors=";".join(sorted(ancestors)),
            brief_rule_ref=r["brief_rule_ref"],binding_note=r["binding_note"])
        result_rows.append(entry)
        edges=[("R",i,x) for i,x in enumerate(rdeps,1)]+[("D",i,x) for i,x in enumerate(ddeps,1)]
        if not edges: edges=[("NONE",0,"N/A")]
        for et,pos,dep in edges:
            result_edges.append(dict(edge_id=f"{did}:{et}:{pos:02}",derived_id=did,
                workbook_row=r["workbook_row"],source_type=et,source_id=dep,
                dependency_ordinal=str(pos),stage2_boundary=state,
                predecessor_kernel=row_by_id[dep]["kernel_id"] if et=="D" else "N/A",
                signal_name=r["derived_signal"],kernel_id=r["kernel_id"],
                raw_dependencies=r["raw_dependencies"],derived_dependencies=r["derived_dependencies"],
                parameter_profiles=r["parameter_profiles"],typed_contexts=r["typed_contexts"],
                parameter_window=r["parameter_window"],brief_rule_ref=r["brief_rule_ref"],
                relationship_class="UNCLASSIFIED",cardinality="UNKNOWN",
                identity_dimensions="UNKNOWN",correlation_basis="UNKNOWN",
                time_basis="UNKNOWN",lineage_rule="UNKNOWN",
                implementation_mechanism="UNMAPPED",proof_status="UNASSESSED"))
    counts=Counter(e["source_type"] for e in result_edges)
    summary={
        "catalogue_sha256":CAT_SHA,
        "source":"handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "stage1_rows":len(result_rows),"all_rows":len(items),
        "raw_edges":counts["R"],"derived_edges":counts["D"],
        "zero_edge_rows":counts["NONE"],
        "total_declared_edges":counts["R"]+counts["D"],
        "csv_edge_records_including_zero_dependency_sentinels":len(result_edges),
        "stage1_closed":sum(r["stage2_boundary"]=="STAGE1_CLOSED" for r in result_rows),
        "cross_stage_direct":sum(r["stage2_boundary"]=="CROSS_STAGE_DIRECT" for r in result_rows),
        "cross_stage_transitive_only":sum(r["stage2_boundary"]=="CROSS_STAGE_TRANSITIVE" for r in result_rows),
        "direct_stage2_edges":sum(len(split(r["direct_stage2_predecessors"])) for r in result_rows),
        "kernel_rows":dict(sorted(Counter(r["kernel_id"] for r in result_rows).items())),
        "stage1_row_ids":sorted(r["derived_id"] for r in result_rows),
        "cross_stage_direct_ids":[r["derived_id"] for r in result_rows if r["stage2_boundary"]=="CROSS_STAGE_DIRECT"],
        "cross_stage_transitive_only_ids":[r["derived_id"] for r in result_rows if r["stage2_boundary"]=="CROSS_STAGE_TRANSITIVE"],
        "zero_edge_ids":[r["derived_id"] for r in result_rows if r["raw_count"]=="0" and r["derived_count"]=="0"]
    }
    if (summary["stage1_closed"],summary["cross_stage_direct"],summary["cross_stage_transitive_only"]) != (144,25,5):
        raise SystemExit("BLOCKED: stage-boundary mismatch")
    return result_rows,result_edges,summary

def write_csv(path: Path, records: list[dict[str,str]]) -> None:
    with path.open("w",newline="",encoding="utf-8") as handle:
        w=csv.DictWriter(handle,fieldnames=list(records[0]))
        w.writeheader(); w.writerows(records)

def main()->None:
    rows,edges,summary=calculate()
    write_csv(OUT/"F1_AUTHORITY_ROW_CENSUS.csv", rows)
    write_csv(OUT/"F1_AUTHORITY_RELATIONSHIP_CENSUS.csv",edges)
    (OUT/"F1_COUNTS.json").write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print({k:v for k,v in summary.items() if isinstance(v,int)})

if __name__=="__main__":
    main()
