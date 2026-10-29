"""Capture planned applied-control checks; never author or admit product proof."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
python = Path(sys.executable).resolve()
output = Path(tempfile.mkdtemp(prefix="nvda-d014-applied-", dir="/tmp"))

def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert not git("status", "--porcelain=v1", "--untracked-files=all")
assert sha(root / "tools/product_proof_claims.py") == (
    "b2670e26f51d4b6f4fc8c656c859b9e5d63ca9aadd84ff2f818ff06cd9bb118a"
), "Stop: reviewed control has not been applied exactly"
assert (root / "config/product_proof/market_measurement_d014/claim.json").is_file()
assert not (root / "tests/product/market_measurement_d014").exists()
assert json.loads((root / "config/product_proof/market_measurement_d014/admission.json").read_text())["current_generation"] is None
head = git("rev-parse", "HEAD")
commands = [
    ("control", ["-m", "pytest", "tests/architecture/test_proof_control.py"], 0, "130 passed"),
    ("mypy", ["-m", "mypy", "src", "tools/product_proof_claims.py", "tools/product_proof_outcomes.py", "tools/validate_product_proof.py", "tools/run_product_proof_gate.py"], 0, "Success: no issues found"),
    ("ruff", ["-m", "ruff", "check", "tools/product_proof_claims.py", "tests/architecture/test_proof_control.py"], 0, "All checks passed!"),
    ("binding", ["tools/validate_implementation_authority.py", "--binding", "implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml", "--brief", "handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md"], 0, "PASS: implementation authority"),
    ("d013", ["tools/run_product_proof_gate.py", "--aggregate", "neutral_market_measurement_truth_d013"], 0, "observed aggregate outcome: exit=0"),
    ("d012", ["tools/run_product_proof_gate.py", "--aggregate", "neutral_market_measurement_truth_d012"], 0, "observed aggregate outcome: exit=0"),
    ("foundation", ["tools/run_product_proof_gate.py", "--aggregate", "neutral_market_measurement_truth_pilot"], 0, "observed aggregate outcome: exit=0"),
    ("raw", ["tools/run_product_proof_gate.py", "--aggregate", "raw_signal_occurrence_truth_sqlite"], 0, "observed aggregate outcome: exit=0"),
    ("d014_null", ["tools/run_product_proof_gate.py", "--aggregate", "neutral_market_measurement_truth_d014"], 4, "INCOMPLETE_NO_PHYSICAL_FAMILIES"),
]
env = os.environ.copy()
temporary = output / "tmp"
temporary.mkdir()
env["TMPDIR"] = str(temporary)
env["PYTHONUNBUFFERED"] = "1"
env["MYPY_CACHE_DIR"] = str(output / "mypy_cache")
env.pop("PYTEST_ADDOPTS", None)
print("OUTPUT", output, "CANDIDATE", head, flush=True)
for name, args, expected_exit, marker in commands:
    assert git("rev-parse", "HEAD") == head
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    argv = [str(python), *args]
    # Use the venv entrypoint, not its resolved base interpreter, for dependencies.
    argv[0] = sys.executable
    record = {"argv": argv, "cwd": str(root), "candidate": head,
              "expected_exit": expected_exit, "expected_marker": marker,
              "exit": None, "completed": False}
    metadata = output / (name + ".json")
    metadata.write_text(json.dumps(record, indent=2) + "\n")
    log = output / (name + ".log")
    print("START", name, flush=True)
    with log.open("xb") as stream:
        result = subprocess.run(argv, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT)
    observed = log.read_bytes()
    record.update(exit=result.returncode, completed=True,
                  log_sha256=sha(log), marker_present=marker.encode() in observed,
                  unchanged_head=git("rev-parse", "HEAD") == head,
                  clean_after=not git("status", "--porcelain=v1", "--untracked-files=all"))
    metadata.write_text(json.dumps(record, indent=2) + "\n")
    print("END", name, json.dumps(record), flush=True)
    if result.returncode != expected_exit or not record["marker_present"] or not record["unchanged_head"] or not record["clean_after"]:
        raise SystemExit("STOP: first failed required invariant in " + name)
print("ALL_PLANNED_APPLIED_CONTROL_CHECKS_OBSERVED", head, output, flush=True)
