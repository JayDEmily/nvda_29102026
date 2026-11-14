#!/usr/bin/env python3
"""Independent, read-only seven-claim source/lineage audit, no pytest or imports from repo."""
import ast
import hashlib
import itertools
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = "b67f3e92470fe4e3281546fbc6fc62e347d5f0ee"
HEAD = "c616dc5da96af2c2901f2c93e05bbf69f489a725"
MANIFEST = ROOT / "handoff/review/t01_ruff_zero_readmission_20261114/PROPOSED_SUCCESSOR_GENERATIONS.json"
run = lambda *args: subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()
digest = lambda b: hashlib.sha256(b).hexdigest()
read = lambda path: (ROOT / path).read_bytes()
assert run("cat-file", "-t", HEAD) == "commit"
assert run("rev-parse", f"{HEAD}~1") == "28baa81fb02f7aad34b0b652b5477788998bb48f"
assert run("merge-base", "--is-ancestor", BASE, HEAD) == ""
m = json.loads(MANIFEST.read_text())
assert len(m["claims"]) == len(m["candidate_source_paths"]) == 7
assert len(set(m["candidate_source_paths"])) == 7
changed = set(run("diff", "--name-only", BASE, HEAD).splitlines())
assert changed == set(m["candidate_source_paths"]) | {
  "handoff/review/t01_ruff_zero_readmission_20261114/INDEPENDENT_REVIEW_REQUEST.md",
  "handoff/review/t01_ruff_zero_readmission_20261114/PROPOSED_SUCCESSOR_GENERATIONS.json",
  "handoff/review/t01_ruff_zero_readmission_20261114/VERIFY_SOURCE_CANDIDATE.py",
}, sorted(changed)
replacement = ast.parse("zip(SAMPLES, SAMPLES[1:])", mode="eval").body
class Normalise(ast.NodeTransformer):
    def __init__(self): self.count=0
    def visit_Call(self,node):
        self.generic_visit(node)
        if isinstance(node.func,ast.Name) and node.func.id=="pairwise":
            assert len(node.args)==1 and isinstance(node.args[0],ast.Name) and node.args[0].id=="SAMPLES"
            assert not node.keywords
            self.count+=1
            return replacement
        return node
catalogue = json.loads(read("config/product_proof/claims.json"))
statuses=[]
for c in m["claims"]:
  claim=c["claim_id"]
  paths=c["changed_hash_paths"]
  assert len(paths)==1 and paths[0] in m["candidate_source_paths"]
  p=paths[0]
  old = subprocess.check_output(["git","-C",str(ROOT),"show",f"{BASE}:{p}"])
  new = read(p)
  assert old != new
  old_ast = ast.parse(old,filename=p)
  new_ast = ast.parse(new,filename=p)
  normalise=Normalise()
  new_ast.body = [n for n in new_ast.body if not (isinstance(n,ast.ImportFrom) and n.module=="itertools" and [x.name for x in n.names]==["pairwise"])]
  new_ast=normalise.visit(new_ast)
  ast.fix_missing_locations(new_ast)
  assert ast.dump(old_ast,include_attributes=False)==ast.dump(new_ast,include_attributes=False),f"semantic AST divergence: {p}"
  count=normalise.count
  assert count==(1 if p.endswith("realised_volatility.py") else 0), (p,count)
  intervals=None
  if count:
    tree=ast.parse(new)
    sample_assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="SAMPLES" for t in n.targets))
    sample_values=ast.literal_eval(sample_assignment.value.args[0].generators[0].iter)
    times=tuple(datetime.fromisoformat(s) for s in sample_values)
    assert tuple(zip(times,times[1:]))==tuple(itertools.pairwise(times))
    intervals=len(times)-1
  admission=json.loads(read(c["admission_path"]))
  assert admission["current_generation"]==c["predecessor_pointer"]
  old_generation_bytes=read(c["predecessor_pointer"]["path"])
  assert digest(old_generation_bytes)==c["predecessor_pointer"]["sha256"]
  generation=json.loads(old_generation_bytes)
  assert generation["generation"]==c["predecessor_generation_number"]
  assert generation["claim_id"]==claim
  proposed=c["proposed_generation_record_REVIEW_ONLY_INCOMPLETE_AUTHORITY"]
  assert proposed["generation"]==generation["generation"]+1
  assert proposed["previous_generation"]==c["predecessor_pointer"]
  assert proposed["claim_id"]==claim
  assert proposed["adequacy_review_ref"] is None and proposed["admission_authority_ref"] is None
  assert not (ROOT/c["proposed_generation_path"]).exists()
  assert proposed["implementation_target_id"]==generation["implementation_target_id"]=="M02"
  for key in ("brief_sha256","binding_sha256","contract_sha256"):
    assert proposed[key]==generation[key],(claim,key)
  expected={e["path"]:e["sha256"] for key in ("family_files","support_files") for e in proposed[key]}
  assert len(expected)==sum(len(proposed[key]) for key in ("family_files","support_files"))
  for path,sha in expected.items(): assert digest(read(path))==sha,(claim,path)
  assert p in expected
  old_pins={e["path"]:e["sha256"] for key in ("family_files","support_files") for e in generation[key]}
  assert expected.keys()==old_pins.keys()
  assert {p for p in expected if expected[p]!=old_pins[p]}==set(paths)
  if claim.endswith("_pilot"):
    entry=next(e for e in catalogue["claims"] if e["claim_id"]==claim)
    brief_path=catalogue["control_authority"]["brief_path"]
  else:
    identity=claim.rsplit("_",1)[-1]
    entry=json.loads(read(f"config/product_proof/market_measurement_{identity}/claim.json"))
    brief_path=entry["brief_path"]
  contract=json.loads(read(entry["contract_path"]))
  assert digest(read(brief_path))==proposed["brief_sha256"]
  assert digest(read(entry["binding_path"]))==proposed["binding_sha256"]
  assert digest(read(entry["contract_path"]))==proposed["contract_sha256"]
  assert contract["claim_id"]==claim
  contract_families={f["path"]:f["required_test_names"] for f in contract["families"]}
  assert contract_families==c["required_test_names_by_family"]
  assert set(contract_families)=={e["path"] for e in proposed["family_files"]}
  assert set(contract["required_support_files"]).issubset({e["path"] for e in proposed["support_files"]})
  assert set(c["admitted_family_paths"])==set(contract_families)
  statuses.append({"claim":claim,"file":p,"ast_equal":True,"pairwise_replacements":count,
      "sample_intervals":intervals,"old_file_sha256":digest(old),"new_file_sha256":digest(new),
      "changed_pin_count":len(paths),"predecessor_generation":generation["generation"],
      "proposed_generation":proposed["generation"],"current_pointer_preserved":True,
      "manifest_valid_to_contract":True})
assert len(statuses)==7 and sum(s["pairwise_replacements"] for s in statuses)==4
assert sum(len(c["required_test_names_by_family"]) for c in m["claims"])==11
assert sum(sum(len(v) for v in c["required_test_names_by_family"].values()) for c in m["claims"])==15
print(json.dumps({"audit":"INDEPENDENT_STATIC_SOURCE_AND_MANIFEST","head":HEAD,
 "base":BASE,"changed_files":len(changed),"source_claims":len(statuses),"status":"PASS",
 "product_proof_executed":False,"admission_written":False,"claims":statuses},indent=2))
