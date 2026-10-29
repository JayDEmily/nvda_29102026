# ruff: noqa: E501,RUF001
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from artifact_tool import Blob, SpreadsheetFile

repo = Path(__file__).resolve().parents[4]
a = repo / "handoff/m01_completion/authority"
o = repo / "handoff/m01_completion/proof/f4_20261012_source_preflight"
rows = list(csv.DictReader((a / "NVDA_DERIVED_SIGNAL_CATALOGUE.csv").read_text().splitlines()))
f1 = {
    r["derived_id"]: r
    for r in csv.DictReader(
        (repo / "handoff/m01_completion/foundation/F1_AUTHORITY_ROW_CENSUS.csv")
        .read_text()
        .splitlines()
    )
}
w = SpreadsheetFile.import_xlsx(
    Blob.load(a / "NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx")
)
raw = {
    str(row[0]): row
    for row in w.worksheets.get_item("Raw Signals").get_range("A5:Q327").values
    if isinstance(row[0], str) and row[0].startswith("R")
}
for id in ["R041", "R044", "R047", "R048", "R075", "R187", "R188", "R189", "R190"]:
    print(id, raw[id][2], raw[id][6], raw[id][7], raw[id][11])
inspected = []
for r in rows:
    id = r["derived_id"]
    if id not in f1:
        continue
    f = f1[id]
    deps = [x for x in r["raw_dependencies"].split(";") if x]
    d = [x for x in r["derived_dependencies"].split(";") if x]
    missing = [x for x in deps if x not in raw]
    if missing:
        raise AssertionError((id, missing))

    mismatch = (
        set(deps) != set(x for x in f["raw_dependencies"].split(";") if x)
        or set(d) != set(x for x in f["derived_dependencies"].split(";") if x)
        or r["kernel_id"] != f["kernel_id"]
    )
    if mismatch and not (
        id == "D116"
        and f["raw_dependencies"] == "R041;R075"
        and r["raw_dependencies"] == "R041;R047;R048"
        and r["kernel_id"] == f["kernel_id"]
        and r["derived_dependencies"] == f["derived_dependencies"]
    ):
        raise AssertionError((id, "UNAUTHORISED F1-CATALOGUE MISMATCH"))
    flags = []
    if id == "D116":
        flags.append("EXPECTED_F1_HISTORICAL_DELTA_AUTHORISATION_20261011")
    if id == "D104":
        flags.append("AUTHORISED_CORRECTION_REPAIRED_FOCUSED_PUBLIC_GREEN")
    if id == "D117":
        flags.append("SUSPECTED_SOURCE_ROLE_DISCREPANCY_R075_DECLARED_NOT_NUMERICALLY_CONSUMED")
    if id == "D123":
        flags.append("LIVE_OFFICIAL_PERIOD_MAPPING_UNVERIFIED_PROVIDER_INDEPENDENT_PROOF_ONLY")
    if id == "D186":
        flags.append("VERIFIED_TYPED_CONTEXT_AND_PARAMETER_REPRESENTATION_DEFECT")
    if id == "D178":
        flags.append("VERIFIED_PREDECESSOR_BOUND_NOT_APPLIED")
    if id == "D189":
        flags.append("VERIFIED_D175_RISK_CLIP_NOT_APPLIED")
    if id == "D192":
        flags.append("VERIFIED_D175_BREACH_PRECONDITION_NOT_APPLIED")
    if id == "D138":
        flags.append("L2_EVENT_STATE_SEMANTICS_REQUIRE_SEPARATE_SOURCE_CONTRACT_REVIEW")
    if f["stage2_boundary"] != "STAGE1_CLOSED":
        flags.append("CROSS_STAGE_KERNEL_AND_PUBLIC_REFUSAL_PROOF_INCOMPLETE")
    inspected.append(
        dict(
            derived_id=id,
            accepted_rule=r["brief_rule_ref"],
            source_workbook_row=r["workbook_row"],
            kernel=r["kernel_id"],
            raw_ids=";".join(deps),
            raw_source_meanings=" | ".join(f"{x}:{raw[x][2]!s}" for x in deps),
            derived_ids=";".join(d),
            stage1_boundary=f["stage2_boundary"],
            profile=r["parameter_profiles"],
            contexts=r["typed_contexts"],
            window=r["parameter_window"],
            units=r["units"],
            source_cadence=r["update_cadence"],
            calculation_concept=r["calculation_concept"],
            catalogue_vs_f1=("AUTHORISED_D116_20261011_DELTA" if id == "D116" else "EXACT"),
            raw_ids_workbook="ALL_PRESENT",
            preflight_flags=";".join(flags)
            or "NO_DISCREPANCY_IDENTIFIED_IN_STRUCTURAL_SOURCE_SURVEY",
            independent_full_row_semantic_proof="NOT_ESTABLISHED_BY_THIS_READ_ONLY_PREFLIGHT",
        )
    )
assert len(inspected) == 174
out = o / "STAGE1_174_ROW_SOURCE_MEANING_SURVEY.csv"
with open(out, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(inspected[0]))
    writer.writeheader()
    writer.writerows(inspected)
counts = Counter(x["stage1_boundary"] for x in inspected)
assert (
    counts["STAGE1_CLOSED"] == 144
    and sum(v for k, v in counts.items() if k != "STAGE1_CLOSED") == 30
)
register = """# M01 F4 — bounded source-semantic preflight and discrepancy register

Date: 12-10-2026. Status: **READ-ONLY PREFLIGHT, NOT AN INDEPENDENT ACCEPTANCE VERDICT**.

## Survey basis and method

The companion CSV explicitly records all **174 Stage-1 calculation rows** from the accepted `NVDA_DERIVED_SIGNAL_CATALOGUE.csv` with kernel, raw and derived dependencies, source-workbook row, raw provider field *human meaning*, accepted rule references, profiles, contexts, window, output units, update cadence, calculation concept and Stage-2 reachability. Its source semantics derive from `authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, `Raw Signals` tab. The F1 inventory and current catalogue were checked for kernel and dependency consistency across all 174, with the exact historically frozen F1 D116 dependency delta specifically allowed by the programme-owner D116 correction, and all declared raw IDs resolve in the workbook. These are mechanical structural checks, **not proof that every accepted mathematical rule or live-provider contract is valid**. Accepted numerical rules require discriminating public tests; a lack of observed discrepancy here is not a claim of exhaustive correctness.

The survey also inspected `_stage1.py`, `api.py`, the D104/D116/D123 authorised addenda, and the F4 relationship ledger. The following findings retain separate evidentiary dispositions rather than being collapsed into a single defect claim.

## Consolidated discrepancy register

| Ref | Class | Scope and source evidence | Required disposition / boundary |
| --- | --- | --- | --- |
| PF-01 | VERIFIED historical implementation defect, **repaired with focused public proof** | D104, catalogue derived deps `D099;D100`; prior mixed-family K03 selector in Git parent `40bddf2`; owner clarification `authority/D104_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261012.md`; `test_m01_f4_d104_owner_rule.py`. | Correct difference-of-differences, exact family history and lineage now covered by 10 focused tests; broader final acceptance still separately required. |
| PF-02 | MISSING/UNVERIFIED LIVE SOURCE CONTRACT (not provider-independent calculation blocker) | D123 uses R047/R048. Accepted D123 addendum documents controlled official-period ordinal and revision precedence. Workbook specifies IBKR `tickSize` tick 27/28 but does not document native official reporting-period identity/revision ordering. | Real IBKR/OCC integration unverified. M01 must fail closed without source-specific official period metadata; controlled M00 provider-independent proof remains distinct. |
| PF-03 | INFERENCE / SUSPECTED SOURCE ROLE DISCREPANCY, investigation required | D117 catalogue declares R041 and R075 (Average Option Volume); `_stage1.py` `_eval_k04` source dispatch explicitly selects R041, not R075 for numerical z-score. Accepted brief §5 K04 specifies matching historical baseline and D117 use of z-score, without establishing R075's independent numerical role. Owner's D116 addendum says D117 legitimately depends on R075. | **Do not** remove or reinterpret R075 or change D117. Clarify whether R075 is a required nonnumerical baseline qualifier/source contract or whether the accepted calculation requires a separate numerical role; not classified as a verified normative inconsistency. |
| PF-04 | INFERENCE / SOURCE CONTRACT REQUIRES INVESTIGATION | D138 declares R188/R189/R190 and D011; native `updateMktDepthL2` source carries event operation R187 and row state. `_stage1.py` D138 slope implementation computes per-side OLS over selected displayed row prices/sizes, without itself replaying R187 operations. Accepted §5 K06 requires cumulative displayed depth versus distance from D011. | Investigate whether admitted upstream M00 projection guarantees co-temporal complete depth states for these three fields. Do not assume event ticks constitute full depth snapshots or change D138 normativity without authority. |
| PF-05 | INCOMPLETE PROOF COVERAGE, not an established calculation defect | 30 cross-stage Stage-1 rows enumerated exactly in `EXEC_PLAN.md` Stage-1 boundary and F1 inventory, comprising 25 direct and five transitive Stage-2 dependencies. Stage-2 predecessors deliberately unavailable through public M00-to-M01 graph. | Individual own-kernel and lawful public-refusal proofs still require row/class-specific discrimination. Direct controlled predecessor tests do not count as public reachability and cannot assert live Stage-2 integration. |
| PF-06 | NO IDENTIFIED DISCREPANCY IN STRUCTURAL SURVEY; semantic certification NOT claimed | All 174 rows have exactly the F1-declared raw/derived sets and kernel and all referenced raw IDs resolve in source workbook; the sole F1-current-catalogue raw dependency mismatch is the authorised D116 R075 -> R047/R048 correction; see 174-row CSV. | Continue F4 independent numerical, temporal, lineage, contextual, version and public-interface proof on actual row classes; do not treat column presence as acceptance. |
| PF-07 | VERIFIED AUTHORISED HISTORICAL F1 DELTA, **not a current normative defect** | F1 original D116 raw set `R041;R075` versus current normative D116 raw set `R041;R047;R048`, explicitly authorised 11-10-2026, recorded `authority/D116_CALCULATION_DEFINITION_AUTHORISED_CORRECTION_20261011.md`. | Historical F1 census is not silently rewritten; the current catalogue with authorised D116 correction governs. |

| PF-08 | VERIFIED IMPLEMENTATION / ADMITTED PARAMETER-CONTRACT MISMATCH, **mandatory unresolved invariant** | D186 accepted §5 K08 requires entry-state D155 occurrence `EntryStateContextV1.d155_occurrence_id`, and versioned P_RULE feature weights/scales. `_stage1.py` D186 instead reads nonexistent `entry.entry_state_vector` and expects `similarity_weights/scales` named pairs; `api.py` `CalculationParameterSetV1` admits only a flat tuple of immutable scalars, refusing nested named pairs. `test_m01_f4_cross_stage_d186_entry_anchor.py` is RED at parameter admission. | Specify an admissible immutable named feature weight/scale representation and resolve entry state using the existing exact D155 occurrence ID; proof-first repair after authority. No fabricated entry-state payload and no blanket parameter-interface broadening. |
| PF-09 | VERIFIED IMPLEMENTATION RULE-DEPENDENCY NONUSE; parameterisation incomplete | D178 accepted brief §5 K08 requires allowed price-cost bound by fresh D133 and D177 edge reserve; `_stage1.py` D178 reads only R034/R035 and `allowed_execution_cost_per_unit`/side and does not evaluate its declared D133/D177 predecessors. | Establish exact versioned cost/edge reserve scaling and bound before claiming its Stage-1 own-kernel semantics. Existing numerical buy-price test is **partial** proof only. |
| PF-10 | VERIFIED IMPLEMENTATION RULE-DEPENDENCY NONUSE; unit-conversion contract unresolved | D189 accepted brief §5 K08 says target-band adjustments must be clipped against D175 active risk limits; `_stage1.py` D189 reads D181–D184 but does not use D175 or a conversion from Greek exposure adjustment to currency risk. | Establish an authorised, exact risk-bound / exposure conversion before claiming full D189 proof. The current band-midpoint arithmetic alone is insufficient. |
| PF-11 | VERIFIED IMPLEMENTATION RULE-PRECONDITION NONUSE; risk-breach contract unresolved | D192 accepted brief §5 K08 orders mandatory hedge **when D175 is breached**; `_stage1.py` D192 hedges when a flag and D189 nonzero hedge exist without evaluating D175 breach. | Establish an exact breach predicate under the typed contexts/declared predecessors; do not invent one or claim complete action-precedence proof from the present numerical test. |

## Limitations and authority

This preflight is strictly read-only as to normative authority and production implementation. The D104 semantic amendment was separately authorised and committed before this survey. No new provider-native field mappings, source reporting identifiers or Stage-2 mathematics have been invented. Findings PF-03/PF-04 are explicitly not proven defects and do not authorise unrelated corrections. The current D104 production repairs are separate from this preflight.
"""
(o / "SOURCE_SEMANTIC_PREFLIGHT_DISCREPANCY_REGISTER.md").write_text(register)
receipt = dict(
    stage1=174,
    closed=144,
    cross=30,
    raw_ids_count=len(raw),
    catalogue_sha256=hashlib.sha256(
        (a / "NVDA_DERIVED_SIGNAL_CATALOGUE.csv").read_bytes()
    ).hexdigest(),
    survey_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
    preflight_status="READ_ONLY_NOT_ACCEPTANCE",
)
(o / "PREFLIGHT_READBACK.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
