#!/usr/bin/env python3
"""Adversarial lint verifier test against an EXACT disposable PR14 worktree.

Never run against main, worker or reviewer; no product pytest / admissions written.
All temporary mutations are reversed, and the worktree must finish git-clean.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

SHA = "831471d69afd092779a6810ee570285182be88a8"


def cli(root: Path, python_executable: Path, ruff: Path) -> tuple[int, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PATH"] = f"{ruff.parent}:{env.get('PATH', '')}"
    run = subprocess.run(
        [str(python_executable), "tools/proposed_admitted_ruff_baseline.py"],
        cwd=root, env=env, capture_output=True, text=True,
    )
    return run.returncode, run.stdout + run.stderr


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disposable", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--ruff", type=Path, required=True)
    opts = parser.parse_args()
    root = opts.disposable.resolve()
    assert root.name == "nvda_t01_pr14_falsification_20261115"
    assert root.is_dir() and (root / ".git").exists()
    assert git(root, "rev-parse", "HEAD").strip() == SHA
    assert not git(root, "status", "--porcelain", "--untracked-files=all")
    results = []
    baseline_rc, baseline_txt = cli(root, opts.python, opts.ruff)
    assert baseline_rc == 0 and "EXACT_MATCH: 51" in baseline_txt
    results.append({"case":"untampered_baseline", "exit":baseline_rc, "accepted":True})

    def corrupt(case: str, relative: str, mutated: bytes, expected: str) -> None:
        p = root / relative
        exists = p.exists()
        original = p.read_bytes() if exists else None
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(mutated)
            code, output = cli(root, opts.python, opts.ruff)
            if code != 1 or expected not in output:
                raise AssertionError(f"{case}: expected refusal {expected!r}, got rc={code}: {output[:800]}")
            results.append({"case":case, "exit":code, "accepted":False, "observed_refusal":expected})
        finally:
            if original is None:
                p.unlink(missing_ok=True)
            else:
                p.write_bytes(original)
        assert not git(root, "status", "--porcelain", "--untracked-files=all")

    source = "tests/product/market_measurement/typing/valid_seam.py"
    corrupt("changed_admitted_proof_file", source,
            (root / source).read_bytes() + b"\n# disposable negative case\n",
            "admitted source bytes changed")

    pointer = "config/product_proof/market_measurement_d030/admission.json"
    original_ptr = (root / pointer).read_text()
    obj = json.loads(original_ptr)
    obj["current_generation"]["path"] = obj["current_generation"]["path"].replace("0002.json", "0001.json")
    corrupt("changed_current_admission_pointer", pointer,
            (json.dumps(obj, indent=2) + "\n").encode(), "selected generation changed")

    gen = "config/product_proof/market_measurement_d030/generations/0002.json"
    corrupt("changed_immutable_generation_bytes", gen,
            (root / gen).read_bytes() + b" \n", "generation bytes or pointer changed")

    manifest = "config/lint/PROPOSED_SHA_BOUND_RUFF_BASELINE.json"
    corrupt("changed_policy_manifest_bytes", manifest,
            (root / manifest).read_bytes() + b"\n", "baseline manifest byte identity changed")

    clean_source = "src/nvda_desk/architecture/_t01_pr14_adversarial_probe.py"
    assert not (root / clean_source).exists()
    corrupt("new_F821_in_other_source", clean_source,
            b"def disposable_negative_case():\n    return totally_undefined_t01_pr14_symbol\n",
            "Ruff findings changed by path")

    assert not git(root, "status", "--porcelain", "--untracked-files=all")
    final_rc, final_txt = cli(root, opts.python, opts.ruff)
    assert final_rc == 0 and "EXACT_MATCH: 51" in final_txt
    results.append({"case":"restored_clean_baseline", "exit":final_rc, "accepted":True})
    print(json.dumps({
        "status":"PASS_ADVERSARIAL_VERIFIER_REFUSALS",
        "disposable_head":SHA,
        "independent_negative_cases":5,
        "product_proof_executed":False,
        "permanent_source_changes":False,
        "worktree_clean_after":True,
        "results":results,
    }, indent=2))


if __name__ == "__main__":
    main()
