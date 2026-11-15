#!/usr/bin/env python3
"""Read-only T01 runtime/proof-contract inventory; not an equivalence or product test."""
from __future__ import annotations
import json
import shutil
import sqlite3
import sys
import tomllib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
base = ROOT / "handoff/review/t01_ruff_zero_readmission_20261114"
manifest = json.loads((base / "PROPOSED_SUCCESSOR_GENERATIONS.json").read_text())
project = tomllib.loads((ROOT / "pyproject.toml").read_text())
contracts = []
for claim in manifest["claims"]:
    if claim["claim_id"].endswith("_pilot"):
        entry = next(c for c in json.loads((ROOT / "config/product_proof/claims.json").read_text())["claims"] if c["claim_id"] == claim["claim_id"])
    else:
        identity = claim["claim_id"].rsplit("_", 1)[-1]
        entry = json.loads((ROOT / f"config/product_proof/market_measurement_{identity}/claim.json").read_text())
    contract = json.loads((ROOT / entry["contract_path"]).read_text())
    assert contract["claim_id"] == claim["claim_id"]
    for family in contract["families"]:
        contracts.append({"claim_id": claim["claim_id"], "family_path": family["path"], "contract_environment": family["environment"]})
print(json.dumps({
 "kind": "READ_ONLY_RUFF_SUCCESSOR_RUNTIME_PREFLIGHT",
 "candidate": "c616dc5da96af2c2901f2c93e05bbf69f489a725",
 "interpreter_executed": sys.executable,
 "interpreter_version": ".".join(map(str,sys.version_info[:3])),
 "sqlite3_loaded_version": sqlite3.sqlite_version,
 "project_requires_python": project["project"]["requires-python"],
 "project_python_version_file": (ROOT / ".python-version").read_text().strip(),
 "python3_12_in_current_PATH": shutil.which("python3.12"),
 "contracts": contracts,
 "contract_count":len({x["claim_id"] for x in contracts}),
 "contract_family_count":len(contracts),
 "claim_of_runtime_equivalence":False,
 "product_tests_executed":False,
 "proof_admissions_executed":False
},indent=2))
