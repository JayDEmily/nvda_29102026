"""Pure documentary source/owner decision packet validation; no product imports or tests."""
from pathlib import Path
from decimal import Decimal
import hashlib,json,subprocess
ROOT = Path(__file__).resolve().parents[4]
PACKET=Path(__file__).resolve().parent
BASE='5be8ee22609e27e765f46437017b1e7cce6c6f2e'
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def digest(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()
def main():
    proposal=read('handoff/m02_completion_28_execution/L01b/R112_OPERATIVE_DECISION_PREP_20261115/SOURCE_ADMISSION_DECISION_CANDIDATE.json')
    source=read(proposal['source_contract_path'])
    raw=read(proposal['source_fixture_path'])
    oracles=read('handoff/m02_completion_28_execution/L01b/DOCUMENTARY_ORACLES.json')
    claim=read('handoff/m02_completion_28_execution/L04/D091_PRE_ADMISSION_20261115/PROPOSED_CASE_ADMISSION.json')
    register=read('handoff/m02_completion_28_execution/EXECUTION_REGISTER.json')
    ledger=read('handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json')
    receipt=json.loads((PACKET/'SQLITE_3491_NONPRODUCT_MECHANISM_RECEIPT.json').read_text())
    assert git('merge-base',BASE,'HEAD')==BASE
    assert proposal['upstream_candidate_commit']==BASE
    assert digest(proposal['source_contract_path'])==proposal['source_contract_sha256']
    assert digest(proposal['source_fixture_path'])==proposal['source_fixture_sha256']
    assert digest('handoff/m02_completion_28_execution/L01b/DOCUMENTARY_ORACLES.json')==proposal['documentary_oracle_sha256']
    assert source['status']=='DOCUMENTARY_SOURCE_CONTRACT_PROPOSAL_NOT_ADMITTED'
    assert source['source_provider']==proposal['proposed_scope']['source_provider']
    assert source['source_variant']==proposal['proposed_scope']['source_variant']
    assert source['model_variant']==proposal['proposed_scope']['model_variant']
    assert source['profile_id']==proposal['proposed_scope']['profile_id']
    assert source['selection']['policy_id']==proposal['proposed_scope']['selection_policy']
    assert source['selection']['history_page_size']==8 and source['selection']['maximum_projected_members']==64
    assert raw['status']=='PROPOSED_LITERAL_CONTROLLED_SOURCE_BATCH_NOT_ADMITTED'
    assert len(raw['members'])==15 and len(oracles['positive_members'])==12 and len(oracles['refusal_members'])==3
    assert claim['proposed_case_count']==2 and claim['admitted_case_count']==0 and claim['executed_case_count']==0
    assert len(register['leaves'])==39 and len(ledger['proof_obligations'])==35
    assert all(not x['test_allocation']['authorised_case_count'] and not x['execution']['runs'] for x in ledger['proof_obligations'])
    for row in oracles['positive_members']:
        x=abs(Decimal(row['signed_delta']))
        matched=[b['name'] for b in source['rule_profile']['bins'] if x>=Decimal(b['min']) and (x<Decimal(b['max']) or (b['max_inclusive'] and x==Decimal(b['max'])))]
        assert matched==[row['expected_label']]
    assert proposal['owner_approval_ref'] is None and proposal['independent_operative_clearance_ref'] is None
    assert proposal['source_admitted'] is False and proposal['d091_implementation_released'] is False
    assert proposal['physical_case_count_admitted']==0 and proposal['product_runs']==0
    assert receipt['product_cases_executed']==0 and receipt['all_checked_mechanisms_observed']
    assert receipt['sqlite_version']=='3.49.1' and receipt['not_equivalence_proof']
    changed=(git('diff','--name-only',BASE,'HEAD').splitlines()+git('diff','--cached','--name-only').splitlines()+git('ls-files','--others','--exclude-standard').splitlines())
    prefix=PACKET.relative_to(ROOT).as_posix()+'/'
    assert changed and all(name.startswith(prefix) for name in changed),changed
    print(json.dumps({'result':'R112_OPERATIVE_DECISION_PACKET_STATIC_PASS','proposed_owner_approval':False,'admitted_source':False,'product_cases_admitted':0,'product_runs':0,'raw_source_member_count':15,'rule_oracles':12,'sqlite_mechanisms_checked':len(receipt['features']),'change_scope_only':prefix,'no_product_imports_or_tests':True},sort_keys=True))
if __name__=='__main__':main()
