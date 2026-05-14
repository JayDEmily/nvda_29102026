#!/usr/bin/env python3
"""Generate a static structural inventory scaffold from the current repo tree.

This tool is audit/control tooling only. It does not import runtime package modules,
execute tests, alter source, alter tests, alter vocabulary, or rewrite Atlas/Bridge JSON.
"""
from __future__ import annotations

import ast
import fnmatch
import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
SCHEMA_PATH = OUT_DIR / "active_code_atlas_schema.json"
ATLAS_PATH = OUT_DIR / "active_code_atlas.json"
INVENTORY_PATH = OUT_DIR / "active_code_atlas_surface_inventory.json"
READ_LEDGER_PATH = OUT_DIR / "active_code_atlas_read_ledger.json"
SURFACE_META_PATH = OUT_DIR / "active_code_atlas_surface_metadata.json"

CURRENT_MAP = ROOT / "NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md"
BLUEPRINT = ROOT / "docs" / "11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md"
LEGACY_ATLAS = ROOT / "var" / "audit" / "imports" / "atlas_bridge_inputs" / "legacy_intent_atlas.json"
BRIDGE_LEDGER = ROOT / "var" / "audit" / "ledgers" / "intent_migration" / "native_intent_satisfaction_ledger.json"
SLICE_MANIFEST = ROOT / "var" / "audit" / "atlas_surface_slices" / "atlas_surface_slice_manifest.json"
LIMITATION_STATEMENT = "This is static structural evidence only. It does not prove semantic correctness, native satisfaction, implementation maturity, or test pass status."


ACTIVE_ROOT_PREFIXES = (
    "src/",
    "tests/",
    "config/",
    "data/",
    "docs/",
    "schemas/",
    "var/audit/",
    "project_control/",
)
ROOT_FILES = {
    "AGENTS.md",
    "PLANS.md",
    "ROADMAP_LEDGER.md",
    "NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md",
    "CURRENT_PROJECT_STATE.md",
    "PROJECT_STRUCTURE.md",
    "README.md",
    "Makefile",
    "pyproject.toml",
    "uv.lock",
    ".python-version",
    ".env.example",
}
EXCLUDED_PREFIXES = (
    "legacy_import/",
    "intent_migration/",
    "remote_bridge_inbox/",
    "_archive/",
    ".git/",
    ".venv/",
    "__pycache__/",
)
SELF_EXCLUDED = (
    "var/audit/active_code_atlas_001/active_code_atlas.json",
    "var/audit/active_code_atlas_001/active_code_atlas_surface_inventory.json",
    "var/audit/active_code_atlas_001/active_code_atlas_read_ledger.json",
    "var/audit/active_code_atlas_001/active_code_atlas_validation_report.json",
    "var/audit/active_code_atlas_001/active_code_atlas_surface_metadata.json",
)

REQUIRED_FIELDS = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["record_required_fields"]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_count(path: Path) -> int:
    data = path.read_bytes()
    if not data:
        return 1
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def parse_markdown_table_line(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_current_map_surfaces() -> dict[str, dict[str, Any]]:
    surfaces: dict[str, dict[str, Any]] = {}
    for lineno, line in enumerate(read_text(CURRENT_MAP).splitlines(), start=1):
        if not line.startswith("| 5."):
            continue
        cells = parse_markdown_table_line(line)
        if len(cells) < 9:
            continue
        row_id, surface, owner, structural, impl, evidence, tests, gap, next_action = cells[:9]
        paths = re.findall(r"`([^`]+)`", evidence + "; " + tests)
        surfaces[surface] = {
            "row_id": row_id,
            "surface": surface,
            "target_owner": owner.strip().rstrip("."),
            "structural_status": structural.strip("`.").strip(),
            "implementation_truth_status": impl.strip("`.").strip(),
            "observed_native_repo_evidence": evidence,
            "observed_proof_test_evidence": tests,
            "current_blocker_or_gap": gap,
            "next_lawful_action": next_action,
            "current_map_line": lineno,
            "current_map_path": rel(CURRENT_MAP),
            "evidence_patterns": paths,
        }
    return surfaces


def parse_blueprint_surface_lines() -> dict[str, dict[str, Any]]:
    text = read_text(BLUEPRINT).splitlines()
    result: dict[str, dict[str, Any]] = {}
    current_surface = None
    start = None
    for idx, line in enumerate(text, start=1):
        m = re.match(r"### (5\.\d+) (.+)$", line)
        if m:
            if current_surface is not None and start is not None:
                result[current_surface]["blueprint_line_end"] = idx - 1
            row, surface = m.groups()
            current_surface = surface
            start = idx
            result[surface] = {"row_id": row, "blueprint_line_start": idx, "blueprint_path": rel(BLUEPRINT)}
    if current_surface is not None and start is not None:
        result[current_surface]["blueprint_line_end"] = len(text)
    return result


def parse_bridge_surface_counts() -> dict[str, int]:
    if not BRIDGE_LEDGER.exists():
        return {}
    data = json.loads(read_text(BRIDGE_LEDGER))
    counts: dict[str, int] = {}
    for record in data.get("records", []):
        surface = record.get("blueprint_surface") or "unknown"
        counts[surface] = counts.get(surface, 0) + 1
    return counts


def parse_atlas_counts() -> dict[str, Any]:
    out: dict[str, Any] = {}
    if LEGACY_ATLAS.exists():
        data = json.loads(read_text(LEGACY_ATLAS))
        out["legacy_intent_record_count"] = len(data.get("records", []))
        out["legacy_intent_sha256"] = sha256_file(LEGACY_ATLAS)
        out["legacy_intent_top_level_keys"] = list(data.keys())
    if BRIDGE_LEDGER.exists():
        data = json.loads(read_text(BRIDGE_LEDGER))
        out["bridge_record_count"] = len(data.get("records", []))
        out["bridge_sha256"] = sha256_file(BRIDGE_LEDGER)
        out["bridge_top_level_keys"] = list(data.keys())
    if SLICE_MANIFEST.exists():
        data = json.loads(read_text(SLICE_MANIFEST))
        out["slice_manifest_sha256"] = sha256_file(SLICE_MANIFEST)
        out["slice_count"] = data.get("slice_count") or len(data.get("slices", []))
        out["slice_manifest_keys"] = list(data.keys())
    return out


def backtick_patterns_to_globs(pattern: str) -> list[str]:
    p = pattern.strip().rstrip(";")
    if not p:
        return []
    if p.endswith("/*"):
        return [p, p[:-1] + "**"]
    if p.endswith("*"):
        return [p]
    if p.endswith("/"):
        return [p + "**"]
    return [p]


def path_matches_pattern(path: str, pattern: str) -> bool:
    for glob in backtick_patterns_to_globs(pattern):
        if fnmatch.fnmatch(path, glob):
            return True
        if glob.endswith("/**") and path.startswith(glob[:-3]):
            return True
        if path == glob:
            return True
    return False


def heuristic_surface(path: str) -> tuple[str, str, str]:
    lower = path.lower()
    if path.startswith("tests/") or path.startswith("docs/08") or "proof" in lower or "test_" in lower:
        return "Testing, proof, and checkpoint surfaces", "inferred", "testing/proof path heuristic"
    if "vocabulary" in lower or path.startswith("docs/10") or path.startswith("docs/vocabulary"):
        return "Vocabulary governance interface", "inferred", "vocabulary path heuristic"
    if "calendar" in lower or "event" in lower and path.startswith("data/reference/financial_calendar"):
        return "Financial and event calendar architecture", "inferred", "calendar/reference path heuristic"
    if "/adapters/" in lower or "/api/" in lower or "external_source" in lower or "broker" in lower:
        return "External source interfaces and API ingress", "inferred", "adapter/api path heuristic"
    if "raw_signal" in lower or "upstream" in lower:
        return "Raw signal families", "inferred", "raw/upstream path heuristic"
    if "raw_bundle" in lower or "source_temporal" in lower:
        return "Raw capture and source temporal law", "inferred", "raw capture path heuristic"
    if "preparation" in lower or "prepared" in lower or "stage_inputs" in lower or "/cognition/ingress/" in lower:
        return "Prepared ingress and runtime context preparation", "inferred", "preparation path heuristic"
    if "dmp" in lower or "packet" in lower or "envelope" in lower:
        return "DMPV3 packet carriage", "inferred", "packet/dmp path heuristic"
    if "/cognition/serial/" in lower or "eligibility_service" in lower or "execution_service" in lower or "posture_service" in lower or "orchestrator" in lower or "regime_context" in lower or "options_flow_context" in lower:
        return "Serial desk-cognition spine", "inferred", "serial cognition path heuristic"
    if "parallel_risk" in lower:
        return "Parallel risk lane", "inferred", "parallel risk path heuristic"
    if "coefficient" in lower or "modifier" in lower or "runtime_settings" in lower or "config_surface" in lower:
        return "Dynamic coefficient and modifier authority", "inferred", "config/coefficient/modifier path heuristic"
    if "playbook" in lower:
        return "Playbook library architecture", "inferred", "playbook path heuristic"
    if "capital" in lower:
        return "Downstream capital deployment authority", "inferred", "capital path heuristic"
    if "opening" in lower or "placement" in lower:
        return "Opening architecture and placement readiness", "inferred", "opening/placement path heuristic"
    if "inventory" in lower or "position" in lower:
        return "Live position and inventory architecture", "inferred", "live inventory/position path heuristic"
    if "exit" in lower or "close" in lower or "lifecycle" in lower:
        return "Exit and close architecture", "inferred", "exit/close path heuristic"
    if "review" in lower or "replay" in lower or "explanation" in lower or "trace" in lower:
        return "Review and explanation layer", "inferred", "review/replay path heuristic"
    if "repository" in lower or "persistence" in lower or "ledger" in lower or "receipt" in lower or path.startswith("alembic/") or path.startswith("var/audit/") or path.startswith("assembly_reports/"):
        return "Persistence, ledgers, and receipts", "inferred", "persistence/audit path heuristic"
    if path.startswith("docs/11"):
        return "blocked_blueprint", "unresolved", "blueprint governs all surfaces, not one surface"
    if path.startswith("docs/") or path in ROOT_FILES or path.startswith("project_control/") or path.startswith("schemas/"):
        return "Testing, proof, and checkpoint surfaces", "inferred", "control/documentation path heuristic"
    return "blocked_blueprint", "unresolved", "no governed surface match"


def map_surface(path: str, surfaces: dict[str, dict[str, Any]]) -> tuple[str, str, str]:
    best: tuple[int, str, str] | None = None
    for surface, meta in surfaces.items():
        for pattern in meta.get("evidence_patterns", []):
            if path_matches_pattern(path, pattern):
                score = len(pattern.replace("*", ""))
                if best is None or score > best[0]:
                    best = (score, surface, pattern)
    if best is not None:
        return best[1], "direct", f"matched current-state map evidence pattern `{best[2]}`"
    return heuristic_surface(path)


def file_kind(path: str) -> tuple[str, str]:
    p = Path(path)
    suffix = p.suffix.lower()
    if path.startswith("src/") and suffix == ".py":
        return "runtime_module", "module"
    if path.startswith("tests/") and suffix == ".py":
        return "test_module", "test_module"
    if path.startswith("config/"):
        return "config_contract", "config_file"
    if path.startswith("data/"):
        return "data_reference", "data_file"
    if path.startswith("schemas/") or suffix == ".schema.json":
        return "schema_contract", "schema_file"
    if path.startswith("docs/") or path in {"AGENTS.md", "PLANS.md", "ROADMAP_LEDGER.md", "NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md"}:
        return "normative_or_control_document", "markdown_document"
    if path.startswith("var/audit/"):
        if "atlas_bridge_inputs" in path or "intent_migration/native_intent_satisfaction" in path or "atlas_surface_slices" in path:
            return "atlas_bridge_evidence", "audit_evidence_file"
        return "audit_receipt_or_ledger", "audit_evidence_file"
    if path.startswith("project_control/"):
        return "project_control_surface", "control_file"
    if path in {"Makefile", "pyproject.toml", "uv.lock", ".python-version", ".env.example"}:
        return "build_or_environment_contract", "config_file"
    return "repo_file", "file"


def python_imports(tree: ast.AST) -> list[str]:
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level + (node.module or "")
            imports.append(prefix)
    return sorted(set(imports))


def decorators(node: ast.AST) -> list[str]:
    out = []
    for dec in getattr(node, "decorator_list", []):
        try:
            out.append(ast.unparse(dec))
        except Exception:
            out.append(type(dec).__name__)
    return out


def signature(node: ast.AST) -> str:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        args = []
        for arg in node.args.posonlyargs + node.args.args:
            args.append(arg.arg)
        if node.args.vararg:
            args.append("*" + node.args.vararg.arg)
        for arg in node.args.kwonlyargs:
            args.append(arg.arg)
        if node.args.kwarg:
            args.append("**" + node.args.kwarg.arg)
        returns = ""
        if node.returns is not None:
            try:
                returns = " -> " + ast.unparse(node.returns)
            except Exception:
                returns = " -> <annotation>"
        return f"({', '.join(args)}){returns}"
    if isinstance(node, ast.ClassDef):
        bases = []
        for base in node.bases:
            try:
                bases.append(ast.unparse(base))
            except Exception:
                bases.append(type(base).__name__)
        return f"({', '.join(bases)})" if bases else "()"
    return ""


def docstring_range(node: ast.AST) -> tuple[int, int] | None:
    body = getattr(node, "body", None)
    if not body:
        return None
    first = body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        return (getattr(first, "lineno", 1), getattr(first, "end_lineno", getattr(first, "lineno", 1)))
    return None


def literal_values(node: ast.AST, limit: int = 12) -> list[str]:
    vals: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, (str, int, float, bool, type(None))):
            if isinstance(child.value, str) and len(child.value) > 80:
                continue
            vals.append(repr(child.value))
            if len(vals) >= limit:
                break
    return vals


def branch_summary(node: ast.AST) -> dict[str, int]:
    counts = {"if": 0, "for": 0, "while": 0, "try": 0, "match": 0, "with": 0, "raise": 0, "return": 0}
    for child in ast.walk(node):
        if isinstance(child, ast.If):
            counts["if"] += 1
        elif isinstance(child, (ast.For, ast.AsyncFor)):
            counts["for"] += 1
        elif isinstance(child, ast.While):
            counts["while"] += 1
        elif isinstance(child, ast.Try):
            counts["try"] += 1
        elif isinstance(child, ast.Match):
            counts["match"] += 1
        elif isinstance(child, (ast.With, ast.AsyncWith)):
            counts["with"] += 1
        elif isinstance(child, ast.Raise):
            counts["raise"] += 1
        elif isinstance(child, ast.Return):
            counts["return"] += 1
    return {k: v for k, v in counts.items() if v}


def assignment_summary(node: ast.AST, limit: int = 20) -> list[str]:
    names: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = []
            if isinstance(child, ast.Assign):
                targets = list(child.targets)
            else:
                targets = [child.target]
            for target in targets:
                try:
                    names.append(ast.unparse(target))
                except Exception:
                    names.append(type(target).__name__)
                if len(names) >= limit:
                    return names
    return names


def calls_summary(node: ast.AST, limit: int = 24) -> list[str]:
    calls = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            try:
                calls.append(ast.unparse(child.func))
            except Exception:
                calls.append(type(child.func).__name__)
            if len(calls) >= limit:
                break
    return sorted(set(calls))


def test_tier(path: str) -> str | None:
    if path.startswith("tests/tier_a/"):
        return "Tier A static/admitted test evidence; not run by this Atlas pass"
    if path.startswith("tests/tier_b/"):
        return "Tier B static/admitted test evidence; not run by this Atlas pass"
    if path.startswith("tests/tier_c/"):
        return "Tier C static/admitted test evidence; not run by this Atlas pass"
    return None


def record_id(seed: str) -> str:
    return "ACA-" + hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12].upper()


def behaviour_unit(surface: str, path: str, symbol: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", surface.lower()).strip("_")[:44]
    h = hashlib.sha1(f"{path}:{symbol}".encode()).hexdigest()[:8]
    return f"ACU-{slug}-{h}"


def make_record(
    *,
    path: str,
    start: int,
    end: int,
    record_type: str,
    construct_type: str,
    symbol: str,
    surface: str,
    surface_meta: dict[str, Any] | None,
    owner_confidence: str,
    owner_reason: str,
    observed: str,
    inputs: list[str] | dict[str, Any] | None = None,
    outputs: list[str] | dict[str, Any] | None = None,
    state_reads: list[str] | dict[str, Any] | None = None,
    state_writes: list[str] | dict[str, Any] | None = None,
    external_dependencies: list[str] | dict[str, Any] | None = None,
    packet_or_schema_effects: list[str] | dict[str, Any] | None = None,
    config_or_coefficient_effects: list[str] | dict[str, Any] | None = None,
    thresholds_or_literals: list[str] | dict[str, Any] | None = None,
    branch_conditions: list[str] | dict[str, Any] | None = None,
    error_null_empty_semantics: list[str] | dict[str, Any] | None = None,
    side_effects: list[str] | dict[str, Any] | None = None,
    docstring_evidence: list[dict[str, Any]] | None = None,
    proof_family: str | None = None,
    evidence_status: str = "static_structural_observation",
    status: str = "structural_inventory_record",
    blockers: list[str] | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    if surface_meta is None:
        surface_meta = {}
    seed = f"{path}:{start}:{end}:{record_type}:{construct_type}:{symbol}"
    impl_status = surface_meta.get("implementation_truth_status", "blocked_blueprint" if surface == "blocked_blueprint" else "unknown")
    target_owner = surface_meta.get("target_owner", "unresolved")
    surface_status = surface_meta.get("structural_status", "blocked" if surface == "blocked_blueprint" else "unknown")
    intended = surface_meta.get("current_blocker_or_gap") or surface_meta.get("observed_native_repo_evidence") or "unknown"
    default_blockers = [
        "static_atlas_record_only",
        "tests_not_run_by_active_code_atlas_pass",
        "not_a_normative_correctness_claim",
    ]
    if blockers:
        default_blockers.extend(blockers)
    rec = {
        "active_code_record_id": record_id(seed),
        "active_behaviour_unit_id": behaviour_unit(surface, path, symbol),
        "source_file": path,
        "source_line_start": start,
        "source_line_end": end,
        "record_type": record_type,
        "construct_type": construct_type,
        "symbol_name": symbol,
        "evidence_status": evidence_status,
        "observed_behaviour": observed,
        "intended_behaviour": intended,
        "inputs": inputs or [],
        "outputs": outputs or [],
        "state_reads": state_reads or [],
        "state_writes": state_writes or [],
        "external_dependencies": external_dependencies or [],
        "packet_or_schema_effects": packet_or_schema_effects or [],
        "config_or_coefficient_effects": config_or_coefficient_effects or [],
        "thresholds_or_literals": thresholds_or_literals or [],
        "branch_conditions": branch_conditions or [],
        "error_null_empty_semantics": error_null_empty_semantics or [],
        "side_effects": side_effects or [],
        "known_bug_or_defect_caveat": None,
        "active_behaviour_unit_summary": f"Static active-repo evidence for {surface}: {symbol}",
        "operating_model_role": f"Active repository evidence mapped to {surface}",
        "blueprint_surface": surface,
        "blueprint_surface_status": surface_status,
        "target_owner": target_owner,
        "lawful_owner_candidate": path,
        "owner_confidence": owner_confidence,
        "proof_family": proof_family or surface_meta.get("observed_proof_test_evidence") or "unknown_not_run",
        "active_test_evidence": test_tier(path) or surface_meta.get("observed_proof_test_evidence") or [],
        "docstring_evidence": docstring_evidence or [],
        "native_satisfaction_status": "unknown",
        "status": status,
        "blockers": sorted(set(default_blockers)),
        "exclusion_reason": None,
        "notes": sorted(set((notes or []) + [owner_reason])),
    }
    for field in REQUIRED_FIELDS:
        if field not in rec:
            raise AssertionError(f"missing {field}")
    return rec


def discover_files() -> list[str]:
    files = git_output("ls-files").splitlines()
    selected = []
    for path in files:
        if any(path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue
        if path in SELF_EXCLUDED:
            continue
        if path.startswith("var/audit/active_code_atlas_001/") and not path.endswith("PLANNING_SETUP_RECEIPT.md") and not path.endswith("active_code_atlas_record_shape_draft.json"):
            continue
        if path in ROOT_FILES or any(path.startswith(prefix) for prefix in ACTIVE_ROOT_PREFIXES):
            selected.append(path)
    return sorted(set(selected))


def parse_python_file(path: str, surfaces: dict[str, dict[str, Any]], records: list[dict[str, Any]]) -> dict[str, Any]:
    abs_path = ROOT / path
    text = read_text(abs_path)
    lines = text.splitlines() or [""]
    surface, confidence, reason = map_surface(path, surfaces)
    meta = surfaces.get(surface)
    try:
        tree = ast.parse(text, filename=path)
    except SyntaxError as exc:
        rt, ct = file_kind(path)
        records.append(make_record(path=path, start=1, end=len(lines), record_type=rt, construct_type="python_file_parse_blocked", symbol=path, surface=surface, surface_meta=meta, owner_confidence=confidence, owner_reason=reason, observed=f"Python file exists but AST parse failed: {exc}", evidence_status="blocked", status="blocked", blockers=["python_ast_parse_failed"], notes=[f"sha256={sha256_file(abs_path)}"]))
        return {"path": path, "line_count": len(lines), "sha256": sha256_file(abs_path), "parse_status": "syntax_error"}
    imports = python_imports(tree)
    rt, ct = file_kind(path)
    records.append(make_record(path=path, start=1, end=len(lines), record_type=rt, construct_type=ct, symbol=path.replace("/", ".").removesuffix(".py"), surface=surface, surface_meta=meta, owner_confidence=confidence, owner_reason=reason, observed=f"Python module file exists with {len(imports)} static import references and {len(tree.body)} top-level AST statements.", external_dependencies=imports, thresholds_or_literals=literal_values(tree), branch_conditions=branch_summary(tree), state_writes=assignment_summary(tree), side_effects=calls_summary(tree), notes=[f"sha256={sha256_file(abs_path)}", "module body statically parsed; runtime not executed"]))
    ds = docstring_range(tree)
    if ds:
        records.append(make_record(path=path, start=ds[0], end=ds[1], record_type="docstring_claim", construct_type="module_docstring", symbol=path.replace("/", ".").removesuffix(".py") + ".__doc__", surface=surface, surface_meta=meta, owner_confidence=confidence, owner_reason=reason, observed="Module docstring claim is present and recorded separately from runtime behaviour.", evidence_status="docstring_only", docstring_evidence=[{"source_file": path, "source_line_start": ds[0], "source_line_end": ds[1]}], notes=["docstring is lowest-authority evidence"]))

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.class_stack: list[str] = []
        def visit_ClassDef(self, node: ast.ClassDef) -> Any:
            qual = ".".join(self.class_stack + [node.name]) if self.class_stack else node.name
            start = getattr(node, "lineno", 1)
            end = getattr(node, "end_lineno", start)
            records.append(make_record(path=path, start=start, end=end, record_type="runtime_behaviour" if path.startswith("src/") else "test_contract", construct_type="class", symbol=path.replace("/", ".").removesuffix(".py") + ":" + qual, surface=surface, surface_meta=meta, owner_confidence=confidence, owner_reason=reason, observed=f"Defines class {qual}{signature(node)}. Static record only; class body not executed.", inputs={"bases_or_args": signature(node)}, outputs=[], external_dependencies=imports, thresholds_or_literals=literal_values(node), branch_conditions=branch_summary(node), state_writes=assignment_summary(node), side_effects=calls_summary(node), notes=["class statically parsed; no proof execution claimed"]))
            ds = docstring_range(node)
            if ds:
                records.append(make_record(path=path, start=ds[0], end=ds[1], record_type="docstring_claim", construct_type="class_docstring", symbol=path.replace("/", ".").removesuffix(".py") + ":" + qual + ".__doc__", surface=surface, surface_meta=meta, owner_confidence=confidence, owner_reason=reason, observed=f"Class docstring claim for {qual} is present and recorded separately.", evidence_status="docstring_only", docstring_evidence=[{"source_file": path, "source_line_start": ds[0], "source_line_end": ds[1]}], notes=["docstring is lowest-authority evidence"]))
            self.class_stack.append(node.name)
            self.generic_visit(node)
            self.class_stack.pop()
        def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
            self._function(node, async_fn=False)
        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
            self._function(node, async_fn=True)
        def _function(self, node: ast.AST, async_fn: bool) -> None:
            assert isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            qual = ".".join(self.class_stack + [node.name]) if self.class_stack else node.name
            start = getattr(node, "lineno", 1)
            end = getattr(node, "end_lineno", start)
            is_test = path.startswith("tests/") or node.name.startswith("test_")
            is_fixture = any("fixture" in d for d in decorators(node))
            if is_test:
                rt = "test_contract"
                ct = "test_function" if node.name.startswith("test_") else "test_helper_function"
            elif is_fixture:
                rt = "test_fixture"
                ct = "pytest_fixture"
            else:
                rt = "runtime_behaviour" if path.startswith("src/") else "support_function"
                ct = "async_function" if async_fn else "function"
            records.append(make_record(path=path, start=start, end=end, record_type=rt, construct_type=ct, symbol=path.replace("/", ".").removesuffix(".py") + ":" + qual, surface=surface, surface_meta=meta, owner_confidence=confidence, owner_reason=reason, observed=f"Defines {'async ' if async_fn else ''}function {qual}{signature(node)}. Static record only; function not executed.", inputs={"signature": signature(node), "decorators": decorators(node)}, outputs={"return_annotation": signature(node).split(" -> ", 1)[1] if " -> " in signature(node) else None}, external_dependencies=imports, thresholds_or_literals=literal_values(node), branch_conditions=branch_summary(node), state_writes=assignment_summary(node), side_effects=calls_summary(node), notes=["function statically parsed; no proof execution claimed"]))
            ds = docstring_range(node)
            if ds:
                records.append(make_record(path=path, start=ds[0], end=ds[1], record_type="docstring_claim", construct_type="function_docstring", symbol=path.replace("/", ".").removesuffix(".py") + ":" + qual + ".__doc__", surface=surface, surface_meta=meta, owner_confidence=confidence, owner_reason=reason, observed=f"Function docstring claim for {qual} is present and recorded separately.", evidence_status="docstring_only", docstring_evidence=[{"source_file": path, "source_line_start": ds[0], "source_line_end": ds[1]}], notes=["docstring is lowest-authority evidence"]))
            self.generic_visit(node)
    Visitor().visit(tree)
    return {"path": path, "line_count": len(lines), "sha256": sha256_file(abs_path), "parse_status": "parsed", "surface": surface, "owner_confidence": confidence, "owner_reason": reason}


def file_summary(path: str) -> dict[str, Any]:
    abs_path = ROOT / path
    suffix = abs_path.suffix.lower()
    lc = line_count(abs_path)
    summary: dict[str, Any] = {"path": path, "line_count": lc, "sha256": sha256_file(abs_path), "parse_status": "not_parsed"}
    if suffix == ".json":
        try:
            data = json.loads(read_text(abs_path))
            summary["parse_status"] = "json_ok"
            if isinstance(data, dict):
                summary["top_level_keys"] = list(data.keys())[:30]
                if "records" in data and isinstance(data["records"], list):
                    summary["records_count"] = len(data["records"])
            elif isinstance(data, list):
                summary["list_count"] = len(data)
        except Exception as exc:
            summary["parse_status"] = f"json_error:{exc}"
    elif suffix in {".md", ".txt", ".tsv", ".yaml", ".yml", ".toml", ".lock", ".example"} or abs_path.name in {"Makefile", ".python-version"}:
        text = read_text(abs_path)
        headings = [line.strip("# ") for line in text.splitlines() if line.startswith("#")][:20]
        summary["parse_status"] = "text_read"
        summary["headings"] = headings
    return summary


def add_file_record(path: str, surfaces: dict[str, dict[str, Any]], records: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    surface, confidence, reason = map_surface(path, surfaces)
    meta = surfaces.get(surface)
    rt, ct = file_kind(path)
    blockers = []
    if surface == "blocked_blueprint":
        blockers.append("no_single_blueprint_surface_assignment")
    notes = [f"sha256={summary['sha256']}", f"parse_status={summary.get('parse_status')}"]
    if "records_count" in summary:
        notes.append(f"contained_records={summary['records_count']}")
    if "top_level_keys" in summary:
        notes.append("top_level_keys=" + ",".join(summary["top_level_keys"]))
    records.append(make_record(path=path, start=1, end=max(1, int(summary["line_count"])), record_type=rt, construct_type=ct, symbol=path, surface=surface, surface_meta=meta, owner_confidence=confidence, owner_reason=reason, observed=f"File-level active repository evidence exists for {path}; parsed as {summary.get('parse_status')} with {summary['line_count']} lines.", external_dependencies=[], thresholds_or_literals=summary.get("top_level_keys", [])[:20], blockers=blockers, notes=notes))


def main() -> None:
    surfaces = parse_current_map_surfaces()
    blueprint_lines = parse_blueprint_surface_lines()
    bridge_counts = parse_bridge_surface_counts()
    for surface, meta in surfaces.items():
        meta.update(blueprint_lines.get(surface, {}))
        meta["bridge_record_count"] = bridge_counts.get(surface, 0)
    records: list[dict[str, Any]] = []
    read_ledger: list[dict[str, Any]] = []
    selected_files = discover_files()
    for path in selected_files:
        if path.endswith(".py") and (path.startswith("src/") or path.startswith("tests/")):
            entry = parse_python_file(path, surfaces, records)
        else:
            entry = file_summary(path)
            add_file_record(path, surfaces, records, entry)
            surface, confidence, reason = map_surface(path, surfaces)
            entry.update({"surface": surface, "owner_confidence": confidence, "owner_reason": reason})
        read_ledger.append(entry)

    # Add one explicit surface-summary record per governed surface so zero-file/reserved surfaces remain visible.
    for surface, meta in surfaces.items():
        path = meta.get("current_map_path", rel(CURRENT_MAP))
        line = int(meta.get("current_map_line", 1))
        records.append(make_record(path=path, start=line, end=line, record_type="surface_summary", construct_type="architecture_surface_row", symbol=f"{meta['row_id']} {surface}", surface=surface, surface_meta=meta, owner_confidence="direct", owner_reason="surface row copied from current-state architecture map", observed=f"Current-state architecture map row {meta['row_id']} names this surface, target owner, evidence paths, proof/test evidence, blocker/gap, and next lawful action.", inputs=meta.get("observed_native_repo_evidence"), outputs=meta.get("observed_proof_test_evidence"), branch_conditions={"current_blocker_or_gap": meta.get("current_blocker_or_gap")}, side_effects={"next_lawful_action": meta.get("next_lawful_action")}, proof_family=meta.get("observed_proof_test_evidence"), notes=[f"blueprint_lines={meta.get('blueprint_line_start')}:{meta.get('blueprint_line_end')}", f"bridge_record_count={meta.get('bridge_record_count', 0)}"]))

    atlas_counts = parse_atlas_counts()
    source_head = git_output("rev-parse", "HEAD")
    source_package_sha = None
    source_tar = Path("/mnt/data/NVDA10_2_TEST_FALSE_POSITIVE_RESISTANCE_FINAL_CLOSEOUT_AUDIT_AMENDED_HANDOFF_0aed0f77942f_2026-05-10.tar.gz")
    if source_tar.exists():
        source_package_sha = sha256_file(source_tar)
    payload = {
        "ledger_name": "active_code_atlas_structural_inventory",
        "schema_version": "1.0",
        "status": "structural_inventory_scaffold_static_only",
        "classification": "ACTIVE_CODE_ATLAS_STRUCTURAL_INVENTORY_001",
        "limitation_statement": LIMITATION_STATEMENT,
        "source_repo_head": source_head,
        "source_repo_branch": git_output("branch", "--show-current"),
        "source_package_sha256": source_package_sha,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "authority_note": LIMITATION_STATEMENT,
        "atlas_bridge_shape_context": atlas_counts,
        "records": sorted(records, key=lambda r: (r["blueprint_surface"], r["source_file"], r["source_line_start"], r["record_type"], r["symbol_name"])),
    }
    ATLAS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    # Inventory by surface and file.
    inventory: dict[str, Any] = {
        "ledger_name": "active_code_atlas_surface_inventory",
        "source_repo_head": source_head,
        "generated_at_utc": payload["generated_at_utc"],
        "selected_file_count": len(selected_files),
        "excluded_prefixes": list(EXCLUDED_PREFIXES),
        "self_excluded_outputs": list(SELF_EXCLUDED),
        "surfaces": {},
    }
    for entry in read_ledger:
        surface = entry.get("surface", "blocked_blueprint")
        inventory["surfaces"].setdefault(surface, {"files": [], "count": 0, "owner_confidence_counts": {}})
        inventory["surfaces"][surface]["files"].append({k: entry.get(k) for k in ("path", "line_count", "sha256", "parse_status", "owner_confidence", "owner_reason")})
        inventory["surfaces"][surface]["count"] += 1
        conf = entry.get("owner_confidence", "unknown")
        inventory["surfaces"][surface]["owner_confidence_counts"][conf] = inventory["surfaces"][surface]["owner_confidence_counts"].get(conf, 0) + 1
    INVENTORY_PATH.write_text(json.dumps(inventory, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    READ_LEDGER_PATH.write_text(json.dumps({"ledger_name": "active_code_atlas_read_ledger", "generated_at_utc": payload["generated_at_utc"], "entries": read_ledger}, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    SURFACE_META_PATH.write_text(json.dumps({"ledger_name": "active_code_atlas_surface_metadata", "generated_at_utc": payload["generated_at_utc"], "surfaces": surfaces}, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    counts_by_surface: dict[str, int] = {}
    counts_by_type: dict[str, int] = {}
    for rec in records:
        counts_by_surface[rec["blueprint_surface"]] = counts_by_surface.get(rec["blueprint_surface"], 0) + 1
        counts_by_type[rec["record_type"]] = counts_by_type.get(rec["record_type"], 0) + 1
    print(json.dumps({
        "active_code_atlas": rel(ATLAS_PATH),
        "record_count": len(records),
        "selected_file_count": len(selected_files),
        "surface_count": len(surfaces),
        "counts_by_surface": counts_by_surface,
        "counts_by_type": counts_by_type,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
