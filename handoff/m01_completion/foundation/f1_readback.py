#!/usr/bin/env python3
"""Independent, fail-closed comparison of F1 outputs against original CSV bytes.

Does not import either F1 census or F1 classification scripts. JSON is evidence only.
"""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
SOURCE=ROOT/"handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv"
HASH="8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a"

def records(path):
    with path.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def split(s):return tuple(x for x in (z.strip() for z in s.split(";")) if x)
def yes_stage(kernel):return bool(re.fullmatch(r"K(?:0[1-8]|16|17)_[A-Z_]+",kernel))
def main():
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=HASH:
        raise SystemExit("BLOCKED: accepted catalogue bytes differ")
    src=records(SOURCE)
    row_census=records(OUT/"F1_AUTHORITY_ROW_CENSUS.csv")
    edge_census=records(OUT/"F1_AUTHORITY_RELATIONSHIP_CENSUS.csv")
    cls=records(OUT/"F1_CLASSIFIED_EDGE_MAP.csv")
    sr={r["derived_id"]:r for r in src}
    # Independently derive the expected exact edge triples and zero-dependency rows.
    expected=set()
    for row in src:
        if not yes_stage(row["kernel_id"]):continue
        did=row["derived_id"]
        raws=split(row["raw_dependencies"]); ds=split(row["derived_dependencies"])
        if not raws and not ds:expected.add((did,"NONE","N/A",0))
        for j,v in enumerate(raws,1):expected.add((did,"R",v,j))
        for j,v in enumerate(ds,1):expected.add((did,"D",v,j))
    actual={(r["derived_id"],r["source_type"],r["source_id"],int(r["dependency_ordinal"])) for r in edge_census}
    classified={(r["derived_id"],r["source_type"],r["source_id"],int(r["dependency_ordinal"])) for r in cls}
    duplicate_source=len(actual)!=len(edge_census)
    duplicate_class=len(classified)!=len(cls)
    srcids={r["derived_id"] for r in src if yes_stage(r["kernel_id"])}
    outids={r["derived_id"] for r in row_census}
    bad_row_fields=[]
    for r in row_census:
        s=sr.get(r["derived_id"])
        if s is None or any(r[field]!=s[field] for field in ("raw_dependencies","derived_dependencies","kernel_id","typed_contexts","parameter_profiles","brief_rule_ref","workbook_row")):
            bad_row_fields.append(r["derived_id"])
    bad_class=[e["edge_id"] for e in cls if not re.fullmatch(r"RC\d{2}",e["relationship_class"])]
    bad_class_ids=[e["edge_id"] for e in cls if e["edge_id"]!=f"{e['derived_id']}:{e['source_type']}:{int(e['dependency_ordinal']):02d}"]
    # Independent iterative closure (no recursive F1a algorithm).
    stage2={r["derived_id"] for r in src if not yes_stage(r["kernel_id"])}
    anystage=set(stage2)
    while True:
        additional={r["derived_id"] for r in src if any(d in anystage for d in split(r["derived_dependencies"]))}
        new=anystage|additional
        if new==anystage:break
        anystage=new
    direct={r["derived_id"] for r in src if yes_stage(r["kernel_id"]) and any(d in stage2 for d in split(r["derived_dependencies"]))}
    trans={r["derived_id"] for r in src if yes_stage(r["kernel_id"]) and r["derived_id"] in anystage}-direct
    statuses={r["derived_id"]:r["stage2_boundary"] for r in row_census}
    bad_stages=[did for did in srcids if statuses.get(did)!=("CROSS_STAGE_DIRECT" if did in direct else "CROSS_STAGE_TRANSITIVE" if did in trans else "STAGE1_CLOSED")]
    findings={
        "authority_sha256":HASH,
        "independent_expected_row_count":len(srcids),
        "independent_expected_raw_edges":sum(x[1]=="R" for x in expected),
        "independent_expected_derived_edges":sum(x[1]=="D" for x in expected),
        "independent_expected_zero_edge_sentinels":sum(x[1]=="NONE" for x in expected),
        "independent_expected_direct_stage2_rows":len(direct),
        "independent_expected_transitive_only_stage2_rows":len(trans),
        "missing":sorted([":".join(map(str,v)) for v in expected-actual]),
        "extra":sorted([":".join(map(str,v)) for v in actual-expected]),
        "classification_missing":sorted([":".join(map(str,v)) for v in expected-classified]),
        "classification_extra":sorted([":".join(map(str,v)) for v in classified-expected]),
        "row_ids_missing":sorted(srcids-outids),
        "row_ids_extra":sorted(outids-srcids),
        "mismatched_row_authority_fields":sorted(bad_row_fields),
        "wrong_stage2_boundaries":sorted(bad_stages),
        "unclassified_edge_ids":sorted(bad_class),
        "bad_class_edge_ids":sorted(bad_class_ids),
        "duplicate_edges":duplicate_source,
        "duplicate_classifications":duplicate_class,
        "observed_cardinality_UNKNOWN":sum(r["cardinality"]=="UNKNOWN" for r in cls),
        "observed_proof_NOT_PER_EDGE_PROVED":sum(r["proof_status"]=="NOT_PER_EDGE_PROVED" for r in cls),
        "class_population":dict(sorted(Counter(r["relationship_class"] for r in cls).items())),
    }
    print(json.dumps(findings,indent=2,sort_keys=True))
    (OUT/"F1_SET_DIFFERENCE.json").write_text(json.dumps(findings,indent=2,sort_keys=True)+"\n")
    blockers=[k for k in ("missing","extra","classification_missing","classification_extra",
        "row_ids_missing","row_ids_extra","mismatched_row_authority_fields",
        "wrong_stage2_boundaries","unclassified_edge_ids","bad_class_edge_ids")
        if findings[k]]
    if blockers or duplicate_source or duplicate_class:
        raise SystemExit("BLOCKED: "+",".join(blockers))
if __name__=="__main__":main()
