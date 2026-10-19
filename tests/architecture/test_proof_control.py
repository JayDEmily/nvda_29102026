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

D012_CLAIM = "neutral_market_measurement_truth_d012"
D012_ROOT = "config/product_proof/market_measurement_d012"
D012_BRIEF = (
    "handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md"
)
D012_CONTRACT = "handoff/foundation_implementation/authority/G6_1_D012_PROOF_CONTRACT_PROPOSED.json"
D012_BINDING = "implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml"

D013_CLAIM = "neutral_market_measurement_truth_d013"
D013_ROOT = "config/product_proof/market_measurement_d013"
D013_BRIEF = (
    "handoff/foundation_implementation/authority/G6_1_D013_IMPLEMENTATION_BRIEF_PROPOSED.md"
)
D013_CONTRACT = "handoff/foundation_implementation/authority/G6_1_D013_PROOF_CONTRACT_PROPOSED.json"
D013_BINDING = "implementation/authority/G6_1_D013_IMPLEMENTATION_AUTHORITY_BINDING.yaml"


def _d013_descriptor():
    return {
        "schema_version": "1.0",
        "claim_id": D013_CLAIM,
        "brief_path": D013_BRIEF,
        "binding_path": D013_BINDING,
        "contract_path": D013_CONTRACT,
        "physical_root": "tests/product/market_measurement_d013",
        "admission_path": D013_ROOT + "/admission.json",
    }


def _d013_control_candidate(tmp_path, body="assert 7 * 6 == 42"):
    # Retain the separately valid D012 extension too: this is a combined
    # physical partition, not a fixture that makes the earlier extension absent.
    root = _d012_control_candidate(tmp_path)
    assert (root / D012_ROOT / "claim.json").read_bytes() == (
        ROOT / D012_ROOT / "claim.json"
    ).read_bytes()
    entry = _d013_descriptor()
    _json_write(root / D013_ROOT / "claim.json", entry)
    contract = json.loads((root / D013_CONTRACT).read_text())
    rows = []
    for family in contract["families"]:
        path = root / family["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(f"def {name}():\n    {body}\n" for name in family["required_test_names"])
        )
        rows.append({"path": family["path"], "sha256": _sha(path)})
    support = []
    for name in contract["required_support_files"]:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Disposable D013 control canary, not domain proof.\n")
        support.append({"path": name, "sha256": _sha(path)})
    generation = {
        "schema_version": "1.0",
        "claim_id": D013_CLAIM,
        "generation": 1,
        "brief_sha256": _sha(root / D013_BRIEF),
        "binding_sha256": _sha(root / D013_BINDING),
        "contract_sha256": _sha(root / D013_CONTRACT),
        "implementation_target_id": "M02",
        "adequacy_review_ref": "control-fixture/d013-review",
        "admission_authority_ref": "control-fixture/d013-admission",
        "family_files": rows,
        "support_files": support,
        "previous_generation": None,
    }
    path = root / D013_ROOT / "generations/0001.json"
    _json_write(path, generation)
    _json_write(
        root / entry["admission_path"],
        {
            "schema_version": "1.0",
            "current_generation": {
                "path": path.relative_to(root).as_posix(),
                "sha256": _sha(path),
            },
        },
    )
    return root


@pytest.mark.parametrize(
    "claim_id,directory",
    [
        ("raw_signal_occurrence_truth_sqlite", "raw_signal_sqlite"),
        ("neutral_market_measurement_truth_pilot", "market_measurement"),
        (D012_CLAIM, "market_measurement_d012"),
    ],
)
@pytest.mark.parametrize("transition", ["advance", "revoke"])
def test_d013_preservation_allows_lawful_generation_transitions(
    tmp_path, monkeypatch, claim_id, directory, transition
):
    # Copy actual current proof/target state, unlike the pre-admission canary
    # helper. Mutations below never operate on the actual repository.
    root = tmp_path / "current"
    root.mkdir()
    for name in ("config", "schemas", "docs", "tests", "implementation", "handoff", "src", "tools"):
        shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("pyproject.toml", "GUARDRAILS.md", "AGENTS.md", ".gitignore"):
        shutil.copy2(ROOT / name, root / name)
    api = _controls()
    assert api.load_product_proof_claim(root, claim_id).state == "READY_FOR_PROOF"
    pointer = root / "config/product_proof" / directory / "admission.json"
    original = json.loads(pointer.read_text())["current_generation"]
    old_generation = root / original["path"]
    old_bytes = old_generation.read_bytes()
    if transition == "advance":
        generation = json.loads(old_bytes)
        generation.update(
            generation=generation["generation"] + 1,
            previous_generation=original,
            adequacy_review_ref="control-fixture/fresh-transition-review",
            admission_authority_ref="control-fixture/fresh-transition-admission",
        )
        path = pointer.parent / "generations" / f"{generation['generation']:04d}.json"
        assert not path.exists()
        _json_write(path, generation)
        _json_write(
            pointer,
            {
                "schema_version": "1.0",
                "current_generation": {
                    "path": path.relative_to(root).as_posix(),
                    "sha256": _sha(path),
                },
            },
        )
        claim = api.load_product_proof_claim(root, claim_id)
        assert claim.state == "READY_FOR_PROOF" and claim.generation_sha256 == _sha(path)
    else:
        _json_write(pointer, {"schema_version": "1.0", "current_generation": None})
        assert api.load_product_proof_claim(root, claim_id).state == "INCOMPLETE_COVERAGE"
    assert old_generation.read_bytes() == old_bytes
    monkeypatch.setitem(globals(), "ROOT", root)
    # The preservation proposition must still hold with either lawful state;
    # one checkpoint's pointer/status is not permanent admission law.
    test_d013_actual_original_claim_generations_are_preserved()
    assert old_generation.read_bytes() == old_bytes


def test_d013_actual_original_claim_generations_are_preserved():
    api = _controls()
    for claim_id, expected in (
        (
            "raw_signal_occurrence_truth_sqlite",
            "51e87129c2a31c71599b7a01beb8ba39717ed5118a4d5c849bcb2015b6c80c6f",
        ),
        (
            "neutral_market_measurement_truth_pilot",
            "24a5af4054c277b01a140ec43481e86851e5e76263826644a80993c12c2495b7",
        ),
        (D012_CLAIM, "26d2b4e371c38b0960cb6081798cc618c9f308567d0df12b2aa40f3777dd2a25"),
    ):
        claim = api.load_product_proof_claim(ROOT, claim_id)
        assert claim.state == "READY_FOR_PROOF" and claim.generation_sha256 == expected


@pytest.mark.parametrize(
    "name", ["_support.py", "nested/helper.py", "test_orphan.py", "dangling.py"]
)
def test_d013_absent_descriptor_rejects_all_python_ownership(tmp_path, name):
    api = _controls()
    root = _d012_control_candidate(tmp_path)
    originals = (
        "raw_signal_occurrence_truth_sqlite",
        "neutral_market_measurement_truth_pilot",
        D012_CLAIM,
    )
    for claim_id in originals:
        api.load_product_proof_claim(root, claim_id)
    path = root / "tests/product/market_measurement_d013" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if name == "dangling.py":
        path.symlink_to("absent-target.py")
    else:
        path.write_text("# Undeclared Python source, no D013 descriptor.\n")
    for claim_id in originals:
        with pytest.raises(ValueError, match=r"unowned|symlink"):
            api.load_product_proof_claim(root, claim_id)


def test_d013_combined_extensions_resolve_without_resealing(tmp_path):
    api = _controls()
    root = _d013_control_candidate(tmp_path)
    original_bytes = {
        name: (root / name).read_bytes()
        for name in (
            "config/product_proof/claims.json",
            "implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml",
            D012_BINDING,
            D012_ROOT + "/claim.json",
            D012_ROOT + "/generations/0001.json",
        )
    }
    for claim_id, brief in ((D012_CLAIM, D012_BRIEF), (D013_CLAIM, D013_BRIEF)):
        claim = api.load_product_proof_claim(root, claim_id)
        assert claim.state == "READY_FOR_PROOF" and claim.target_id == "M02"
        assert claim.authority_sha256 == _sha(ROOT / brief)
        assert len(claim.families) == 1 and len(claim.families[0].proof_ids) == 6
    for claim_id in (
        "raw_signal_occurrence_truth_sqlite",
        "neutral_market_measurement_truth_pilot",
    ):
        assert (
            api.load_product_proof_claim(root, claim_id).state == "INCOMPLETE_NO_PHYSICAL_FAMILIES"
        )
    for name, expected in original_bytes.items():
        assert (root / name).read_bytes() == expected


@pytest.mark.parametrize(
    "surface",
    [
        "extra_key",
        "overlap",
        "wrong_claim",
        "wrong_target",
        "intents",
        "brief",
        "binding",
        "contract",
        "generation_claim",
        "generation_target",
        "unowned",
        "missing_binding",
        "support_hash",
    ],
)
def test_d013_extension_corruption_rejects_every_selected_claim(tmp_path, surface):
    api = _controls()
    root = _d013_control_candidate(tmp_path)
    assert api.load_product_proof_claim(root, D013_CLAIM).state == "READY_FOR_PROOF"
    if surface in {"extra_key", "overlap", "wrong_claim"}:
        descriptor = _d013_descriptor()
        descriptor.update(
            {
                "extra_key": {"extra": True},
                "overlap": {"physical_root": "tests/product/market_measurement_d012"},
                "wrong_claim": {"claim_id": D012_CLAIM},
            }[surface]
        )
        _json_write(root / D013_ROOT / "claim.json", descriptor)
    elif surface in {"generation_claim", "generation_target"}:
        path = root / D013_ROOT / "generations/0001.json"
        value = json.loads(path.read_text())
        value["claim_id" if surface == "generation_claim" else "implementation_target_id"] = (
            D012_CLAIM if surface == "generation_claim" else "M00"
        )
        _json_write(path, value)
        _json_write(
            root / D013_ROOT / "admission.json",
            {
                "schema_version": "1.0",
                "current_generation": {
                    "path": path.relative_to(root).as_posix(),
                    "sha256": _sha(path),
                },
            },
        )
    elif surface == "unowned":
        (root / "tests/product/market_measurement_d013/nested_helper.py").write_text("pass\n")
    elif surface == "support_hash":
        (root / "tests/product/market_measurement_d013/_support.py").write_text("changed\n")
    elif surface == "missing_binding":
        (root / D013_BINDING).unlink()
    elif surface in {"wrong_target", "intents"}:
        path = root / D013_BINDING
        path.write_text(
            path.read_text().replace("M02", "M00")
            if surface == "wrong_target"
            else path.read_text().replace("G01", "A00")
        )
    else:
        path = (
            root
            / {"brief": D013_BRIEF, "binding": D013_BINDING, "contract": D013_CONTRACT}[surface]
        )
        path.write_bytes(path.read_bytes() + b"\n")
    for claim_id in (
        "raw_signal_occurrence_truth_sqlite",
        "neutral_market_measurement_truth_pilot",
        D012_CLAIM,
        D013_CLAIM,
    ):
        with pytest.raises((ValueError, OSError)):
            api.load_product_proof_claim(root, claim_id)


def test_d013_null_generation_is_incomplete_not_success(tmp_path):
    root = _d013_control_candidate(tmp_path)
    _json_write(
        root / D013_ROOT / "admission.json", {"schema_version": "1.0", "current_generation": None}
    )
    assert _controls().load_product_proof_claim(root, D013_CLAIM).state == "INCOMPLETE_COVERAGE"


@pytest.mark.parametrize(
    "body,expected",
    [
        ("assert 7 * 6 == 42", 0),
        ("import pytest; pytest.skip('control canary')", 1),
        ("from pathlib import Path; Path('GUARDRAILS.md').write_text('fixture mutation')", 6),
    ],
)
def test_d013_direct_strict_outcomes(tmp_path, body, expected):
    _controls()
    root = _d013_control_candidate(tmp_path, body)
    result = _run_control_probe(root, D013_CLAIM)
    assert result.returncode == expected, result.stdout + result.stderr


def _d012_descriptor():
    return {
        "schema_version": "1.0",
        "claim_id": D012_CLAIM,
        "brief_path": D012_BRIEF,
        "binding_path": D012_BINDING,
        "contract_path": D012_CONTRACT,
        "physical_root": "tests/product/market_measurement_d012",
        "admission_path": D012_ROOT + "/admission.json",
    }


def _d012_control_candidate(tmp_path, body="assert 7 * 6 == 42"):
    root = _copy_candidate(tmp_path)
    # Existing target and original pre-admission controls are independent facts.
    for name in ("modules.yaml", "implementation_allocations.yaml", "dependency_rules.yaml"):
        shutil.copy2(ROOT / "config/architecture" / name, root / "config/architecture" / name)
    entry = _d012_descriptor()
    _json_write(root / D012_ROOT / "claim.json", entry)
    contract = json.loads((root / D012_CONTRACT).read_text())
    rows = []
    for family in contract["families"]:
        path = root / family["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(f"def {name}():\n    {body}\n" for name in family["required_test_names"])
        )
        rows.append({"path": family["path"], "sha256": _sha(path)})
    support = []
    for name in contract["required_support_files"]:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Disposable control witness, not domain proof.\n")
        support.append({"path": name, "sha256": _sha(path)})
    generation = {
        "schema_version": "1.0",
        "claim_id": D012_CLAIM,
        "generation": 1,
        "brief_sha256": _sha(root / D012_BRIEF),
        "binding_sha256": _sha(root / D012_BINDING),
        "contract_sha256": _sha(root / D012_CONTRACT),
        "implementation_target_id": "M02",
        "adequacy_review_ref": "control-fixture/d012-review",
        "admission_authority_ref": "control-fixture/d012-admission",
        "family_files": rows,
        "support_files": support,
        "previous_generation": None,
    }
    path = root / D012_ROOT / "generations/0001.json"
    _json_write(path, generation)
    _json_write(
        root / entry["admission_path"],
        {
            "schema_version": "1.0",
            "current_generation": {
                "path": path.relative_to(root).as_posix(),
                "sha256": _sha(path),
            },
        },
    )
    return root


@pytest.mark.parametrize("name", ["_support.py", "nested/helper.py", "test_orphan.py"])
def test_d012_absent_descriptor_cannot_hide_unowned_python(tmp_path, name):
    api = _controls()
    root = _copy_candidate(tmp_path)
    api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")
    path = root / "tests/product/market_measurement_d012" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Unowned extension source, no descriptor.\n")
    with pytest.raises(ValueError, match="unowned"):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


def test_d012_extension_resolves_without_resealing_original_claims(tmp_path):
    api = _controls()
    root = _d012_control_candidate(tmp_path)
    claim = api.load_product_proof_claim(root, D012_CLAIM)
    assert claim.state == "READY_FOR_PROOF" and claim.target_id == "M02"
    assert claim.authority_sha256 == _sha(ROOT / D012_BRIEF)
    assert len(claim.families) == 1 and len(claim.families[0].proof_ids) == 6
    assert (root / "config/product_proof/claims.json").read_bytes() == (
        ROOT / "config/product_proof/claims.json"
    ).read_bytes()
    for original in (
        "raw_signal_occurrence_truth_sqlite",
        "neutral_market_measurement_truth_pilot",
    ):
        resolved = api.load_product_proof_claim(root, original)
        assert resolved.authority_sha256 == _sha(
            ROOT
            / "handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md"
        )
        assert resolved.state == "INCOMPLETE_NO_PHYSICAL_FAMILIES"


@pytest.mark.parametrize(
    "surface",
    [
        "extra_key",
        "overlap",
        "wrong_claim",
        "wrong_target",
        "intents",
        "brief",
        "binding",
        "contract",
        "generation_claim",
        "generation_target",
        "unowned",
        "missing_binding",
    ],
)
def test_d012_extension_corruption_rejects_even_original_claim(tmp_path, surface):
    api = _controls()
    root = _d012_control_candidate(tmp_path)
    if surface in {"extra_key", "overlap", "wrong_claim"}:
        descriptor = _d012_descriptor()
        descriptor.update(
            {
                "extra_key": {"extra": True},
                "overlap": {"physical_root": "tests/product/market_measurement"},
                "wrong_claim": {"claim_id": "neutral_market_measurement_truth_pilot"},
            }[surface]
        )
        _json_write(root / D012_ROOT / "claim.json", descriptor)
    elif surface in {"generation_claim", "generation_target"}:
        p = root / D012_ROOT / "generations/0001.json"
        value = json.loads(p.read_text())
        value["claim_id" if surface == "generation_claim" else "implementation_target_id"] = (
            "neutral_market_measurement_truth_pilot" if surface == "generation_claim" else "M00"
        )
        _json_write(p, value)
        _json_write(
            root / D012_ROOT / "admission.json",
            {
                "schema_version": "1.0",
                "current_generation": {
                    "path": p.relative_to(root).as_posix(),
                    "sha256": _sha(p),
                },
            },
        )
    elif surface == "unowned":
        (root / "tests/product/market_measurement_d012/test_unowned.py").write_text("pass\n")
    elif surface == "missing_binding":
        (root / D012_BINDING).unlink()
    elif surface in {"wrong_target", "intents"}:
        p = root / D012_BINDING
        p.write_text(
            p.read_text().replace("M02", "M00")
            if surface == "wrong_target"
            else (p.read_text().replace("G01", "A00"))
        )
    else:
        p = (
            root
            / {"brief": D012_BRIEF, "binding": D012_BINDING, "contract": D012_CONTRACT}[surface]
        )
        p.write_bytes(p.read_bytes() + b"\n")
    with pytest.raises((ValueError, OSError)):
        api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite")


def test_d012_missing_generation_is_not_ready(tmp_path):
    root = _d012_control_candidate(tmp_path)
    _json_write(
        root / D012_ROOT / "admission.json",
        {
            "schema_version": "1.0",
            "current_generation": None,
        },
    )
    assert _controls().load_product_proof_claim(root, D012_CLAIM).state == "INCOMPLETE_COVERAGE"


@pytest.mark.parametrize(
    "body,expected",
    [
        ("assert 7 * 6 == 42", 0),
        ("import pytest; pytest.skip('control canary')", 1),
        ("from pathlib import Path; Path('GUARDRAILS.md').write_text('fixture mutation')", 6),
    ],
)
def test_d012_direct_strict_runner_outcomes(tmp_path, body, expected):
    _controls()
    root = _d012_control_candidate(tmp_path, body)
    result = _run_control_probe(root, D012_CLAIM)
    assert result.returncode == expected, result.stdout + result.stderr


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
    # Control canaries require an explicit pre-admission universe, independently of
    # the real checkout's evolving product generations. Never rewrite actual history.
    assert tmp_path.resolve() != ROOT.resolve() and not (tmp_path / ".git").exists()
    # This fixture owns the original pre-admission universe, even after lawful
    # optional extensions exist in the real checkout. Actual claims stay intact.
    for relative in (
        "config/product_proof/market_measurement_d012",
        "tests/product/market_measurement_d012",
    ):
        disposable = tmp_path / relative
        if disposable.exists():
            shutil.rmtree(disposable)
    catalogue = json.loads((tmp_path / "config/product_proof/claims.json").read_text())
    for entry in catalogue["claims"]:
        if entry["profile"] != "accepted_brief_v2":
            continue
        physical = tmp_path / entry["physical_root"]
        assert physical.is_relative_to(tmp_path / "tests/product")
        if physical.exists():
            shutil.rmtree(physical)
        pointer = tmp_path / entry["admission_path"]
        generations = pointer.parent / "generations"
        if generations.exists():
            shutil.rmtree(generations)
        _json_write(pointer, {"schema_version": "1.0", "current_generation": None})
    import yaml

    path = tmp_path / "config/architecture/modules.yaml"
    doc = yaml.safe_load(path.read_text())
    removed = {
        item["id"] for item in doc["modules"] if item["name"] == "neutral_market_measurement_truth"
    }
    doc["modules"] = [item for item in doc["modules"] if item["id"] not in removed]
    path.write_text(yaml.safe_dump(doc))
    path = tmp_path / "config/architecture/implementation_allocations.yaml"
    doc = yaml.safe_load(path.read_text())
    doc["implementation_allocations"] = [
        item for item in doc["implementation_allocations"] if item["object_id"] not in removed
    ]
    path.write_text(yaml.safe_dump(doc))
    path = tmp_path / "config/architecture/dependency_rules.yaml"
    doc = yaml.safe_load(path.read_text())
    doc["declared_owner_edges"] = [
        edge
        for edge in doc["declared_owner_edges"]
        if edge["source"] not in removed and edge["target"] not in removed
    ]
    path.write_text(yaml.safe_dump(doc))
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


def test_pending_authority_target_and_empty_proof_are_not_success(tmp_path):
    api = _controls()
    root = _copy_candidate(tmp_path)
    assert api.load_product_proof_claim(root, "raw_signal_occurrence_truth_sqlite").state == (
        "INCOMPLETE_NO_PHYSICAL_FAMILIES"
    )
    assert api.load_product_proof_claim(root, "neutral_market_measurement_truth_pilot").state == (
        "AWAITING_TARGET"
    )


def test_actual_m00_and_foundation_generations_remain_distinct():
    api = _controls()
    raw = api.load_product_proof_claim(ROOT, "raw_signal_occurrence_truth_sqlite")
    foundation = api.load_product_proof_claim(ROOT, "neutral_market_measurement_truth_pilot")
    assert raw.state == "READY_FOR_PROOF" and raw.target_id == "M00"
    assert raw.target_status == "active" and raw.generation_sha256 is not None
    assert foundation.target_status == "active"
    # G5.3 admits only the isolated pilot; claim/generation separation remains.
    assert foundation.target_id == "M02"
    assert foundation.state == "READY_FOR_PROOF"
    assert foundation.generation_sha256 is not None
    assert foundation.generation_sha256 != raw.generation_sha256


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


def _run_control_probe(root, aggregate=None):
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
        [
            sys.executable,
            str(root / "tools/run_product_proof_gate.py"),
            *([] if aggregate is None else ["--aggregate", aggregate]),
        ],
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
    root = _copy_candidate(tmp_path)
    assert _run_control_probe(root).returncode == 4
    env = dict(os.environ, PYTHONPATH=str(root / "tools") + os.pathsep + str(root / "src"))
    result = subprocess.run(
        [
            sys.executable,
            str(root / "tools/run_product_proof_gate.py"),
            "--aggregate",
            "raw_signal_occurrence_truth_product",
        ],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
    )
    reason = json.loads((root / "config/product_proof/claims.json").read_text())["claims"][0][
        "reason"
    ]
    assert result.returncode == 4
    assert reason in result.stdout


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


@pytest.mark.parametrize("mode", ["reinstate_uncommitted", "reinstate_committed", "new_generation"])
def test_revoked_generation_requires_fresh_admission(tmp_path, mode):
    api = _controls()
    root = _copy_candidate(tmp_path)
    entry, _, record, _ = _control_generation(root)
    assert _run_control_probe(root).returncode == 0
    path = root / entry["admission_path"]
    old_pointer = json.loads(path.read_text())
    _json_write(path, {"schema_version": "1.0", "current_generation": None})
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    commit = [
        "git",
        "-c",
        "user.name=Control fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-qm",
    ]
    subprocess.run([*commit, "revoke generation1"], cwd=root, check=True)
    assert api.load_product_proof_claim(root, entry["claim_id"]).state == "INCOMPLETE_COVERAGE"
    if mode == "new_generation":
        record["generation"] = 2
        record["previous_generation"] = old_pointer["current_generation"]
        record["adequacy_review_ref"] = "control-fixture/new-review"
        record["admission_authority_ref"] = "control-fixture/new-admission"
        name = Path(entry["admission_path"]).parent / "generations/0002.json"
        _json_write(root / name, record)
        _json_write(
            path,
            {
                "schema_version": "1.0",
                "current_generation": {"path": name.as_posix(), "sha256": _sha(root / name)},
            },
        )
        assert api.load_product_proof_claim(root, entry["claim_id"]).state == "READY_FOR_PROOF"
    else:
        _json_write(path, old_pointer)
        if mode == "reinstate_committed":
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                [*commit, "counterfeit old admission reinstatement"], cwd=root, check=True
            )
        with pytest.raises(ValueError, match=r"revoked|history|advance"):
            api.load_product_proof_claim(root, entry["claim_id"])


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
