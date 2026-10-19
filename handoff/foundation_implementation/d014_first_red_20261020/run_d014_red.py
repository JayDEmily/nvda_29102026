"""Capture one native admitted D014 RED attempt, never mutate or admit proof."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
expected_head = sys.argv[2]


def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode().strip()


assert git("rev-parse", "HEAD") == expected_head
assert not git("status", "--porcelain=v1", "--untracked-files=all")
assert not (root / "src/nvda_desk/market_measurement_truth/_raw_rational.py").exists()
pointer = json.loads((root / "config/product_proof/market_measurement_d014/admission.json").read_bytes())
assert pointer["current_generation"] is not None
generation = root / pointer["current_generation"]["path"]
assert hashlib.sha256(generation.read_bytes()).hexdigest() == pointer["current_generation"]["sha256"]
record = json.loads(generation.read_bytes())
assert record["generation"] == 1 and record["adequacy_review_ref"]
expected = {
    "tests/product/market_measurement_d014/test_raw_ratio.py": "588abd5c69bda15ea1305a12a3bbc35e7fe3f0ed3f57515e7cdd7926524d8db2",
    "tests/product/market_measurement_d014/_support.py": "49c6149d1ff64e002154b275bc9c54793cf60623bb0c9878c0fd5539fbc058e6",
    "tests/product/market_measurement_d014/typing/valid_seam.py": "3d1e2ac2449fc13be7db8f0e26c2b505dee5e6810d591dd190d4044bf859dacc",
    "tests/product/market_measurement_d014/typing/invalid_seam.py": "84b2806f0c8be162321c35f792f987550a3cf2ff428d37edd007042fcc699fc9",
}
assert {item["path"]: item["sha256"] for item in record["family_files"] + record["support_files"]} == expected
for path, digest in expected.items():
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest
output = Path(tempfile.mkdtemp(prefix="nvda-d014-first-red-", dir="/tmp"))
temporary = output / "tmp"
temporary.mkdir()
argv = [sys.executable, "tools/run_product_proof_gate.py", "--aggregate", "neutral_market_measurement_truth_d014"]
metadata = dict(candidate=expected_head, tree=git("rev-parse", "HEAD^{tree}"), argv=argv,
                cwd=str(root), generation_sha256=pointer["current_generation"]["sha256"],
                completed=False, exit=None)
metadata_path = output / "result.json"
metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
env = os.environ.copy()
env.update(TMPDIR=str(temporary), PYTHONUNBUFFERED="1", MYPY_CACHE_DIR=str(output / "mypy-cache"))
env.pop("PYTEST_ADDOPTS", None)
print("FIRST_RED_ATTEMPT", output, expected_head, flush=True)
log = output / "strict.log"
with log.open("xb") as stream:
    result = subprocess.run(argv, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT)
observed = log.read_bytes()
message = b"AssertionError: admitted additive D014 raw-ratio seam is absent"
guard_failures = len(re.findall(rb"^E\s+" + re.escape(message) + rb"\s*$", observed, re.MULTILINE))
metadata.update(completed=True, exit=result.returncode,
                log_sha256=hashlib.sha256(observed).hexdigest(),
                guard_failures=guard_failures,
                actual_collection_202=b"collected 202 items" in observed,
                actual_failed_202=b"202 failed" in observed,
                actual_strict_1=b"observed aggregate outcome: exit=1" in observed,
                unchanged_head=git("rev-parse", "HEAD") == expected_head,
                clean_after=not git("status", "--porcelain=v1", "--untracked-files=all"))
metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
print(json.dumps(metadata, indent=2), flush=True)
assert result.returncode == 1 and metadata["actual_collection_202"] and metadata["actual_failed_202"]
assert metadata["actual_strict_1"] and guard_failures == 202
assert metadata["unchanged_head"] and metadata["clean_after"]
print("INTENDED_ABSENT_ADDITIVE_SEAM_RED_OBSERVED", flush=True)
