#!/usr/bin/env python3
"""F1b secondary, nonnormative relationship annotations over F1a exact edge census.

Unknown detail stays UNKNOWN; never extrapolate a join key from a Python dictionary key.
"""
from __future__ import annotations
import csv
from pathlib import Path
from collections import Counter
from f1_census import calculate, write_csv

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
KERNELS={
 "K01_TIME":"RC01",
 "K02_ALGEBRA":"RC02",
 "K03_CHANGE_RETURN":"RC03",
 "K04_STANDARDISE_RANK":"RC04",
 "K05_REALIZED_RISK":"RC04",
 "K06_REGRESSION_DEPENDENCE":"RC05",
 "K07_WEIGHTED_SCORE":"RC06",
 "K08_RULE_BUCKET_POLICY":"RC11",
 "K16_STRUCTURED_ASSEMBLY":"RC17",
 "K17_ORDER_FLOW_IMBALANCE":"RC12",
}
SPECIAL={
 "RC01": {"D001","D002","D003","D004","D005","D006","D008","D010","D062","D065","D085","D086","D209"},
 "RC05": {"D078","D079","D080","D081","D082"},
 "RC07": {"D015"},
 "RC08": {"D016","D120"},
 "RC09": {"D017"},
 "RC10": {"D109","D170"},
 "RC11": {"D091","D121","D122","D124","D128"},
 "RC12": {"D131","D134","D135","D136","D137","D138","D139","D140","D141","D142","D143","D144","D145"},
 "RC13": {"D071","D072","D073","D074","D075","D076","D077","D083","D151"},
 "RC14": {"D087","D088","D089","D090","D092","D093","D094","D095","D097","D098","D099","D100","D101","D103","D104","D105","D106","D107","D108","D110","D116","D117","D118","D119"},
 "RC15": {"D164","D166","D167","D168","D171","D172","D173","D175","D176","D178","D190"},
 "RC16": {"D179","D180","D181","D182","D183","D184","D185","D187","D189","D191","D192","D193","D199","D200"},
 "RC17": {"D155","D156","D157","D158","D159","D163","D186"},
 "RC19": {"D207","D208"},
 "RC20": {"D009"},
 "RC21": {"D063","D064","D146","D147","D148","D149","D150"},
}
# Every override belongs to exactly one row-specific class.
assert len([d for s in SPECIAL.values() for d in s])==len(set().union(*SPECIAL.values()))
CLASS={
"RC01":("Temporal/event/expiry selection","UNKNOWN","event/receipt kind; subject where material; exchange calendar/expiry where declared","event/receipt basis, UTC/local conversion; cutoff; no invented event instant","per-event or as-of selection; D006/D008 require score/time alignment","api.py _materialise/_raw_values; _stage1.py _eval_k01/_eval_k07/_eval_k08","§5 K01; §§8.1,11"),
"RC02":("Exact same-subject algebraic inputs","UNKNOWN","canonical subject; exact contract when option input; versions","as-of eligible latest; freshness/skew; cutoff","point/snapshot values not inferred equivalent across different observation IDs","api.py _raw_values/_materialise; _stage1.py _eval_k02","§5 K02; §§8.1,13"),
"RC03":("Same-subject history and matched time anchor","many-to-one","subject; anchor/window version; ordered observations","strict historical anchor; no look-ahead or nearest substitution","history points to one output window; multiple time points mandatory where specified","_stage1.py _history_anchor/_eval_k03; api.py _materialise","§5 K03; §§8,8.1"),
"RC04":("Historical baseline / realised-risk window","many-to-one","subject/contract if material; exact versioned baseline/window","strictly prior baseline or exact sampling window","multiple eligible samples -> one result; refuse short/inconsistent sample sets","_stage1.py _eval_k04/_eval_k05; api.py _compatible_history","§5 K04/K05; §§8,8.1"),
"RC05":("Regression/dependence aligned input history","many-to-one","model version; aligned subject basket/factor series; window","synchronised history and matched returns under cutoff","aligned feature/response pairs/matrix, exact model input identity","_stage1.py _factor_rows/_eval_k06; api.py _materialise","§5 K06; §§8,13"),
"RC06":("Versioned multi-feature weighted scoring","many-to-one","exact feature identities/extractors; parameter/context versions","eligible aligned feature timestamps and required baseline where used","all required features and extractors; no silent weight renormalisation","_stage1.py extract_scalar/_score/_eval_k07; api.py _materialise","§5 K07; §§6,13"),
"RC07":("Trade event to eligible quote and tick sign","UNKNOWN","same trade subject/contract; R120 source event; R126/R127 and D011 quote temporal match","quote timestamp/cutoff; prior distinct trade for tick test","one signed classification *of trade* with quote; quote-to-trade matching cardinality not explicitly numbered","_stage1.py _eval_k08 D015; api.py _materialise","§5 K08 D015; §§8.1,12,13"),
"RC08":("Per-trade signed quantity/notional correlation","many-to-one","same individual R120/R121 trade, contract, multiplier and D015's ultimate M00 observation lineage; never D-raw ID equality","selected trade window; no forward classification; cutoff","many exact signed trade facts -> one sum; missing match cannot silently become zero","_stage1.py _eval_k08 D016/D120; api.py _occurrence_kernel_value/_materialise","§5 K08 D015/D016/D120; §§8.1,9,12–14,17"),
"RC09":("Per-observation trade price/size VWAP aggregation","many-to-one","same M00 trade occurrence for R120 and R121; subject; session/window","session window, cutoff, ordered trade observations","many price*size pairs -> one VWAP; requires matching source observations","_stage1.py _align_occurrence_fields/_eval_k02 D017","§5 K02 D017; §§8.1,9,12"),
"RC10":("Exact per-contract predecessor within multi-leg/pair parent","one-to-many","D109 distinct call/put same strike+expiry; D170 candidate leg's exact contract; scoped child policy","same as-of and cutoff with scoped child policy","one parent may require several distinct D087/D091 child occurrences","api.py _scoped_contract_requests/_materialise; _stage1.py _eval_k02 D109/D170","§5 K02 D109/D170; §6 CandidateStructureContext; §§8.1,13"),
"RC11":("Versioned bucket/group membership and aggregation","many-to-one","exact delta/expiry/strike/member; per-contract D120/D091/D085 membership; P_RULE boundaries","same qualifying window and cutoff; each source's own contract/time identity","grouped sums by declared bucket; D091 scalar bucket has single input; class cardinality conditional","_stage1.py _eval_k08 D091/D121/D122/D124/D128; api.py _materialise","§5 K08 D091/D121/D122/D124/D128; §§6,8.1,13"),
"RC12":("Book-event reconstruction and quote/depth correlation","many-to-one","subject/option contract, venue, side, level, price, exact L2 events","sequence/operation/time window, pre/post state and cutoff","event stream -> reconstructed book and aggregate; where quote matching mandatory use compatible book state","_stage1.py reconstruct_book/_book_events/_eval_k02/_eval_k08/_eval_k17","§5 K02/K08 L2 and K17; §§8.1,9,12"),
"RC13":("Versioned multi-instrument basket and common-return factor alignment","many-to-one","exact subject per member; basket identity; coherent NVDA dependent and market/sector factors","matched cross-sectional snapshots/history by declared model/window","explicit member set and model response; no opportunistic member substitution","_stage1.py _latest_by_subject/_factor_rows/_eval_k06/_eval_k02","§5 K02/K03/K04/K06; §§6,8.1,13"),
"RC14":("Option-contract/delta/strike/expiry and IV geometry","UNKNOWN","exact underlying/contract/strike/right/expiry/delta bucket as applicable","window, cutoff and matched terms; no nearest strike unless permitted","multi-strike/delta right comparison where row explicitly demands; otherwise exact contract","_stage1.py _eval_k02/_eval_k03/_eval_k04; api.py _selection_policy_satisfies_row_authority","§5 K02/K03/K04; §§8.1,13"),
"RC15":("Candidate structure/leg/set/neighbour comparison","UNKNOWN","versioned CandidateStructureContext; CandidateSetContext identity/order/neighbour where bound; exact contract per leg","same candidate/model and as-of/cutoff","one candidate or eligible candidate set; explicit ordered membership; neighbour relation never inferred","api.py _contexts_for_row/_scoped_contract_requests; _stage1.py _eval_k02/_eval_k07/_eval_k08","§5 K02/K07/K08; §6; §§8.1,13"),
"RC16":("Live position, fill, execution or attribution state","UNKNOWN","exact position/order/fill M00 occurrence, signed quantities, multiplier and convention where admitted","same position snapshot or exact path/window and cutoff","matching executed quantity/path/position state; no aggregate Greek proxy for nonlinear repricing","_stage1.py _eval_k02/_eval_k08; api.py _contexts_for_row/_materialise","§5 K02/K08; §6; §§8.1,12,13"),
"RC17":("Structured component occurrence/state-vector comparison","many-to-one","D155 component occurrence IDs, units and schema version; D186 entry anchor; relevant model context","same aligned time/window; entry occurrence explicitly versioned","ordered named D components into vector; matrices/score consume exactly named component occurrences","_stage1.py _eval_k16/_eval_k06/_eval_k07/_eval_k08","§5 K16/K07/K06/K08; §§6,12–13"),
"RC18":("Policy-only D007 (zero R/D dependencies)","N/A","RequiredFieldPolicy version and requirement identity","available policy/read eligibility under cutoff","policy requirement completeness, no R/D edge in catalogue","_stage1.py _eval_k08 D007; api.py _contexts_for_row","§4 D007; §5 K08; §6"),
"RC19":("Evaluation/disposition from named model evidence","UNKNOWN","EvaluationSet identity/version and class/feature extractor where required","evaluation historical window/knowledge cutoff","fixed evidence vector and threshold classification; cross-stage dependent D203/D206/D202 deferred","_stage1.py _eval_k07/_eval_k08; api.py _materialise","§5 K07/K08; §§6,13"),
"RC20":("Macro observation revision and vintage tracking","UNKNOWN","same macro series, release/revision/vintage identity","as-of visibility and receipt vs release/period distinction","related raw revision fields; latest known vintage not invented","_stage1.py _eval_k01 D009; api.py _raw_values","§5 K01 D009; §§8.1,11"),
"RC21":("Versioned macro-event/factor score association","UNKNOWN","same released series/event or declared score feature/model ID","release/surprise as-of cutoff; aligned named series as required","event series to surprise/factor and versioned extractor","_stage1.py _eval_k04/_eval_k07; api.py _materialise","§5 K04/K07; §§6,8,8.1"),
}
def choice(e):
    if e["source_type"]=="NONE": return "RC18"
    d=e["derived_id"]
    for c, ds in SPECIAL.items():
        if d in ds: return c
    return KERNELS[e["kernel_id"]]

def main():
    rows,edges,summary=calculate()
    output=[]
    for e in edges:
        cid=choice(e)
        label,card,identity,timebasis,correlation,mechanism,ref=CLASS[cid]
        rec=dict(e)
        rec.update(
            relationship_class=cid,relationship_label=label,
            cardinality=card,identity_dimensions=identity,correlation_basis=correlation,
            time_basis=timebasis,lineage_rule=(
                "N/A: policy-only row" if e["source_type"]=="NONE" else
                "M00 raw observation ID + exact field mapping and unit convention refs" if e["source_type"]=="R" else
                "Dxxx opaque occurrence ID + direct predecessor and inherited ultimate M00 lineage"
            ),
            mandatory_versions=e["parameter_profiles"]+" | "+(e["typed_contexts"] or "no row-specific typed context")+
                " | request calculation-definition, InputSelectionPolicyVersion, mapping/unit versions",
            implementation_mechanism=mechanism,authority_rule=ref+"; catalogue "+e["derived_id"]+"/"+e["source_id"],
            proof_status="KNOWN_PUBLIC_FAILURE" if e["derived_id"] in {"D016","D120"} else
            "INDEPENDENT_GROUP_PATH_UNASSESSED" if e["derived_id"] in {"D121","D122"} else
            "STAGE2_GRAPH_DEFERRED" if e["source_type"]=="D" and e["predecessor_kernel"] not in ("N/A",) and not e["predecessor_kernel"].startswith(("K01_","K02_","K03_","K04_","K05_","K06_","K07_","K08_","K16_","K17_")) else
            "NOT_PER_EDGE_PROVED",
            )
        # D091 is one delta value to one bucket; D128 is grouped rather than single.
        if e["derived_id"]=="D091": rec["cardinality"]="one-to-one"
        if e["derived_id"] in {"D121","D122"}: rec["cardinality"]="many-to-one"
        if e["derived_id"]=="D007": rec["cardinality"]="N/A"
        if e["derived_id"]=="D015" and e["source_id"]=="R120": rec["cardinality"]="one-to-one"
        if e["derived_id"]=="D109" and e["source_id"]=="D091": rec["cardinality"]="UNKNOWN" # bucket selection relation
        if e["derived_id"]=="D170" and e["source_type"]=="R": rec["cardinality"]="UNKNOWN" # spot raw field to candidate legs
        output.append(rec)
    if any(e["relationship_class"] not in CLASS for e in output):
        raise SystemExit("unclassified relationship")
    write_csv(OUT/"F1_CLASSIFIED_EDGE_MAP.csv",output)
    print("classified records",len(output),"edge types",Counter(e["source_type"] for e in output))
    print("class counts",dict(sorted(Counter(e["relationship_class"] for e in output).items())))
if __name__=="__main__":main()
