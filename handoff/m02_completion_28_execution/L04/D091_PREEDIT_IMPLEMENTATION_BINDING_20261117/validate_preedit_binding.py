"""Static D091/L01b documentary contract validation; never imports product modules or runs tests."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
THIS = Path(__file__).resolve().parent
BASE = Path("handoff/m02_completion_28_execution")
REVIEWED_BASE = "11969c8a51f8446f0b731d502270036326489bbd"
SOURCE_SHA = "31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
POSITIVE_SHA = "1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def check(ok: bool, label: str, report: dict) -> None:
    report["checks"][label] = bool(ok)
    if not ok:
        raise AssertionError(label)

def main() -> None:
    report: dict = {
        "schema": "D091_PREEDIT_BINDING_STATIC_VALIDATION_V1",
        "proof_class": "DOCUMENTARY_SOURCE_HASH_AND_CENSUS_ONLY",
        "not_product_test": True,
        "checks": {},
    }
    try:
        binding = load(THIS / "PREEDIT_BINDING_PROPOSAL.json")
        proof = load(THIS / "PREEDIT_PROOF_CONTRACT_PROPOSAL.json")
        brief = THIS / "IMPLEMENTATION_BRIEF.md"
        owner = load(REPO / BASE / "OWNER_D091_L01B_FINITE_CASE_ADMISSION_20261117" / "OWNER_FINITE_CASE_ADMISSION_20261117.json")
        ledger = load(REPO / BASE / "TEST_EVIDENCE_LEDGER.json")
        inv = load(REPO / BASE / "L04/D091_FINITE_ADEQUACY_REVISION_20261117/REVISED_CASE_INVENTORY.json")
        fm = load(REPO / BASE / "L04/D091_FINITE_ADEQUACY_REVISION_20261117/FIELD_DISCRIMINATION_MATRIX.json")
        nc = load(REPO / BASE / "L04/D091_FINITE_ADEQUACY_REVISION_20261117/NEGATIVE_ONLY_SEALED_COHORTS.json")
        contract_path = REPO / BASE / "L01b/R112_SOURCE_CONTRACT_PROPOSED.json"
        source_path = REPO / BASE / "L01b/CONTROLLED_BATCH_INPUTS.json"
        source = load(source_path)
        contract = load(contract_path)
        d = binding["owner_approved_case_allocations"]["D091_L04"]
        s = binding["owner_approved_case_allocations"]["L01b_R112"]
        d_active = next(v for v in ledger["proof_obligations"] if v["proof_id"] == "M02-C28-D091")["test_allocation"]
        s_active = next(v for v in ledger["source_support_test_allocations"] if v["proof_id"] == "M02-C28-L01B-R112-SOURCE-SUPPORT")["test_allocation"]
        d_inv = [v for v in inv["physical_cases"] if v["jurisdiction"] == "L04_D091"]
        s_inv = [v for v in inv["physical_cases"] if v["jurisdiction"] == "L01b_R112_SOURCE_SUPPORT_NOT_D091"]
        check(sha(brief) == binding["technical_brief"]["raw_utf8_sha256"], "brief_exact_SHA256", report)
        check(sha(contract_path) == SOURCE_SHA == binding["raw_source"]["contract_utf8_sha256"], "approved_source_contract_SHA256", report)
        check(sha(source_path) == POSITIVE_SHA == binding["raw_source"]["positive_sha256"], "frozen_15_source_SHA256", report)
        check(len(source["members"]) == 15 and len([v for v in source["members"] if v["purpose"] == "positive"]) == 12, "source_15_member_12_positive", report)
        check([v["observation"]["observation_occurrence_id"] for v in source["members"]] == binding["raw_source"]["positive_observation_ids"], "source_15_member_ids", report)
        check(source["members"][12]["observation"]["native_record"]["model"]["delta"]["text"] == "1.01", "original_t12_range", report)
        check(source["members"][13]["observation"]["native_record"]["model"]["delta"]["text"] == "NaN", "original_t13_nonfinite", report)
        check("delta" not in source["members"][14]["observation"]["native_record"]["model"], "original_t14_absent", report)
        check(len(contract["contract_identity_fields"]) == 11 and binding["raw_source"]["eleven_identity_fields"] == contract["contract_identity_fields"], "eleven_identity_fields", report)
        check(contract["mapping"] == binding["raw_source"]["mapping"] and contract["selection"] == binding["raw_source"]["selection"], "exact_mapping_selection", report)
        check(contract["rule_profile"] == binding["categorical_result"]["rule_profile"] and len(contract["rule_profile"]["bins"]) == 5, "five_exact_rule_bins", report)
        check(len(d_inv) == 18 and len(s_inv) == 15, "reviewed_18_15_jurisdiction_count", report)
        check(d["count"] == d["hard_ceiling"] == d_active["authorised_case_count"] == d_active["hard_ceiling"] == 18, "D091_admitted_ceiling_18", report)
        check(s["count"] == s["hard_ceiling"] == s_active["authorised_case_count"] == s_active["hard_ceiling"] == 15, "L01b_admitted_ceiling_15", report)
        ids_d = [v["case_id"] for v in d_inv]
        ids_s = [v["case_id"] for v in s_inv]
        check(ids_d == [v["case_id"] for v in d["physical_cases"]] == [v["case_id"] for v in d_active["cases"]], "D091_exact_18_IDs", report)
        check(ids_s == [v["case_id"] for v in s["physical_cases"]] == [v["case_id"] for v in s_active["cases"]], "L01b_exact_15_IDs", report)
        check(len(set(ids_d + ids_s)) == 33, "33_unique_physical_IDs", report)
        check(owner["approved_separate_jurisdictions"]["L04_D091"]["authorised_case_count"] == 18 and owner["approved_separate_jurisdictions"]["L01b_R112_SOURCE_SUPPORT_NOT_D091"]["authorised_case_count"] == 15, "direct_owner_case_admissions", report)
        check(not d_active["execution_release"] and not s_active["execution_release"] and not d_active["cases"][0]["execution_authorised"], "execution_held_active_ledger", report)
        check(len(fm["cases"]) == 15 and {v["case_id"]: v["refusal_field_path"] for v in fm["cases"]} == {v["case_id"]: v["path"] for v in binding["bounded_faults"]["source_A_15"]}, "all_15_specific_ingress_predicates", report)
        for v in binding["bounded_faults"]["source_A_15"]:
            check(sha(REPO / v["fixture_path"]) == v["fixture_sha256"], "A_fixture_" + v["case_id"], report)
        for name, v in binding["coordinator"]["negative_manifest_fixtures"].items():
            check(sha(REPO / v["path"]) == v["sha256"], "B_cohort_fixture_" + name, report)
        check(binding["coordinator"]["negative_manifest_fixtures"]["B_TIE_2"]["member_count"] == 2 and binding["coordinator"]["negative_manifest_fixtures"]["B_OVER64_65"]["member_count"] == 65, "two_genuine_distinct_B_manifests", report)
        check(binding["coordinator"]["negative_manifest_fixtures"]["B_OVER64_65"]["history_expected_pages"] == [8] * 8 + [1], "B65_nine_actual_page_oracle", report)
        for v in d["physical_cases"] + s["physical_cases"]:
            if v["fixture_path"]:
                check(sha(REPO / v["fixture_path"]) == v["fixture_sha256"], "approved_case_fixture_" + v["case_id"], report)
        check(len(proof["families"]) == 2 and proof["families"][0]["authorised_physical_count"] == 18 and proof["families"][1]["authorised_physical_count"] == 15, "proof_contract_18_15", report)
        check([v["case_id"] for v in d["physical_cases"]] == proof["families"][0]["physical_case_ids"] and [v["case_id"] for v in s["physical_cases"]] == proof["families"][1]["physical_case_ids"], "proof_contract_IDs_match", report)
        check(binding["dto_and_public_interface_proposal"]["diagnostic_exact_five_field_order"] == ["request_identity","source_observation_occurrence_id","stage","source_profile_ref","rule_profile_ref"], "five_field_observer", report)
        check(len(binding["dto_and_public_interface_proposal"]["exact_diagnostic_stage_allowlist"]) == 7, "seven_D091_business_stages", report)
        check(binding["proposed_claim_registry"]["generation_actual"] is None and binding["proposed_claim_registry"]["generation_sha256"] is None and proof["versioning"]["actual_claim_generation"] is None, "claim_generation_UNBOUND", report)
        check(all(not v["execution_released"] for v in d["physical_cases"] + s["physical_cases"]) and binding["release_gates"]["product_executions"] == 0, "all_33_cases_unexecuted", report)
        check(binding["release_gates"]["preedit_independent_review"] == "PENDING" and binding["release_gates"]["author_tests"] == "HELD" and binding["release_gates"]["author_code"] == "HELD" and binding["release_gates"]["D145"] == "PAUSED", "preedit_and_D145_holds", report)
        head = subprocess.check_output(["git","-C",str(REPO),"rev-parse","HEAD"],text=True).strip()
        changed = subprocess.check_output(["git","-C",str(REPO),"diff","--name-only",REVIEWED_BASE,head],text=True).splitlines()
        check(all(v.startswith(str(THIS.relative_to(REPO)) + "/") for v in changed), "no_product_code_test_or_ledger_changes_since_base", report)
        report["git_head"] = head
        report["changed_paths_from_reviewed_base"] = changed
        report["case_counts"] = {"D091":18,"L01b":15}
        report["status"] = "STATIC_DOCUMENTARY_PASS"
    except BaseException as exc:
        report["status"] = "STATIC_DOCUMENTARY_FAIL"
        report["failure"] = f"{type(exc).__name__}: {exc}"
    report["source_files_sha256"] = {
        "brief":sha(THIS / "IMPLEMENTATION_BRIEF.md"),
        "binding":sha(THIS / "PREEDIT_BINDING_PROPOSAL.json"),
        "proof_contract":sha(THIS / "PREEDIT_PROOF_CONTRACT_PROPOSAL.json"),
    }
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nvda_d091_preedit_validation_receipt_20261117.json")
    output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"check_count":len(report["checks"]),"failure":report.get("failure"),"git_head":report.get("git_head"),"receipt":str(output)}))
    if report["status"] != "STATIC_DOCUMENTARY_PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
