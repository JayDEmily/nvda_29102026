"""Capture native readiness and two exact already-admitted component witnesses."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
head = "78358831f5159b8f0745baffb01ae49f358432d5"


def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()


assert git("rev-parse", "HEAD") == head
assert not git("status", "--porcelain=v1", "--untracked-files=all")
out = Path(tempfile.mkdtemp(prefix="nvda-d014-component-", dir="/tmp"))
temporary = out / "tmp"
temporary.mkdir()
env = os.environ.copy()
env.update(TMPDIR=str(temporary), PYTHONUNBUFFERED="1")
env.pop("PYTEST_ADDOPTS", None)
commands = [
    ("readiness", ["tools/validate_product_proof.py", "--claim", "neutral_market_measurement_truth_d014"], 0, b"state=READY_FOR_PROOF"),
    ("memory", ["-m", "pytest", "tests/product/market_measurement_d014/test_raw_ratio.py::test_d014_actual_raw_projections_exact_ratio[memory]"], 0, b"1 passed"),
    ("storage_red", ["-m", "pytest", "tests/product/market_measurement_d014/test_raw_ratio.py::test_d014_sqlite_recovery_faults_and_integrity[profile]"], 1, b"AssertionError: admitted isolated D014 SQLite behaviour is absent"),
]
print("COMPONENT_ATTEMPT", out, head, flush=True)
for name, args, expected_exit, marker in commands:
    assert git("rev-parse", "HEAD") == head and not git("status", "--porcelain=v1", "--untracked-files=all")
    argv = [sys.executable, *args]
    record = dict(candidate=head, argv=argv, cwd=str(root), expected_exit=expected_exit,
                  expected_marker=marker.decode(), completed=False, exit=None)
    metadata = out / (name + ".json")
    metadata.write_text(json.dumps(record, indent=2) + "\n")
    log = out / (name + ".log")
    with log.open("xb") as stream:
        result = subprocess.run(argv, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT)
    data = log.read_bytes()
    record.update(completed=True, exit=result.returncode, marker_present=marker in data,
                  log_sha256=hashlib.sha256(data).hexdigest(), unchanged_head=git("rev-parse", "HEAD") == head,
                  clean_after=not git("status", "--porcelain=v1", "--untracked-files=all"))
    metadata.write_text(json.dumps(record, indent=2) + "\n")
    print(name, json.dumps(record), flush=True)
    if result.returncode != expected_exit or not record["marker_present"] or not record["unchanged_head"] or not record["clean_after"]:
        raise SystemExit("STOP_FIRST_FAILED_COMPONENT_INVARIANT " + name)
print("ADMITTED_MEMORY_GREEN_AND_EXPLICIT_MISSING_STORAGE_RED_OBSERVED", flush=True)
