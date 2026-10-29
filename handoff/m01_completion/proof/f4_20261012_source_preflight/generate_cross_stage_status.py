"""Evidence-only, fail-closed cross-stage 30-row progress matrix."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
F1 = ROOT / "handoff/m01_completion/foundation/F1_AUTHORITY_ROW_CENSUS.csv"
DEST = Path(__file__).with_name("CROSS_STAGE_30_ROW_PROOF_STATUS.csv")

DIRECT = {
    "D097",
    "D098",
    "D107",
    "D108",
    "D157",
    "D158",
    "D159",
    "D163",
    "D171",
    "D172",
    "D187",
    "D200",
    "D207",
    "D128",
    "D166",
    "D175",
    "D176",
    "D178",
    "D189",
    "D191",
    "D199",
    "D208",
    "D164",
    "D155",
    "D156",
    "D167",
    "D190",
    "D192",
}
EXISTING = {"D173"}
PUBLIC_SMOKE = {"D097", "D098", "D107", "D108"}
SOURCE_RULE_ISSUES = {"D178", "D189", "D192"}
rows = []
for r in csv.DictReader(F1.open()):
    if r["stage2_boundary"] == "STAGE1_CLOSED":
        continue
    did = r["derived_id"]
    own = (
        "BLOCKED_ADMITTED_ENTRY_CONTEXT_AND_P_RULE_PARAMETER_SHAPE"
        if did == "D186"
        else "PARTIAL_ARITHMETIC_UNAPPLIED_RULE"
        if did in SOURCE_RULE_ISSUES
        else "BOUNDED_CONTROLLED_OWN_KERNEL_POSITIVE_AND_REFUSAL"
        if did in DIRECT
        else "EXISTING_CONTROLLED_DIRECT_K07_D173_NEIGHBOUR_PROOF"
        if did in EXISTING
        else "UNPROVED"
    )
    if did in DIRECT:
        if did in {"D097", "D098", "D107", "D108"}:
            f = "tests/product/derived_signal/test_m01_f4_cross_stage_k02_stage1_kernel.py"
        elif did in {"D157", "D158", "D159", "D163", "D171", "D172", "D187", "D200", "D207"}:
            f = "tests/product/derived_signal/test_m01_f4_cross_stage_k07_own_kernel.py"
        elif did in {"D155", "D156", "D167", "D190", "D192"}:
            f = "tests/product/derived_signal/test_m01_f4_cross_stage_remaining_own_kernel.py"
        else:
            f = "tests/product/derived_signal/test_m01_f4_cross_stage_rule_algebra_own_kernel.py"
    elif did == "D173":
        f = "tests/product/derived_signal/test_m01_stage1_leaf3_catalogue_kernels.py"
    else:
        f = "tests/product/derived_signal/test_m01_f4_cross_stage_d186_entry_anchor.py"
    rows.append(
        dict(
            derived_id=did,
            kernel=r["kernel_id"],
            boundary=r["stage2_boundary"],
            raw_dependencies=r["raw_dependencies"],
            derived_dependencies=r["derived_dependencies"],
            own_kernel_evidence=own,
            evidence_file=f,
            public_stage2_refusal=(
                "BOUNDARY_SMOKE_ONLY_NO_STAGE2_TRUTH"
                if did in PUBLIC_SMOKE
                else "NOT_DISCRIMINATINGLY_PROVED"
            ),
            acceptance="NOT_READY",
            note=(
                "Stage2 truth absent; synthetic predecessors do not prove "
                "public integration or live provider data"
            ),
        )
    )
assert len(rows) == 30 and set(x["derived_id"] for x in rows) == (DIRECT | EXISTING | {"D186"})
with DEST.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print("cross_rows=30 direct_new=28 existing_direct=1 blocked=1 public_partial=4 complete=0")
