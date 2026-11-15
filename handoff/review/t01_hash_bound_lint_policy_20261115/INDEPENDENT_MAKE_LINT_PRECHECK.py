#!/usr/bin/env python3
"""Read-only check of an alternative lint entrypoint on original PR14 head."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess

HEAD = "831471d69afd092779a6810ee570285182be88a8"

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--candidate",type=Path,required=True)
    p.add_argument("--ruff",type=Path,required=True)
    opts=p.parse_args()
    root=opts.candidate.resolve()
    assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip()==HEAD
    assert not subprocess.check_output(["git","status","--porcelain"],cwd=root,text=True)
    env=os.environ.copy()
    env["PATH"]=f"{opts.ruff.resolve().parent}:{env['PATH']}"
    env["PYTHONDONTWRITEBYTECODE"]="1"
    out=subprocess.run(["make","lint"],cwd=root,env=env,text=True,capture_output=True)
    combined=(out.stdout+"\n"+out.stderr).splitlines()
    assert out.returncode != 0
    assert "Found 51 errors." in (out.stdout+out.stderr)
    assert any("Makefile:23: lint" in line for line in combined)
    assert not subprocess.check_output(["git","status","--porcelain"],cwd=root,text=True)
    print(json.dumps({
        "candidate":HEAD,
        "observation":"EXPECTED_DIFFERENT_LINT_ENTRYPOINT",
        "command":"make lint",
        "exit_code":out.returncode,
        "found_errors":51,
        "strict_make_lint_pass":False,
        "sha_bound_workflow_ci_pass_separate":True,
        "worktree_clean_after":True,
        "product_tests_executed":False,
        "output_tail":combined[-13:],
    },indent=2))

if __name__ == "__main__":
    main()
