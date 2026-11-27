"""Exact accepted claim, target, physical-proof and immutable-generation resolution."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Literal

import yaml

from nvda_desk.architecture.implementation_authority import validate_implementation_authority
from nvda_desk.architecture.registry import ArchitectureRegistry
from nvda_desk.architecture.schema import validate_instance


@dataclass(frozen=True, slots=True)
class AdmittedProductFamily:
    family_id: str
    path: str
    proof_ids: tuple[str, ...]
    required_test_names: tuple[str, ...]
    sha256: str | None


@dataclass(frozen=True, slots=True)
class ProductProofClaim:
    claim_id: str
    profile: str
    target_id: str | None
    target_status: str | None
    authority_sha256: str | None
    generation_sha256: str | None
    state: str
    families: tuple[AdmittedProductFamily, ...]
    support_files: tuple[tuple[str, str], ...]
    governed_files: tuple[tuple[str, str], ...]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, value in items:
        if name in result:
            raise ValueError(f"duplicate JSON key: {name}")
        result[name] = value
    return result


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc


def safe_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or "\\" in name:
        raise ValueError("invalid repository-relative path")
    relative = PurePosixPath(name)
    if relative.is_absolute() or any(p in {".", ".."} for p in name.split("/")):
        raise ValueError(f"unsafe repository path: {name}")
    path = root / name
    for parent in (path, *path.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError(f"symlink in governed path: {name}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"escaping repository path: {name}")
    return path


def _schema(root: Path, document: Any, name: str) -> None:
    validate_instance(document, read_json(root / "schemas" / name))


def _marker(text: str, name: str) -> str:
    lines = re.findall(rf"^{re.escape(name)}: ([0-9a-f]{{64}})$", text, re.MULTILINE)
    if len(lines) != 1 or sum(line.startswith(name + ":") for line in text.splitlines()) != 1:
        raise ValueError(f"missing/duplicate malformed companion marker: {name}")
    return lines[0]


def _authority(root: Path, catalogue: dict[str, Any]) -> tuple[str, dict[str, str]] | None:
    control = catalogue["control_authority"]
    brief = safe_path(root, control["brief_path"])
    binding = safe_path(root, control["binding_path"])
    if not binding.exists():
        return None
    validate_implementation_authority(root, binding, brief)
    # The native kernel proves bytes/projection only; external acceptance and
    # adequacy are separately required human facts, never created by this tool.
    document = yaml.safe_load(binding.read_text(encoding="utf-8"))
    intents = document["targets"]
    expected = [
        {"action": "create", "category": "M", "name": "neutral_market_measurement_truth"},
        *({"action": "modify", "object_id": name} for name in ("M00", "G01", "A00")),
    ]
    if intents != expected:
        raise ValueError("accepted version3 projection intent mismatch")
    text = brief.read_text(encoding="utf-8")
    incorporated = dict(re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$", text, re.M))
    if not incorporated:
        raise ValueError("missing incorporated authority table")
    for name, digest in incorporated.items():
        if sha256(safe_path(root, name)) != digest:
            raise ValueError(f"incorporated companion hash mismatch: {name}")
    catalogue_path = root / "config/product_proof/claims.json"
    if sha256(catalogue_path) != _marker(text, "SQLITE-CLAIM-CATALOGUE-SHA256"):
        raise ValueError("active catalogue hash mismatch")
    for marker, suffix in (
        ("SQLITE-FOUNDATION-CONTRACT-SHA256", "FOUNDATION_SQLITE_PROOF_CONTRACT_PROPOSED.json"),
        ("SQLITE-M00-CONTRACT-SHA256", "M00_SQLITE_PROOF_CONTRACT_PROPOSED.json"),
        ("SQLITE-LEGACY-DISPOSITIONS-SHA256", "SQLITE_LEGACY_PROOF_DISPOSITIONS_PROPOSED.json"),
    ):
        matches = [digest for name, digest in incorporated.items() if name.endswith("/" + suffix)]
        if matches != [_marker(text, marker)]:
            raise ValueError(f"companion marker mismatch: {marker}")
    legacy_brief = next(
        name
        for name in incorporated
        if name.endswith("/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md")
    )
    legacy_table = re.findall(
        r"^\| `([^`]+)` \| evidence \| `([0-9a-f]{64})` \|$",
        (root / legacy_brief).read_text(encoding="utf-8"),
        re.M,
    )
    for name, digest in legacy_table:
        if (
            name.startswith("config/product_proof/") or name.startswith("schemas/product_proof_")
        ) and sha256(safe_path(root, name)) != digest:
            raise ValueError(f"preserved legacy control hash mismatch: {name}")
    return sha256(brief), incorporated


def governed_snapshot(root: Path) -> tuple[tuple[str, str], ...]:
    """Exact tracked bytes plus all governed candidate files, including absence."""
    tracked = (
        subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=False)
        .stdout.decode()
        .split("\0")
    )
    paths = {name for name in tracked if name}
    for prefix in (
        "config",
        "schemas",
        "tools",
        "src",
        "tests",
        "implementation/authority",
        "handoff/foundation_implementation/authority",
    ):
        base = root / prefix
        if base.exists():
            paths.update(
                p.relative_to(root).as_posix()
                for p in base.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".pyo"}
            )
    return tuple(
        (name, sha256(safe_path(root, name)) if (root / name).is_file() else "ABSENT")
        for name in sorted(paths)
    )


# These two exact files have independent TEST-AUTHORING acceptance only.
# They are not runnable proof families until a separately governed descriptor,
# authority binding, claim contract and immutable generation are admitted.
_D091_STAGED_AUTHORING = {
    "tests/product/m02_completion_28/d091/test_signal.py":
        "d1eab7802786344ecf9ab4d4e2f46b802aba6d2fea0c72d14ad149492504b86f",
    "tests/product/m02_completion_28/l01b_r112/test_source.py":
        "1f648998ca4c64829a3655057598e5ae5687b6568bb7e9eebf7ca2f17caa56f5",
}


def _d091_staged_authoring_paths(root: Path) -> set[str]:
    """Permit exact unadmitted files without manufacturing a proof claim.

    Any bytes changed after the independent authoring verdict require a new
    explicit binding/review: they cannot be silently excused as staged code.
    """
    if (root / "config/product_proof/m02_d091/claim.json").exists():
        return set()
    for name, expected_sha in _D091_STAGED_AUTHORING.items():
        file = safe_path(root, name)
        if not file.is_file() or sha256(file) != expected_sha:
            raise ValueError("unadmitted D091/L01b test source differs from accepted authoring")
    return set(_D091_STAGED_AUTHORING)


def _partition(root: Path, catalogue: dict[str, Any], contracts: dict[str, Any]) -> None:
    disposition = read_json(safe_path(root, catalogue["transitional_dispositions"]))
    owned: dict[str, str] = {}
    roots: list[str] = []
    for entry in catalogue["claims"]:
        prefix = entry["physical_root"]
        safe_path(root, prefix)
        if not prefix.startswith("tests/product/"):
            raise ValueError("invalid physical claim root")
        if any(
            prefix == old or prefix.startswith(old + "/") or old.startswith(prefix + "/")
            for old in roots
        ):
            raise ValueError("overlapping physical claim roots")
        roots.append(prefix)
        if entry["profile"] == "historical_backend_v1":
            paths = [row["path"] for row in disposition["legacy_current_claim_paths"]]
        else:
            paths = [row["path"] for row in contracts[entry["claim_id"]]["families"]]
            allowed = set(
                paths
                + contracts[entry["claim_id"]]["required_support_files"]
                + contracts[entry["claim_id"]]["optional_support_files"]
            )
            for path in (root / prefix).rglob("*.py"):
                if path.relative_to(root).as_posix() not in allowed:
                    raise ValueError("unowned physical proof support file")
        for name in paths:
            if name in owned or not name.startswith(prefix + "/"):
                raise ValueError("overlapping or mismatched claim path")
            safe_path(root, name)
            owned[name] = entry["claim_id"]
    for row in disposition["preserved_transitional_paths"]:
        name = row["path"]
        if name in owned:
            raise ValueError("overlapping transitional path")
        safe_path(root, name)
        owned[name] = "preserved_transitional"
    for row in disposition["legacy_current_claim_paths"]:
        if sha256(safe_path(root, row["path"])) != row["baseline_sha256"]:
            raise ValueError("preserved legacy physical proof hash mismatch")
    staged_authoring = _d091_staged_authoring_paths(root)
    for path in (root / "tests/product").rglob("*"):
        if path.is_symlink():
            raise ValueError("symlink in product proof jurisdiction")
        if path.is_file() and path.name.startswith("test_") and path.suffix == ".py":
            name = path.relative_to(root).as_posix()
            if name not in owned and name not in staged_authoring:
                raise ValueError(f"unowned physical product path: {name}")
    for name, owner in owned.items():
        if (
            owner in {"preserved_transitional", disposition["legacy_claim_id"]}
            and not (root / name).is_file()
        ):
            raise ValueError(f"missing preserved product path: {name}")


def _target(root: Path, target: dict[str, Any]) -> tuple[str | None, str | None]:
    registry = ArchitectureRegistry.from_repository(root)
    matches = [item for item in registry.objects if item.package == target["package"]]
    if not matches:
        if target["intent"] == "modify":
            raise ValueError("missing existing modify target")
        return None, None
    if len(matches) != 1:
        raise ValueError("ambiguous implementation target")
    actual = matches[0]
    if (
        actual.public_seam != target["public_seam"]
        or actual.name != target["responsibility_name"]
        or not actual.id.startswith(target["category"])
    ):
        raise ValueError("implementation target identity/package/seam mismatch")
    if target["intent"] == "modify" and actual.id != target["existing_object_id"]:
        raise ValueError("existing target ID mismatch")
    allocations = yaml.safe_load(
        (root / "config/architecture/implementation_allocations.yaml").read_text()
    )["implementation_allocations"]
    if not any(row["object_id"] == actual.id and row["name"] == actual.name for row in allocations):
        raise ValueError("implementation target lacks durable allocation")
    return actual.id, actual.status


def _admission_history(root: Path, entry: dict[str, Any], pointer: dict[str, Any]) -> None:
    """Retained Git transitions distinguish first admission from revoked reuse.

    Pure document fixtures may have no Git history. Actual execution separately
    requires a committed clean repository; inspect every retained pointer change
    and then the current bytes, so committing a counterfeit transition cannot
    erase revocation. Never infer admission from the latest pointer alone.
    """
    directory = str(PurePosixPath(entry["admission_path"]).parent)
    completed = subprocess.run(
        ["git", "log", "--reverse", "--format=%H", "--", directory],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return
    previous: dict[str, str] | None = None
    last_admitted: dict[str, str] | None = None
    highest = 0
    snapshots: list[tuple[str | None, dict[str, Any]]] = []
    for commit in completed.stdout.splitlines():
        content = subprocess.run(
            ["git", "show", f"{commit}:{entry['admission_path']}"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if content.returncode == 0:
            historical = json.loads(content.stdout, object_pairs_hook=_pairs)
            _schema(root, historical, "product_proof_admission.schema.json")
            if set(historical) != {"schema_version", "current_generation"}:
                raise ValueError("invalid historical admission pointer")
            snapshots.append((commit, historical))
    snapshots.append((None, pointer))
    for historical_commit, historical in snapshots:
        reference = historical["current_generation"]
        if reference is None:
            previous = None
            continue
        safe_path(root, reference["path"])
        if historical_commit is None:
            raw = (root / reference["path"]).read_bytes()
        else:
            raw = subprocess.check_output(
                ["git", "show", f"{historical_commit}:{reference['path']}"],
                cwd=root,
            )
        if hashlib.sha256(raw).hexdigest() != reference["sha256"]:
            raise ValueError("admission history generation hash mismatch")
        record = json.loads(raw, object_pairs_hook=_pairs)
        _schema(root, record, "product_proof_admission.schema.json")
        if "generation" not in record:
            raise ValueError("invalid historical generation record")
        if reference != previous:
            if (
                record["generation"] != highest + 1
                or record["previous_generation"] != last_admitted
            ):
                raise ValueError("revoked/reused generation must advance admission history")
            highest = record["generation"]
            last_admitted = reference
        previous = reference


def _generation(
    root: Path,
    entry: dict[str, Any],
    contract: dict[str, Any],
    brief_hash: str,
    target_id: str | None,
) -> tuple[str | None, dict[str, str]]:
    pointer_path = safe_path(root, entry["admission_path"])
    if not pointer_path.exists():
        return None, {}
    pointer = read_json(pointer_path)
    _schema(root, pointer, "product_proof_admission.schema.json")
    if set(pointer) != {"schema_version", "current_generation"}:
        raise ValueError("invalid admission pointer shape")
    reference = pointer["current_generation"]
    if reference is None:
        return None, {}
    _admission_history(root, entry, pointer)
    prefix = str(PurePosixPath(entry["admission_path"]).parent / "generations") + "/"
    seen: set[str] = set()
    current: dict[str, Any] | None = None
    expected_number = None
    while reference is not None:
        name = reference["path"]
        if name in seen or not name.startswith(prefix):
            raise ValueError("generation path/cycle/cross-claim mismatch")
        path = safe_path(root, name)
        if sha256(path) != reference["sha256"]:
            raise ValueError("generation pointer hash mismatch")
        seen.add(name)
        record = read_json(path)
        _schema(root, record, "product_proof_admission.schema.json")
        if "generation" not in record or record["generation"] < 1:
            raise ValueError("invalid generation number")
        if expected_number is not None and record["generation"] != expected_number:
            raise ValueError("generation predecessor number mismatch")
        if record["claim_id"] != entry["claim_id"]:
            raise ValueError("generation claim mismatch")
        if record["generation"] == 1 and record["previous_generation"] is not None:
            raise ValueError("generation1 must have no predecessor")
        if record["generation"] > 1 and record["previous_generation"] is None:
            raise ValueError("generation predecessor missing")
        if current is None:
            current = record
        expected_number = record["generation"] - 1
        reference = record["previous_generation"]
    assert current is not None
    retained = {path.relative_to(root).as_posix() for path in (root / prefix).glob("*.json")}
    if retained != seen:
        raise ValueError("generation rollback/fork or unreferenced retained generation")
    for key, expected in {
        "brief_sha256": brief_hash,
        "binding_sha256": sha256(root / entry["binding_path"]),
        "contract_sha256": sha256(root / entry["contract_path"]),
        "implementation_target_id": target_id,
    }.items():
        if current[key] != expected:
            raise ValueError(f"generation {key} mismatch")
    files: dict[str, str] = {}
    for key, required, allowed in (
        (
            "family_files",
            {f["path"] for f in contract["families"]},
            {f["path"] for f in contract["families"]},
        ),
        (
            "support_files",
            set(contract["required_support_files"]),
            set(contract["required_support_files"] + contract["optional_support_files"]),
        ),
    ):
        rows = current[key]
        names = [row["path"] for row in rows]
        if len(names) != len(set(names)) or not required <= set(names) <= allowed:
            raise ValueError(f"generation {key} membership mismatch")
        if key == "support_files":
            present = {name for name in allowed if (root / name).exists()}
            if set(names) != present:
                raise ValueError("untracked/missing support file in generation")
        for row in rows:
            if row["path"] in files or sha256(safe_path(root, row["path"])) != row["sha256"]:
                raise ValueError("admitted family/support hash mismatch")
            files[row["path"]] = row["sha256"]
    return pointer["current_generation"]["sha256"], files


def _scalar_extension(
    root: Path,
    identity: Literal[
        "D001",
        "D002",
        "D003",
        "D004",
        "D005",
        "D009",
        "D010",
        "D012",
        "D013",
        "D014",
        "D015",
        "D016",
        "D017",
        "D018",
        "D019",
        "D020",
        "D021",
        "D022",
        "D023",
        "D024",
        "D025",
        "D026",
        "D027",
        "D028",
        "D029",
        "D030",
        "D031",
        "D032",
        "D033",
        "D034",
        "D035",
        "D036",
        "D037",
        "D038",
        "D039",
        "D042",
        "D043",
        "D044",
        "D045",
        "D046",
        "D047",
        "D048",
        "D049",
        "D050",
        "D051",
        "D052",
        "D053",
        "D054",
        "D055",
        "D056",
        "D057",
        "D058",
        "D059",
        "D060",
        "D063",
        "D066",
        "D067",
        "D068",
        "D069",
        "D071",
        "D072",
        "D073",
        "D074",
        "D075",
        "D076",
        "D077",
        "D082",
        "D083",
        "D087",
        "D088",
        "D089",
        "D090",
        "D092",
        "D093",
        "D094",
        "D099",
        "D100",
        "D101",
        "D103",
        "D104",
        "D105",
        "D106",
        "D116",
        "D117",
        "D118",
        "D119",
        "D123",
        "D124",
        "D131",
        "D134",
        "D135",
        "D136",
        "D137",
        "D138",
        "D139",
        "D140",
        "D143",
    ],
) -> tuple[dict[str, Any], dict[str, Any], str] | None:
    """Fixed separately admitted signal extensions; never discover arbitrary claims."""
    name = identity.lower()
    directory = f"config/product_proof/market_measurement_{name}"
    descriptor = safe_path(root, directory + "/claim.json")
    if not descriptor.exists():
        physical = safe_path(root, f"tests/product/market_measurement_{name}")
        if physical.exists() and any(p.is_file() or p.is_symlink() for p in physical.rglob("*.py")):
            raise ValueError(f"unowned {identity} extension Python source without descriptor")
        return None
    legacy = identity in ("D012", "D013", "D014")
    label = f"G6_1_{identity}" if legacy else identity
    prefix = f"handoff/foundation_implementation/authority/{label}_"
    expected = {
        "schema_version": "1.0",
        "claim_id": f"neutral_market_measurement_truth_{name}",
        "brief_path": prefix
        + ("IMPLEMENTATION_BRIEF_PROPOSED.md" if legacy else "IMPLEMENTATION_BRIEF.md"),
        "binding_path": (f"implementation/authority/{label}_IMPLEMENTATION_AUTHORITY_BINDING.yaml"),
        "contract_path": prefix
        + ("PROOF_CONTRACT_PROPOSED.json" if legacy else "PROOF_CONTRACT.json"),
        "physical_root": f"tests/product/market_measurement_{name}",
        "admission_path": directory + "/admission.json",
    }
    if read_json(descriptor) != expected:
        raise ValueError(f"invalid {identity} extension descriptor")
    brief = safe_path(root, expected["brief_path"])
    binding = safe_path(root, expected["binding_path"])
    validate_implementation_authority(root, binding, brief)
    intents = yaml.safe_load(binding.read_text(encoding="utf-8"))["targets"]
    if intents != [{"action": "modify", "object_id": name} for name in ("M02", "G01")]:
        raise ValueError(f"{identity} projection intent mismatch")
    text = brief.read_text(encoding="utf-8")
    rows = re.findall(r"^\| ([^|]+?) \| ([0-9a-f]{64}) \|$", text, re.M)
    count = {
        "D001": 7,
        "D002": 7,
        "D003": 7,
        "D004": 7,
        "D005": 7,
        "D009": 7,
        "D010": 7,
        "D012": 8,
        "D013": 11,
        "D014": 8,
        "D015": 7,
        "D016": 7,
        "D017": 7,
        "D018": 7,
        "D019": 7,
        "D020": 7,
        "D021": 7,
        "D022": 7,
        "D023": 7,
        "D024": 7,
        "D025": 7,
        "D026": 7,
        "D027": 7,
        "D028": 8,
        "D029": 7,
        "D030": 7,
        "D031": 7,
        "D032": 7,
        "D033": 7,
        "D034": 7,
        "D035": 7,
        "D036": 7,
        "D037": 7,
        "D038": 7,
        "D039": 7,
        "D042": 7,
        "D043": 7,
        "D044": 7,
        "D045": 7,
        "D046": 7,
        "D047": 7,
        "D048": 7,
        "D049": 7,
        "D050": 7,
        "D051": 7,
        "D052": 7,
        "D053": 7,
        "D054": 7,
        "D055": 7,
        "D056": 7,
        "D057": 7,
        "D058": 7,
        "D059": 7,
        "D060": 7,
        "D063": 7,
        "D066": 7,
        "D067": 7,
        "D068": 7,
        "D069": 7,
        "D071": 7,
        "D072": 7,
        "D073": 7,
        "D074": 7,
        "D075": 7,
        "D076": 7,
        "D077": 7,
        "D082": 7,
        "D083": 7,
        "D087": 7,
        "D088": 7,
        "D089": 7,
        "D090": 7,
        "D092": 7,
        "D093": 7,
        "D094": 7,
        "D099": 7,
        "D100": 7,
        "D101": 7,
        "D103": 7,
        "D104": 7,
        "D105": 7,
        "D106": 7,
        "D116": 8,
        "D117": 9,
        "D118": 7,
        "D119": 6,
        "D123": 7,
        "D124": 6,
        "D131": 6,
        "D134": 6,
        "D135": 7,
        "D136": 7,
        "D137": 6,
        "D138": 7,
        "D139": 6,
        "D140": 6,
        "D143": 6,
    }[identity]
    if len(rows) != count or len(dict(rows)) != count:
        raise ValueError(f"invalid {identity} incorporated-byte table")
    for name, digest in rows:
        if sha256(safe_path(root, name)) != digest:
            raise ValueError(f"{identity} incorporated companion hash mismatch")
    contract_path = safe_path(root, expected["contract_path"])
    if sha256(contract_path) != _marker(text, f"{identity}-PROOF-CONTRACT-SHA256"):
        raise ValueError(f"{identity} contract marker mismatch")
    contract = read_json(contract_path)
    _schema(root, contract, "accepted_brief_product_proof.schema.json")
    if (
        contract["claim_id"] != expected["claim_id"]
        or contract["semantic_brief_path"] != expected["brief_path"]
        or contract["target"]["intent"] != "modify"
        or contract["target"].get("existing_object_id") != "M02"
    ):
        raise ValueError(f"{identity} cross-claim authority association mismatch")
    entry = {key: value for key, value in expected.items() if key != "brief_path"}
    entry["profile"] = "accepted_brief_v2"
    target_id, _ = _target(root, contract["target"])
    # Validate an admitted extension even when an original claim was selected.
    _generation(root, entry, contract, sha256(brief), target_id)
    return entry, contract, sha256(brief)


def _configured_extension(
    root: Path,
    identity: Literal["D040", "D041"],
) -> tuple[dict[str, Any], dict[str, Any], str] | None:
    """Two fixed P02 owner declarations; unchanged target/generation/partition algorithms."""
    name = identity.lower()
    directory = f"config/product_proof/configured_conditions_{name}"
    prefix = "handoff/configured_market_conditions/authority/"
    expected = {
        "schema_version": "1.0",
        "claim_id": f"configured_market_conditions_{name}",
        "brief_path": prefix + f"{identity}_IMPLEMENTATION_BRIEF.md",
        "binding_path": (
            f"implementation/authority/{identity}_IMPLEMENTATION_AUTHORITY_BINDING.yaml"
        ),
        "contract_path": prefix + f"{identity}_PROOF_CONTRACT.json",
        "physical_root": f"tests/product/configured_conditions_{name}",
        "admission_path": directory + "/admission.json",
    }
    descriptor = safe_path(root, directory + "/claim.json")
    if not descriptor.exists():
        physical = safe_path(root, expected["physical_root"])
        if physical.exists() and any(p.is_file() for p in physical.rglob("*.py")):
            raise ValueError(f"unowned {identity} configured proof source")
        return None
    if read_json(descriptor) != expected:
        raise ValueError(f"invalid {identity} configured descriptor")
    brief, binding = (safe_path(root, expected[k]) for k in ("brief_path", "binding_path"))
    validate_implementation_authority(root, binding, brief)
    if yaml.safe_load(binding.read_text())["targets"] != [
        {"action": "modify", "object_id": key} for key in ("M03", "M02", "G01")
    ]:
        raise ValueError(f"{identity} owning projection mismatch")
    rows = re.findall(r"^\| ([^|]+?) \| ([0-9a-f]{64}) \|$", brief.read_text(), re.M)
    required = {
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        f"handoff/configured_market_conditions/authority/{identity}_PROFILE.json",
        expected["contract_path"],
    }
    if len(rows) != 4 or set(dict(rows)) != required:
        raise ValueError(f"{identity} incorporated authority membership mismatch")
    if any(sha256(safe_path(root, path)) != digest for path, digest in rows):
        raise ValueError(f"{identity} incorporated authority hash mismatch")
    contract = read_json(safe_path(root, expected["contract_path"]))
    _schema(root, contract, "accepted_brief_product_proof.schema.json")
    if (
        sha256(root / expected["contract_path"])
        != _marker(brief.read_text(), f"{identity}-PROOF-CONTRACT-SHA256")
        or contract["claim_id"] != expected["claim_id"]
        or contract["semantic_brief_path"] != expected["brief_path"]
        or contract["target"]
        != {
            "category": "M",
            "responsibility_name": "configured_market_conditions",
            "package": "nvda_desk.configured_market_conditions",
            "public_seam": "nvda_desk.configured_market_conditions.api",
            "intent": "modify",
            "existing_object_id": "M03",
        }
    ):
        raise ValueError(f"{identity} exact owning contract mismatch")
    entry = {k: v for k, v in expected.items() if k != "brief_path"}
    entry["profile"] = "accepted_brief_v2"
    target_id, _ = _target(root, contract["target"])
    _generation(root, entry, contract, sha256(brief), target_id)
    return entry, contract, sha256(brief)


def _m00_brief2_extension(root: Path) -> tuple[dict[str, Any], dict[str, Any], str] | None:
    """One exact owner-commissioned M00 extension; original claims remain sealed."""
    expected = {
        "schema_version": "1.0",
        "claim_id": "m00_brief2",
        "brief_path": "handoff/planning/m00_brief2_20261027/"
        "BRIEF_2_M00_RECONCILED_V3_20261027_1622_AEDT.md",
        "binding_path": "implementation/authority/M00_BRIEF2_BINDING.yaml",
        "contract_path": "handoff/m00_brief2/authority/PROOF_CONTRACT.json",
        "physical_root": "tests/product/m00_brief2",
        "admission_path": "config/product_proof/m00_brief2/admission.json",
    }
    descriptor = safe_path(root, "config/product_proof/m00_brief2/claim.json")
    if not descriptor.exists():
        physical = safe_path(root, expected["physical_root"])
        if physical.exists() and any(physical.rglob("*.py")):
            raise ValueError("unowned M00 Brief2 proof source")
        return None
    if read_json(descriptor) != expected:
        raise ValueError("invalid M00 Brief2 descriptor")
    brief, binding = (safe_path(root, expected[k]) for k in ("brief_path", "binding_path"))
    digest = "0d5ee211c1285b31834062ab2d871670ed2f318cbb955e7df95f80067d562007"
    if sha256(brief) != digest:
        raise ValueError("M00 Brief2 original brief bytes mismatch")
    validate_implementation_authority(root, binding, brief)
    if yaml.safe_load(binding.read_text())["targets"] != [
        {"action": "modify", "object_id": name} for name in ("M00", "G01")
    ]:
        raise ValueError("M00 Brief2 owning projection mismatch")
    contract = read_json(safe_path(root, expected["contract_path"]))
    _schema(root, contract, "accepted_brief_product_proof.schema.json")
    target = {
        "category": "M", "responsibility_name": "raw_signal_occurrence_truth",
        "package": "nvda_desk.raw_signal_occurrence_truth",
        "public_seam": "nvda_desk.raw_signal_occurrence_truth.api",
        "intent": "modify", "existing_object_id": "M00",
    }
    if (contract["claim_id"] != "m00_brief2"
        or contract["semantic_brief_path"] != expected["brief_path"]
        or contract["target"] != target
        or any(value != "FAIL" for value in contract["execution_policy"].values())):
        raise ValueError("M00 Brief2 contract/target association mismatch")
    names = ["test_ibkr_native_projection.py", "test_ibkr_history.py",
             "test_ibkr_controls.py", "test_export.py"]
    paths = [family["path"] for family in contract["families"]]
    required = [expected["physical_root"] + "/" + name for name in names]
    if not paths or paths != required[:len(paths)]:
        raise ValueError("M00 Brief2 family sequence mismatch")
    entry = {key: value for key, value in expected.items() if key != "brief_path"}
    entry["profile"] = "accepted_brief_v2"
    target_id, _ = _target(root, target)
    _generation(root, entry, contract, digest, target_id)
    return entry, contract, digest


def _d091_l01b_extension(
    root: Path,
) -> tuple[dict[str, Any], dict[str, Any], str] | None:
    """Register one exact two-jurisdiction D091 claim ONLY after a descriptor.

    The original positive R112 source and both finite test jurisdictions are
    fixed. This routine does not install an admission pointer or generation.
    """
    descriptor_path = "config/product_proof/m02_d091/claim.json"
    descriptor = safe_path(root, descriptor_path)
    if not descriptor.exists():
        return None
    expected = {
        "schema_version": "1.0",
        "claim_id": "neutral_market_measurement_truth_d091",
        "brief_path": "handoff/m02_completion_28_execution/L04/"
        "D091_PREEDIT_BINDING_REVISION_20261117/EXACT_RETURN_REPAIR_R1_R3.md",
        "binding_path": "implementation/authority/"
        "D091_IMPLEMENTATION_AUTHORITY_BINDING.yaml",
        "contract_path": "handoff/m02_completion_28_execution/L04/"
        "D091_PREEDIT_BINDING_REVISION_20261117/PRODUCT_PROOF_REGISTRATION_PROPOSAL.json",
        "physical_root": "tests/product/m02_completion_28",
        "admission_path": "config/product_proof/m02_d091/admission.json",
    }
    if read_json(descriptor) != expected:
        raise ValueError("D091 claim descriptor differs from fixed proposed authority")
    brief = safe_path(root, expected["brief_path"])
    binding = safe_path(root, expected["binding_path"])
    validate_implementation_authority(root, binding, brief)
    if yaml.safe_load(binding.read_text(encoding="utf-8"))["targets"] != [
        {"action": "modify", "object_id": name} for name in ("M02", "G01")
    ]:
        raise ValueError("D091 owning architecture projection mismatch")
    contract = read_json(safe_path(root, expected["contract_path"]))
    _schema(root, contract, "accepted_brief_product_proof.schema.json")
    exact_families = (
        ("tests/product/m02_completion_28/d091/test_signal.py", 18, "M02-C28-D091"),
        ("tests/product/m02_completion_28/l01b_r112/test_source.py", 15,
         "M02-C28-L01B-R112-SOURCE-SUPPORT"),
    )
    admitted = read_json(safe_path(
        root, "handoff/m02_completion_28_execution/L04/"
              "D091_FINITE_ADEQUACY_REVISION_20261117/REVISED_CASE_INVENTORY.json"
    ))["physical_cases"]
    if len(admitted) != 33:
        raise ValueError("D091/L01b owner-admitted finite case count mismatch")
    if (
        contract["claim_id"] != expected["claim_id"]
        or contract["semantic_brief_path"] != expected["brief_path"]
        or contract["target"] != {
            "category": "M", "responsibility_name": "neutral_market_measurement_truth",
            "package": "nvda_desk.market_measurement_truth",
            "public_seam": "nvda_desk.market_measurement_truth.api",
            "intent": "modify", "existing_object_id": "M02",
        }
        or len(contract["families"]) != 2
        or set(contract["required_proof_ids"]) != {row[2] for row in exact_families}
        or any(v != "FAIL" for v in contract["execution_policy"].values())
    ):
        raise ValueError("D091 proof contract/owner association mismatch")
    for family, (name, count, proof_id) in zip(
        contract["families"], exact_families, strict=True
    ):
        names = [
            row["proposed_test_node"].split("::", 1)[1]
            for row in admitted
            if row["proposed_test_node"].split("::", 1)[0] == name
        ]
        if (
            family["path"] != name
            or family["proof_obligation_ids"] != [proof_id]
            or len(names) != count
            or family["required_test_names"] != names
            or family["command"] != "python -m pytest " + name
        ):
            raise ValueError("D091 and L01b physical case identity/jurisdiction mismatch")
    entry = {key: value for key, value in expected.items() if key != "brief_path"}
    entry["profile"] = "accepted_brief_v2"
    target_id, _ = _target(root, contract["target"])
    # No pointer exists or is installed by this extension. Existing strict
    # generation verification governs if a future owner-approved pointer
    # becomes present.
    _generation(root, entry, contract, sha256(brief), target_id)
    return entry, contract, sha256(brief)


def _scalar_straddle_extensions(
    root: Path,
) -> tuple[tuple[dict[str, Any], dict[str, Any], str], ...]:
    """Fixed additive scalar straddle claim jurisdiction, never a release.

    Only the three owner-approved identities and their distinct sibling roots
    are recognised. No discovery, staged-test exception, old-claim rewrite
    or automatic generation/pointer creation.
    """
    leaf = "handoff/m02_completion_28_execution/L10c/"
    exact = (
        (
            "SUPPORT", "neutral_market_measurement_truth_l10c_scalar_pair_support",
            "M02-C28-L10C-SCALAR-PAIR-SUPPORT", "m02_l10c_scalar_pair_source_support",
            "m02_scalar_straddle_support", "test_source.py", 16,
        ),
        (
            "D109", "neutral_market_measurement_truth_d109", "M02-C28-D109",
            "m02_l17_scalar_straddle_d109", "m02_scalar_straddle_d109", "test_signal.py", 8,
        ),
        (
            "D110", "neutral_market_measurement_truth_d110", "M02-C28-D110",
            "m02_l18_scalar_straddle_d110", "m02_scalar_straddle_d110", "test_signal.py", 10,
        ),
    )
    present = tuple(
        row for row in exact
        if safe_path(root, f"config/product_proof/{row[4]}/claim.json").exists()
    )
    if not present:
        return ()
    brief_path = leaf + "SCALAR_STRADDLE_PREEDIT_DESIGN_AND_REVIEW_20261125.md"
    binding_path = "implementation/authority/SCALAR_STRADDLE_IMPLEMENTATION_AUTHORITY_BINDING.yaml"
    owner_path = leaf + "OWNER_SCALAR_STRADDLE_CONDITIONAL_EXECUTION_GRANT_20261125.json"
    inventory_path = leaf + "SCALAR_STRADDLE_FINITE_CASES_PROPOSED_20261125.json"
    pins = {
        brief_path: "04697219c5d5057ac3884aceb09d754dc391a66f6ed4a425459c938c684b1d8d",
        binding_path: "5a9397b702faaf05abf667d4d289677b88bb580ca1d5f23fa227e2282c2eb9b9",
        owner_path: "a7fb45cc876e1450f59678c6599113d86b7b59db9a855e0481edd64f717dc375",
        inventory_path: "d8fd00cb7352d11fcd364b98a533b894b45c864d2cd6311b8db5cb70eaf57480",
    }
    for name, digest in pins.items():
        if sha256(safe_path(root, name)) != digest:
            raise ValueError("scalar straddle fixed authority bytes mismatch: " + name)
    brief = safe_path(root, brief_path)
    binding = safe_path(root, binding_path)
    validate_implementation_authority(root, binding, brief)
    authority = yaml.safe_load(binding.read_text(encoding="utf-8"))
    if (
        authority["targets"] != [{"action": "modify", "object_id": n} for n in ("M02", "G01")]
        or authority["acceptance"] != {
            "status": "ACCEPTED_FOR_IMPLEMENTATION", "authority_ref": owner_path,
        }
    ):
        raise ValueError("scalar straddle ordered owner projection mismatch")
    owner = read_json(safe_path(root, owner_path))
    grant = owner["exact_proposal_approved"]
    inventory = read_json(safe_path(root, inventory_path))
    cases = inventory["physical_cases"]
    if (
        grant["proposed_exact_nonfungible_ceilings"] != {row[0]: row[6] for row in exact}
        or grant["brief"]["sha256"] != pins[brief_path]
        or grant["finite_inventory"]["sha256"] != pins[inventory_path]
        or len(cases) != 34 or len({case["case_id"] for case in cases}) != 34
        or len({case["node"] for case in cases}) != 34
    ):
        raise ValueError("scalar straddle exact owner allocation mismatch")
    result = []
    for jurisdiction, claim_id, proof_id, family_id, directory, filename, count in present:
        prefix = "config/product_proof/" + directory
        physical_root = "tests/product/" + directory
        family_path = physical_root + "/" + filename
        expected = {
            "schema_version": "1.0",
            "claim_id": claim_id,
            "brief_path": brief_path,
            "binding_path": binding_path,
            "contract_path": leaf + "SCALAR_STRADDLE_" + jurisdiction + "_PROOF_CONTRACT.json",
            "physical_root": physical_root,
            "admission_path": prefix + "/admission.json",
        }
        if read_json(safe_path(root, prefix + "/claim.json")) != expected:
            raise ValueError("scalar straddle fixed claim descriptor mismatch")
        rows = [case for case in cases if case["family"] == jurisdiction]
        names = [case["node"].split("::", 1)[1] for case in rows]
        owner_rows = owner["physical_cases_by_jurisdiction"][jurisdiction]
        if (
            len(rows) != count
            or any(case["proof_id"] != proof_id for case in rows)
            or any(case["node"] != family_path + "::" + name
                   for case, name in zip(rows, names, strict=True))
            or [(row["case_id"], row["node"]) for row in owner_rows]
            != [(row["case_id"], row["node"]) for row in rows]
        ):
            raise ValueError("scalar straddle physical allocation identity mismatch")
        claim_rows = [row for row in inventory["claims"] if row["jurisdiction"] == jurisdiction]
        if (
            len(claim_rows) != 1
            or claim_rows[0]["claim_id"] != claim_id
            or claim_rows[0]["proof_id"] != proof_id
            or claim_rows[0]["descriptor_directory"] != prefix
            or claim_rows[0]["physical_root"] != physical_root
            or claim_rows[0]["family_path"] != family_path
            or claim_rows[0]["proposed_case_count"] != count
        ):
            raise ValueError("scalar straddle inventory/claim association mismatch")
        contract = read_json(safe_path(root, expected["contract_path"]))
        _schema(root, contract, "accepted_brief_product_proof.schema.json")
        if (
            contract["claim_id"] != claim_id
            or contract["semantic_brief_path"] != brief_path
            or contract["target"] != {
                "category": "M", "responsibility_name": "neutral_market_measurement_truth",
                "package": "nvda_desk.market_measurement_truth",
                "public_seam": "nvda_desk.market_measurement_truth.api",
                "intent": "modify", "existing_object_id": "M02",
            }
            or contract["required_proof_ids"] != [proof_id]
            or len(contract["families"]) != 1
            or any(v != "FAIL" for v in contract["execution_policy"].values())
        ):
            raise ValueError("scalar straddle exact contract/owner association mismatch")
        family = contract["families"][0]
        if (
            family["id"] != family_id
            or family["path"] != family_path
            or family["proof_obligation_ids"] != [proof_id]
            or family["required_test_names"] != names
            or family["command"] != "python -m pytest " + family_path
            or contract["required_support_files"]
            or contract["optional_support_files"]
        ):
            raise ValueError("scalar straddle exact family/node jurisdiction mismatch")
        entry = {key: value for key, value in expected.items() if key != "brief_path"}
        entry["profile"] = "accepted_brief_v2"
        target_id, _ = _target(root, contract["target"])
        _generation(root, entry, contract, pins[brief_path], target_id)
        result.append((entry, contract, pins[brief_path]))
    return tuple(result)


def _aligned_history_extensions(
    root: Path,
) -> tuple[tuple[dict[str, Any], dict[str, Any], str], ...]:
    """Five exact reviewed underlying-history claim routes, dormant without descriptors."""
    leaf = "handoff/m02_completion_28_execution/L01a/"
    # Separate, nonfungible own-brief, binding, contract and descriptor pins.
    exact = (
        (
            'D071',
            '65f2d0f9135f291773ab6081ec76892a967315df3ecb9c1760a4e2687a296e5e',
            '30cbb5fe2f8a1b720bc58b55b05f3c88b736401f03d03199404444b60330dc03',
            '5f771b88c96699b9dd56b724e9e87df6f541706bdfff442842ee70d4daaedb30',
            'cea962241291786b3c2606cc56f003b77809352c7643408af88487e8200cb526',
        ),
        (
            'D072',
            '4f8214d1ca11eaf0769206f3f322c799f44883bd266e63748e937dea5602b739',
            '637ff9b90b916ee69ee956db28e191ef86be3764ce2004b5fc24e371fa5869df',
            '1b1974b23aa8e79b6c420b0cb32f09ad34220d7672d7239bc0b425ce14ff82e3',
            '1260a7c77fe9ac48c07b44cb53c3830df4a0f6b6d77c1824d224325613eb5abb',
        ),
        (
            'D073',
            'a7234477d581e6cba27e470919fa092c4ed5054d5a1aa31d2019d8fa94d16f48',
            '867444cecdf23c191269b1b3856410cc1ee6e3b81b8730dafa6d6528b78d6e0a',
            '0105ec67828efed9019c75808c6d79315ddb7c9e0c9a8a666d49b46cf9fcfdb5',
            '8e61dc08aa7324bdf128419096ac4afb85731e047ca4bfcc2da377e2f0f4a084',
        ),
        (
            'D074',
            '524b2d2a4aa94a0c1c55ea376650d14648af67c46e73763ce3e8cc0f2e9e0c0e',
            'f2a2208a73d291e614577eaf2b81ffd13d699c4efbc2eeeb6258569ac8aa1c34',
            '708f6dc03c755e68c8232f699d80b2b27d973b7e2406daacf4f5fdc3f34d8d79',
            '622726a8fa4da0cc4890390335d6f159aacc823f9a13917a007f2ef77f1eb94a',
        ),
        (
            'D075',
            '24ec8f08faf1a61059cee69b8c675767345809ae6a0dd90ab852a2fc30977750',
            '50120c02327ed212e8821ac3795d4f64daa3e38d77ecd5c92c7b20f6a2ba8c3f',
            '6bfc41f1415ff9c68776f0ae79c6b35ec19cb3e0a16dc2a0706970be57dc8d8f',
            '19d2f6e7c31089158bb7aa6fa4fafb00fd0448e4e8db1f16bbd581315dbbaf13',
        ),
    )
    present = tuple(
        row for row in exact
        if safe_path(
            root, f"config/product_proof/m02_aligned_history_{row[0].lower()}/claim.json",
        ).exists()
    )
    if not present:
        return ()
    owner_path = (
        "handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json"
    )
    policy_path = leaf + "ALIGNED_HISTORY_SOURCE_POLICY_PROPOSED_20261126.json"
    manifest_path = leaf + "ALIGNED_HISTORY_FINITE_SPECIMENS_PROPOSED_20261126.json"
    inventory_path = leaf + "ALIGNED_HISTORY_JOINT_FIT_FINITE_CASES_PROPOSED_20261126.json"
    remap_owner_path = leaf + "OWNER_G01_PROSPECTIVE_PARTITION_REMAP_AUTHORIZATION_20261128.json"
    remap_path = leaf + "G01_PARTITION_REMAP_20261128/PATH_ONLY_SUCCESSOR_AUTHORITY.json"
    pins = {
        remap_owner_path: "cbc85f756911a9f1a926f862284168acc6f83266f8f07c0b1b68e3e2547190ff",
        remap_path: "11d90adf234d5195d3bd31a6b42df9b046c4ad53690cb279ef071d52b3049aa7",
        owner_path: "6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41",
        policy_path: "9ba56098c273007980c893db39931ac86e7a3185bbb665f8c3f1e14f99b72af1",
        manifest_path: "bb03481de75e1820c7aff61777a4a3aa4f676440ec03e373a05c032a0417c76d",
        inventory_path: "3be150f2998b4187a81720b424c848099edeba7a9f638ae90d9aae95d4c5d5c1",
    }
    for path, digest in pins.items():
        if sha256(safe_path(root, path)) != digest:
            raise ValueError("aligned history fixed authority mismatch: " + path)
    owner = read_json(safe_path(root, owner_path))
    package, = [row for row in owner["adopted_packages"] if row["package"] == "aligned_history"]
    inventory = read_json(safe_path(root, inventory_path))
    remapping = read_json(safe_path(root, remap_path))
    cases = inventory["physical_cases"]
    if (
        owner["exact_total_cases"] != 64
        or package["policy"]["sha256"] != pins[policy_path]
        or package["specimens"]["sha256"] != pins[manifest_path]
        or package["inventory"]["sha256"] != pins[inventory_path]
        or package["claims"] != inventory["claims"]
        or package["exact_nonfungible_ceilings"] != inventory["proposed_exact_nonfungible_ceilings"]
        or len(cases) != 34 or len({row["case_id"] for row in cases}) != 34
        or len({row["node"] for row in cases}) != 34
    ):
        raise ValueError("aligned history owner finite-allocation mismatch")
    result = []
    for jurisdiction, brief_hash, binding_hash, contract_hash, descriptor_hash in present:
        lower = jurisdiction.lower()
        prefix = f"config/product_proof/m02_aligned_history_{lower}"
        original_root = f"tests/product/m02_completion_28/support/{lower}-history"
        original_family_path = original_root + "/test_profile.py"
        physical_root = f"tests/product/m02_completion_28_prospective/support/{lower}-history"
        family_path = physical_root + "/test_profile.py"
        claim_id = f"neutral_market_measurement_truth_l01a_{lower}_history"
        proof_id = f"SUP-{jurisdiction}-HISTORY"
        family_id = f"m02_l01a_aligned_history_{lower}"
        brief_path = leaf + f"ALIGNED_HISTORY_{jurisdiction}_IMPLEMENTATION_BRIEF.md"
        binding_path = (
            f"implementation/authority/T01_ALIGNED_HISTORY_{jurisdiction}_AUTHORITY_BINDING.yaml"
        )
        original_contract_path = leaf + f"ALIGNED_HISTORY_{jurisdiction}_PROOF_CONTRACT.json"
        contract_path = (
            leaf + "G01_PARTITION_REMAP_20261128/"
            + f"ALIGNED_HISTORY_{jurisdiction}_PROOF_CONTRACT.json"
        )
        expected = {
            "schema_version": "1.0",
            "claim_id": claim_id,
            "brief_path": brief_path,
            "binding_path": binding_path,
            "contract_path": contract_path,
            "physical_root": physical_root,
            "admission_path": prefix + "/admission.json",
        }
        for path, digest in (
            (brief_path, brief_hash), (binding_path, binding_hash),
            (contract_path, contract_hash), (prefix + "/claim.json", descriptor_hash),
        ):
            if sha256(safe_path(root, path)) != digest:
                raise ValueError("aligned history exact own-jurisdiction bytes mismatch: " + path)
        if read_json(safe_path(root, prefix + "/claim.json")) != expected:
            raise ValueError("aligned history exact claim descriptor mismatch")
        binding, brief = safe_path(root, binding_path), safe_path(root, brief_path)
        validate_implementation_authority(root, binding, brief)
        authority = yaml.safe_load(binding.read_text(encoding="utf-8"))
        if (
            authority["targets"] != [
                {"action": "modify", "object_id": n} for n in ("M02", "G01")
            ]
            or authority["acceptance"] != {
                "status": "ACCEPTED_FOR_IMPLEMENTATION", "authority_ref": owner_path,
            }
        ):
            raise ValueError("aligned history own binding target or authority mismatch")
        claim, = [row for row in inventory["claims"] if row["jurisdiction"] == jurisdiction]
        own = [row for row in cases if row["family"] == jurisdiction]
        nodes = [row["node"] for row in own]
        names = [node.split("::", 1)[1] for node in nodes]
        if (
            package["exact_nonfungible_ceilings"][jurisdiction] != 2
            or len(own) != 2 or any(row["proof_id"] != proof_id for row in own)
            or claim["proof_id"] != proof_id or claim["claim_id"] != claim_id
            or claim["family_id"] != family_id or claim["family_path"] != original_family_path
            or claim["descriptor_directory"] != prefix or claim["physical_root"] != original_root
            or claim["own_brief_path"] != brief_path or claim["own_binding_path"] != binding_path
            or claim["future_contract_path"] != original_contract_path
            or claim["proposed_case_count"] != 2 or claim["proposed_nonfungible_ceiling"] != 2
            or claim["ordered_case_ids"] != [row["case_id"] for row in own]
            or claim["ordered_nodes"] != nodes
            or nodes != [original_family_path + "::" + name for name in names]
        ):
            raise ValueError("aligned history nonfungible family allocation mismatch")
        remap, = [row for row in remapping["claims"] if row["proof_id"] == proof_id]
        if (
            remap["package"] != "aligned_history"
            or remap["jurisdiction"] != jurisdiction
            or remap["claim_id"] != claim_id or remap["family_id"] != family_id
            or remap["original_root"] != original_root
            or remap["original_family_path"] != original_family_path
            or remap["original_ordered_nodes"] != nodes
            or remap["ordered_case_ids"] != claim["ordered_case_ids"]
            or remap["descriptor_directory"] != prefix
            or remap["own_brief_path"] != brief_path
            or remap["own_binding_path"] != binding_path
            or remap["original_contract_path"] != original_contract_path
            or remap["new_contract_path"] != contract_path
            or remap["new_root"] != physical_root or remap["new_family_path"] != family_path
            or remap["new_ordered_nodes"] != [family_path + "::" + name for name in names]
            or remap["exact_case_count"] != 2 or remap["exact_nonfungible_ceiling"] != 2
            or remap["scope"] != "INACTIVE_FIRST_STAGE_ARTEFACTS"
            or remap["execution_release"] is not False
        ):
            raise ValueError("aligned history path-only successor authority mismatch")
        contract = read_json(safe_path(root, contract_path))
        _schema(root, contract, "accepted_brief_product_proof.schema.json")
        if (
            contract["claim_id"] != claim_id
            or contract["semantic_brief_path"] != brief_path
            or contract["target"] != {
                "category": "M", "responsibility_name": "neutral_market_measurement_truth",
                "package": "nvda_desk.market_measurement_truth",
                "public_seam": "nvda_desk.market_measurement_truth.api",
                "intent": "modify", "existing_object_id": "M02",
            }
            or contract["required_proof_ids"] != [proof_id]
            or len(contract["families"]) != 1
            or any(value != "FAIL" for value in contract["execution_policy"].values())
        ):
            raise ValueError("aligned history exact contract/owner association mismatch")
        family = contract["families"][0]
        if (
            family["id"] != family_id or family["path"] != family_path
            or family["proof_obligation_ids"] != [proof_id]
            or family["required_test_names"] != names
            or family["command"] != "python -m pytest " + family_path
            or contract["required_support_files"] or contract["optional_support_files"]
        ):
            raise ValueError("aligned history exact family/node mismatch")
        entry = {key: value for key, value in expected.items() if key != "brief_path"}
        entry["profile"] = "accepted_brief_v2"
        target_id, _ = _target(root, contract["target"])
        _generation(root, entry, contract, brief_hash, target_id)
        result.append((entry, contract, brief_hash))
    return tuple(result)


def _native_reconciliation_extensions(
    root: Path,
) -> tuple[tuple[dict[str, Any], dict[str, Any], str], ...]:
    """The eleven exact L01 commissioned M02 siblings, admitted per owning leaf.

    A missing descriptor remains unadmitted; native test Python without its
    matching descriptor is refused. Original claim controls stay unchanged.
    """
    plan = read_json(safe_path(
        root, "handoff/downstream_reconciliation/authority/NATIVE_CLAIM_PLAN_V1.json"))
    if plan.get("schema_version") != 1 or len(plan.get("claims", ())) != 11:
        raise ValueError("fixed native reconciliation claim inventory mismatch")
    result = []
    seen: set[str] = set()
    for fixed in plan["claims"]:
        identity = fixed["identity"]
        if identity in seen or identity not in {
            "SOURCE", "D087", "D131", "D134", "D135", "D136", "D137",
            "D138", "D139", "D140", "D143",
        }:
            raise ValueError("unapproved native claim identity")
        seen.add(identity)
        expected = {name: fixed[name] for name in (
            "schema_version", "claim_id", "brief_path", "binding_path",
            "contract_path", "physical_root", "admission_path",
        )}
        descriptor = safe_path(root, fixed["descriptor_path"])
        if not descriptor.exists():
            physical = safe_path(root, fixed["physical_root"])
            if physical.exists() and any(physical.rglob("*.py")):
                raise ValueError("native source without fixed descriptor")
            continue
        if read_json(descriptor) != expected:
            raise ValueError("native fixed descriptor mismatch")
        brief = safe_path(root, fixed["brief_path"])
        binding = safe_path(root, fixed["binding_path"])
        if sha256(brief) != fixed["brief_sha256"] or sha256(binding) != fixed["binding_sha256"]:
            raise ValueError("native frozen authority bytes mismatch")
        validate_implementation_authority(root, binding, brief)
        if yaml.safe_load(binding.read_text())["targets"] != [
            {"action": "modify", "object_id": name} for name in ("M02", "G01")
        ]:
            raise ValueError("native owning target projection mismatch")
        contract = read_json(safe_path(root, fixed["contract_path"]))
        _schema(root, contract, "accepted_brief_product_proof.schema.json")
        if (contract["claim_id"] != fixed["claim_id"]
            or contract["semantic_brief_path"] != fixed["brief_path"]
            or len(contract["families"]) != 1
            or contract["families"][0]["path"] != fixed["family_path"]
            or contract["families"][0]["required_test_names"] != fixed["test_names"]
            or contract["target"] != {
                "category": "M", "responsibility_name": "neutral_market_measurement_truth",
                "package": "nvda_desk.market_measurement_truth",
                "public_seam": "nvda_desk.market_measurement_truth.api",
                "intent": "modify", "existing_object_id": "M02",
            }
            or any(v != "FAIL" for v in contract["execution_policy"].values())):
            raise ValueError("native exact claim association mismatch")
        entry = {k: v for k, v in expected.items() if k != "brief_path"}
        entry["profile"] = "accepted_brief_v2"
        target_id, _ = _target(root, contract["target"])
        _generation(root, entry, contract, fixed["brief_sha256"], target_id)
        result.append((entry, contract, fixed["brief_sha256"]))
    return tuple(result)


def load_product_proof_claim(repository_root: Path, claim_id: str) -> ProductProofClaim:
    root = repository_root.resolve()
    catalogue = read_json(root / "config/product_proof/claims.json")
    _schema(root, catalogue, "product_proof_claims.schema.json")
    authority = _authority(root, catalogue)
    extensions: dict[str, tuple[dict[str, Any], dict[str, Any], str]] = {}
    if authority is not None:
        identities: tuple[
            Literal[
                "D001",
                "D002",
                "D003",
                "D004",
                "D005",
                "D009",
        "D010",
                "D012",
                "D013",
                "D014",
                "D015",
                "D016",
                "D017",
                "D018",
                "D019",
                "D020",
                "D021",
                "D022",
                "D023",
                "D024",
                "D025",
                "D026",
                "D027",
                "D028",
                "D029",
                "D030",
                "D031",
                "D032",
                "D033",
                "D034",
                "D035",
                "D036",
                "D037",
                "D038",
                "D039",
                "D042",
                "D043",
                "D044",
                "D045",
                "D046",
                "D047",
                "D048",
                "D049",
                "D050",
                "D051",
                "D052",
                "D053",
                "D054",
                "D055",
                "D056",
                "D057",
                "D058",
                "D059",
                "D060",
                "D063",
                "D066",
                "D067",
                "D068",
                "D069",
                "D071",
                "D072",
                "D073",
                "D074",
                "D075",
                "D076",
                "D077",
                "D082",
                "D083",
                "D087",
                "D088",
        "D089",
        "D090",
        "D092",
        "D093",
        "D094",
        "D099",
        "D100",
        "D101",
        "D103",
        "D104",
        "D105",
        "D106",
        "D116",
        "D117",
        "D118",
        "D119",
        "D123",
        "D124",
        "D131",
        "D134",
        "D135",
        "D136",
        "D137",
        "D138",
        "D139",
        "D140",
        "D143",
            ],
            ...,
        ] = (
            "D001",
            "D002",
            "D003",
            "D004",
            "D005",
            "D009",
        "D010",
            "D012",
            "D013",
            "D014",
            "D015",
            "D016",
            "D017",
            "D018",
            "D019",
            "D020",
            "D021",
            "D022",
            "D023",
            "D024",
            "D025",
            "D026",
            "D027",
            "D028",
            "D029",
            "D030",
            "D031",
            "D032",
            "D033",
            "D034",
            "D035",
            "D036",
            "D037",
            "D038",
            "D039",
            "D042",
            "D043",
            "D044",
            "D045",
            "D046",
            "D047",
            "D048",
            "D049",
            "D050",
            "D051",
            "D052",
            "D053",
            "D054",
            "D055",
            "D056",
            "D057",
            "D058",
            "D059",
            "D060",
            "D063",
            "D066",
            "D067",
            "D068",
            "D069",
            "D071",
            "D072",
            "D073",
            "D074",
            "D075",
            "D076",
            "D077",
            "D082",
            "D083",
            "D087",
            "D088",
        "D089",
        "D090",
        "D092",
        "D093",
        "D094",
        "D099",
        "D100",
        "D101",
        "D103",
        "D104",
        "D105",
        "D106",
        "D116",
        "D117",
        "D118",
        "D119",
        "D123",
        "D124",
        "D131",
        "D134",
        "D135",
        "D136",
        "D137",
        "D138",
        "D139",
        "D140",
        "D143",
        )
        for identity in identities:
            extension = _scalar_extension(root, identity)
            if extension is not None:
                extensions[extension[0]["claim_id"]] = extension
        for configured_identity in ("D040", "D041"):
            configured = _configured_extension(root, configured_identity)
            if configured is not None:
                extensions[configured[0]["claim_id"]] = configured
    m00 = _m00_brief2_extension(root) if authority is not None else None
    if m00 is not None:
        extensions[m00[0]["claim_id"]] = m00
    if authority is not None:
        for native in _native_reconciliation_extensions(root):
            extensions[native[0]["claim_id"]] = native
        d091 = _d091_l01b_extension(root)
        if d091 is not None:
            extensions[d091[0]["claim_id"]] = d091
        for scalar_straddle in _scalar_straddle_extensions(root):
            claim = scalar_straddle[0]["claim_id"]
            if claim in extensions:
                raise ValueError("duplicate scalar straddle claim extension identity")
            extensions[claim] = scalar_straddle
        for aligned in _aligned_history_extensions(root):
            claim = aligned[0]["claim_id"]
            if claim in extensions:
                raise ValueError("duplicate aligned history claim extension identity")
            extensions[claim] = aligned
    if extensions:
        catalogue = {
            **catalogue,
            "claims": [*catalogue["claims"], *(item[0] for item in extensions.values())],
        }
    ids = [entry["claim_id"] for entry in catalogue["claims"]]
    if len(ids) != len(set(ids)) or claim_id not in ids:
        raise ValueError(f"unknown/duplicate product claim: {claim_id}")
    entry = next(row for row in catalogue["claims"] if row["claim_id"] == claim_id)
    if authority is None:
        return ProductProofClaim(
            claim_id, entry["profile"], None, None, None, None, "AWAITING_AUTHORITY", (), (), ()
        )
    brief_hash, incorporated = authority
    contracts = {}
    for row in catalogue["claims"]:
        if row["profile"] == "accepted_brief_v2":
            is_extension = row["claim_id"] in extensions
            if not is_extension and row["contract_path"] not in incorporated:
                raise ValueError("unincorporated claim contract")
            contract = read_json(safe_path(root, row["contract_path"]))
            _schema(root, contract, "accepted_brief_product_proof.schema.json")
            if contract["claim_id"] != row["claim_id"] or (
                not is_extension
                and (
                    contract["semantic_brief_path"] != catalogue["control_authority"]["brief_path"]
                    or row["binding_path"] != catalogue["control_authority"]["binding_path"]
                )
            ):
                raise ValueError("cross-claim authority association mismatch")
            paths = [family["path"] for family in contract["families"]]
            family_ids = [family["id"] for family in contract["families"]]
            if len(set(paths)) != len(paths) or len(set(family_ids)) != len(family_ids):
                raise ValueError("duplicate family path/identity")
            covered = set()
            for family in contract["families"]:
                if family["command"] != "python -m pytest " + family["path"]:
                    raise ValueError("arbitrary family command")
                covered.update(family["proof_obligation_ids"])
                for dimension in family["case_coverage"].values():
                    if bool(dimension.get("cases")) == bool(dimension.get("not_applicable_reason")):
                        raise ValueError("invalid four-case dimension")
            if covered != set(contract["required_proof_ids"]):
                raise ValueError("incomplete contract proposition coverage")
            contracts[row["claim_id"]] = contract
    owned_family_ids: set[str] = set()
    proof_ids: set[str] = set()
    for contract in contracts.values():
        current_families = {family["id"] for family in contract["families"]}
        current_proofs = set(contract["required_proof_ids"])
        if owned_family_ids & current_families or proof_ids & current_proofs:
            raise ValueError("cross-claim family/proof ownership collision")
        owned_family_ids.update(current_families)
        proof_ids.update(current_proofs)
    from validate_product_proof import _validate_legacy_product_proof

    legacy_families = yaml.safe_load((root / "config/product_proof/families.yaml").read_text())[
        "families"
    ]
    _validate_legacy_product_proof(root, {f["path"] for f in legacy_families})
    _partition(root, catalogue, contracts)
    snapshot = governed_snapshot(root)
    if entry["profile"] == "historical_backend_v1":
        families = legacy_families
        result = tuple(
            AdmittedProductFamily(
                f["id"], f["path"], tuple(f["proof_obligation_ids"]), (), sha256(root / f["path"])
            )
            for f in families
        )
        return ProductProofClaim(
            claim_id,
            entry["profile"],
            "M00",
            "active",
            brief_hash,
            None,
            "HISTORICAL_NOT_RUNNABLE",
            result,
            (),
            snapshot,
        )
    contract = contracts[claim_id]
    if claim_id in extensions:
        brief_hash = extensions[claim_id][2]
    target_id, status = _target(root, contract["target"])
    generation_hash, files = _generation(root, entry, contract, brief_hash, target_id)
    families = tuple(
        AdmittedProductFamily(
            f["id"],
            f["path"],
            tuple(f["proof_obligation_ids"]),
            tuple(f["required_test_names"]),
            files.get(f["path"]),
        )
        for f in contract["families"]
    )
    if target_id is None or status not in {"bootstrap", "active"}:
        state = "AWAITING_TARGET"
    elif not any((root / f.path).exists() for f in families):
        state = "INCOMPLETE_NO_PHYSICAL_FAMILIES"
    elif generation_hash is None:
        state = "INCOMPLETE_COVERAGE"
    else:
        state = "READY_FOR_PROOF"
    family_paths = {f.path for f in families}
    support = tuple(
        sorted((name, digest) for name, digest in files.items() if name not in family_paths)
    )
    return ProductProofClaim(
        claim_id,
        entry["profile"],
        target_id,
        status,
        brief_hash,
        generation_hash,
        state,
        families,
        support,
        snapshot,
    )
