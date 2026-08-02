"""Deterministic repository-local probe for continuation-readiness structure.

This probe validates only mechanical conditions. It does not adjudicate semantic
meaning. The accepted dependency graph and its bounded exceptions are declared
below from the current canonical plan and continuation authority.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.proof_authority import load_and_validate_authority  # noqa: E402

SOURCE_ROOT = REPO_ROOT / "src" / "nvda_desk"

OWNER_PREFIXES = {
    "m00_application_shell": "M00",
    "m01_source_admission": "M01",
    "m02_financial_calendar": "M02",
    "m03_preparation": "M03",
    "m05_serial_cognition": "M05",
    "m06_parallel_risk": "M06",
    "m07_coefficient_modifier_authority": "M07",
    "m08_playbook_catalogue": "M08",
    "m09_capital_authority": "M09",
    "m10_execution_gateway": "M10",
    "m11_portfolio_lifecycle": "M11",
    "m12_evidence_replay": "M12",
    "m13_state_kernel": "M13",
}

ACCEPTED_DIRECT_DEPENDENCIES = {
    "M01": set(),
    "M02": {"M01"},
    "M03": {"M01", "M02"},
    "M04": set(),
    "M05": {"M03", "M04", "M07", "M08"},
    "M06": {"M03", "M04"},
    "M07": set(),
    "M08": set(),
    "M09": {"M05", "M06", "M07"},
    "M10": {"M09"},
    "M11": {"M10"},
    "M12": {"M04"},
    "M13": set(),
}

BOUNDED_EXCEPTIONS = {
    ("M09", "M04"): {
        "kind": "packet_carriage",
        "authority": (
            "CONTINUATION.md sections 8.2-8.4 and accepted signal-phase/DMPV3 "
            "repair: canonical M09 validates M04-owned DMPV3 carriage without "
            "acquiring packet meaning"
        ),
        "target_prefix": "nvda_desk.contracts.packets",
    },
    ("M10", "M13"): {
        "kind": "transaction_mechanics",
        "authority": (
            "canonical ExecPlan dependency law: M13 supplies transaction mechanics "
            "without owning domain meaning"
        ),
        "target_prefix": "nvda_desk.m13_state_kernel",
    },
    ("M11", "M13"): {
        "kind": "transaction_mechanics",
        "authority": (
            "canonical ExecPlan dependency law: M13 supplies transaction mechanics "
            "without owning domain meaning"
        ),
        "target_prefix": "nvda_desk.m13_state_kernel",
    },
    ("M11", "M06"): {
        "kind": "read_only_owner_fact_contract",
        "authority": (
            "accepted M06 owner-fact completion: M11 issues immutable M11-owned "
            "inventory/concentration facts consumed read-only by M06"
        ),
        "target_prefix": "nvda_desk.m06_parallel_risk.owner_facts",
    },
}


def _module_name(path: Path) -> str:
    relative = path.relative_to(REPO_ROOT / "src").with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _available_modules() -> tuple[dict[str, Path], set[str]]:
    modules: dict[str, Path] = {}
    packages: set[str] = {"nvda_desk"}
    for path in sorted(SOURCE_ROOT.rglob("*.py")):
        name = _module_name(path)
        modules[name] = path
        parts = name.split(".")
        for index in range(1, len(parts)):
            packages.add(".".join(parts[:index]))
    return modules, packages | set(modules)


def _resolve_import_from(
    *, source_module: str, source_path: Path, level: int, module: str | None
) -> str:
    if level == 0:
        return module or ""
    package = (
        source_module if source_path.name == "__init__.py" else source_module.rpartition(".")[0]
    )
    return importlib.util.resolve_name("." * level + (module or ""), package)


def _internal_imports(
    modules: dict[str, Path], available: set[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    edges: list[dict[str, Any]] = []
    syntax_errors: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for source, path in sorted(modules.items()):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            syntax_errors.append(
                {
                    "path": path.relative_to(REPO_ROOT).as_posix(),
                    "line": exc.lineno,
                    "message": exc.msg,
                }
            )
            continue
        for node in ast.walk(tree):
            references: list[tuple[str, str]] = []
            if isinstance(node, ast.Import):
                references = [(alias.name, alias.name) for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                base = _resolve_import_from(
                    source_module=source,
                    source_path=path,
                    level=node.level,
                    module=node.module,
                )
                for alias in node.names:
                    candidate = f"{base}.{alias.name}" if base and alias.name != "*" else base
                    target = candidate if candidate in available else base
                    references.append((candidate, target))
            else:
                continue
            for reference, target in references:
                if not reference.startswith("nvda_desk"):
                    continue
                if target not in available:
                    unresolved.append(
                        {
                            "source": source,
                            "reference": reference,
                            "resolved_target": target,
                            "path": path.relative_to(REPO_ROOT).as_posix(),
                            "line": node.lineno,
                        }
                    )
                    continue
                edges.append(
                    {
                        "source": source,
                        "target": target,
                        "reference": reference,
                        "path": path.relative_to(REPO_ROOT).as_posix(),
                        "line": node.lineno,
                    }
                )
    return edges, syntax_errors, unresolved


def _strongly_connected_components(
    nodes: Iterable[str], edges: Iterable[tuple[str, str]]
) -> list[list[str]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for source, target in edges:
        if source != target:
            adjacency[source].add(target)
    index = 0
    indexes: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indexes[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in sorted(adjacency.get(node, ())):
            if target not in indexes:
                visit(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in on_stack:
                lowlinks[node] = min(lowlinks[node], indexes[target])
        if lowlinks[node] == indexes[node]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            if len(component) > 1:
                components.append(sorted(component))

    for node in sorted(nodes):
        if node not in indexes:
            visit(node)
    return sorted(components)


def _owner(module: str) -> str | None:
    parts = module.split(".")
    if len(parts) >= 2 and parts[0] == "nvda_desk":
        return OWNER_PREFIXES.get(parts[1])
    if module.startswith("nvda_desk.contracts.packets"):
        return "M04"
    return None


def _dependency_conformance(edges: list[dict[str, Any]]) -> dict[str, Any]:
    observed: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    for edge in edges:
        source_owner = _owner(edge["source"])
        target_owner = _owner(edge["target"])
        if not source_owner or not target_owner or source_owner == target_owner:
            continue
        classification = "accepted_direct"
        authority = "canonical ExecPlan accepted dependency graph"
        if source_owner == "M00":
            classification = "composition_root"
            authority = "M00 is the final composition owner"
        elif target_owner in ACCEPTED_DIRECT_DEPENDENCIES.get(source_owner, set()):
            classification = "accepted_direct"
        else:
            exception = BOUNDED_EXCEPTIONS.get((source_owner, target_owner))
            if exception and edge["target"].startswith(exception["target_prefix"]):
                classification = exception["kind"]
                authority = exception["authority"]
            else:
                classification = "violation"
        item = {
            **edge,
            "source_owner": source_owner,
            "target_owner": target_owner,
            "classification": classification,
            "authority": authority,
        }
        observed.append(item)
        if classification == "violation":
            violations.append(item)
    return {
        "observed_cross_owner_edges": observed,
        "observed_cross_owner_edge_count": len(observed),
        "violations": violations,
        "violation_count": len(violations),
    }


def _fresh_import_probe(module_names: list[str]) -> dict[str, Any]:
    code = """
import importlib, json, sys
names = json.loads(sys.argv[1])
failures = []
for name in names:
    try:
        importlib.import_module(name)
    except BaseException as exc:
        failures.append({"module": name, "type": type(exc).__name__, "message": str(exc)})
print(json.dumps({"attempted": len(names), "failures": failures}, sort_keys=True))
raise SystemExit(1 if failures else 0)
"""
    environment = dict(os.environ)
    source_path = str(REPO_ROOT / "src")
    environment["PYTHONPATH"] = source_path + os.pathsep + environment.get("PYTHONPATH", "")
    results: dict[str, Any] = {}
    for order, names in (("forward", module_names), ("reverse", list(reversed(module_names)))):
        completed = subprocess.run(
            [sys.executable, "-c", code, json.dumps(names)],
            cwd=REPO_ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        payload = (
            json.loads(lines[-1])
            if lines
            else {"attempted": 0, "failures": [{"message": completed.stderr}]}
        )
        payload["exit_code"] = completed.returncode
        results[order] = payload
    return results


def _proof_inventory() -> dict[str, Any]:
    model = load_and_validate_authority(repo_root=REPO_ROOT)
    physical = {
        path.relative_to(REPO_ROOT).as_posix()
        for tier in ("tier_a", "tier_b", "tier_c")
        for path in (REPO_ROOT / "tests" / tier).rglob("test_*.py")
    }
    admitted = set(model.path_admissions)
    alpha = set(model.promotion_sets["alpha_current"].test_paths)

    registry = yaml.safe_load(
        (REPO_ROOT / "config/retained_test_registry.yaml").read_text(encoding="utf-8")
    )
    retired: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("native_test_path") == "retired_after_successor_split":
                retired.append(
                    {
                        "test_family_id": value.get("test_family_id"),
                        "successor_test_family_ids": value.get("successor_test_family_ids", []),
                    }
                )
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for key, value in registry.items():
        if key != "canonical_admission_model":
            walk(value)

    canonical_family_ids = set(model.families)
    selected_family_ids = {
        family_id for block in model.proof_blocks.values() for family_id in block.test_family_ids
    }
    retired_conflicts = [
        item
        for item in retired
        if item["test_family_id"] in canonical_family_ids
        or item["test_family_id"] in selected_family_ids
    ]
    return {
        "physical_count": len(physical),
        "admitted_count": len(admitted),
        "missing_admissions": sorted(physical - admitted),
        "stale_admissions": sorted(admitted - physical),
        "alpha_current_path_count": len(alpha),
        "alpha_paths_outside_physical_or_admission": sorted(alpha - (physical & admitted)),
        "retired_predecessor_family_count": len(retired),
        "retired_predecessor_families": retired,
        "retired_family_control_conflicts": retired_conflicts,
        "family_count": len(model.families),
        "proof_block_count": len(model.proof_blocks),
    }


def _module_record_check() -> dict[str, Any]:
    records = sorted(
        (REPO_ROOT / "project_control/canonical_project_manager/modules").glob("M*/**/*.md")
    )
    conflicts: list[dict[str, Any]] = []
    for path in records:
        text = path.read_text(encoding="utf-8")
        if (
            "FOUNDATION-READINESS-RECONCILIATION-V1" in text
            or "CONTINUATION:ALPHA_FOUNDATION_READY" in text
        ):
            conflicts.append(
                {
                    "path": path.relative_to(REPO_ROOT).as_posix(),
                    "foundation_pack_mentions": text.count(
                        "FOUNDATION-READINESS-RECONCILIATION-V1"
                    ),
                    "ready_state_mentions": text.count("CONTINUATION:ALPHA_FOUNDATION_READY"),
                }
            )
    return {
        "markdown_record_count": len(records),
        "live_programme_state_mentions": conflicts,
        "live_programme_state_mention_count": len(conflicts),
        "interpretation": (
            "module records remain historical bounded acceptance evidence; no module record "
            "claims the live foundation-readiness control state"
        ),
    }


def _git_state() -> dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
        ).stdout.strip()

    return {
        "branch": run("branch", "--show-current"),
        "commit": run("rev-parse", "HEAD"),
        "status_porcelain": run("status", "--porcelain"),
    }


def build_report() -> dict[str, Any]:
    modules, available = _available_modules()
    edges, syntax_errors, unresolved = _internal_imports(modules, available)
    graph_edges = {(edge["source"], edge["target"]) for edge in edges}
    cycles = _strongly_connected_components(modules, graph_edges)
    dependency = _dependency_conformance(edges)
    imports = _fresh_import_probe(sorted(modules))
    proof = _proof_inventory()
    records = _module_record_check()
    git = _git_state()

    failures: list[str] = []
    if syntax_errors:
        failures.append("syntax_errors")
    if unresolved:
        failures.append("unresolved_internal_imports")
    if cycles:
        failures.append("module_cycles")
    if dependency["violation_count"]:
        failures.append("dependency_violations")
    if any(result["exit_code"] != 0 for result in imports.values()):
        failures.append("fresh_import_failures")
    if proof["missing_admissions"] or proof["stale_admissions"]:
        failures.append("physical_admission_mismatch")
    if proof["alpha_paths_outside_physical_or_admission"]:
        failures.append("alpha_path_outside_inventory")
    if proof["retired_family_control_conflicts"]:
        failures.append("retired_family_in_active_control")
    if records["live_programme_state_mention_count"]:
        failures.append("module_record_live_state_conflict")

    return {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "git": git,
        "proof_inventory": proof,
        "module_graph": {
            "module_count": len(modules),
            "internal_import_reference_count": len(edges),
            "internal_import_location_count": len(
                {(edge["source"], edge["target"], edge["path"], edge["line"]) for edge in edges}
            ),
            "internal_import_edge_count": len(graph_edges),
            "syntax_errors": syntax_errors,
            "unresolved_internal_imports": unresolved,
            "cycles": cycles,
            "cycle_count": len(cycles),
            "dependency_conformance": dependency,
        },
        "fresh_imports": imports,
        "module_records": records,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    report = build_report()
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
