"""Serial planned engineering checks; stop before any dependent check after failure."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
head = git_head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"]).decode().strip()


def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()


assert git("rev-parse", "HEAD") == head
assert not git("status", "--porcelain=v1", "--untracked-files=all")
out = Path(tempfile.mkdtemp(prefix="nvda-d014-engineering-", dir="/tmp"))
temporary = out / "tmp"
temporary.mkdir()
env = os.environ.copy()
env.update(TMPDIR=str(temporary), PYTHONUNBUFFERED="1", MYPY_CACHE_DIR=str(out / "mypy-cache"))
env.pop("PYTEST_ADDOPTS", None)
family = "tests/product/market_measurement_d014/test_raw_ratio.py::"
commands = [
    ("readiness", ["tools/validate_product_proof.py", "--claim", "neutral_market_measurement_truth_d014"], b"state=READY_FOR_PROOF"),
    ("mypy", ["-m", "mypy", "src", "tools/product_proof_claims.py", "tools/product_proof_outcomes.py", "tools/validate_product_proof.py", "tools/run_product_proof_gate.py"], b"Success: no issues found"),
    ("p01_p04", ["-m", "pytest", family + "test_d014_actual_raw_projections_exact_ratio", family + "test_d014_selection_and_refusal", family + "test_d014_exact_ratio_arithmetic_domain", family + "test_d014_identity_versions_and_later_retry"], b"173 passed"),
    ("p05", ["-m", "pytest", family + "test_d014_sqlite_recovery_faults_and_integrity"], b"28 passed"),
    ("p06", ["-m", "pytest", family + "test_d014_additive_types_and_legacy_preservation"], b"1 passed"),
    ("strict", ["tools/run_product_proof_gate.py", "--aggregate", "neutral_market_measurement_truth_d014"], b"observed aggregate outcome: exit=0"),
]
print("ENGINEERING_ATTEMPT", out, head, flush=True)
for name, args, marker in commands:
    assert git("rev-parse", "HEAD") == head and not git("status", "--porcelain=v1", "--untracked-files=all")
    argv = [sys.executable, *args]
    record = dict(candidate=head, tree=git("rev-parse", "HEAD^{tree}"), argv=argv, cwd=str(root), completed=False, exit=None, expected_marker=marker.decode())
    metadata = out / (name + ".json")
    metadata.write_text(json.dumps(record, indent=2) + "\n")
    log = out / (name + ".log")
    print("START", name, flush=True)
    with log.open("xb") as stream:
        result = subprocess.run(argv, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT)
    data = log.read_bytes()
    record.update(completed=True, exit=result.returncode, marker_present=marker in data,
                  log_sha256=hashlib.sha256(data).hexdigest(), unchanged_head=git("rev-parse", "HEAD") == head,
                  clean_after=not git("status", "--porcelain=v1", "--untracked-files=all"))
    metadata.write_text(json.dumps(record, indent=2) + "\n")
    print("END", name, json.dumps(record), flush=True)
    if result.returncode != 0 or not record["marker_present"] or not record["unchanged_head"] or not record["clean_after"]:
        raise SystemExit("STOP_FIRST_FAILED_ENGINEERING_INVARIANT " + name)
print("ALL_PLANNED_NEW_ENGINEERING_CHECKS_OBSERVED", head, out, flush=True)

