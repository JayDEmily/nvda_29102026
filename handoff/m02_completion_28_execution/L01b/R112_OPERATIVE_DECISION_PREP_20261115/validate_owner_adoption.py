"""Pure-document verification of later owner decision; no product imports or case execution."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = "ec9112bf8b94d167de768ca7b151026f965f0838"
EXPECTED_SOURCE_SHA = "31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
def load(p): return json.loads((ROOT / p).read_text(encoding="utf-8"))
def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()
def main():
    adoption = load("handoff/m02_completion_28_execution/L01b/R112_OPERATIVE_DECISION_PREP_20261115/OWNER_SOURCE_ADOPTION_20261115.json")
    prep = load("handoff/m02_completion_28_execution/L01b/R112_OPERATIVE_DECISION_PREP_20261115/SOURCE_ADMISSION_DECISION_CANDIDATE.json")
    source_path = ROOT / adoption["source_contract_path"]
    source = json.loads(source_path.read_text(encoding="utf-8"))
    sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
    assert sha == adoption["source_contract_sha256"] == prep["source_contract_sha256"] == EXPECTED_SOURCE_SHA
    assert adoption["verbatim_owner_reply"] == "I approve the controlled synthetic R112 source policy for those leaves."
    assert adoption["preceding_question"] == "Do you approve this exact, synthetic-only R112 source policy for L01b → L04?"
    assert adoption["status"] == "OWNER_POLICY_ADOPTED_INDEPENDENT_OPERATIVE_CLEARANCE_PENDING"
    assert (adoption["leaf"], adoption["consumer_leaf"], adoption["derived_id"]) == ("L01b","L04","D091")
    assert source["source_provider"] == adoption["source_provider"]
    assert source["source_variant"] == adoption["source_variant"]
    assert source["model_variant"] == adoption["source_model"]
    assert source["profile_id"] == adoption["source_contract_profile_id"]
    assert source["selection"]["policy_id"] == adoption["selection_policy_id"]
    assert source["selection"]["history_page_size"] == 8 and source["selection"]["maximum_projected_members"] == 64
    assert source["synthetic_only"] and not source["live_provider_claim"]
    assert adoption["synthetic_only"] and adoption["source_closed_batch_required"]
    assert not adoption["production_policy_adopted"] and not adoption["snapshot_api_inferred"]
    assert adoption["operative_independent_clearance"] is None
    assert not adoption["l00_qualified"] and not adoption["l01b_source_admitted"]
    assert not adoption["d091_implementation_released"] and not adoption["strict_tester_designated"]
    assert adoption["physical_product_cases_admitted"] == adoption["product_tests_executed"] == 0
    assert adoption["d145"] == "PAUSED"
    assert prep["owner_approval_ref"] is None, "Historical decision candidate must remain unmodified"
    assert git("merge-base", BASE, "HEAD") == BASE
    rel = HERE.relative_to(ROOT).as_posix() + "/"
    names = git("diff", "--name-only", BASE, "HEAD").splitlines()
    names += git("diff", "--cached", "--name-only").splitlines()
    names += git("ls-files", "--others", "--exclude-standard").splitlines()
    assert names and all(n.startswith(rel) for n in names), names
    print(json.dumps({"result":"R112_OWNER_ADOPTION_RECORD_STATIC_PASS",
       "contract_sha256":sha, "status":adoption["status"],
       "independently_source_admitted":False,"product_cases_admitted":0,
       "product_tests_executed":0,"change_scope":rel,
       "limits":"Worker validates recorded owner statement and file consistency, not independent authenticity or operative clearance."},sort_keys=True))
if __name__=="__main__":
    main()
