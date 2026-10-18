import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from nvda_desk.architecture.proof import load_and_validate_proof_state

ROOT = Path(__file__).resolve().parents[2]


def _controls():
    # An attributable missing-capability assertion, after the interpreter and
    # existing kernel imports are established. Never call import failure RED.
    assert (ROOT / "tools/product_proof_claims.py").is_file(), "claim resolver is not implemented"
    if str(ROOT / "tools") not in sys.path:
        sys.path.insert(0, str(ROOT / "tools"))
    return importlib.import_module("product_proof_claims")


def _copy_candidate(tmp_path):
    for name in ("config", "schemas", "docs", "tests", "implementation", "handoff", "src"):
        shutil.copytree(ROOT / name, tmp_path / name)
    shutil.copytree(ROOT / "tools", tmp_path / "tools")
    for name in ("pyproject.toml", "GUARDRAILS.md", "AGENTS.md", ".gitignore"):
        shutil.copy2(ROOT / name, tmp_path / name)
    return tmp_path


def _json_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _control_generation(root, claim_id="raw_signal_occurrence_truth_sqlite", body=None):
    # These are temporary control canaries, never actual admitted product proof.
    catalogue = json.loads((root / "config/product_proof/claims.json").read_text())
    entry = next(c for c in catalogue["claims"] if c["claim_id"] == claim_id)
    contract = json.loads((root / entry["contract_path"]).read_text())
    rows = []
    for family in contract["families"]:
        path = root / family["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        code = "\n".join(
            f"def {name}():\n    {body or 'assert 7 * 6 == 42'}\n"
            for name in family["required_test_names"]
        )
        path.write_text(code, encoding="utf-8")
        rows.append({"path": family["path"], "sha256": _sha(path)})
    support = []
    for name in contract["required_support_files"]:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Temporary control-fixture support only.\n", encoding="utf-8")
        support.append({"path": name, "sha256": _sha(path)})
    generation = {
        "schema_version": "1.0",
        "claim_id": claim_id,
        "generation": 1,
        "brief_sha256": _sha(root / contract["semantic_brief_path"]),
        "binding_sha256": _sha(root / entry["binding_path"]),
        "contract_sha256": _sha(root / entry["contract_path"]),
        "implementation_target_id": "M00",
        "adequacy_review_ref": "control-fixture/review",
        "admission_authority_ref": "control-fixture/admission",
        "family_files": rows,
        "support_files": support,
        "previous_generation": None,
    }
    path = Path(entry["admission_path"]).parent / "generations/0001.json"
    _json_write(root / path, generation)
    _json_write(
        root / entry["admission_path"],
        {
            "schema_version": "1.0",
            "current_generation": {"path": path.as_posix(), "sha256": _sha(root / path)},
        },
    )
    return entry, contract, generation, path


def test_legacy_m00_claim_is_preserved():
    api = _controls()
    claim = api.load_product_proof_claim(ROOT, "raw_signal_occurrence_truth_product")
    assert claim.state == "HISTORICAL_NOT_RUNNABLE"
    assert len(claim.families) == 6
    assert len({p for f in claim.families for p in f.proof_ids}) == 13


def test_foundation_claim_is_separate():
    api = _controls()
    raw = api.load_product_proof_claim(ROOT, "raw_signal_occurrence_truth_sqlite")
    foundation = api.load_product_proof_claim(ROOT, "neutral_market_measurement_truth_pilot")
    assert len(raw.families) == 4 and len(foundation.families) == 5
    assert {p for f in foundation.families for p in f.proof_ids} == {
        f"FND-P{n:02}" for n in range(1, 8)
    }
    assert not ({f.path for f in raw.families} & {f.path for f in foundation.families})


@pytest.mark.parametrize("surface", ["brief", "contract", "binding", "catalogue", "admission"])
def test_native_brief_and_companion_bytes_are_bound(tmp_path, surface):
    api = _controls()
    root = _copy_candidate(tmp_path)
    api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")
    names = {
        "brief": (
            "handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md"
        ),
        "contract": (
            "handoff/foundation_implementation/authority/M00_SQLITE_PROOF_CONTRACT_PROPOSED.json"
        ),
        "binding": "implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml",
        "catalogue": "config/product_proof/claims.json",
        "admission": "config/product_proof/raw_signal_sqlite/admission.json",
    }
    path = root / names[surface]
    path.write_bytes(path.read_bytes() + (b"\ncorrupt" if surface == "admission" else b"\n"))
    if surface == "binding":
        path.write_text(path.read_text().replace("ACCEPTED_FOR_IMPLEMENTATION", "NOT_ACCEPTED"))
    with pytest.raises(ValueError):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


def test_physical_product_partition_is_complete(tmp_path):
    api = _controls()
    root = _copy_candidate(tmp_path)
    api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")
    extra = root / "tests/product/derived_signal/nested/test_counterfeit.py"
    extra.parent.mkdir()
    extra.write_text("def test_counterfeit(): assert True\n")
    with pytest.raises(ValueError, match="unowned"):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


def test_pending_authority_target_and_empty_proof_are_not_success():
    api = _controls()
    assert api.load_product_proof_claim(ROOT, "raw_signal_occurrence_truth_sqlite").state == (
        "INCOMPLETE_NO_PHYSICAL_FAMILIES"
    )
    assert api.load_product_proof_claim(ROOT, "neutral_market_measurement_truth_pilot").state == (
        "AWAITING_TARGET"
    )


def test_target_status_does_not_make_red_circular(tmp_path):
    api = _controls()
    root = _copy_candidate(tmp_path)
    import yaml

    path = root / "config/architecture/modules.yaml"
    doc = yaml.safe_load(path.read_text())
    target = dict(doc["modules"][1])
    target.update(
        id="M02",
        name="neutral_market_measurement_truth",
        status="bootstrap",
        package="nvda_desk.market_measurement_truth",
        public_seam="nvda_desk.market_measurement_truth.api",
    )
    doc["modules"].append(target)
    path.write_text(yaml.safe_dump(doc))
    path = root / "config/architecture/implementation_allocations.yaml"
    allocations = yaml.safe_load(path.read_text())
    allocations["implementation_allocations"].append(
        {
            "object_id": "M02",
            "name": "neutral_market_measurement_truth",
            "implemented_on": "2026-10-19",
        }
    )
    path.write_text(yaml.safe_dump(allocations))
    claim = api.load_product_proof_claim(root, "neutral_market_measurement_truth_pilot")
    assert claim.target_id == "M02" and claim.target_status == "bootstrap"
    assert claim.state == "INCOMPLETE_NO_PHYSICAL_FAMILIES"


def test_proof_generation_hash_and_supersession(tmp_path):
    api = _controls()
    root = _copy_candidate(tmp_path)
    _, contract, _, _ = _control_generation(root)
    assert api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite").state == (
        "READY_FOR_PROOF"
    )
    path = root / contract["families"][0]["path"]
    path.write_text(path.read_text() + "# changed after admission\n")
    with pytest.raises(ValueError, match="hash"):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


def _run_control_probe(root):
    env = dict(os.environ, PYTHONPATH=str(root / "tools") + os.pathsep + str(root / "src"))
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Control fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "temporary control canary",
        ],
        cwd=root,
        check=True,
    )
    return subprocess.run(
        [sys.executable, str(root / "tools/run_product_proof_gate.py")],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
    )


def test_aggregate_collects_all_required_proof(tmp_path):
    _controls()
    root = _copy_candidate(tmp_path)
    _, contract, _, _ = _control_generation(root)
    path = root / contract["families"][0]["path"]
    path.write_text("def test_wrong_name(): assert True\n")
    # Reseal only this deliberately constructed temporary control fixture.
    # Production generations may never be edited this way.
    _reseal_control_fixture(root, path)
    result = _run_control_probe(root)
    assert result.returncode == 5, result.stdout + result.stderr


def _reseal_control_fixture(root, path):
    pointer_path = root / "config/product_proof/raw_signal_sqlite/admission.json"
    pointer = json.loads(pointer_path.read_text())
    generation_path = root / pointer["current_generation"]["path"]
    generation = json.loads(generation_path.read_text())
    for row in generation["family_files"]:
        if row["path"] == path.relative_to(root).as_posix():
            row["sha256"] = _sha(path)
    _json_write(generation_path, generation)
    pointer["current_generation"]["sha256"] = _sha(generation_path)
    _json_write(pointer_path, pointer)


@pytest.mark.parametrize(
    "body",
    [
        "__import__('pytest').skip('control canary')",
        "__import__('pytest').xfail('control canary')",
        "xpass",
    ],
)
def test_skipped_xfailed_and_xpassed_proof_cannot_pass(tmp_path, body):
    _controls()
    root = _copy_candidate(tmp_path)
    _, contract, _, _ = _control_generation(root, body="assert True" if body == "xpass" else body)
    if body == "xpass":
        for family in contract["families"]:
            path = root / family["path"]
            path.write_text(
                "import pytest\npytestmark = pytest.mark.xfail(strict=False)\n" + path.read_text()
            )
            _reseal_control_fixture(root, path)
    result = _run_control_probe(root)
    assert result.returncode == 1, result.stdout + result.stderr


def test_outcome_report_is_fresh_and_exact():
    _controls()
    outcomes = importlib.import_module("product_proof_outcomes")
    assert outcomes.validate_outcomes({}, "fresh", {}, 0) != 0
    report = {
        "nonce": "old",
        "collected": ["x.py::test_x"],
        "outcomes": {},
        "collection_errors": [],
        "deselected": [],
        "exitstatus": 0,
    }
    assert outcomes.validate_outcomes(report, "fresh", {"x.py": ("test_x",)}, 0) != 0


def test_governed_mutation_and_dirty_start_fail_closed(tmp_path):
    _controls()
    root = _copy_candidate(tmp_path)
    _control_generation(root)
    assert _run_control_probe(root).returncode == 0
    (root / "unexpected.txt").write_text("dirty start")
    env = dict(os.environ, PYTHONPATH=str(root / "tools") + os.pathsep + str(root / "src"))
    result = subprocess.run(
        [sys.executable, str(root / "tools/run_product_proof_gate.py")],
        cwd=root,
        env=env,
        capture_output=True,
    )
    assert result.returncode == 2


def test_claim_membership_is_registry_derived():
    api = _controls()
    with pytest.raises(ValueError, match="unknown"):
        api.load_product_proof_claim(ROOT, "counterfeit")


def test_historical_backend_is_accounted_but_not_executable(tmp_path):
    api = _controls()
    claim = api.load_product_proof_claim(ROOT, "raw_signal_occurrence_truth_product")
    assert claim.state == "HISTORICAL_NOT_RUNNABLE" and len(claim.families) == 6


def test_sqlite_claim_target_uses_existing_m00_modify_intent(tmp_path):
    api = _controls()
    root = _copy_candidate(tmp_path)
    assert (
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite").target_id == "M00"
    )
    path = root / "implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml"
    path.write_text(path.read_text().replace("object_id: A00", "object_id: M01"))
    with pytest.raises(ValueError, match="intent"):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


def test_sqlite_claim_generations_do_not_cross_certify(tmp_path):
    api = _controls()
    root = _copy_candidate(tmp_path)
    _, _, generation, path = _control_generation(root)
    generation["claim_id"] = "neutral_market_measurement_truth_pilot"
    _json_write(root / path, generation)
    pointer = root / "config/product_proof/raw_signal_sqlite/admission.json"
    value = json.loads(pointer.read_text())
    value["current_generation"]["sha256"] = _sha(root / path)
    _json_write(pointer, value)
    with pytest.raises(ValueError, match="claim"):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


def test_sqlite_default_and_m00_regression_are_explicit(tmp_path):
    _controls()
    root = _copy_candidate(tmp_path)
    _control_generation(root)
    result = _run_control_probe(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "raw_signal_occurrence_truth_sqlite" in result.stdout


def test_sqlite_current_and_historical_paths_partition_exactly(tmp_path):
    api = _controls()
    root = _copy_candidate(tmp_path)
    assert len(list((root / "tests/product").rglob("test_*.py"))) == 93
    api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")
    target = root / "tests/product/derived_signal/test_escape.py"
    target.symlink_to(root / "tests/architecture/test_proof_control.py")
    with pytest.raises(ValueError, match=r"symlink|unowned"):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


@pytest.mark.parametrize(
    "mutation", ["retained_config", "retained_test", "unowned_helper", "generation_rollback"]
)
def test_sqlite_integrity_falsifiers(tmp_path, mutation):
    api = _controls()
    root = _copy_candidate(tmp_path)
    api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")
    if mutation == "retained_config":
        path = root / "config/product_proof/authority.yaml"
        path.write_text(path.read_text() + "\n# changed preserved bytes\n")
    elif mutation == "retained_test":
        path = root / "tests/product/raw_signal/test_u01_contract_owner_boundary.py"
        path.write_text(path.read_text() + "\n# changed preserved bytes\n")
    elif mutation == "unowned_helper":
        path = root / "tests/product/raw_signal_sqlite/hidden_helper.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("VALUE = 1\n")
    else:
        entry, _, generation, _ = _control_generation(root)
        pointer = json.loads((root / entry["admission_path"]).read_text())
        generation["generation"] = 2
        generation["previous_generation"] = pointer["current_generation"]
        _json_write(
            root / Path(entry["admission_path"]).parent / "generations/0002.json", generation
        )
    with pytest.raises(ValueError):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


@pytest.mark.parametrize(
    "mutation",
    ["cycle", "missing_predecessor", "wrong_target", "empty_review", "support", "revocation"],
)
def test_generation_failure_and_revocation(tmp_path, mutation):
    api = _controls()
    root = _copy_candidate(tmp_path)
    entry, _, record, name = _control_generation(root)
    assert api.load_product_proof_claim(root, entry["claim_id"]).state == "READY_FOR_PROOF"
    pointer_path = root / entry["admission_path"]
    pointer = json.loads(pointer_path.read_text())
    if mutation == "revocation":
        pointer["current_generation"] = None
        _json_write(pointer_path, pointer)
        assert (root / name).is_file()
        assert api.load_product_proof_claim(root, entry["claim_id"]).state == "INCOMPLETE_COVERAGE"
        return
    if mutation == "cycle":
        record["previous_generation"] = pointer["current_generation"]
    elif mutation == "missing_predecessor":
        record["generation"] = 2
    elif mutation == "wrong_target":
        record["implementation_target_id"] = "M01"
    elif mutation == "empty_review":
        record["adequacy_review_ref"] = ""
    else:
        (root / record["support_files"][0]["path"]).write_text("changed support\n")
    _json_write(root / name, record)
    pointer["current_generation"]["sha256"] = _sha(root / name)
    _json_write(pointer_path, pointer)
    with pytest.raises(ValueError):
        api.load_product_proof_claim(root, entry["claim_id"])


def test_mutation_during_observed_run_is_rejected(tmp_path):
    _controls()
    root = _copy_candidate(tmp_path)
    _control_generation(
        root,
        body=(
            "__import__('pathlib').Path('config/product_proof/claims.json').write_text('mutated')"
        ),
    )
    result = _run_control_probe(root)
    assert result.returncode == 6, result.stdout + result.stderr


def test_outcome_positive_and_phase_corruption():
    _controls()
    import copy

    outcomes = importlib.import_module("product_proof_outcomes")
    positive = {
        "nonce": "fresh",
        "collected": ["x.py::test_x"],
        "collection_errors": [],
        "deselected": [],
        "exitstatus": 0,
        "outcomes": {
            "x.py::test_x": [
                {"when": phase, "outcome": "passed", "wasxfail": False}
                for phase in ("setup", "call", "teardown")
            ]
        },
    }
    assert outcomes.validate_outcomes(positive, "fresh", {"x.py": ("test_x",)}, 0) == 0
    for mutation in ("missing_phase", "skip", "xfail", "wrong_node", "wrong_exit", "deselect"):
        probe = copy.deepcopy(positive)
        if mutation == "missing_phase":
            probe["outcomes"]["x.py::test_x"].pop()
        elif mutation == "skip":
            probe["outcomes"]["x.py::test_x"][1]["outcome"] = "skipped"
        elif mutation == "xfail":
            probe["outcomes"]["x.py::test_x"][1]["wasxfail"] = True
        elif mutation == "wrong_node":
            probe["collected"] = ["other.py::test_x"]
        elif mutation == "wrong_exit":
            probe["exitstatus"] = 1
        else:
            probe["deselected"] = ["x.py::test_x"]
        assert outcomes.validate_outcomes(probe, "fresh", {"x.py": ("test_x",)}, 0) != 0


def test_current_proof_population_is_exact_and_registry_derived() -> None:
    state = load_and_validate_proof_state(ROOT)
    assert len(state.families) == 11
    assert len(state.paths_for_set("architecture_kernel")) == 11
    assert {family["tier"] for family in state.families} == {"Tier A"}
    assert {family["lifecycle"] for family in state.families} == {"current_blocking"}


def test_unadmitted_physical_test_is_rejected(tmp_path: Path) -> None:
    for name in ("config", "schemas", "docs", "tests"):
        source = ROOT / name
        target = tmp_path / name
        if source.is_dir():
            shutil.copytree(source, target)
    extra = tmp_path / "tests/architecture/test_unadmitted.py"
    extra.write_text("def test_unadmitted(): assert True\n", encoding="utf-8")
    with pytest.raises(ValueError, match="test admission mismatch"):
        load_and_validate_proof_state(tmp_path)


def test_unadmitted_nested_physical_test_is_rejected(tmp_path: Path) -> None:
    for name in ("config", "schemas", "docs", "tests"):
        source = ROOT / name
        target = tmp_path / name
        if source.is_dir():
            shutil.copytree(source, target)
    extra = tmp_path / "tests/architecture/nested/test_unadmitted_nested.py"
    extra.parent.mkdir(parents=True)
    extra.write_text("def test_unadmitted_nested(): assert True\n", encoding="utf-8")
    with pytest.raises(ValueError, match="test admission mismatch"):
        load_and_validate_proof_state(tmp_path)
