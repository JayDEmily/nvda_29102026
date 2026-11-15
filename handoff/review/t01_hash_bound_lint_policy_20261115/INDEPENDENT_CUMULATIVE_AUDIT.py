#!/usr/bin/env python3
"""Independent PR14 read-only source/policy audit; Ruff only, no product tests."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

OLD = "ded4b98e1e5999d1ddf2f067e660b691917bcd71"
MAIN = "a73349834fe4aa1422c194da0492315044b32b98"
HEAD = "831471d69afd092779a6810ee570285182be88a8"
FIXTURE = "86b23f1ef5bf4a1510e93333fa4b2cfc869c3b71"
DIGEST = "08ae839b0596c31ecb73a4667845f0d19dfe0c4503c52079434dd98e835a2a8f"
MANIFEST_SHA = "d38367ce1f63a1731c0cd9b69e12af021a291d71b0206f83ba17f3b69dbfc97c"
FIXTURE_SHA = "3840d197d6b570cd7912aea606ce859d529ffc14c1ff93ce0378f767ebfc54b9"


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def command(root: Path, *argv: str, allowed: tuple[int, ...] = (0,)) -> str:
    r = subprocess.run(argv, cwd=root, capture_output=True, text=True)
    if r.returncode not in allowed:
        raise AssertionError(f"CLI {argv}, exit={r.returncode}, stderr={r.stderr[:700]}")
    return r.stdout


def committed(root: Path, ref: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=root)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", type=Path, required=True)
    ap.add_argument("--ruff", type=Path, required=True)
    args = ap.parse_args()
    root = args.candidate.resolve()
    assert command(root, "git", "rev-parse", "HEAD").strip() == HEAD
    assert command(root, "git", "merge-base", OLD, HEAD).strip() == OLD
    assert command(root, "git", "merge-base", MAIN, HEAD).strip() == OLD
    assert not command(root, "git", "status", "--porcelain")
    diff_old = command(root, "git", "diff", "--name-only", OLD, HEAD).splitlines()
    diff_now = command(root, "git", "diff", "--name-only", MAIN, HEAD).splitlines()
    assert len(diff_old) == 23
    assert len(diff_now) == 24
    assert set(diff_now) - set(diff_old) == {"AGENTS.md"}
    assert (root / "AGENTS.md").read_bytes() == committed(root, OLD, "AGENTS.md")
    assert committed(root, MAIN, "AGENTS.md").startswith(b"**CONTINUOUS EXECUTION")
    unchanged_roots = ["GUARDRAILS.md", "EXEC_PLAN.md", "AGENTS.md",
                       "tests/AGENTS.override.md", "config/product_proof"]
    assert not command(root, "git", "diff", "--name-only", OLD, HEAD, "--", *unchanged_roots).strip()

    manifest_raw = (root / "config/lint/PROPOSED_SHA_BOUND_RUFF_BASELINE.json").read_bytes()
    assert hash_bytes(manifest_raw) == MANIFEST_SHA
    manifest = json.loads(manifest_raw)
    assert manifest["status"] == "PROPOSED_NOT_ACCEPTED"
    assert manifest["diagnostic_count"] == 51
    assert manifest["diagnostic_set_sha256"] == DIGEST
    assert command(root, str(args.ruff), "--version").strip() == "ruff 0.15.11"

    sources = []
    for item in manifest["files"]:
        name = item["path"]
        raw = (root / name).read_bytes()
        assert hash_bytes(raw) == item["sha256"]
        assert raw == committed(root, OLD, name)
        ref = json.loads((root / item["admission_path"]).read_text())["current_generation"]
        assert ref["path"] == item["generation_path"]
        gen_raw = (root / ref["path"]).read_bytes()
        assert hash_bytes(gen_raw) == ref["sha256"] == item["generation_sha256"]
        gen = json.loads(gen_raw)
        assert gen["claim_id"] == item["claim_id"]
        matching = [v for v in gen[item["admission_kind"]] if v["path"] == name]
        assert len(matching) == 1 and matching[0]["sha256"] == item["sha256"]
        sources.append({"claim":item["claim_id"],"source":name,"sha256":item["sha256"]})
    assert len(sources) == 7

    for path in ("src/nvda_desk/derived_signal_calculation_truth/_financial_policy.py",
                 "tests/product/derived_signal/test_m01_stage1_semantics.py"):
        orig = ast.dump(ast.parse(committed(root, OLD, path).decode()), include_attributes=False)
        updated = ast.dump(ast.parse((root / path).read_text()), include_attributes=False)
        assert orig == updated

    fixture_raw = (root / "tests/architecture/fixtures/pre_admission_20261018_inventory.json").read_bytes()
    assert hash_bytes(fixture_raw) == FIXTURE_SHA
    inv = json.loads(fixture_raw)
    originals = command(root, "git", "ls-tree", "-r", "--name-only", FIXTURE,
                        "--", "tests/product").splitlines()
    original_configs = command(root, "git", "ls-tree", "-r", "--name-only", FIXTURE,
                               "--", "config/product_proof").splitlines()
    python_files = {v for v in originals if v.endswith(".py")}
    assert set(inv["product_python_paths"]) == python_files
    assert set(inv["proof_config_paths"]) == set(original_configs)
    assert sum(v.rsplit("/", 1)[-1].startswith("test_") for v in python_files) == inv["original_test_count"] == 93

    raw = command(root, str(args.ruff), "check", "--output-format=json",
                  "src", "tests", "tools", allowed=(1,))
    normalised = []
    for d in json.loads(raw):
        normalised.append({
            "path": Path(d["filename"]).resolve().relative_to(root).as_posix(),
            "code": d["code"], "message": d["message"],
            "row": d["location"]["row"], "column": d["location"]["column"],
        })
    normalised.sort(key=lambda x: (x["path"], x["row"], x["column"], x["code"], x["message"]))
    diagnostics_sha = hash_bytes((json.dumps(normalised, sort_keys=True, separators=(",", ":")) + "\n").encode())
    path_counts = Counter(v["path"] for v in normalised)
    codes = Counter(v["code"] for v in normalised)
    assert len(normalised) == 51 and diagnostics_sha == DIGEST
    assert path_counts == Counter({row["path"]:row["diagnostic_count"] for row in manifest["files"]})
    assert codes == Counter({"E501":38, "I001":5, "B905":4, "RUF007":4})
    assert not command(root, "git", "status", "--porcelain")
    print(json.dumps({
        "result":"PASS_INDEPENDENT_READ_ONLY_PR14_CUMULATIVE",
        "candidate":HEAD, "historical_base":OLD, "current_main":MAIN,
        "historical_cumulative_paths":diff_old,
        "historical_cumulative_count":len(diff_old),
        "current_main_difference_count":len(diff_now),
        "current_main_additional_path":"AGENTS.md",
        "governance_and_proof_admission_not_modified_on_candidate":True,
        "proof_sources_preserved":sources,
        "history_manifest_test_count":93,
        "historical_fixture_exact_path_membership":True,
        "two_other_python_files_ast_unchanged":True,
        "actual_ruff_diagnostics":len(normalised),
        "ruff_codes":dict(sorted(codes.items())),
        "ruff_exact_digest_sha256":diagnostics_sha,
        "policy_accepted_by_owner":False,
        "product_proof_executed":False,
    },indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
