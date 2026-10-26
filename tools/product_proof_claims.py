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
    for path in (root / "tests/product").rglob("*"):
        if path.is_symlink():
            raise ValueError("symlink in product proof jurisdiction")
        if path.is_file() and path.name.startswith("test_") and path.suffix == ".py":
            name = path.relative_to(root).as_posix()
            if name not in owned:
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
        )
        for identity in identities:
            extension = _scalar_extension(root, identity)
            if extension is not None:
                extensions[extension[0]["claim_id"]] = extension
        for configured_identity in ("D040", "D041"):
            configured = _configured_extension(root, configured_identity)
            if configured is not None:
                extensions[configured[0]["claim_id"]] = configured
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
