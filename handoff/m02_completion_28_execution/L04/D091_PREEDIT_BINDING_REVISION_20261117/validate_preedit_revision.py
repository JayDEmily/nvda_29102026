"""Documentary only: exact D091 R1–R3 binding and existing proof-schema inspection.

Never imports M00/M02 source, invokes pytest or runs a product case.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = "handoff/m02_completion_28_execution"
PRE = ROOT / BASE / "L04/D091_PREEDIT_IMPLEMENTATION_BINDING_20261117"
PARENT = "19abd87934783eeddb2f4f9c18edf3beb3a708d1"

def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))
def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()
def check(condition: bool, key: str, out: dict) -> None:
    out["checks"][key] = bool(condition)
    if not condition:
        raise AssertionError(key)

def main() -> None:
    out: dict = {
        "status": "UNVERIFIED", "kind": "DOCUMENTARY_R1_R3_STATIC_VALIDATION",
        "product_tests_executed": 0, "product_code_imported": False,
        "checks": {}, "validator": "system Python jsonschema"
    }
    try:
        spec=load(HERE / "TECHNICAL_REPAIR_BINDING_V2.json")
        proof=load(HERE / "PRODUCT_PROOF_REGISTRATION_PROPOSAL.json")
        old=load(PRE / "PREEDIT_BINDING_PROPOSAL.json")
        schema=load(ROOT / "schemas/accepted_brief_product_proof.schema.json")
        jsonschema.validate(proof, schema)
        check(True, "registered_family_contract_matches_existing_json_schema", out)
        cases=old["owner_approved_case_allocations"]
        d=cases["D091_L04"]["physical_cases"]
        l=cases["L01b_R112"]["physical_cases"]
        check(len(d)==18 and len(l)==15 and len(set(x["case_id"] for x in d+l))==33, "18_plus_15_distinct_predecessor_cases", out)
        check(spec["admitted_jurisdictions"]["physical_case_ids"]==[x["case_id"] for x in d+l], "V2_preserves_all_33_original_case_ids", out)
        check(spec["unchanged_source_contract_sha256"]==old["raw_source"]["contract_utf8_sha256"],"R112_contract_identity_unchanged",out)
        check(spec["unchanged_positive_source_sha256"]==old["raw_source"]["positive_sha256"],"positive_15_source_identity_unchanged",out)
        check(len(spec["bound_request"]["fields"])==21 and len(set(row[0] for row in spec["bound_request"]["fields"]))==21,"request_exact_21_field_declaration",out)
        check(spec["bound_request"]["computed_readonly_property"]=="request_identity" and "init=False" in spec["bound_request"]["byte_roundtrip"],"read_only_property_no_codec_init_false",out)
        check(len(spec["bound_occurrence"]["fields"])==19 and len(set(row[0] for row in spec["bound_occurrence"]["fields"]))==19,"occurrence_exact_19_field_declaration",out)
        check(spec["bound_category"]["labels"]==[v["name"] for v in old["categorical_result"]["rule_profile"]["bins"]], "unchanged_five_bins",out)
        check(spec["bound_category"]["codec_tag_shape"]["t"]=="record" and spec["bound_category"]["codec_tag_shape"]["n"]=="D091CategoryV1","categorical_dataclass_record_codec_shape",out)
        check(spec["public_protocol"]["observer_event_fields"]==old["dto_and_public_interface_proposal"]["diagnostic_exact_five_field_order"],"five_field_observer_preserved",out)
        check(spec["public_protocol"]["diagnostic_stages"]==old["dto_and_public_interface_proposal"]["exact_diagnostic_stage_allowlist"],"seven_original_refusal_stages_preserved",out)
        check("calculated_at_utc" in spec["bound_occurrence"]["logical_id_noninputs"],"logical_ID_excludes_owner_clock",out)
        check(spec["bound_request"]["clock_source"].startswith("single owner.utc_now()"),"clock_owned_by_constructor",out)
        fault=spec["fault_path"]
        check(fault["D03"]["baseline_signed_decimal"]=="0.499" and fault["D03"]["test_corrupted_candidate_decimal"]=="0.498" and fault["D03"]["category"]=="ABS_25_50", "same_bucket_test_only_second_payload_candidate",out)
        check(fault["D01"]["real_event_order"][-2:] == ["outcome_uncertain=False","fresh reader no row"] and "outcome_uncertain=True" in fault["D02"]["real_event_order"],"commit_phase_D01_D02_oracles",out)
        check(fault["conditional_new_source_path_approval_required"] and spec["proof_registry"]["conditional_extra_changed_path_owner_approval_required"],"new_two_paths_marked_unapproved",out)
        check(spec["proof_registry"]["parent_physical_root"]=="tests/product/m02_completion_28","common_parent_physical_root",out)
        check([x["path"] for x in proof["families"]]==[old["proposed_changed_paths"]["test_files_before_source"][0],old["proposed_changed_paths"]["test_files_before_source"][1]],"two_separate_families_correct_paths",out)
        check([len(x["required_test_names"]) for x in proof["families"]]==[18,15],"exact_18_15_function_names",out)
        check(proof["families"][0]["required_test_names"]==[x["proposed_node"].split("::")[1] for x in d],"D091_all_nodes_match",out)
        check(proof["families"][1]["required_test_names"]==[x["proposed_node"].split("::")[1] for x in l],"L01b_all_nodes_match",out)
        check({x for f in proof["families"] for x in f["proof_obligation_ids"]}==set(proof["required_proof_ids"]),"both_proof_obligations_exact",out)
        check(all(f["command"]=="python -m pytest "+f["path"] for f in proof["families"]),"future_command_shape_fits_current_runner",out)
        check(all(v=="FAIL" for v in proof["execution_policy"].values()),"future_strict_execution_policy",out)
        check(not spec["proof_registry"]["registry_installed"] and not spec["proof_registry"]["loader_recognises_claim_now"] and spec["proof_registry"]["generation"] is None,"registry_and_generation_UNINSTALLED",out)
        check(not spec["admitted_jurisdictions"]["execution_release"] and spec["review"]["product_tests"]==0 and spec["review"]["D145"]=="PAUSED","execution_held_and_D145_paused",out)
        code=(ROOT / "tools/product_proof_claims.py").read_text(encoding="utf-8")
        check("def load_product_proof_claim" in code and "def _partition" in code and "unknown/duplicate product claim" in code,"actual_loader_bound",out)
        check("def _d091_l01b_extension" not in code,"proposed_extension_not_falsely_claimed_installed",out)
        record=(ROOT / "src/nvda_desk/market_measurement_truth/_record_store.py").read_text(encoding="utf-8")
        check("def _transaction(" in record and "def _existing(" in record and 'c.execute("COMMIT")' in record,"real_transaction_and_conflict_seams_exist",out)
        check("D01_AFTER_INSERT_BEFORE_COMMIT" not in record,"fault_hook_not_falsely_claimed_installed",out)
        head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        paths=subprocess.check_output(["git","diff","--name-only",PARENT,head],cwd=ROOT,text=True).splitlines()
        check(all(p.startswith(HERE.relative_to(ROOT).as_posix()+"/") for p in paths),"revision_changes_only_under_documentary_folder",out)
        out["head"]=head
        out["changed_paths"]=paths
        out["revision_blob_sha256"]={n:sha(HERE / n) for n in ("EXACT_RETURN_REPAIR_R1_R3.md","TECHNICAL_REPAIR_BINDING_V2.json","PRODUCT_PROOF_REGISTRATION_PROPOSAL.json")}
        out["status"]="STATIC_DOCUMENTARY_PASS"
    except BaseException as e:
        out["status"]="STATIC_DOCUMENTARY_FAIL"
        out["error"]=f"{type(e).__name__}: {e}"
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path("/tmp/nvda_d091_preedit_r1_r3_revision_validation.json")
    dest.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":out["status"],"checks":len(out["checks"]),"failed":out.get("error"),"receipt":str(dest),"head":out.get("head")}))
    if out["status"]!="STATIC_DOCUMENTARY_PASS":
        raise SystemExit(1)

if __name__=="__main__":
    main()
