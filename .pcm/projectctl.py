#!/usr/bin/env python3
"""Deterministic project-control utility for repository-resident governance."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_PATH = Path(__file__).resolve()


def _discover_git_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        text=True, capture_output=True, check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return SCRIPT_PATH.parents[1]
    return Path(result.stdout.strip()).resolve()


ROOT = _discover_git_root(SCRIPT_PATH.parent)
if (ROOT / "control" / "project.json").is_file():
    PCM_HOME = ROOT
elif (ROOT / ".pcm" / "control" / "project.json").is_file():
    PCM_HOME = ROOT / ".pcm"
else:
    # Source-methodology mode before an install target exists.
    PCM_HOME = ROOT


def _root_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


PROJECT_JSON = PCM_HOME / "control" / "project.json"
TASKS_JSON = PCM_HOME / "control" / "tasks.json"
HANDOFF_JSON = PCM_HOME / "control" / "handoff.json"
LCR_JSON = PCM_HOME / "control" / "lcr.json"
CLAIMS_JSON = PCM_HOME / "control" / "claims.json"
DELEGATION_JSON = PCM_HOME / "control" / "delegation.json"
INSTANTIATION_JSON = PCM_HOME / "control" / "instantiation.json"
RECEIPTS_DIR = PCM_HOME / "control" / "receipts"
PROGRAMME_OWNER_DECISIONS_DIR = PCM_HOME / "control" / "programme_owner_decisions"
INDEPENDENT_REVIEW_RESULTS_DIR = PCM_HOME / "control" / "independent_review_results"
PROJECT_REL = _root_rel(PROJECT_JSON)
TASKS_REL = _root_rel(TASKS_JSON)
HANDOFF_REL = _root_rel(HANDOFF_JSON)
LCR_REL = _root_rel(LCR_JSON)
CLAIMS_REL = _root_rel(CLAIMS_JSON)
DELEGATION_REL = _root_rel(DELEGATION_JSON)
INSTANTIATION_REL = _root_rel(INSTANTIATION_JSON)
RECEIPTS_REL_PREFIX = _root_rel(RECEIPTS_DIR).rstrip("/") + "/"
PROGRAMME_OWNER_DECISIONS_REL_PREFIX = _root_rel(PROGRAMME_OWNER_DECISIONS_DIR).rstrip("/") + "/"
INDEPENDENT_REVIEW_RESULTS_REL_PREFIX = _root_rel(INDEPENDENT_REVIEW_RESULTS_DIR).rstrip("/") + "/"
SCRIPT_REL = _root_rel(SCRIPT_PATH)
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
REQ_HEADING_RE = re.compile(r"^##\s+(REQ-\d+)\b", re.MULTILINE)
STABLE_ID_PATTERN = r"[A-Z0-9]+(?:[_.-][A-Z0-9]+)*"
STABLE_ID_RE = re.compile(rf"^{STABLE_ID_PATTERN}$")
TASK_MARKER_RE = re.compile(rf"<!--\s*CONTROL:TASK:({STABLE_ID_PATTERN}):(START|END)\s*-->")
SECTION_MARKER_RE = re.compile(r"<!--\s*CONTROL:SECTION:([A-Z0-9][A-Z0-9_.-]*):(START|END)\s*-->")
GLOBAL_START = "<!-- CONTROL:GLOBAL:START -->"
GLOBAL_END = "<!-- CONTROL:GLOBAL:END -->"
ALLOWED_STATUS = {"pending", "in_progress", "accepted", "blocked"}
SAFE_GENERATED_STATE_PATHS = {HANDOFF_REL, LCR_REL}
ACTOR_CLASSES = {"AUTONOMOUS", "INDEPENDENT_REVIEW", "PROGRAMME_OWNER"}
ROUTE_MODES = {"CONSUME_ADMITTED", "CHANGE_MEANING"}
WORK_TYPES = {"non_code", "test_proof", "implementation"}
TASK_SEMANTIC_FIELDS = (
    "requirements", "depends_on", "write_paths", "acceptance",
    "verification", "independent_review", "programme_owner_review",
    "semantic_routes", "refinement", "work_type", "test_first",
)
CLAIM_STATUS = {"VERIFIED", "INFERRED", "UNKNOWN", "BLOCKED"}
VERIFICATION_GATES = {"leaf-close": "leaf_close", "promotion": "promotion"}
NATIVE_AUTHORITY_CANDIDATES = (
    "PROJECT_OBJECTIVE.md", "REQUIREMENTS.md", "GUARDRAILS.md", "AGENTS.md",
    "EXEC_PLAN.md", "CHATGPT_PROJECT_INSTRUCTIONS.md",
)
HANDOFF_REQUIRED = {
    "schema_version", "generated_at", "active_task", "authority_hashes",
    "repo_fingerprint", "task_contract_hash", "source_head", "source_tree",
    "branch", "working_state_digest", "ready_tasks", "unresolved_claims",
    "last_receipt", "acceptance_tags", "receipt_hashes", "claims_hash",
}
LCR_REQUIRED = {
    "schema_version", "generated_at", "active_leaf", "authority_hashes",
    "repo_fingerprint", "task_contract_hash", "claims_hash", "checkpoint",
    "accepted_base", "ready_tasks", "unresolved_claims", "blockers",
    "last_receipt", "acceptance_tags", "receipt_hashes", "applicable_context",
    "next_transition", "migration_provenance",
}


class ControlError(RuntimeError):
    pass


def run_git(*args: str, allow_failure: bool = False) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0 and not allow_failure:
        raise ControlError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def git_result(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ControlError(f"missing required file {path.relative_to(ROOT)}") from exc
    except UnicodeDecodeError as exc:
        raise ControlError(f"unreadable UTF-8 file {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ControlError(f"invalid JSON {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise ControlError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ControlError(f"missing required file {path.relative_to(ROOT)}") from exc
    except UnicodeDecodeError as exc:
        raise ControlError(f"unreadable UTF-8 file {path.relative_to(ROOT)}") from exc


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    try:
        return sha256_bytes(path.read_bytes())
    except FileNotFoundError as exc:
        raise ControlError(f"missing required file {path.relative_to(ROOT)}") from exc


def safe_rel_path(rel: str, field: str) -> str:
    if not isinstance(rel, str) or not rel or "\x00" in rel:
        raise ControlError(f"unsafe path in {field}: {rel!r}")
    p = Path(rel)
    if p.is_absolute() or any(part in {"", ".", ".."} for part in p.parts):
        raise ControlError(f"unsafe path in {field}: {rel!r}")
    normalized = p.as_posix()
    if normalized.startswith(".git/") or normalized == ".git":
        raise ControlError(f"unsafe path in {field}: {rel!r}")
    return normalized


def config() -> dict[str, Any]:
    cfg = load_json(PROJECT_JSON)
    if cfg.get("schema_version") != 1:
        raise ControlError("unsupported control/project.json schema_version")
    files = cfg.get("authority_files")
    if not isinstance(files, list) or not files or not all(isinstance(x, str) for x in files):
        raise ControlError("control/project.json authority_files must be a non-empty string list")
    normalized = [safe_rel_path(x, "authority_files") for x in files]
    if len(normalized) != len(set(normalized)):
        raise ControlError("duplicate authority_files entry")
    cfg["authority_files"] = normalized
    requirements_rel = safe_rel_path(cfg.get("requirements_path", "REQUIREMENTS.md"), "requirements_path")
    execution_plan_rel = safe_rel_path(cfg.get("execution_plan_path", "EXEC_PLAN.md"), "execution_plan_path")
    project_objective_rel = safe_rel_path(cfg.get("project_objective_path", "PROJECT_OBJECTIVE.md"), "project_objective_path")
    for field, rel in (("requirements_path", requirements_rel), ("execution_plan_path", execution_plan_rel), ("project_objective_path", project_objective_rel)):
        if rel not in cfg["authority_files"]:
            raise ControlError(f"{field} must identify a configured authority file: {rel}")
        cfg[field] = rel
    raw_project_authority = cfg.get("project_authority_files", cfg["authority_files"])
    if not isinstance(raw_project_authority, list) or not raw_project_authority or not all(isinstance(x, str) for x in raw_project_authority):
        raise ControlError("project_authority_files must be a non-empty string list")
    project_authority = [safe_rel_path(x, "project_authority_files") for x in raw_project_authority]
    if len(project_authority) != len(set(project_authority)):
        raise ControlError("duplicate project_authority_files entry")
    unknown_project_authority = [rel for rel in project_authority if rel not in cfg["authority_files"]]
    if unknown_project_authority:
        raise ControlError(f"project authority file is not configured authority: {unknown_project_authority[0]}")
    cfg["project_authority_files"] = project_authority
    if cfg.get("instantiation_required", False) is True:
        expected_root = _root_rel(PCM_HOME / "project").rstrip("/")
        expected = {
            "requirements_path": f"{expected_root}/REQUIREMENTS.md",
            "execution_plan_path": f"{expected_root}/EXEC_PLAN.md",
            "project_objective_path": f"{expected_root}/PROJECT_OBJECTIVE.md",
        }
        for field, rel in expected.items():
            if cfg[field] != rel:
                raise ControlError(f"installed consuming project {field} must be {rel}")
    raw_generated = cfg.get("generated_state_paths", [HANDOFF_REL])
    if not isinstance(raw_generated, list) or not all(isinstance(x, str) for x in raw_generated):
        raise ControlError("generated_state_paths must be a string list")
    generated = [safe_rel_path(x.rstrip("/"), "generated_state_paths") + ("/" if x.endswith("/") else "") for x in raw_generated]
    unsupported = [x for x in generated if x not in SAFE_GENERATED_STATE_PATHS]
    if unsupported:
        raise ControlError(
            "generated_state_paths may contain only controller-owned outputs; "
            f"unsupported entry {unsupported[0]!r}"
        )
    if len(generated) != 1:
        raise ControlError("generated_state_paths must contain exactly one controller state file")
    cfg["generated_state_paths"] = generated
    migration = cfg.get("lcr_migration")
    if migration is not None:
        required_migration = {"legacy_state_commit", "legacy_handoff_sha256", "legacy_source_head", "legacy_source_tree"}
        if not isinstance(migration, dict) or set(migration) != required_migration:
            raise ControlError("invalid lcr_migration provenance in control/project.json")
        if not all(isinstance(migration[k], str) and migration[k] for k in required_migration):
            raise ControlError("lcr_migration provenance values must be non-empty strings")
    branch = cfg.get("acceptance_branch", "main")
    if not isinstance(branch, str) or not re.fullmatch(r"[A-Za-z0-9._/-]+", branch):
        raise ControlError("acceptance_branch must be a safe branch name")
    cfg["acceptance_branch"] = branch
    max_bytes = cfg.get("context_max_bytes", 65536)
    if not isinstance(max_bytes, int) or max_bytes <= 0:
        raise ControlError("context_max_bytes must be a positive integer")
    raw_universal = cfg.get("context_universal_files", [])
    if not isinstance(raw_universal, list) or not all(isinstance(x, str) for x in raw_universal):
        raise ControlError("context_universal_files must be a string list")
    universal = [safe_rel_path(x, "context_universal_files") for x in raw_universal]
    if len(universal) != len(set(universal)):
        raise ControlError("duplicate context_universal_files entry")
    unknown_universal = [rel for rel in universal if rel not in cfg["authority_files"]]
    if unknown_universal:
        raise ControlError(
            f"context universal file is not configured authority: {unknown_universal[0]}"
        )
    cfg["context_universal_files"] = universal
    test_first_policy = cfg.get("test_first_policy", "legacy")
    if test_first_policy not in {"legacy", "required"}:
        raise ControlError("test_first_policy must be either legacy or required")
    cfg["test_first_policy"] = test_first_policy
    instantiation_required = cfg.get("instantiation_required", False)
    if not isinstance(instantiation_required, bool):
        raise ControlError("instantiation_required must be boolean")
    cfg["instantiation_required"] = instantiation_required
    runtime_budget = cfg.get("runtime_budget_minutes", 300)
    flush_margin = cfg.get("durability_flush_margin_minutes", 5)
    if isinstance(runtime_budget, bool) or not isinstance(runtime_budget, int) or runtime_budget <= 0:
        raise ControlError("runtime_budget_minutes must be a positive integer")
    if isinstance(flush_margin, bool) or not isinstance(flush_margin, int) or flush_margin <= 0:
        raise ControlError("durability_flush_margin_minutes must be a positive integer")
    if flush_margin >= runtime_budget:
        raise ControlError("durability_flush_margin_minutes must be smaller than runtime_budget_minutes")
    cfg["runtime_budget_minutes"] = runtime_budget
    cfg["durability_flush_margin_minutes"] = flush_margin
    return cfg


def require_project_mode(cfg: dict[str, Any], operation: str) -> None:
    if cfg.get("instantiation_required", False) and cfg.get("template_mode", False):
        raise ControlError(
            f"{operation} is unavailable while consuming-project instantiation is incomplete; "
            "complete the project authority drafts and run finalize-instantiation under PROGRAMME_OWNER"
        )


def validate_instantiation_record(cfg: dict[str, Any]) -> None:
    if not cfg.get("instantiation_required", False):
        return
    record = load_json(INSTANTIATION_JSON)
    required = {"schema_version", "status", "methodology", "target_source", "accepted_brief", "native_authority", "approval"}
    if set(record) != required or record.get("schema_version") != 1:
        raise ControlError(f"invalid {INSTANTIATION_REL} schema")
    if record["status"] not in {"draft", "approved"}:
        raise ControlError(f"{INSTANTIATION_REL} status must be draft or approved")
    methodology = record["methodology"]
    if not isinstance(methodology, dict) or set(methodology) != {"commit", "tree", "controller_sha256"}:
        raise ControlError(f"{INSTANTIATION_REL} methodology identity has invalid shape")
    for field in ("commit", "tree"):
        if not isinstance(methodology[field], str) or re.fullmatch(r"[0-9a-f]{40,64}", methodology[field]) is None:
            raise ControlError(f"{INSTANTIATION_REL} methodology {field} is invalid")
    if not isinstance(methodology["controller_sha256"], str) or re.fullmatch(r"[0-9a-f]{64}", methodology["controller_sha256"]) is None:
        raise ControlError(f"{INSTANTIATION_REL} methodology controller_sha256 is invalid")
    if sha256_file(SCRIPT_PATH) != methodology["controller_sha256"]:
        raise ControlError("installed projectctl does not match recorded methodology controller hash")

    target = record["target_source"]
    if not isinstance(target, dict) or set(target) != {"commit", "tree", "branch"}:
        raise ControlError(f"{INSTANTIATION_REL} target_source identity has invalid shape")
    if not git_commit_exists(target.get("commit")):
        raise ControlError("instantiation target-source commit is missing from repository history")
    if commit_tree(target["commit"]) != target.get("tree"):
        raise ControlError("instantiation target-source tree does not match its commit")
    current_head = run_git("rev-parse", "HEAD")
    if not is_ancestor(target["commit"], current_head):
        raise ControlError("instantiation target-source commit is not an ancestor of current HEAD")
    if not isinstance(target.get("branch"), str) or not target["branch"]:
        raise ControlError("instantiation target-source branch is invalid")

    native = record["native_authority"]
    if not isinstance(native, list):
        raise ControlError("instantiation native_authority must be a list")
    seen_native: set[str] = set()
    for item in native:
        required_native = {"path", "sha256", "blob"}
        if not isinstance(item, dict) or set(item) != required_native:
            raise ControlError("instantiation native_authority entry has invalid shape")
        rel = safe_rel_path(item.get("path"), "native_authority path")
        if rel not in NATIVE_AUTHORITY_CANDIDATES:
            raise ControlError(f"unsupported native authority path {rel}")
        if rel in seen_native:
            raise ControlError(f"duplicate native authority path {rel}")
        seen_native.add(rel)
        if not isinstance(item.get("sha256"), str) or re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is None:
            raise ControlError(f"native authority sha256 is invalid for {rel}")
        if not isinstance(item.get("blob"), str) or re.fullmatch(r"[0-9a-f]{40,64}", item["blob"]) is None:
            raise ControlError(f"native authority blob is invalid for {rel}")
        tree = git_result("ls-tree", target["commit"], "--", rel)
        lines = [line for line in tree.stdout.splitlines() if line.strip()]
        if tree.returncode != 0 or len(lines) != 1 or "\t" not in lines[0]:
            raise ControlError(f"native authority source identity is missing or ambiguous: {rel}")
        meta, shown_rel = lines[0].split("\t", 1)
        parts = meta.split()
        if len(parts) != 3 or parts[1] != "blob" or parts[0] == "120000" or shown_rel != rel:
            raise ControlError(f"native authority must be a regular Git file at source commit: {rel}")
        if parts[2] != item["blob"]:
            raise ControlError(f"native authority blob identity mismatch: {rel}")
        raw = _git_file_bytes_at_commit(target["commit"], rel, "native authority")
        if sha256_bytes(raw) != item["sha256"]:
            raise ControlError(f"native authority hash mismatch at source commit: {rel}")
        if record["status"] == "draft":
            current = ROOT / rel
            if not current.is_file() or current.is_symlink() or sha256_file(current) != item["sha256"]:
                raise ControlError(f"native authority changed during draft instantiation: {rel}")
    expected_native: set[str] = set()
    for rel in NATIVE_AUTHORITY_CANDIDATES:
        tree = git_result("ls-tree", target["commit"], "--", rel)
        if tree.returncode == 0 and any(line.strip() for line in tree.stdout.splitlines()):
            expected_native.add(rel)
    if seen_native != expected_native:
        raise ControlError("instantiation native_authority does not exactly match canonical authority present at target source commit")

    brief = record["accepted_brief"]
    required_brief = {"kind", "stored_path", "sha256", "source_name", "source_commit", "source_tree"}
    if not isinstance(brief, dict) or set(brief) != required_brief:
        raise ControlError(f"{INSTANTIATION_REL} accepted_brief identity has invalid shape")
    if brief["kind"] not in {"file", "git_tree_archive"}:
        raise ControlError(f"{INSTANTIATION_REL} accepted_brief kind is invalid")
    stored_rel = safe_rel_path(brief["stored_path"], "accepted_brief stored_path")
    if not path_under(stored_rel, _root_rel(PCM_HOME / "brief")):
        raise ControlError("accepted brief must be stored under the installed PCM brief directory")
    brief_path = ROOT / stored_rel
    if sha256_file(brief_path) != brief.get("sha256"):
        raise ControlError("accepted brief stored bytes do not match recorded hash")
    if not isinstance(brief.get("source_name"), str) or not brief["source_name"]:
        raise ControlError("accepted brief source_name is invalid")
    if brief["kind"] == "git_tree_archive":
        for field in ("source_commit", "source_tree"):
            if not isinstance(brief[field], str) or re.fullmatch(r"[0-9a-f]{40,64}", brief[field]) is None:
                raise ControlError(f"accepted brief {field} is invalid")
    elif brief["source_commit"] is not None or brief["source_tree"] is not None:
        raise ControlError("standalone accepted brief file cannot claim Git commit/tree identity")

    approval = record["approval"]
    if record["status"] == "draft":
        if approval is not None:
            raise ControlError("draft instantiation cannot contain approval evidence")
        if not cfg.get("template_mode", False):
            raise ControlError("draft instantiation requires template_mode=true")
    else:
        required_approval = {"actor_class", "note", "approved_at"}
        if not isinstance(approval, dict) or set(approval) != required_approval:
            raise ControlError("approved instantiation requires complete approval evidence")
        if approval.get("actor_class") != "PROGRAMME_OWNER":
            raise ControlError("instantiation approval requires actor class PROGRAMME_OWNER")
        if not isinstance(approval.get("note"), str) or not approval["note"].strip():
            raise ControlError("instantiation approval note must be non-empty")
        if not isinstance(approval.get("approved_at"), str) or not approval["approved_at"]:
            raise ControlError("instantiation approved_at must be non-empty")
        if cfg.get("template_mode", False):
            raise ControlError("approved instantiation requires template_mode=false")


def generated_state_rel(cfg: dict[str, Any]) -> str:
    return cfg["generated_state_paths"][0]


def generated_state_file(cfg: dict[str, Any]) -> Path:
    return ROOT / generated_state_rel(cfg)


def state_mode(cfg: dict[str, Any]) -> str:
    rel = generated_state_rel(cfg)
    if rel == HANDOFF_REL:
        return "handoff"
    if rel == LCR_REL:
        return "lcr"
    raise ControlError(f"unsupported generated state file {rel}")


def authority_hashes(cfg: dict[str, Any]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in cfg["authority_files"]:
        path = ROOT / rel
        if path.is_symlink():
            raise ControlError(f"authority file must not be a symlink: {rel}")
        hashes[rel] = sha256_file(path)
    return hashes


def is_generated_path(rel: str, cfg: dict[str, Any]) -> bool:
    normalized = rel.replace(os.sep, "/")
    for item in cfg.get("generated_state_paths", []):
        if item.endswith("/") and normalized.startswith(item):
            return True
        if normalized == item:
            return True
    return False


def repo_fingerprint(cfg: dict[str, Any]) -> str:
    tracked_raw = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=False)
    if tracked_raw.returncode != 0:
        raise ControlError("git ls-files failed while computing repository fingerprint")
    paths = sorted(p.decode("utf-8") for p in tracked_raw.stdout.split(b"\0") if p)
    h = hashlib.sha256()
    for rel in paths:
        if is_generated_path(rel, cfg):
            continue
        path = ROOT / rel
        h.update(rel.encode("utf-8") + b"\0")
        if path.is_symlink():
            h.update(b"<symlink>" + os.readlink(path).encode("utf-8"))
        elif path.is_file():
            h.update(sha256_file(path).encode("ascii"))
        else:
            h.update(b"<missing>")
        h.update(b"\0")
    return h.hexdigest()


def working_state_digest(cfg: dict[str, Any] | None = None) -> str:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if result.returncode != 0:
        raise ControlError("git status failed while computing working-state digest")
    records = [x for x in result.stdout.split(b"\0") if x]
    kept: list[bytes] = []
    i = 0
    while i < len(records):
        rec = records[i]
        text = rec.decode("utf-8", errors="strict")
        status = text[:2] if len(text) >= 2 else ""
        rel = text[3:] if len(text) >= 4 else ""
        generated = bool(cfg and is_generated_path(rel, cfg))
        rename_or_copy = "R" in status or "C" in status
        if not generated:
            kept.append(rec)
            path = ROOT / rel
            if path.is_file() and status == "??":
                kept.append((rel + "\0" + sha256_file(path)).encode("utf-8"))
        if rename_or_copy and i + 1 < len(records):
            extra = records[i + 1]
            if not generated:
                kept.append(extra)
            i += 1
        i += 1
    h = hashlib.sha256()
    for rec in kept:
        h.update(rec + b"\0")
    return h.hexdigest()


def clean_worktree() -> bool:
    return git_result("status", "--porcelain=v1", "--untracked-files=all").stdout == ""


def staged_paths() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "-z"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if result.returncode != 0:
        raise ControlError("git diff --cached failed while reading staged paths")
    return sorted(p.decode("utf-8") for p in result.stdout.split(b"\0") if p)


def unstaged_or_untracked_paths() -> list[str]:
    unstaged = subprocess.run(
        ["git", "diff", "--name-only", "-z"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if unstaged.returncode != 0:
        raise ControlError("git diff failed while reading unstaged paths")
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if untracked.returncode != 0:
        raise ControlError("git ls-files failed while reading untracked paths")
    values = [p.decode("utf-8") for p in unstaged.stdout.split(b"\0") if p]
    values.extend(p.decode("utf-8") for p in untracked.stdout.split(b"\0") if p)
    return sorted(set(values))


def clean_working_state_digest() -> str:
    return hashlib.sha256(b"").hexdigest()


def external_git(repo: Path, *args: str, allow_failure: bool = False) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=False
    )
    if result.returncode != 0 and not allow_failure:
        raise ControlError(f"git -C {repo} {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def external_git_result(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=False
    )


def external_clean_worktree(repo: Path) -> bool:
    result = external_git_result(repo, "status", "--porcelain=v1", "--untracked-files=all")
    if result.returncode != 0:
        raise ControlError(f"target repository status failed: {result.stderr.strip()}")
    return result.stdout == ""


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def task_contract_hash() -> str:
    return sha256_file(TASKS_JSON)


def task_semantic_contract(task: dict[str, Any]) -> dict[str, Any]:
    values = {field: task.get(field) for field in TASK_SEMANTIC_FIELDS}
    if values["verification"] is None:
        values["verification"] = {"leaf_close": [], "promotion": []}
    return values


def historical_tasks_at_commit(commit: str) -> list[dict[str, Any]]:
    result = git_result("show", f"{commit}:{TASKS_REL}")
    if result.returncode != 0:
        raise ControlError(f"admitted task history is missing control/tasks.json at {commit[:12]}")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ControlError(f"admitted task history has invalid control/tasks.json at {commit[:12]}") from exc
    tasks = data.get("tasks") if isinstance(data, dict) else None
    if not isinstance(tasks, list) or not all(isinstance(task, dict) for task in tasks):
        raise ControlError(f"admitted task history has invalid task list at {commit[:12]}")
    return tasks



def _change_meaning_owner_hash_refresh_only(
    previous: dict[str, Any], current: dict[str, Any], anchor: str
) -> bool:
    previous_contract = task_semantic_contract(previous)
    current_contract = task_semantic_contract(current)
    previous_routes = previous_contract.pop("semantic_routes", None)
    current_routes = current_contract.pop("semantic_routes", None)
    if previous_contract != current_contract:
        return False
    if not isinstance(previous_routes, list) or not isinstance(current_routes, list):
        return False
    if len(previous_routes) != len(current_routes):
        return False
    refreshed = False
    for old_route, new_route in zip(previous_routes, current_routes):
        if not isinstance(old_route, dict) or not isinstance(new_route, dict):
            return False
        old_copy = json.loads(json.dumps(old_route))
        new_copy = json.loads(json.dumps(new_route))
        if old_copy.get("id") != new_copy.get("id") or old_copy.get("route_mode") != new_copy.get("route_mode"):
            return False
        if old_copy.get("route_mode") == "CHANGE_MEANING":
            old_owner = old_copy.get("owner_record")
            new_owner = new_copy.get("owner_record")
            if isinstance(old_owner, dict) and isinstance(new_owner, dict):
                old_sha = old_owner.get("sha256")
                new_sha = new_owner.get("sha256")
                if old_sha != new_sha:
                    old_without = dict(old_owner); old_without.pop("sha256", None)
                    new_without = dict(new_owner); new_without.pop("sha256", None)
                    if old_without != new_without or new_owner.get("admitted_task_id") is not None:
                        return False
                    rel = new_owner.get("path")
                    if not isinstance(rel, str):
                        return False
                    try:
                        if old_sha != sha256_bytes(git_file_bytes(anchor, rel)):
                            return False
                        if new_sha != sha256_file(ROOT / rel):
                            return False
                    except (ControlError, OSError):
                        return False
                    old_copy["owner_record"]["sha256"] = new_sha
                    refreshed = True
        if old_copy != new_copy:
            return False
    return refreshed


def validate_admitted_task_semantics(
    state: dict[str, Any], cfg: dict[str, Any], tasks: list[dict[str, Any]], actor_class: str
) -> None:
    head = run_git("rev-parse", "HEAD")
    anchor = latest_generated_state_commit(cfg, head) if state_mode(cfg) == "lcr" else state_source_head(state, cfg)
    if not anchor:
        return
    previous = historical_tasks_at_commit(anchor)
    previous_blocks = historical_plan_blocks_at_commit(anchor)
    _global, current_blocks = parse_plan()
    previous_by_id = {task.get("id"): task for task in previous if isinstance(task.get("id"), str)}
    current_by_id = {task["id"]: task for task in tasks}
    changed: list[str] = []
    active_task = state_active_task(state, cfg)
    for task_id in sorted(previous_by_id.keys() & current_by_id.keys()):
        previous_block = previous_blocks.get(task_id)
        current_block = current_blocks.get(task_id)
        if previous_block is None:
            raise ControlError(
                f"admitted task history is missing EXEC_PLAN.md task block {task_id} at {anchor[:12]}"
            )
        if current_block is None:
            raise ControlError(f"current EXEC_PLAN.md is missing task block {task_id}")
        if task_semantic_identity(previous_by_id[task_id], previous_block) != task_semantic_identity(
            current_by_id[task_id], current_block
        ):
            plan_same = plan_task_semantic_block(task_id, previous_block) == plan_task_semantic_block(
                task_id, current_block
            )
            if not (
                task_id == active_task
                and plan_same
                and _change_meaning_owner_hash_refresh_only(
                    previous_by_id[task_id], current_by_id[task_id], anchor
                )
            ):
                changed.append(task_id)
    added = sorted(current_by_id.keys() - previous_by_id.keys())
    disappeared = sorted(previous_by_id.keys() - current_by_id.keys())
    if actor_class != "PROGRAMME_OWNER":
        unbounded = [task_id for task_id in added if current_by_id[task_id].get("refinement") is None]
        if unbounded:
            raise ControlError(
                f"new task {unbounded[0]} is not a bounded refinement; "
                "new programme work requires actor class PROGRAMME_OWNER"
            )
        for task_id in added:
            envelope_id = current_by_id[task_id]["refinement"]["envelope_task_id"]
            if envelope_id not in previous_by_id:
                raise ControlError(
                    f"new refinement {task_id} does not use a previously admitted envelope; "
                    "route this change to PROGRAMME_OWNER"
                )
    if (changed or disappeared) and actor_class != "PROGRAMME_OWNER":
        affected = ", ".join(changed + disappeared)
        raise ControlError(
            f"admitted stable ID semantic identity changed ({affected}); "
            "plan restructuring requires actor class PROGRAMME_OWNER"
        )


def load_claims() -> list[dict[str, Any]]:
    data = load_json(CLAIMS_JSON)
    if data.get("schema_version") != 1 or not isinstance(data.get("claims"), list):
        raise ControlError("invalid control/claims.json schema")
    claims = data["claims"]
    ids: list[str] = []
    required = {"id", "statement", "status", "evidence"}
    for claim in claims:
        if not isinstance(claim, dict) or not required.issubset(claim):
            raise ControlError("every claim must contain id, statement, status, and evidence")
        claim_id = claim["id"]
        if not isinstance(claim_id, str) or not re.fullmatch(r"CLAIM-[A-Z0-9_-]+", claim_id):
            raise ControlError(f"invalid claim id {claim_id!r}")
        if not isinstance(claim["statement"], str) or not claim["statement"].strip():
            raise ControlError(f"{claim_id} statement must be non-empty")
        if claim["status"] not in CLAIM_STATUS:
            raise ControlError(f"invalid status for {claim_id}: {claim['status']}")
        if not isinstance(claim["evidence"], list) or not all(isinstance(x, str) for x in claim["evidence"]):
            raise ControlError(f"{claim_id} evidence must be a string list")
        ids.append(claim_id)
    if len(ids) != len(set(ids)):
        raise ControlError("duplicate claim identifier in control/claims.json")
    return claims


def claims_hash() -> str:
    return sha256_file(CLAIMS_JSON)


def unresolved_claim_ids() -> list[str]:
    return sorted(claim["id"] for claim in load_claims() if claim["status"] != "VERIFIED")


def parse_requirements(cfg: dict[str, Any] | None = None) -> set[str]:
    cfg = cfg or config()
    rel = cfg["requirements_path"]
    text = read_text(ROOT / rel)
    ids = REQ_HEADING_RE.findall(text)
    if len(ids) != len(set(ids)):
        raise ControlError(f"duplicate requirement identifier in {rel}")
    if not ids:
        raise ControlError(f"no requirement identifiers found in {rel}")
    return set(ids)


def parse_plan_text(text: str) -> tuple[str, dict[str, str]]:
    if text.count(GLOBAL_START) != 1 or text.count(GLOBAL_END) != 1:
        raise ControlError("EXEC_PLAN.md must contain exactly one global START/END marker pair")
    gs = text.index(GLOBAL_START) + len(GLOBAL_START)
    ge = text.index(GLOBAL_END)
    if ge <= gs:
        raise ControlError("EXEC_PLAN.md global markers are out of order")
    global_block = text[gs:ge].strip()

    events = list(TASK_MARKER_RE.finditer(text))
    blocks: dict[str, str] = {}
    active: tuple[str, int] | None = None
    seen: set[str] = set()
    for event in events:
        task_id, kind = event.group(1), event.group(2)
        if kind == "START":
            if active is not None:
                raise ControlError(f"nested or crossing plan task markers: {active[0]} then {task_id}")
            if task_id in seen:
                raise ControlError(f"duplicate plan task marker {task_id}")
            active = (task_id, event.end())
            seen.add(task_id)
        else:
            if active is None:
                raise ControlError(f"unpaired plan task marker {task_id}")
            if active[0] != task_id:
                raise ControlError(f"nested or crossing plan task markers: {active[0]} then {task_id}")
            blocks[task_id] = text[active[1]:event.start()].strip()
            active = None
    if active is not None:
        raise ControlError(f"unpaired plan task marker {active[0]}")
    if not blocks:
        raise ControlError("EXEC_PLAN.md contains no task blocks")
    return global_block, blocks


def parse_plan(cfg: dict[str, Any] | None = None) -> tuple[str, dict[str, str]]:
    cfg = cfg or config()
    return parse_plan_text(read_text(ROOT / cfg["execution_plan_path"]))


def historical_project_config_at_commit(commit: str) -> dict[str, Any]:
    result = git_result("show", f"{commit}:{PROJECT_REL}")
    if result.returncode != 0:
        raise ControlError(f"admitted task history is missing {PROJECT_REL} at {commit[:12]}")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ControlError(f"admitted project config is invalid at {commit[:12]}") from exc
    if not isinstance(data, dict):
        raise ControlError(f"admitted project config is invalid at {commit[:12]}")
    return data


def historical_authority_path_at_commit(commit: str, field: str, default: str) -> str:
    data = historical_project_config_at_commit(commit)
    return safe_rel_path(data.get(field, default), field)


def historical_plan_blocks_at_commit(commit: str) -> dict[str, str]:
    rel = historical_authority_path_at_commit(commit, "execution_plan_path", "EXEC_PLAN.md")
    result = git_result("show", f"{commit}:{rel}")
    if result.returncode != 0:
        raise ControlError(f"admitted task history is missing {rel} at {commit[:12]}")
    try:
        _global, blocks = parse_plan_text(result.stdout)
    except ControlError as exc:
        raise ControlError(f"admitted {rel} is invalid at {commit[:12]}: {exc}") from exc
    return blocks


def plan_task_semantic_block(task_id: str, block: str) -> str:
    heading = re.compile(
        rf"^##\s+{re.escape(task_id)}\s+—\s+(.+?)\s*$",
        flags=re.MULTILINE,
    )
    matches = list(heading.finditer(block))
    if len(matches) != 1:
        raise ControlError(
            f"{task_id} plan block requires exactly one semantic heading for identity binding"
        )
    match = matches[0]
    return block[:match.start()] + f"## {task_id} — <human-label>" + block[match.end():]


def task_semantic_identity(task: dict[str, Any], plan_block: str) -> dict[str, Any]:
    return {
        "task_contract": task_semantic_contract(task),
        "plan_block": plan_task_semantic_block(task["id"], plan_block),
    }


def parse_context_ref(ref: str, cfg: dict[str, Any]) -> tuple[str, str]:
    if not isinstance(ref, str) or ref.count("#") != 1:
        raise ControlError(f"invalid context section reference {ref!r}; expected <authority-file>#<section-id>")
    rel_raw, section_id = ref.split("#", 1)
    rel = safe_rel_path(rel_raw, "context_refs")
    if rel not in cfg["authority_files"]:
        raise ControlError(f"context section reference uses non-authority file: {rel}")
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9_.-]*", section_id):
        raise ControlError(f"invalid stable section id in context reference {ref!r}")
    if re.fullmatch(r"(?:L|LINE-?)\d+", section_id, flags=re.IGNORECASE):
        raise ControlError(f"line-number-style context section id is not durable: {section_id}")
    return rel, section_id


def parse_authority_sections(rel: str) -> dict[str, str]:
    text = read_text(ROOT / rel)
    events = list(SECTION_MARKER_RE.finditer(text))
    sections: dict[str, str] = {}
    active: tuple[str, int] | None = None
    seen: set[str] = set()
    for event in events:
        section_id, kind = event.group(1), event.group(2)
        if kind == "START":
            if active is not None:
                raise ControlError(
                    f"nested or crossing authority section markers in {rel}: {active[0]} then {section_id}"
                )
            if section_id in seen:
                raise ControlError(f"duplicate authority section marker {rel}#{section_id}")
            active = (section_id, event.end())
            seen.add(section_id)
        else:
            if active is None:
                raise ControlError(f"unpaired authority section marker {rel}#{section_id}")
            if active[0] != section_id:
                raise ControlError(
                    f"nested or crossing authority section markers in {rel}: {active[0]} then {section_id}"
                )
            sections[section_id] = text[active[1]:event.start()].strip()
            active = None
    if active is not None:
        raise ControlError(f"unpaired authority section marker {rel}#{active[0]}")
    return sections


def validate_context_references(cfg: dict[str, Any], tasks: list[dict[str, Any]]) -> None:
    cache: dict[str, dict[str, str]] = {}
    for task in tasks:
        for ref in task.get("context_refs", []):
            rel, section_id = parse_context_ref(ref, cfg)
            if rel not in cache:
                cache[rel] = parse_authority_sections(rel)
            if section_id not in cache[rel]:
                raise ControlError(f"missing referenced authority section {rel}#{section_id}")


def dependency_closure(tasks: list[dict[str, Any]], task_id: str) -> list[str]:
    by_id = {task["id"]: task for task in tasks}
    ordered: list[str] = []
    seen: set[str] = set()

    def visit(current: str) -> None:
        for dep in by_id[current]["depends_on"]:
            visit(dep)
            if dep not in seen:
                seen.add(dep)
                ordered.append(dep)

    visit(task_id)
    return ordered


def structural_ancestor_ids(task_id: str) -> list[str]:
    ancestors: list[str] = []
    current = task_id
    while "." in current:
        current = current.rsplit(".", 1)[0]
        ancestors.append(current)
    ancestors.reverse()
    return ancestors


def bounded_context_scope(
    cfg: dict[str, Any], tasks: list[dict[str, Any]], active: str | None
) -> dict[str, Any]:
    if not active:
        return {
            "authority_files": list(cfg["context_universal_files"]),
            "requirements": [],
            "plan_leaf": None,
            "ancestors": [],
            "dependencies": [],
        }
    by_id = {task["id"]: task for task in tasks}
    active_task = by_id[active]

    # Semantic routes are the context/meaning graph. Once present, execution
    # dependencies MUST NOT be projected merely because they determine readiness.
    # Legacy tasks without semantic_routes retain the legacy bounded-context behaviour.
    if "semantic_routes" in active_task:
        refs = list(dict.fromkeys(active_task.get("context_refs", [])))
        return {
            "authority_files": list(cfg["context_universal_files"]) + refs,
            "requirements": list(dict.fromkeys(active_task["requirements"])),
            "plan_leaf": active,
            "ancestors": [],
            "dependencies": [],
        }

    dependencies = dependency_closure(tasks, active)
    ancestors: list[str] = []
    for scoped_leaf in dependencies + [active]:
        for ancestor in structural_ancestor_ids(scoped_leaf):
            if ancestor != active and ancestor not in ancestors:
                ancestors.append(ancestor)
    scoped_ids = list(dict.fromkeys(ancestors + dependencies + [active]))
    requirements: list[str] = []
    refs: list[str] = []
    for task_id in scoped_ids:
        for req in by_id[task_id]["requirements"]:
            if req not in requirements:
                requirements.append(req)
        for ref in by_id[task_id].get("context_refs", []):
            if ref not in refs:
                refs.append(ref)
    return {
        "authority_files": list(cfg["context_universal_files"]) + refs,
        "requirements": requirements,
        "plan_leaf": active,
        "ancestors": ancestors,
        "dependencies": dependencies,
    }


def path_is_gitignored(rel: str) -> bool:
    base = rel.rstrip("/") or rel
    probes = [base, f"{base}/.projectctl-probe"]
    for probe in probes:
        result = git_result("check-ignore", "-q", "--no-index", "--", probe)
        if result.returncode not in (0, 1):
            raise ControlError(f"git check-ignore failed for {rel}")
        if result.returncode == 0:
            return True
    return False


def load_tasks() -> list[dict[str, Any]]:
    data = load_json(TASKS_JSON)
    if data.get("schema_version") != 1 or not isinstance(data.get("tasks"), list):
        raise ControlError("invalid control/tasks.json schema")
    tasks = data["tasks"]
    ids: list[str] = []
    required = {"id", "title", "requirements", "depends_on", "write_paths", "status", "acceptance"}
    for task in tasks:
        if not isinstance(task, dict) or not required.issubset(task):
            raise ControlError("every task must contain all required fields")
        task_id = task["id"]
        if not isinstance(task_id, str) or STABLE_ID_RE.fullmatch(task_id) is None:
            raise ControlError(f"invalid task id {task_id!r}")
        title = task.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ControlError(f"{task_id} title must be non-empty human-readable text")
        ids.append(task_id)
        if task["status"] not in ALLOWED_STATUS:
            raise ControlError(f"invalid status for {task_id}: {task['status']}")
        for field in ("requirements", "depends_on", "write_paths", "acceptance"):
            if not isinstance(task[field], list) or not all(isinstance(x, str) for x in task[field]):
                raise ControlError(f"{task_id} field {field} must be a string list")
        context_refs = task.get("context_refs", [])
        if not isinstance(context_refs, list) or not all(isinstance(x, str) and x for x in context_refs):
            raise ControlError(f"{task_id} field context_refs must be a string list")
        if len(context_refs) != len(set(context_refs)):
            raise ControlError(f"{task_id} field context_refs contains duplicates")
        if not task["acceptance"] or any(not x.strip() for x in task["acceptance"]):
            raise ControlError(f"{task_id} acceptance criteria must be non-empty")
        verification = task.get("verification", {"leaf_close": [], "promotion": []})
        if not isinstance(verification, dict) or set(verification) != {"leaf_close", "promotion"}:
            raise ControlError(
                f"{task_id} verification must contain exactly leaf_close and promotion"
            )
        verification_ids: list[str] = []
        for gate_name in ("leaf_close", "promotion"):
            checks = verification[gate_name]
            if not isinstance(checks, list):
                raise ControlError(f"{task_id} verification {gate_name} must be a list")
            for check in checks:
                required_check = {"id", "proposition", "command", "inputs"}
                optional_check = {"expected_exit_codes"}
                if (
                    not isinstance(check, dict)
                    or not required_check.issubset(check)
                    or set(check) - required_check - optional_check
                ):
                    raise ControlError(
                        f"{task_id} verification {gate_name} check must contain id, proposition, "
                        "command, inputs, and optionally expected_exit_codes"
                    )
                check_id = check["id"]
                if not isinstance(check_id, str) or not re.fullmatch(r"VERIFY-[A-Z0-9_-]+", check_id):
                    raise ControlError(f"{task_id} has invalid verification id {check_id!r}")
                verification_ids.append(check_id)
                if not isinstance(check["proposition"], str) or not check["proposition"].strip():
                    raise ControlError(f"{task_id} verification {check_id} proposition must be non-empty")
                if (
                    not isinstance(check["command"], list)
                    or not check["command"]
                    or not all(isinstance(part, str) and part for part in check["command"])
                ):
                    raise ControlError(f"{task_id} verification {check_id} command must be a non-empty string list")
                if (
                    not isinstance(check["inputs"], list)
                    or not check["inputs"]
                    or not all(isinstance(rel, str) and rel for rel in check["inputs"])
                ):
                    raise ControlError(f"{task_id} verification {check_id} inputs must be a non-empty string list")
                normalized_inputs = [safe_rel_path(rel, f"{task_id} verification {check_id} inputs") for rel in check["inputs"]]
                if len(normalized_inputs) != len(set(normalized_inputs)):
                    raise ControlError(f"{task_id} verification {check_id} inputs contain duplicates")
                check["inputs"] = normalized_inputs
                if "expected_exit_codes" in check:
                    expected_codes = check["expected_exit_codes"]
                    if (
                        not isinstance(expected_codes, list)
                        or not expected_codes
                        or any(isinstance(code, bool) or not isinstance(code, int) or code < 0 for code in expected_codes)
                        or len(expected_codes) != len(set(expected_codes))
                    ):
                        raise ControlError(
                            f"{task_id} verification {check_id} expected_exit_codes must be a non-empty unique list of non-negative integers"
                        )
        if len(verification_ids) != len(set(verification_ids)):
            raise ControlError(f"{task_id} verification check ids must be unique")
        task["verification"] = verification
        review = task.get("independent_review")
        if review is not None:
            required_review = {"source_paths", "candidate_paths", "evidence_paths", "repair_task_id"}
            if not isinstance(review, dict) or set(review) != required_review:
                raise ControlError(
                    f"{task_id} independent_review must contain exactly source_paths, "
                    "candidate_paths, evidence_paths, and repair_task_id"
                )
            for field in ("source_paths", "candidate_paths", "evidence_paths"):
                values = review[field]
                if not isinstance(values, list) or not all(isinstance(rel, str) and rel for rel in values):
                    raise ControlError(f"{task_id} independent_review {field} must be a string list")
                normalized = [safe_rel_path(rel, f"{task_id} independent_review {field}") for rel in values]
                if len(normalized) != len(set(normalized)):
                    raise ControlError(f"{task_id} independent_review {field} contains duplicates")
                review[field] = normalized
            if not review["source_paths"]:
                raise ControlError(f"{task_id} independent_review source_paths must not be empty")
            if not review["candidate_paths"]:
                raise ControlError(f"{task_id} independent_review candidate_paths must not be empty")
            repair_task_id = review["repair_task_id"]
            if not isinstance(repair_task_id, str) or STABLE_ID_RE.fullmatch(repair_task_id) is None:
                raise ControlError(f"{task_id} independent_review repair_task_id must be a task id")
            all_review_paths = review["source_paths"] + review["candidate_paths"] + review["evidence_paths"]
            if len(all_review_paths) != len(set(all_review_paths)):
                raise ControlError(f"{task_id} independent_review paths must not overlap across roles")
        owner_review = task.get("programme_owner_review")
        if owner_review is not None:
            required_owner_review = {
                "candidate_paths", "material_decisions", "freedoms",
                "prohibitions", "requested_decision",
            }
            if not isinstance(owner_review, dict) or set(owner_review) != required_owner_review:
                raise ControlError(
                    f"{task_id} programme_owner_review must contain exactly candidate_paths, "
                    "material_decisions, freedoms, prohibitions, and requested_decision"
                )
            candidates = owner_review["candidate_paths"]
            if not isinstance(candidates, list) or not candidates or not all(
                isinstance(rel, str) and rel for rel in candidates
            ):
                raise ControlError(f"{task_id} programme_owner_review candidate_paths must be a non-empty string list")
            normalized_candidates = [
                safe_rel_path(rel, f"{task_id} programme_owner_review candidate_paths")
                for rel in candidates
            ]
            if len(normalized_candidates) != len(set(normalized_candidates)):
                raise ControlError(f"{task_id} programme_owner_review candidate_paths contains duplicates")
            owner_review["candidate_paths"] = normalized_candidates
            for field in ("material_decisions", "freedoms", "prohibitions"):
                values = owner_review[field]
                if not isinstance(values, list) or not values or not all(
                    isinstance(value, str) and value.strip() for value in values
                ):
                    raise ControlError(f"{task_id} programme_owner_review {field} must be a non-empty string list")
            requested = owner_review["requested_decision"]
            if not isinstance(requested, str) or not requested.strip():
                raise ControlError(f"{task_id} programme_owner_review requested_decision must be non-empty")
        for rel in task["write_paths"]:
            safe_rel_path(rel.rstrip("/"), f"{task_id} write_paths")
            if path_is_gitignored(rel):
                raise ControlError(f"{task_id} write path is gitignored and cannot carry durable work: {rel}")
    if len(ids) != len(set(ids)):
        raise ControlError("duplicate task identifier in control/tasks.json")
    if not tasks:
        raise ControlError("control/tasks.json contains no tasks")
    task_ids = set(ids)
    for task_id in ids:
        if "." in task_id:
            parent_id = task_id.rsplit(".", 1)[0]
            if parent_id not in task_ids:
                raise ControlError(f"{task_id} structural parent {parent_id} is missing")
    return tasks


def _validate_route_record_shape(record: Any, field: str) -> dict[str, Any]:
    required = {"id", "path", "sha256", "admitted_task_id"}
    if not isinstance(record, dict) or set(record) != required:
        raise ControlError(
            f"{field} record must contain exactly id, path, sha256, and admitted_task_id"
        )
    record_id = record["id"]
    if not isinstance(record_id, str) or STABLE_ID_RE.fullmatch(record_id) is None:
        raise ControlError(f"{field} record has invalid id {record_id!r}")
    record["path"] = safe_rel_path(record["path"], f"{field} record path")
    digest = record["sha256"]
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise ControlError(f"{field} record sha256 must be 64 lowercase hexadecimal characters")
    admitted = record["admitted_task_id"]
    if admitted is not None and (
        not isinstance(admitted, str) or STABLE_ID_RE.fullmatch(admitted) is None
    ):
        raise ControlError(f"{field} admitted_task_id must be null or a stable task id")
    return record


def _route_record_key(record: dict[str, Any]) -> tuple[str, str, str | None]:
    return (record["path"], record["sha256"], record["admitted_task_id"])


def _validate_route_record_source(
    record: dict[str, Any],
    field: str,
    tasks_by_id: dict[str, dict[str, Any]],
    tags: dict[str, str],
    *,
    validate_current_hash: bool = True,
) -> None:
    admitted = record["admitted_task_id"]
    if admitted is None:
        path = ROOT / record["path"]
        if path.is_symlink() or not path.is_file():
            raise ControlError(f"{field} current source must be a regular file: {record['path']}")
        if not validate_current_hash:
            return
        actual = sha256_file(path)
    else:
        task = tasks_by_id.get(admitted)
        if task is None:
            raise ControlError(f"{field} references unknown admitted task {admitted}")
        if task["status"] != "accepted":
            raise ControlError(f"{field} references task {admitted} that is not accepted")
        commit = tags.get(admitted)
        if commit is None:
            raise ControlError(f"{field} references admitted task {admitted} without accepted tag")
        actual = sha256_bytes(git_file_bytes(commit, record["path"]))
    if actual != record["sha256"]:
        raise ControlError(
            f"semantic route/source hash drift for {field} record {record['id']}: "
            f"expected {record['sha256']} observed {actual}"
        )


def validate_semantic_routes(tasks: list[dict[str, Any]], tags: dict[str, str]) -> None:
    tasks_by_id = {task["id"]: task for task in tasks}
    active_task = derived_active_task(tasks)
    for task in tasks:
        routes = task.get("semantic_routes", [])
        if not isinstance(routes, list):
            raise ControlError(f"{task['id']} semantic_routes must be a list")
        route_ids: list[str] = []
        for index, route in enumerate(routes):
            field = f"{task['id']} semantic_routes[{index}]"
            required = {
                "id", "owner_record", "route_mode", "complete_records",
                "bounded_records", "conditional_triggers", "exclusions",
                "unresolved_stops",
            }
            if not isinstance(route, dict) or set(route) != required:
                raise ControlError(
                    f"{field} must contain exactly id, owner_record, route_mode, "
                    "complete_records, bounded_records, conditional_triggers, exclusions, "
                    "and unresolved_stops"
                )
            route_id = route["id"]
            if not isinstance(route_id, str) or STABLE_ID_RE.fullmatch(route_id) is None:
                raise ControlError(f"{field} has invalid route id {route_id!r}")
            route_ids.append(route_id)
            mode = route["route_mode"]
            if mode not in ROUTE_MODES:
                raise ControlError(
                    f"{task['id']} semantic route {route_id} has invalid route_mode {mode!r}"
                )

            owner = _validate_route_record_shape(route["owner_record"], f"{field}.owner_record")
            _validate_route_record_source(
                owner, f"{field}.owner_record", tasks_by_id, tags,
                validate_current_hash=(task["id"] == active_task and mode == "CHANGE_MEANING"),
            )

            included: list[dict[str, Any]] = []
            for list_name in ("complete_records", "bounded_records"):
                values = route[list_name]
                if not isinstance(values, list):
                    raise ControlError(f"{field}.{list_name} must be a list")
                seen_keys: set[tuple[str, str, str | None]] = set()
                for record_index, raw_record in enumerate(values):
                    record_field = f"{field}.{list_name}[{record_index}]"
                    record = _validate_route_record_shape(raw_record, record_field)
                    key = _route_record_key(record)
                    if key in seen_keys:
                        raise ControlError(f"{field}.{list_name} contains duplicate record source")
                    seen_keys.add(key)
                    if list_name == "bounded_records" and record["admitted_task_id"] is None:
                        raise ControlError(
                            f"{record_field} must identify an admitted task for bounded consumption"
                        )
                    _validate_route_record_source(
                        record, record_field, tasks_by_id, tags,
                        validate_current_hash=(task["id"] == active_task),
                    )
                    included.append(record)
            if mode == "CONSUME_ADMITTED" and route["complete_records"]:
                raise ControlError(
                    f"{task['id']} semantic route {route_id} CONSUME_ADMITTED cannot declare complete_records"
                )
            if mode == "CONSUME_ADMITTED" and not route["bounded_records"]:
                raise ControlError(
                    f"{task['id']} semantic route {route_id} CONSUME_ADMITTED requires bounded admitted records"
                )

            included_keys = {_route_record_key(record) for record in included}
            trigger_ids: list[str] = []
            triggers = route["conditional_triggers"]
            if not isinstance(triggers, list):
                raise ControlError(f"{field}.conditional_triggers must be a list")
            for trigger_index, trigger in enumerate(triggers):
                trigger_field = f"{field}.conditional_triggers[{trigger_index}]"
                required_trigger = {"id", "record", "triggered", "evidence_record", "reason"}
                if not isinstance(trigger, dict) or set(trigger) != required_trigger:
                    raise ControlError(
                        f"{trigger_field} must contain exactly id, record, triggered, evidence_record, and reason"
                    )
                trigger_id = trigger["id"]
                if not isinstance(trigger_id, str) or STABLE_ID_RE.fullmatch(trigger_id) is None:
                    raise ControlError(f"{trigger_field} has invalid trigger id {trigger_id!r}")
                trigger_ids.append(trigger_id)
                if not isinstance(trigger["triggered"], bool):
                    raise ControlError(f"{trigger_field}.triggered must be boolean")
                if not isinstance(trigger["reason"], str) or not trigger["reason"].strip():
                    raise ControlError(f"{trigger_field}.reason must be non-empty")
                target = _validate_route_record_shape(trigger["record"], f"{trigger_field}.record")
                evidence = _validate_route_record_shape(
                    trigger["evidence_record"], f"{trigger_field}.evidence_record"
                )
                _validate_route_record_source(
                    target, f"{trigger_field}.record", tasks_by_id, tags,
                    validate_current_hash=(task["id"] == active_task and trigger["triggered"]),
                )
                _validate_route_record_source(
                    evidence, f"{trigger_field}.evidence_record", tasks_by_id, tags,
                    validate_current_hash=(task["id"] == active_task),
                )
                target_key = _route_record_key(target)
                active = target_key in included_keys
                if trigger["triggered"] and not active:
                    raise ControlError(
                        f"{task['id']} semantic route {route_id} triggered dependency {trigger_id} is not active"
                    )
                if not trigger["triggered"] and active:
                    raise ControlError(
                        f"{task['id']} semantic route {route_id} untriggered dependency {trigger_id} asserted as active"
                    )
            if len(trigger_ids) != len(set(trigger_ids)):
                raise ControlError(f"{task['id']} semantic route {route_id} trigger ids must be unique")

            exclusions = route["exclusions"]
            if not isinstance(exclusions, list):
                raise ControlError(f"{field}.exclusions must be a list")
            excluded_keys: set[tuple[str, str, str | None]] = set()
            for exclusion_index, exclusion in enumerate(exclusions):
                exclusion_field = f"{field}.exclusions[{exclusion_index}]"
                if not isinstance(exclusion, dict) or set(exclusion) != {"record", "reason"}:
                    raise ControlError(
                        f"{exclusion_field} must contain exactly record and reason"
                    )
                if not isinstance(exclusion["reason"], str) or not exclusion["reason"].strip():
                    raise ControlError(f"{exclusion_field} requires an explicit non-empty reason")
                record = _validate_route_record_shape(exclusion["record"], f"{exclusion_field}.record")
                _validate_route_record_source(
                    record, f"{exclusion_field}.record", tasks_by_id, tags,
                    validate_current_hash=False,
                )
                key = _route_record_key(record)
                if key in included_keys:
                    raise ControlError(
                        f"{task['id']} semantic route {route_id} cannot both include and exclude record {record['id']}"
                    )
                if key in excluded_keys:
                    raise ControlError(f"{field}.exclusions contains duplicate record source")
                excluded_keys.add(key)

            stops = route["unresolved_stops"]
            if not isinstance(stops, list):
                raise ControlError(f"{field}.unresolved_stops must be a list")
            stop_ids: list[str] = []
            for stop_index, stop in enumerate(stops):
                stop_field = f"{field}.unresolved_stops[{stop_index}]"
                if not isinstance(stop, dict) or set(stop) != {"id", "reason"}:
                    raise ControlError(f"{stop_field} must contain exactly id and reason")
                stop_id = stop["id"]
                if not isinstance(stop_id, str) or STABLE_ID_RE.fullmatch(stop_id) is None:
                    raise ControlError(f"{stop_field} has invalid stop id {stop_id!r}")
                if not isinstance(stop["reason"], str) or not stop["reason"].strip():
                    raise ControlError(f"{stop_field}.reason must be non-empty")
                stop_ids.append(stop_id)
            if len(stop_ids) != len(set(stop_ids)):
                raise ControlError(f"{task['id']} semantic route {route_id} unresolved stop ids must be unique")
            if stops:
                raise ControlError(
                    f"{task['id']} semantic route {route_id} has unresolved stop {stops[0]['id']}: {stops[0]['reason']}"
                )
        if len(route_ids) != len(set(route_ids)):
            raise ControlError(f"{task['id']} semantic route ids must be unique")


def load_delegation(tasks: list[dict[str, Any]], cfg: dict[str, Any]) -> dict[str, str]:
    rel = DELEGATION_REL
    if rel not in cfg["authority_files"]:
        raise ControlError(f"{DELEGATION_REL} must be part of authority_files")
    data = load_json(DELEGATION_JSON)
    if set(data) != {"schema_version", "leaf_actor_class"} or data.get("schema_version") != 1:
        raise ControlError("invalid control/delegation.json schema")
    mapping = data.get("leaf_actor_class")
    if not isinstance(mapping, dict):
        raise ControlError("delegation leaf_actor_class must be an object")
    task_ids = {task["id"] for task in tasks}
    policy_ids = set(mapping)
    missing = sorted(task_ids - policy_ids)
    extra = sorted(policy_ids - task_ids)
    if missing:
        raise ControlError(f"delegation policy missing leaf {missing[0]}")
    if extra:
        raise ControlError(f"delegation policy references unknown leaf {extra[0]}")
    for task_id, actor in mapping.items():
        if actor not in ACTOR_CLASSES:
            raise ControlError(f"invalid actor class for {task_id}: {actor!r}")
    return {task_id: str(mapping[task_id]) for task_id in sorted(task_ids)}



def validate_test_first_contracts(
    tasks: list[dict[str, Any]], delegation: dict[str, str], cfg: dict[str, Any]
) -> None:
    if cfg.get("test_first_policy", "legacy") != "required":
        return
    by_id = {task["id"]: task for task in tasks}
    for task in tasks:
        task_id = task["id"]
        work_type = task.get("work_type")
        if work_type not in WORK_TYPES:
            raise ControlError(
                f"{task_id} must declare work_type as one of {sorted(WORK_TYPES)} when test_first_policy is required"
            )
        test_first = task.get("test_first")
        if work_type != "implementation":
            if test_first is not None:
                raise ControlError(f"{task_id} test_first is allowed only for implementation work_type")
            continue
        required = {"test_task_id", "red_required", "red_check_id", "exception_task_id"}
        if not isinstance(test_first, dict) or set(test_first) != required:
            raise ControlError(
                f"{task_id} implementation test_first must contain exactly test_task_id, red_required, red_check_id, and exception_task_id"
            )
        red_required = test_first["red_required"]
        if not isinstance(red_required, bool):
            raise ControlError(f"{task_id} test_first.red_required must be boolean")
        test_task_id = test_first["test_task_id"]
        red_check_id = test_first["red_check_id"]
        exception_task_id = test_first["exception_task_id"]
        if exception_task_id is not None:
            if test_task_id is not None or red_check_id is not None or red_required:
                raise ControlError(
                    f"{task_id} programme-owner test-first exception cannot also declare test predecessor or RED evidence"
                )
            if not isinstance(exception_task_id, str) or exception_task_id not in by_id:
                raise ControlError(f"{task_id} test-first exception references unknown task")
            if exception_task_id not in task["depends_on"]:
                raise ControlError(f"{task_id} test-first exception task must be an execution dependency")
            exception_task = by_id[exception_task_id]
            if delegation.get(exception_task_id) != "PROGRAMME_OWNER" or exception_task.get("programme_owner_review") is None:
                raise ControlError(
                    f"{task_id} test-first exception must reference a PROGRAMME_OWNER dependency with programme_owner_review"
                )
            continue
        if not isinstance(test_task_id, str) or test_task_id not in by_id:
            raise ControlError(f"{task_id} implementation requires a governing test/proof predecessor")
        if test_task_id not in task["depends_on"]:
            raise ControlError(f"{task_id} governing test/proof predecessor must be in depends_on")
        predecessor = by_id[test_task_id]
        if predecessor.get("work_type") != "test_proof":
            raise ControlError(f"{task_id} predecessor {test_task_id} is not work_type test_proof")
        if red_required:
            if not isinstance(red_check_id, str) or not red_check_id:
                raise ControlError(f"{task_id} expected RED requires red_check_id")
            checks = predecessor.get("verification", {}).get("leaf_close", [])
            matching = [check for check in checks if check.get("id") == red_check_id]
            if len(matching) != 1:
                raise ControlError(
                    f"{task_id} expected RED check {red_check_id} is not a unique leaf-close verification on {test_task_id}"
                )
            if "expected_exit_codes" not in matching[0]:
                raise ControlError(f"{task_id} expected RED check must declare non-zero expected_exit_codes")
            expected_codes = verification_expected_exit_codes(matching[0])
            if 0 in expected_codes:
                raise ControlError(f"{task_id} expected RED check cannot accept exit code 0")
        elif red_check_id is not None:
            raise ControlError(f"{task_id} red_check_id must be null when red_required is false")


def _refinement_contract(task: dict[str, Any]) -> dict[str, Any] | None:
    refinement = task.get("refinement")
    if refinement is None:
        return None
    required = {
        "envelope_task_id", "mechanism_id", "prior_repair_task_ids", "fresh_review_required"
    }
    if not isinstance(refinement, dict) or set(refinement) != required:
        raise ControlError(
            f"{task['id']} refinement must contain exactly envelope_task_id, mechanism_id, "
            "prior_repair_task_ids, and fresh_review_required"
        )
    envelope = refinement["envelope_task_id"]
    if not isinstance(envelope, str) or STABLE_ID_RE.fullmatch(envelope) is None:
        raise ControlError(f"{task['id']} refinement envelope_task_id must be a stable task id")
    mechanism = refinement["mechanism_id"]
    if not isinstance(mechanism, str) or STABLE_ID_RE.fullmatch(mechanism) is None:
        raise ControlError(f"{task['id']} refinement mechanism_id must be a stable id")
    prior = refinement["prior_repair_task_ids"]
    if not isinstance(prior, list) or not all(
        isinstance(item, str) and STABLE_ID_RE.fullmatch(item) is not None for item in prior
    ):
        raise ControlError(f"{task['id']} refinement prior_repair_task_ids must be a task-id list")
    if len(prior) != len(set(prior)):
        raise ControlError(f"{task['id']} refinement prior_repair_task_ids contains duplicates")
    if refinement["fresh_review_required"] is not True:
        raise ControlError(f"{task['id']} refinement must require fresh review for changed candidate bytes")
    return refinement


def _normalized_refinement_envelope(task: dict[str, Any]) -> dict[str, Any]:
    verification = task.get("verification")
    if verification is None:
        verification = {"leaf_close": [], "promotion": []}
    return {
        "requirements": task.get("requirements"),
        "write_paths": task.get("write_paths"),
        "acceptance": task.get("acceptance"),
        "verification": verification,
        "semantic_routes": task.get("semantic_routes"),
        "independent_review": task.get("independent_review"),
        "programme_owner_review": task.get("programme_owner_review"),
        "context_refs": task.get("context_refs", []),
    }


def validate_refinement_contracts(tasks: list[dict[str, Any]], delegation: dict[str, str]) -> None:
    by_id = {task["id"]: task for task in tasks}
    seen_repairs: list[dict[str, Any]] = []
    for task in tasks:
        refinement = _refinement_contract(task)
        if refinement is None:
            continue
        task_id = task["id"]
        envelope_id = refinement["envelope_task_id"]
        envelope = by_id.get(envelope_id)
        if envelope is None:
            raise ControlError(f"{task_id} refinement envelope task is unknown: {envelope_id}")
        if envelope_id == task_id:
            raise ControlError(f"{task_id} refinement cannot use itself as its envelope")
        if envelope.get("refinement") is not None:
            raise ControlError(
                f"{task_id} refinement envelope must name the approved root task, not another repair task"
            )
        if "semantic_routes" not in envelope or "semantic_routes" not in task:
            raise ControlError(
                f"{task_id} bounded refinement requires successor semantic_routes on repair and envelope"
            )
        envelope_contract = _normalized_refinement_envelope(envelope)
        repair_contract = _normalized_refinement_envelope(task)
        for field in envelope_contract:
            if repair_contract[field] != envelope_contract[field]:
                raise ControlError(
                    f"{task_id} refinement changes approved envelope field {field}; "
                    "route this change to PROGRAMME_OWNER"
                )
        if delegation[task_id] != delegation[envelope_id]:
            raise ControlError(
                f"{task_id} refinement changes actor class from {delegation[envelope_id]} "
                f"to {delegation[task_id]}; route this change to PROGRAMME_OWNER"
            )
        expected_prior = [
            prior_task["id"]
            for prior_task in seen_repairs
            if prior_task["refinement"]["envelope_task_id"] == envelope_id
            and prior_task["refinement"]["mechanism_id"] == refinement["mechanism_id"]
        ]
        if refinement["prior_repair_task_ids"] != expected_prior:
            raise ControlError(
                f"{task_id} refinement recurrence history must list every prior repair for mechanism "
                f"{refinement['mechanism_id']} in order: {expected_prior}"
            )
        seen_repairs.append(task)


def historical_delegation_at_commit(commit: str) -> dict[str, str]:
    result = git_result("show", f"{commit}:{DELEGATION_REL}")
    if result.returncode != 0:
        raise ControlError(f"admitted task history is missing control/delegation.json at {commit[:12]}")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ControlError(f"admitted delegation history is invalid at {commit[:12]}") from exc
    mapping = data.get("leaf_actor_class") if isinstance(data, dict) else None
    if not isinstance(mapping, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in mapping.items()):
        raise ControlError(f"admitted delegation history has invalid actor mapping at {commit[:12]}")
    return {str(k): str(v) for k, v in mapping.items()}


def bounded_refinement_delegation_transition(
    anchor: str, tasks: list[dict[str, Any]], current: dict[str, str]
) -> bool:
    previous = historical_delegation_at_commit(anchor)
    if any(current.get(task_id) != actor for task_id, actor in previous.items()):
        return False
    if set(previous) - set(current):
        return False
    by_id = {task["id"]: task for task in tasks}
    added = sorted(set(current) - set(previous))
    if not added:
        return False
    for task_id in added:
        task = by_id.get(task_id)
        refinement = task.get("refinement") if task else None
        if not isinstance(refinement, dict):
            return False
        envelope_id = refinement.get("envelope_task_id")
        if envelope_id not in previous:
            return False
        if current[task_id] != previous[envelope_id]:
            return False
    return True


def validate_independent_review_contracts(
    tasks: list[dict[str, Any]], delegation: dict[str, str], cfg: dict[str, Any]
) -> None:
    by_id = {task["id"]: task for task in tasks}
    authority = set(cfg["authority_files"])
    for task in tasks:
        task_id = task["id"]
        actor = delegation[task_id]
        review = task.get("independent_review")
        if actor == "INDEPENDENT_REVIEW" and review is None:
            raise ControlError(
                f"{task_id} actor class INDEPENDENT_REVIEW requires an independent_review contract"
            )
        if review is None:
            continue
        unknown_sources = [rel for rel in review["source_paths"] if rel not in authority]
        if unknown_sources:
            raise ControlError(
                f"{task_id} independent_review source is not configured authority: {unknown_sources[0]}"
            )
        repair = review["repair_task_id"]
        if repair not in by_id:
            raise ControlError(
                f"{task_id} independent_review repair_task_id must name a known owning leaf"
            )


def validate_programme_owner_review_contracts(
    tasks: list[dict[str, Any]], delegation: dict[str, str]
) -> None:
    for task in tasks:
        task_id = task["id"]
        actor = delegation[task_id]
        owner_review = task.get("programme_owner_review")
        if actor == "PROGRAMME_OWNER" and owner_review is None:
            raise ControlError(
                f"{task_id} actor class PROGRAMME_OWNER requires a programme_owner_review contract"
            )


def validate_dependency_graph(tasks: list[dict[str, Any]]) -> None:
    by_id = {task["id"]: task for task in tasks}
    for task in tasks:
        for dep in task["depends_on"]:
            if dep not in by_id:
                raise ControlError(f"{task['id']} depends on unknown task {dep}")
            if dep == task["id"]:
                raise ControlError(f"dependency cycle includes {task['id']}")
    visiting: set[str] = set(); visited: set[str] = set()
    def visit(task_id: str) -> None:
        if task_id in visiting:
            raise ControlError(f"dependency cycle detected at {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dep in by_id[task_id]["depends_on"]:
            visit(dep)
        visiting.remove(task_id); visited.add(task_id)
    for task_id in by_id:
        visit(task_id)
    for task in tasks:
        if task["status"] == "accepted":
            bad = [dep for dep in task["depends_on"] if by_id[dep]["status"] != "accepted"]
            if bad:
                raise ControlError(f"accepted task {task['id']} has unaccepted dependency {bad[0]}")


def ready_tasks(tasks: list[dict[str, Any]]) -> list[str]:
    by_id = {task["id"]: task for task in tasks}
    return [
        task["id"] for task in tasks
        if task["status"] == "pending"
        and all(by_id[dep]["status"] == "accepted" for dep in task["depends_on"])
    ]


def derived_active_task(tasks: list[dict[str, Any]]) -> str | None:
    by_id = {task["id"]: task for task in tasks}
    in_progress = [task["id"] for task in tasks if task["status"] == "in_progress"]
    if len(in_progress) > 1:
        raise ControlError("more than one task is in_progress; active task is ambiguous")
    if in_progress:
        active = in_progress[0]
        if any(by_id[dep]["status"] != "accepted" for dep in by_id[active]["depends_on"]):
            raise ControlError(f"in_progress task {active} is blocked by an unaccepted dependency")
        return active
    ready = ready_tasks(tasks)
    return ready[0] if len(ready) == 1 else None


def current_branch() -> str:
    branch = run_git("branch", "--show-current")
    if not branch:
        raise ControlError("detached HEAD is not allowed")
    return branch


def git_identity() -> tuple[str, str, str]:
    return run_git("rev-parse", "HEAD"), run_git("rev-parse", "HEAD^{tree}"), current_branch()


def git_commit_time(commit: str) -> str:
    return run_git("show", "-s", "--format=%cI", commit)


def git_commit_exists(commit: str | None) -> bool:
    if not isinstance(commit, str) or not commit:
        return False
    return git_result("cat-file", "-e", f"{commit}^{{commit}}").returncode == 0


def commit_tree(commit: str) -> str:
    return run_git("rev-parse", f"{commit}^{{tree}}")


def is_ancestor(older: str, newer: str) -> bool:
    return git_result("merge-base", "--is-ancestor", older, newer).returncode == 0


def resolve_acceptance_ref(cfg: dict[str, Any]) -> str:
    branch = cfg["acceptance_branch"]
    local = f"refs/heads/{branch}"
    if git_result("show-ref", "--verify", "--quiet", local).returncode == 0:
        return local
    out = run_git("for-each-ref", "--format=%(refname)", "refs/remotes")
    suffix = "/" + branch
    candidates = sorted(
        ref for ref in out.splitlines()
        if ref.endswith(suffix) and not ref.endswith("/HEAD")
    )
    if not candidates:
        raise ControlError(f"acceptance branch {branch} does not exist")
    targets: dict[str, list[str]] = {}
    for ref in candidates:
        target = run_git("rev-parse", ref)
        targets.setdefault(target, []).append(ref)
    if len(targets) != 1:
        raise ControlError(f"acceptance branch {branch} is ambiguous across remote-tracking refs")
    return candidates[0]


def acceptance_tag_targets(
    tasks: list[dict[str, Any]], cfg: dict[str, Any], *, allow_missing: bool = False,
) -> dict[str, str]:
    by_id = {t["id"]: t for t in tasks}
    targets: dict[str, str] = {}
    tags = set(run_git("tag", "--list", "accepted/*").splitlines())
    for tag in tags:
        task_id = tag.split("accepted/", 1)[1]
        if task_id not in by_id:
            raise ControlError(f"acceptance tag {tag} references unknown task")
        if by_id[task_id]["status"] != "accepted":
            raise ControlError(f"acceptance tag {tag} exists but task status is {by_id[task_id]['status']}")
    for task in tasks:
        task_id = task["id"]
        tag = f"accepted/{task_id}"
        if task["status"] != "accepted":
            continue
        if tag not in tags:
            if allow_missing:
                continue
            raise ControlError(f"accepted task {task_id} requires Git tag {tag}")
        target = run_git("rev-parse", f"refs/tags/{tag}^{{commit}}")
        branch_ref = resolve_acceptance_ref(cfg)
        branch_head = run_git("rev-parse", branch_ref)
        if not is_ancestor(target, branch_head):
            raise ControlError(f"acceptance tag {tag} is not on acceptance branch {cfg['acceptance_branch']}")
        shown = git_result("show", f"{target}:{TASKS_REL}")
        if shown.returncode != 0:
            raise ControlError(f"acceptance tag {tag} has no control/tasks.json")
        try:
            at_tag = json.loads(shown.stdout)
        except json.JSONDecodeError as exc:
            raise ControlError(f"acceptance tag {tag} has invalid control/tasks.json") from exc
        tagged_tasks = {t.get("id"): t for t in at_tag.get("tasks", []) if isinstance(t, dict)}
        tagged = tagged_tasks.get(task_id)
        if not tagged or tagged.get("status") != "accepted":
            raise ControlError(f"acceptance tag {tag} tagged commit does not mark {task_id} accepted")
        for dep in tagged.get("depends_on", []):
            if tagged_tasks.get(dep, {}).get("status") != "accepted":
                raise ControlError(f"acceptance tag {tag} tagged commit has unaccepted dependency {dep}")
        for field in (
            "requirements", "depends_on", "write_paths", "acceptance", "verification",
            "independent_review", "programme_owner_review", "refinement", "work_type", "test_first",
        ):
            tagged_value = tagged.get(field)
            if field == "verification" and tagged_value is None:
                tagged_value = {"leaf_close": [], "promotion": []}
            if tagged_value != task.get(field):
                raise ControlError(
                    f"accepted task {task_id} semantic contract differs from {tag}: {field}"
                )
        tagged_blocks = historical_plan_blocks_at_commit(target)
        _global, current_blocks = parse_plan()
        tagged_block = tagged_blocks.get(task_id)
        current_block = current_blocks.get(task_id)
        if tagged_block is None or current_block is None:
            raise ControlError(
                f"accepted task {task_id} semantic contract differs from {tag}: EXEC_PLAN.md task block"
            )
        if plan_task_semantic_block(task_id, tagged_block) != plan_task_semantic_block(task_id, current_block):
            raise ControlError(
                f"accepted task {task_id} semantic contract differs from {tag}: EXEC_PLAN.md task block"
            )
        # semantic_routes marks the successor task contract; required verification requires
        # every declared leaf-close/promotion check to have admissible evidence
        # in the exact acceptance-tag commit. Legacy contracts without the
        # successor route field retain their historical validation semantics.
        if "semantic_routes" in tagged:
            validate_required_verification_at_acceptance(tagged, "leaf-close", target)
            validate_required_verification_at_acceptance(tagged, "promotion", target)
        targets[task_id] = target
    return dict(sorted(targets.items()))


def validate_test_first_acceptance_evidence(
    tasks: list[dict[str, Any]], tags: dict[str, str], cfg: dict[str, Any]
) -> None:
    if cfg.get("test_first_policy", "legacy") != "required":
        return
    by_id = {task["id"]: task for task in tasks}
    for task in tasks:
        if task.get("work_type") != "implementation":
            continue
        contract = task.get("test_first")
        if not isinstance(contract, dict) or contract.get("exception_task_id") is not None:
            continue
        predecessor_id = contract.get("test_task_id")
        predecessor = by_id.get(predecessor_id)
        if predecessor is None or predecessor.get("status") != "accepted":
            continue
        target = tags.get(predecessor_id)
        if target is None:
            raise ControlError(
                f"{task['id']} governing test/proof predecessor {predecessor_id} has no accepted tag evidence"
            )
        if contract.get("red_required"):
            validate_required_verification_at_acceptance(predecessor, "leaf-close", target)


def receipt_hashes() -> dict[str, str]:
    if not RECEIPTS_DIR.exists():
        return {}
    values: dict[str, str] = {}
    for path in sorted(RECEIPTS_DIR.glob("*.json")):
        if path.is_symlink():
            raise ControlError(f"verification receipt must not be a symlink: {path.relative_to(ROOT)}")
        rel = path.relative_to(ROOT).as_posix()
        values[rel] = sha256_file(path)
    return values


def verification_input_fingerprint(inputs: list[str]) -> str:
    h = hashlib.sha256()
    for rel in inputs:
        path = ROOT / rel
        if path.is_symlink():
            raise ControlError(f"verification input must not be a symlink: {rel}")
        if not path.is_file():
            raise ControlError(f"verification input is missing or not a regular file: {rel}")
        h.update(rel.encode("utf-8") + b"\0")
        h.update(sha256_file(path).encode("ascii") + b"\0")
    return h.hexdigest()


def verification_governing_fingerprint(
    task: dict[str, Any], gate: str, check: dict[str, Any]
) -> str:
    _global, plan_blocks = parse_plan()
    block = plan_blocks.get(task["id"])
    if block is None:
        raise ControlError(f"verification task {task['id']} has no plan block")
    requirement_text = extract_requirement_sections(task["requirements"])
    contract = {
        "task": {
            key: task.get(key)
            for key in (
                "id", "title", "requirements", "depends_on", "write_paths",
                "acceptance", "context_refs",
            )
        },
        "gate": gate,
        "check": check,
        "plan_block": block,
        "requirements": requirement_text,
    }
    encoded = json.dumps(contract, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(encoded)


def verification_expected_exit_codes(check: dict[str, Any]) -> list[int]:
    value = check.get("expected_exit_codes")
    return list(value) if isinstance(value, list) else [0]


def verification_evidence_key(
    task: dict[str, Any], gate: str, check: dict[str, Any],
    input_fingerprint: str, governing_fingerprint: str,
) -> str:
    payload = {
        "task_id": task["id"],
        "gate": gate,
        "check_id": check["id"],
        "proposition": check["proposition"],
        "command": check["command"],
        "input_fingerprint": input_fingerprint,
        "governing_fingerprint": governing_fingerprint,
    }
    if "expected_exit_codes" in check:
        payload["expected_exit_codes"] = verification_expected_exit_codes(check)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(encoded)


def _git_file_bytes_at_commit(commit: str, rel: str, purpose: str) -> bytes:
    tree = git_result("ls-tree", commit, "--", rel)
    if tree.returncode != 0 or not tree.stdout.strip():
        raise ControlError(f"{purpose} is missing at acceptance commit: {rel}")
    line = tree.stdout.strip().splitlines()
    if len(line) != 1 or "\t" not in line[0]:
        raise ControlError(f"{purpose} has ambiguous Git identity at acceptance commit: {rel}")
    meta, shown_rel = line[0].split("\t", 1)
    parts = meta.split()
    if len(parts) != 3 or parts[1] != "blob" or parts[0] == "120000" or shown_rel != rel:
        raise ControlError(f"{purpose} is not a regular Git file at acceptance commit: {rel}")
    shown = subprocess.run(
        ["git", "show", f"{commit}:{rel}"], cwd=ROOT, capture_output=True, check=False
    )
    if shown.returncode != 0:
        raise ControlError(f"{purpose} cannot be read at acceptance commit: {rel}")
    return shown.stdout


def verification_input_fingerprint_at_commit(inputs: list[str], commit: str) -> str:
    h = hashlib.sha256()
    for rel in inputs:
        data = _git_file_bytes_at_commit(commit, rel, "verification input")
        h.update(rel.encode("utf-8") + b"\0")
        h.update(sha256_bytes(data).encode("ascii") + b"\0")
    return h.hexdigest()


def _requirement_sections_from_text(text: str, required_ids: list[str]) -> str:
    matches = list(REQ_HEADING_RE.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[match.start():end].strip()
    missing = [req for req in required_ids if req not in sections]
    if missing:
        raise ControlError(f"complete requirement lookup failed for {', '.join(missing)}")
    return "\n\n".join(sections[req] for req in required_ids)


def verification_governing_fingerprint_at_commit(
    task: dict[str, Any], gate: str, check: dict[str, Any], commit: str
) -> str:
    plan_blocks = historical_plan_blocks_at_commit(commit)
    block = plan_blocks.get(task["id"])
    if block is None:
        raise ControlError(f"verification task {task['id']} has no plan block at acceptance commit")
    requirements_rel = historical_authority_path_at_commit(commit, "requirements_path", "REQUIREMENTS.md")
    requirements_bytes = _git_file_bytes_at_commit(commit, requirements_rel, "requirements authority")
    try:
        requirements_text = requirements_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ControlError(f"{requirements_rel} is not UTF-8 at acceptance commit") from exc
    requirement_text = _requirement_sections_from_text(requirements_text, task["requirements"])
    contract = {
        "task": {
            key: task.get(key)
            for key in (
                "id", "title", "requirements", "depends_on", "write_paths",
                "acceptance", "context_refs",
            )
        },
        "gate": gate,
        "check": check,
        "plan_block": block,
        "requirements": requirement_text,
    }
    encoded = json.dumps(contract, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(encoded)


def _required_receipts_at_commit(commit: str) -> list[tuple[str, dict[str, Any]]]:
    listed = git_result("ls-tree", "-r", "--name-only", commit, "--", RECEIPTS_REL_PREFIX.rstrip("/"))
    if listed.returncode != 0:
        raise ControlError("cannot enumerate verification receipts at acceptance commit")
    values: list[tuple[str, dict[str, Any]]] = []
    for rel in sorted(line for line in listed.stdout.splitlines() if line.endswith(".json")):
        raw = _git_file_bytes_at_commit(commit, rel, "verification receipt")
        try:
            receipt = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(receipt, dict):
            values.append((rel, receipt))
    return values


def validate_required_verification_at_acceptance(
    task: dict[str, Any], gate: str, commit: str
) -> None:
    gate_key = VERIFICATION_GATES[gate]
    checks = task.get("verification", {"leaf_close": [], "promotion": []})[gate_key]
    if not checks:
        return
    receipts = _required_receipts_at_commit(commit)
    for check in checks:
        input_fingerprint = verification_input_fingerprint_at_commit(check["inputs"], commit)
        governing_fingerprint = verification_governing_fingerprint_at_commit(
            task, gate, check, commit
        )
        evidence_key = verification_evidence_key(
            task, gate, check, input_fingerprint, governing_fingerprint
        )
        expected = {
            "evidence_type": "required-check",
            "task_id": task["id"],
            "gate": gate,
            "check_id": check["id"],
            "proposition": check["proposition"],
            "command": check["command"],
            "input_scope": check["inputs"],
            "input_fingerprint": input_fingerprint,
            "governing_fingerprint": governing_fingerprint,
            "evidence_key": evidence_key,
        }
        if "expected_exit_codes" in check:
            expected["expected_exit_codes"] = verification_expected_exit_codes(check)
        matching: list[tuple[str, dict[str, Any]]] = []
        for rel, receipt in receipts:
            if all(receipt.get(key) == value for key, value in expected.items()):
                matching.append((rel, receipt))
        allowed_exit_codes = verification_expected_exit_codes(check)
        successful = [
            rel for rel, receipt in matching
            if receipt.get("exit_code") in allowed_exit_codes and receipt.get("repository_mutated") is False
        ]
        if successful:
            continue
        failed = [rel for rel, _receipt in matching]
        detail = f"; matching non-success receipt(s): {', '.join(failed)}" if failed else ""
        raise ControlError(
            f"accepted task {task['id']} requires current successful {gate} receipt "
            f"for {check['id']} at {commit[:12]}{detail}"
        )


def reusable_verification_receipt(evidence_key: str, expected_exit_codes: list[int]) -> Path | None:
    if not RECEIPTS_DIR.exists():
        return None
    for path in sorted(RECEIPTS_DIR.glob("*.json")):
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(receipt, dict):
            continue
        if (
            receipt.get("evidence_key") == evidence_key
            and receipt.get("exit_code") in expected_exit_codes
            and receipt.get("repository_mutated") is False
        ):
            return path
    return None


def reusable_failed_verification_receipt(
    evidence_key: str, result: subprocess.CompletedProcess[str], mutated: bool,
) -> Path | None:
    if mutated or not RECEIPTS_DIR.exists():
        return None
    stdout_hash = sha256_bytes(result.stdout.encode("utf-8"))
    stderr_hash = sha256_bytes(result.stderr.encode("utf-8"))
    for path in sorted(RECEIPTS_DIR.glob("*.json")):
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(receipt, dict):
            continue
        if (
            receipt.get("evidence_key") == evidence_key
            and receipt.get("exit_code") == result.returncode
            and receipt.get("stdout_sha256") == stdout_hash
            and receipt.get("stderr_sha256") == stderr_hash
            and receipt.get("repository_mutated") is False
        ):
            return path
    return None


def write_required_verification_receipt(
    task: dict[str, Any], gate: str, check: dict[str, Any],
    input_fingerprint: str, governing_fingerprint: str, evidence_key: str,
    result: subprocess.CompletedProcess[str], mutated: bool,
    before_head: str, before_tree: str, branch: str,
    before_fp: str, before_state: str, before_auth: dict[str, str],
) -> Path:
    now = datetime.now(timezone.utc)
    stem = now.strftime("%Y%m%dT%H%M%S%fZ") + "-" + check["id"].lower()
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPTS_DIR / f"{stem}.json"
    if receipt_path.exists():
        raise ControlError("verification receipt path collision")
    receipt = {
        "schema_version": 2,
        "generated_at": now.isoformat(),
        "evidence_type": "required-check",
        "task_id": task["id"],
        "gate": gate,
        "check_id": check["id"],
        "proposition": check["proposition"],
        "command": check["command"],
        "input_scope": check["inputs"],
        "input_fingerprint": input_fingerprint,
        "governing_fingerprint": governing_fingerprint,
        "evidence_key": evidence_key,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "stdout_sha256": sha256_bytes(result.stdout.encode("utf-8")),
        "stderr_sha256": sha256_bytes(result.stderr.encode("utf-8")),
        "source_head": before_head,
        "source_tree": before_tree,
        "branch": branch,
        "repo_fingerprint": before_fp,
        "working_state_digest": before_state,
        "authority_hashes": before_auth,
        "repository_mutated": mutated,
        "claim_boundary": (
            "This receipt establishes only the declared proposition for the recorded "
            "verification check against its recorded input and governing fingerprints."
        ),
    }
    if "expected_exit_codes" in check:
        receipt["expected_exit_codes"] = verification_expected_exit_codes(check)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt_path


def validate_handoff_schema(handoff: dict[str, Any]) -> None:
    if handoff.get("schema_version") != 2:
        raise ControlError("invalid control/handoff.json schema_version")
    missing = sorted(HANDOFF_REQUIRED - set(handoff))
    if missing:
        raise ControlError(f"control/handoff.json missing required field(s): {', '.join(missing)}")
    extra = sorted(set(handoff) - HANDOFF_REQUIRED)
    if extra:
        raise ControlError(f"control/handoff.json contains unsupported field(s): {', '.join(extra)}")
    if not isinstance(handoff["authority_hashes"], dict):
        raise ControlError("handoff authority_hashes must be an object")
    if not isinstance(handoff["ready_tasks"], list) or not all(isinstance(x, str) for x in handoff["ready_tasks"]):
        raise ControlError("handoff ready_tasks must be a string list")
    if not isinstance(handoff["acceptance_tags"], dict):
        raise ControlError("handoff acceptance_tags must be an object")
    if not isinstance(handoff["receipt_hashes"], dict):
        raise ControlError("handoff receipt_hashes must be an object")
    if not isinstance(handoff["unresolved_claims"], list):
        raise ControlError("handoff unresolved_claims must be a list")


def first_parent(commit: str) -> str | None:
    result = git_result("rev-parse", f"{commit}^")
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def derived_checkpoint_source_head(head: str, generated_rel: str = HANDOFF_REL) -> str:
    current = head
    while True:
        paths = commit_paths(current)
        if not paths:
            raise ControlError(f"empty commit after checkpoint is not allowed: {current[:12]}")
        if set(paths) != {generated_rel}:
            return current
        parent = first_parent(current)
        if parent is None:
            raise ControlError("cannot derive checkpoint source from a generated-state-only root commit")
        current = parent


def build_expected_handoff(
    cfg: dict[str, Any],
    tasks: list[dict[str, Any]],
    hashes: dict[str, str],
    tags: dict[str, str],
    receipts: dict[str, str],
    source_head: str,
) -> dict[str, Any]:
    if not git_commit_exists(source_head):
        raise ControlError("derived handoff source_head does not identify a Git commit")
    _head, _tree, branch = git_identity()
    current_ready = ready_tasks(tasks)
    return {
        "schema_version": 2,
        "generated_at": git_commit_time(source_head),
        "active_task": derived_active_task(tasks),
        "authority_hashes": hashes,
        "repo_fingerprint": repo_fingerprint(cfg),
        "task_contract_hash": task_contract_hash(),
        "claims_hash": claims_hash(),
        "source_head": source_head,
        "source_tree": commit_tree(source_head),
        "branch": branch,
        "working_state_digest": working_state_digest(cfg),
        "ready_tasks": current_ready,
        "unresolved_claims": unresolved_claim_ids(),
        "last_receipt": sorted(receipts)[-1] if receipts else None,
        "acceptance_tags": tags,
        "receipt_hashes": receipts,
    }


def blocked_claim_ids() -> list[str]:
    return sorted(claim["id"] for claim in load_claims() if claim["status"] == "BLOCKED")


def derived_next_leaf(tasks: list[dict[str, Any]], active: str | None) -> str | None:
    if not active:
        return None
    candidates = [
        task["id"] for task in tasks
        if active in task["depends_on"] and task["status"] in {"pending", "blocked"}
    ]
    return candidates[0] if len(candidates) == 1 else None


def accepted_base_record(cfg: dict[str, Any]) -> dict[str, str]:
    ref = resolve_acceptance_ref(cfg)
    branch_head = run_git("rev-parse", ref)
    base = derived_checkpoint_source_head(branch_head, generated_state_rel(cfg))
    return {"branch": cfg["acceptance_branch"], "head": base, "tree": commit_tree(base)}


def migration_provenance(cfg: dict[str, Any]) -> dict[str, str] | None:
    value = cfg.get("lcr_migration")
    return dict(value) if isinstance(value, dict) else None


def verify_lcr_migration_provenance(cfg: dict[str, Any]) -> None:
    migration = migration_provenance(cfg)
    if migration is None:
        return
    state_commit = migration["legacy_state_commit"]
    source_head = migration["legacy_source_head"]
    if not git_commit_exists(state_commit) or not git_commit_exists(source_head):
        raise ControlError("LCR migration provenance references a missing commit")
    current_head = run_git("rev-parse", "HEAD")
    if not is_ancestor(state_commit, current_head):
        raise ControlError("LCR migration legacy state is not an ancestor of current HEAD")
    shown = subprocess.run(
        ["git", "show", f"{state_commit}:{HANDOFF_REL}"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if shown.returncode != 0:
        raise ControlError("LCR migration legacy state commit has no control/handoff.json")
    if sha256_bytes(shown.stdout) != migration["legacy_handoff_sha256"]:
        raise ControlError("LCR migration legacy handoff hash mismatch")
    try:
        legacy = json.loads(shown.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ControlError("LCR migration legacy handoff is unreadable") from exc
    validate_handoff_schema(legacy)
    if legacy.get("source_head") != source_head:
        raise ControlError("LCR migration legacy source_head mismatch")
    if legacy.get("source_tree") != migration["legacy_source_tree"]:
        raise ControlError("LCR migration legacy source_tree mismatch")
    if commit_tree(source_head) != migration["legacy_source_tree"]:
        raise ControlError("LCR migration legacy source tree no longer matches Git")


def validate_lcr_schema(lcr: dict[str, Any], *, allow_legacy_context_shape: bool = False) -> None:
    if lcr.get("schema_version") != 1:
        raise ControlError("invalid control/lcr.json schema_version")
    missing = sorted(LCR_REQUIRED - set(lcr))
    if missing:
        raise ControlError(f"control/lcr.json missing required field(s): {', '.join(missing)}")
    extra = sorted(set(lcr) - LCR_REQUIRED)
    if extra:
        raise ControlError(f"control/lcr.json contains unsupported field(s): {', '.join(extra)}")
    if lcr["active_leaf"] is not None:
        leaf = lcr["active_leaf"]
        if not isinstance(leaf, dict) or set(leaf) != {"id", "label", "status"}:
            raise ControlError("LCR active_leaf must be null or {id,label,status}")
    if not isinstance(lcr["authority_hashes"], dict):
        raise ControlError("LCR authority_hashes must be an object")
    if not isinstance(lcr["checkpoint"], dict) or set(lcr["checkpoint"]) != {"source_head", "source_tree", "branch", "working_state_digest"}:
        raise ControlError("LCR checkpoint has invalid shape")
    if not isinstance(lcr["accepted_base"], dict) or set(lcr["accepted_base"]) != {"branch", "head", "tree"}:
        raise ControlError("LCR accepted_base has invalid shape")
    context = lcr["applicable_context"]
    current_context_fields = {"authority_files", "requirements", "plan_leaf", "ancestors", "dependencies"}
    legacy_context_fields = {"authority_files", "requirements", "plan_leaf", "dependencies"}
    if not isinstance(context, dict) or (
        set(context) != current_context_fields
        and not (allow_legacy_context_shape and set(context) == legacy_context_fields)
    ):
        raise ControlError("LCR applicable_context has invalid shape")
    if not isinstance(lcr["next_transition"], dict) or set(lcr["next_transition"]) != {"actor_class", "next_leaf"}:
        raise ControlError("LCR next_transition has invalid shape")
    if lcr["next_transition"].get("actor_class") not in ACTOR_CLASSES:
        raise ControlError("LCR next_transition actor_class is invalid")
    for field in ("ready_tasks", "unresolved_claims", "blockers"):
        if not isinstance(lcr[field], list) or not all(isinstance(x, str) for x in lcr[field]):
            raise ControlError(f"LCR {field} must be a string list")
    for field in ("acceptance_tags", "receipt_hashes"):
        if not isinstance(lcr[field], dict):
            raise ControlError(f"LCR {field} must be an object")


def build_expected_lcr(
    cfg: dict[str, Any],
    tasks: list[dict[str, Any]],
    hashes: dict[str, str],
    tags: dict[str, str],
    receipts: dict[str, str],
    source_head: str,
    *,
    working_state_digest_override: str | None = None,
    accepted_base_override: dict[str, str] | None = None,
    acceptance_tags_override: dict[str, str] | None = None,
) -> dict[str, Any]:
    if not git_commit_exists(source_head):
        raise ControlError("derived LCR source_head does not identify a Git commit")
    _head, _tree, branch = git_identity()
    active = derived_active_task(tasks)
    delegation = load_delegation(tasks, cfg)
    by_id = {task["id"]: task for task in tasks}
    active_task = by_id.get(active) if active else None
    active_leaf = None if active_task is None else {
        "id": active_task["id"],
        "label": active_task["title"],
        "status": active_task["status"],
    }
    applicable = bounded_context_scope(cfg, tasks, active)
    return {
        "schema_version": 1,
        "generated_at": git_commit_time(source_head),
        "active_leaf": active_leaf,
        "authority_hashes": hashes,
        "repo_fingerprint": repo_fingerprint(cfg),
        "task_contract_hash": task_contract_hash(),
        "claims_hash": claims_hash(),
        "checkpoint": {
            "source_head": source_head,
            "source_tree": commit_tree(source_head),
            "branch": branch,
            "working_state_digest": (
                working_state_digest_override
                if working_state_digest_override is not None
                else working_state_digest(cfg)
            ),
        },
        "accepted_base": accepted_base_override if accepted_base_override is not None else accepted_base_record(cfg),
        "ready_tasks": ready_tasks(tasks),
        "unresolved_claims": unresolved_claim_ids(),
        "blockers": blocked_claim_ids(),
        "last_receipt": sorted(receipts)[-1] if receipts else None,
        "acceptance_tags": acceptance_tags_override if acceptance_tags_override is not None else tags,
        "receipt_hashes": receipts,
        "applicable_context": applicable,
        "next_transition": {
            "actor_class": delegation[active] if active else "AUTONOMOUS",
            "next_leaf": active,
        },
        "migration_provenance": migration_provenance(cfg),
    }


def commit_paths(commit: str) -> list[str]:
    out = run_git("diff-tree", "--root", "-m", "--first-parent", "--no-commit-id", "--name-only", "-r", commit)
    return [line for line in out.splitlines() if line]


def intervening_commits(anchor: str, head: str) -> list[str]:
    if anchor == head:
        return []
    if not is_ancestor(anchor, head):
        raise ControlError("checkpoint history anchor is not an ancestor of current HEAD")
    out = run_git("rev-list", "--reverse", f"{anchor}..{head}")
    return [line for line in out.splitlines() if line]


def latest_generated_state_commit(cfg: dict[str, Any], head: str) -> str | None:
    rel = generated_state_rel(cfg)
    result = git_result("log", "-1", "--format=%H", head, "--", rel)
    value = result.stdout.strip()
    return value or None


def validate_check_history(anchor: str, head: str, generated_rel: str = HANDOFF_REL) -> None:
    for commit in intervening_commits(anchor, head):
        paths = commit_paths(commit)
        if not paths:
            raise ControlError(f"empty commit after checkpoint is not allowed: {commit[:12]}")
        if any(path != generated_rel for path in paths):
            raise ControlError(f"repository history changed after checkpoint at {commit[:12]}")


def generated_only_history(anchor: str, head: str, generated_rel: str) -> bool:
    try:
        validate_check_history(anchor, head, generated_rel)
        return True
    except ControlError:
        return False


def validate_lcr_checkpoint_shape(source: str, head: str, cfg: dict[str, Any]) -> None:
    state_commit = latest_generated_state_commit(cfg, head)
    if state_commit != head:
        raise ControlError("repository history changed after LCR checkpoint")
    if not is_ancestor(source, head):
        raise ControlError("LCR checkpoint source is not an ancestor of current HEAD")
    if first_parent(head) != source:
        raise ControlError("LCR checkpoint must bind the immediately preceding first-parent state")
    paths = commit_paths(head)
    if not paths:
        raise ControlError(f"empty LCR checkpoint commit is not allowed: {head[:12]}")
    if generated_state_rel(cfg) not in paths:
        raise ControlError("current LCR checkpoint commit does not contain generated LCR state")


def validate_admitted_paths(
    cfg: dict[str, Any], tasks: list[dict[str, Any]], state: dict[str, Any], paths: list[str],
    args: argparse.Namespace, *, context: str,
) -> None:
    active = state_active_task(state, cfg)
    by_id = {t["id"]: t for t in tasks}
    scopes = by_id.get(active, {}).get("write_paths", []) if active else []
    control_context_prefix = _root_rel(PCM_HOME / "control" / "context").rstrip("/") + "/"
    for rel in paths:
        if rel == generated_state_rel(cfg):
            continue
        if rel.startswith(RECEIPTS_REL_PREFIX):
            if not args.admit_receipts:
                raise ControlError(f"verification receipt {context} requires --admit-receipts")
            continue
        if rel == CLAIMS_REL:
            if not args.admit_claims_change:
                raise ControlError(f"claims state {context} requires --admit-claims-change")
            continue
        if rel.startswith(INDEPENDENT_REVIEW_RESULTS_REL_PREFIX):
            if not args.admit_independent_review_result:
                raise ControlError(
                    f"independent-review result {context} requires --admit-independent-review-result"
                )
            if args.actor_class != "INDEPENDENT_REVIEW":
                raise ControlError(
                    "independent-review result admission requires actor class INDEPENDENT_REVIEW"
                )
            continue
        if rel.startswith(PROGRAMME_OWNER_DECISIONS_REL_PREFIX):
            if not args.admit_programme_owner_decision:
                raise ControlError(
                    f"programme-owner decision {context} requires --admit-programme-owner-decision"
                )
            if args.actor_class != "PROGRAMME_OWNER":
                raise ControlError(
                    "programme-owner decision admission requires actor class PROGRAMME_OWNER"
                )
            continue
        if rel in {TASKS_REL, PROJECT_REL, cfg["execution_plan_path"]}:
            if not args.admit_contract_change:
                raise ControlError(f"contract change {rel} requires --admit-contract-change")
            continue
        if rel in cfg["authority_files"]:
            if not args.admit_authority_change:
                raise ControlError(f"authority change {rel} requires --admit-authority-change")
            continue
        if rel in {SCRIPT_REL, "README.md", "Makefile", ".gitignore"} or rel.startswith("tests/") or rel.startswith(".github/") or rel.startswith(control_context_prefix):
            if not args.admit_control_change:
                raise ControlError(f"controller change {rel} requires --admit-control-change")
            continue
        if args.admit_work and any(path_under(rel, scope) for scope in scopes):
            continue
        raise ControlError(f"unadmitted repository {context} path {rel}")


def path_under(rel: str, scope: str) -> bool:
    scope = scope.rstrip("/")
    return rel == scope or rel.startswith(scope + "/")


def state_source_head(state: dict[str, Any], cfg: dict[str, Any]) -> str | None:
    if state_mode(cfg) == "handoff":
        value = state.get("source_head")
    else:
        checkpoint = state.get("checkpoint")
        value = checkpoint.get("source_head") if isinstance(checkpoint, dict) else None
    return value if isinstance(value, str) and value else None


def state_branch(state: dict[str, Any], cfg: dict[str, Any]) -> str | None:
    if state_mode(cfg) == "handoff":
        value = state.get("branch")
    else:
        checkpoint = state.get("checkpoint")
        value = checkpoint.get("branch") if isinstance(checkpoint, dict) else None
    return value if isinstance(value, str) and value else None


def state_active_task(state: dict[str, Any], cfg: dict[str, Any]) -> str | None:
    if state_mode(cfg) == "handoff":
        value = state.get("active_task")
    else:
        leaf = state.get("active_leaf")
        value = leaf.get("id") if isinstance(leaf, dict) else None
    return value if isinstance(value, str) and value else None


def validate_checkpoint_history(
    cfg: dict[str, Any], tasks: list[dict[str, Any]], state: dict[str, Any], head: str, args: argparse.Namespace
) -> None:
    anchor = latest_generated_state_commit(cfg, head) if state_mode(cfg) == "lcr" else state_source_head(state, cfg)
    if not anchor:
        return
    if not git_commit_exists(anchor):
        raise ControlError("generated-state source_head does not identify a Git commit")
    for commit in intervening_commits(anchor, head):
        paths = commit_paths(commit)
        if not paths:
            raise ControlError(f"empty commit after checkpoint is not allowed: {commit[:12]}")
        validate_admitted_paths(cfg, tasks, state, paths, args, context=f"history at {commit[:12]}")


def governance_paths(cfg: dict[str, Any]) -> list[Path]:
    paths = [ROOT / rel for rel in cfg["project_authority_files"]]
    paths.extend([PROJECT_JSON, TASKS_JSON, CLAIMS_JSON])
    return paths


def structural_core(
    *, allow_pending_acceptance: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, str], dict[str, str], dict[str, str]]:
    cfg = config()
    hashes = authority_hashes(cfg)
    validate_instantiation_record(cfg)
    requirements = parse_requirements(cfg)
    _global, plan_blocks = parse_plan(cfg)
    tasks = load_tasks()
    load_claims()
    validate_dependency_graph(tasks)
    delegation = load_delegation(tasks, cfg)
    validate_test_first_contracts(tasks, delegation, cfg)
    validate_refinement_contracts(tasks, delegation)
    validate_independent_review_contracts(tasks, delegation, cfg)
    validate_programme_owner_review_contracts(tasks, delegation)
    validate_context_references(cfg, tasks)
    task_ids = {task["id"] for task in tasks}
    if task_ids != set(plan_blocks):
        missing = sorted(task_ids - set(plan_blocks)); extra = sorted(set(plan_blocks) - task_ids)
        pieces = []
        if missing: pieces.append(f"missing plan blocks {', '.join(missing)}")
        if extra: pieces.append(f"unregistered plan blocks {', '.join(extra)}")
        raise ControlError("plan/task mismatch: " + "; ".join(pieces))
    for task in tasks:
        block = plan_blocks[task["id"]]
        heading = re.search(
            rf"^##\s+{re.escape(task['id'])}\s+—\s+(.+?)\s*$",
            block,
            flags=re.MULTILINE,
        )
        if not heading or not heading.group(1).strip():
            raise ControlError(
                f"{task['id']} plan block requires heading '## {task['id']} — <human-readable label>'"
            )
        if heading.group(1).strip() != task["title"].strip():
            raise ControlError(
                f"{task['id']} plan label does not match control/tasks.json title"
            )
        for req in task["requirements"]:
            if req not in requirements:
                raise ControlError(f"{task['id']} references unknown requirement {req}")
            pattern = re.compile(rf"(?<![A-Z0-9_-]){re.escape(req)}(?![A-Z0-9_-])")
            if not pattern.search(block):
                raise ControlError(f"{task['id']} plan block does not explicitly reference {req}")
    if not cfg.get("template_mode", False):
        for path in governance_paths(cfg):
            match = PLACEHOLDER_RE.search(read_text(path))
            if match:
                raise ControlError(f"unresolved placeholder {match.group(0)} in {path.relative_to(ROOT)}")
    tags = acceptance_tag_targets(tasks, cfg, allow_missing=allow_pending_acceptance)
    if not allow_pending_acceptance:
        validate_test_first_acceptance_evidence(tasks, tags, cfg)
        validate_semantic_routes(tasks, tags)
    review_results = load_independent_review_results(tasks, delegation)
    if not allow_pending_acceptance:
        validate_independent_review_acceptance(tasks, delegation, review_results, tags)
    decisions = load_programme_owner_decisions(tasks, delegation)
    validate_programme_owner_acceptance(tasks, delegation, decisions)
    receipts = receipt_hashes()
    return cfg, tasks, hashes, tags, receipts


def validate_handoff_state(
    cfg: dict[str, Any], tasks: list[dict[str, Any]], hashes: dict[str, str],
    tags: dict[str, str], receipts: dict[str, str], ignore_staleness: bool = False,
) -> None:
    handoff = load_json(HANDOFF_JSON)
    validate_handoff_schema(handoff)
    canonical = json.dumps(handoff, indent=2, sort_keys=True) + "\n"
    if HANDOFF_JSON.read_text(encoding="utf-8") != canonical:
        raise ControlError("control/handoff.json is not canonical JSON")
    if cfg.get("template_mode", False) and not handoff.get("authority_hashes"):
        return
    if ignore_staleness:
        return
    if set(handoff["authority_hashes"]) != set(hashes):
        raise ControlError("handoff authority_hashes do not exactly match configured authority_files")
    for rel, current in hashes.items():
        if handoff["authority_hashes"].get(rel) != current:
            raise ControlError(f"stale authority hash for {rel}")
    if handoff["task_contract_hash"] != task_contract_hash():
        raise ControlError("stale task contract hash in control/handoff.json")
    if handoff["claims_hash"] != claims_hash():
        raise ControlError("stale claims hash in control/handoff.json")
    if handoff["repo_fingerprint"] != repo_fingerprint(cfg):
        raise ControlError("stale repository fingerprint in control/handoff.json")
    if handoff["ready_tasks"] != ready_tasks(tasks):
        raise ControlError("stale ready_tasks in control/handoff.json")
    if handoff["working_state_digest"] != working_state_digest(cfg):
        raise ControlError("stale working state digest in control/handoff.json")
    head, _tree, branch = git_identity()
    if handoff["branch"] != branch:
        raise ControlError(f"stale branch in control/handoff.json: recorded {handoff['branch']}, current {branch}")
    source = handoff["source_head"]
    if not git_commit_exists(source):
        raise ControlError("handoff source_head does not identify a Git commit")
    if handoff["source_tree"] != commit_tree(source):
        raise ControlError("handoff source_tree does not match source_head")
    validate_check_history(source, head, HANDOFF_REL)
    if handoff["acceptance_tags"] != tags:
        raise ControlError("stale acceptance tag targets in control/handoff.json")
    if handoff["receipt_hashes"] != receipts:
        raise ControlError("stale verification receipt hashes in control/handoff.json")
    derived_source = derived_checkpoint_source_head(head, HANDOFF_REL)
    expected = build_expected_handoff(cfg, tasks, hashes, tags, receipts, derived_source)
    if handoff != expected:
        differing = sorted(key for key in HANDOFF_REQUIRED if handoff.get(key) != expected.get(key))
        raise ControlError("derived handoff mismatch: " + ", ".join(differing))


def validate_lcr_state(
    cfg: dict[str, Any], tasks: list[dict[str, Any]], hashes: dict[str, str],
    tags: dict[str, str], receipts: dict[str, str], ignore_staleness: bool = False,
) -> None:
    lcr = load_json(LCR_JSON)
    validate_lcr_schema(lcr)
    canonical = json.dumps(lcr, indent=2, sort_keys=True) + "\n"
    if LCR_JSON.read_text(encoding="utf-8") != canonical:
        raise ControlError(f"{LCR_REL} is not canonical JSON")
    if cfg.get("template_mode", False) and not lcr.get("authority_hashes"):
        return
    if ignore_staleness:
        return
    verify_lcr_migration_provenance(cfg)
    if set(lcr["authority_hashes"]) != set(hashes):
        raise ControlError("LCR authority_hashes do not exactly match configured authority_files")
    for rel, current in hashes.items():
        if lcr["authority_hashes"].get(rel) != current:
            raise ControlError(f"stale authority hash for {rel}")
    if lcr["task_contract_hash"] != task_contract_hash():
        raise ControlError("stale task contract hash in control/lcr.json")
    if lcr["claims_hash"] != claims_hash():
        raise ControlError("stale claims hash in control/lcr.json")
    if lcr["repo_fingerprint"] != repo_fingerprint(cfg):
        raise ControlError("stale repository fingerprint in control/lcr.json")
    if lcr["ready_tasks"] != ready_tasks(tasks):
        raise ControlError("stale ready_tasks in control/lcr.json")
    head, _tree, branch = git_identity()
    checkpoint = lcr["checkpoint"]
    if checkpoint["working_state_digest"] != working_state_digest(cfg):
        raise ControlError("stale working state digest in control/lcr.json")
    if checkpoint["branch"] != branch:
        raise ControlError(f"stale branch in control/lcr.json: recorded {checkpoint['branch']}, current {branch}")
    source = checkpoint["source_head"]
    if not git_commit_exists(source):
        raise ControlError("LCR checkpoint source_head does not identify a Git commit")
    if checkpoint["source_tree"] != commit_tree(source):
        raise ControlError("LCR checkpoint source_tree does not match source_head")
    validate_lcr_checkpoint_shape(source, head, cfg)
    for tag, target in lcr["acceptance_tags"].items():
        if tags.get(tag) != target:
            raise ControlError("stale acceptance evidence in control/lcr.json")
    if lcr["receipt_hashes"] != receipts:
        raise ControlError("stale verification receipt hashes in control/lcr.json")

    current_base = accepted_base_record(cfg)
    recorded_base = lcr["accepted_base"]
    if recorded_base != current_base:
        state_commit = latest_generated_state_commit(cfg, head)
        coalesced_acceptance_advance = (
            branch == cfg["acceptance_branch"]
            and state_commit == head
            and recorded_base.get("branch") == cfg["acceptance_branch"]
            and isinstance(recorded_base.get("head"), str)
            and git_commit_exists(recorded_base["head"])
            and recorded_base.get("tree") == commit_tree(recorded_base["head"])
            and is_ancestor(recorded_base["head"], source)
            and generated_only_history(recorded_base["head"], source, LCR_REL)
        )
        if not coalesced_acceptance_advance:
            raise ControlError("stale accepted_base in control/lcr.json")

    expected = build_expected_lcr(
        cfg, tasks, hashes, tags, receipts, source,
        accepted_base_override=recorded_base,
        acceptance_tags_override=lcr["acceptance_tags"],
    )
    if lcr != expected:
        differing = sorted(key for key in LCR_REQUIRED if lcr.get(key) != expected.get(key))
        raise ControlError("derived LCR mismatch: " + ", ".join(differing))


def structural_validation(ignore_handoff_staleness: bool = False) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, str]]:
    cfg, tasks, hashes, tags, receipts = structural_core()
    if state_mode(cfg) == "handoff":
        validate_handoff_state(cfg, tasks, hashes, tags, receipts, ignore_handoff_staleness)
    else:
        validate_lcr_state(cfg, tasks, hashes, tags, receipts, ignore_handoff_staleness)
    return cfg, tasks, hashes


def _source_methodology_identity() -> dict[str, str]:
    if not clean_worktree():
        raise ControlError("instantiate requires a clean methodology repository")
    head, tree, _branch = git_identity()
    return {
        "commit": head,
        "tree": tree,
        "controller_sha256": sha256_file(SCRIPT_PATH),
    }


def _prepare_accepted_brief(source: Path, target_root: Path) -> dict[str, Any]:
    brief_dir = target_root / ".pcm" / "brief"
    brief_dir.mkdir(parents=True, exist_ok=True)
    if source.is_symlink():
        raise ControlError("accepted brief source must not be a symlink")
    if source.is_file():
        suffix = source.suffix if source.suffix else ".bin"
        destination = brief_dir / f"accepted_brief{suffix}"
        destination.write_bytes(source.read_bytes())
        return {
            "kind": "file",
            "stored_path": destination.relative_to(target_root).as_posix(),
            "sha256": sha256_file(destination),
            "source_name": source.name,
            "source_commit": None,
            "source_tree": None,
        }
    if source.is_dir():
        git_root_result = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=False,
        )
        if git_root_result.returncode != 0:
            raise ControlError("accepted brief directory must be a Git repository root")
        brief_root = Path(git_root_result.stdout.strip()).resolve()
        if brief_root != source.resolve():
            raise ControlError("accepted brief directory must identify the Git repository root, not a subdirectory")
        if not external_clean_worktree(brief_root):
            raise ControlError("accepted brief Git repository must be clean")
        head = external_git(brief_root, "rev-parse", "HEAD")
        tree = external_git(brief_root, "rev-parse", "HEAD^{tree}")
        destination = brief_dir / "accepted_brief.tar"
        archive = subprocess.run(
            ["git", "-C", str(brief_root), "archive", "--format=tar", "--output", str(destination), head],
            text=True, capture_output=True, check=False,
        )
        if archive.returncode != 0:
            raise ControlError(f"accepted brief Git archive failed: {archive.stderr.strip()}")
        return {
            "kind": "git_tree_archive",
            "stored_path": destination.relative_to(target_root).as_posix(),
            "sha256": sha256_file(destination),
            "source_name": brief_root.name,
            "source_commit": head,
            "source_tree": tree,
        }
    raise ControlError("accepted brief must be a regular file or a Git repository root")


def _write_instantiation_skeletons(project_root: Path) -> None:
    project_root.mkdir(parents=True, exist_ok=False)
    skeletons = {
        "PROJECT_OBJECTIVE.md": (
            "# Project Objective\n\n<!-- CONTROL:SECTION:PROJECT-OBJECTIVE:START -->\n"
            "{{PROJECT_OBJECTIVE}}\n<!-- CONTROL:SECTION:PROJECT-OBJECTIVE:END -->\n"
        ),
        "REQUIREMENTS.md": (
            "# Requirements\n\n## REQ-001 — Project requirement draft\n\n"
            "**Statement:** {{PROJECT_REQUIREMENT}}\n"
        ),
        "EXEC_PLAN.md": (
            "# Execution Plan\n\n<!-- CONTROL:GLOBAL:START -->\n## Global constraints\n\n"
            "- {{GLOBAL_CONSTRAINT}}\n<!-- CONTROL:GLOBAL:END -->\n\n"
            "<!-- CONTROL:TASK:PCM-I01:START -->\n"
            "## PCM-I01 — Project authority instantiation draft\n\n"
            "**Requirements:** REQ-001\n\n"
            "**Objective:** {{PROJECT_INSTANTIATION_OBJECTIVE}}\n"
            "<!-- CONTROL:TASK:PCM-I01:END -->\n"
        ),
    }
    for rel, content in skeletons.items():
        path = project_root / rel
        if path.exists() or path.is_symlink():
            raise ControlError(f"instantiate will not overwrite PCM project authority file {path.relative_to(ROOT)}")
        path.write_text(content, encoding="utf-8")


def _native_authority_identity(target: Path, source_commit: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for rel in NATIVE_AUTHORITY_CANDIDATES:
        path = target / rel
        if not path.exists() and not path.is_symlink():
            continue
        if path.is_symlink() or not path.is_file():
            raise ControlError(f"native authority must be a regular file: {rel}")
        tree = external_git_result(target, "ls-tree", source_commit, "--", rel)
        lines = [line for line in tree.stdout.splitlines() if line.strip()]
        if tree.returncode != 0 or len(lines) != 1 or "\t" not in lines[0]:
            raise ControlError(f"native authority is not uniquely tracked at target source commit: {rel}")
        meta, shown_rel = lines[0].split("\t", 1)
        parts = meta.split()
        if len(parts) != 3 or parts[1] != "blob" or parts[0] == "120000" or shown_rel != rel:
            raise ControlError(f"native authority must be a regular Git file at target source commit: {rel}")
        raw = subprocess.run(
            ["git", "-C", str(target), "show", f"{source_commit}:{rel}"],
            capture_output=True, check=False,
        )
        if raw.returncode != 0:
            raise ControlError(f"cannot read native authority at target source commit: {rel}")
        current = path.read_bytes()
        if current != raw.stdout:
            raise ControlError(f"native authority working bytes differ from clean target source commit: {rel}")
        records.append({"path": rel, "sha256": sha256_bytes(raw.stdout), "blob": parts[2]})
    return records


def command_instantiate(args: argparse.Namespace) -> int:
    target: Path | None = None
    try:
        source_cfg, _source_tasks, _source_hashes = structural_validation()
        methodology = _source_methodology_identity()
        target = Path(args.target_repo).expanduser().resolve()
        brief_source = Path(args.accepted_brief).expanduser().resolve()
        if target == ROOT.resolve():
            raise ControlError("target repository must be different from the methodology repository")
        if not target.is_dir() or external_git_result(target, "rev-parse", "--show-toplevel").returncode != 0:
            raise ControlError("target-repo must be an existing Git repository root")
        if Path(external_git(target, "rev-parse", "--show-toplevel")).resolve() != target:
            raise ControlError("target-repo must identify the Git repository root")
        if not external_clean_worktree(target):
            raise ControlError("target repository must be clean before instantiation")
        branch = external_git(target, "branch", "--show-current")
        if not branch:
            raise ControlError("target repository must be on an attached branch")
        target_source_head = external_git(target, "rev-parse", "HEAD")
        target_source_tree = external_git(target, "rev-parse", "HEAD^{tree}")
        if (target / ".pcm").exists():
            raise ControlError("target repository already contains .pcm; refusing to overwrite an existing instantiation")

        native_authority = _native_authority_identity(target, target_source_head)
        pcm_home = target / ".pcm"
        (pcm_home / "control").mkdir(parents=True, exist_ok=False)
        project_root = pcm_home / "project"
        _write_instantiation_skeletons(project_root)
        shutil.copy2(SCRIPT_PATH, pcm_home / "projectctl.py")
        for rel in ("AGENTS.md", "GUARDRAILS.md", "CODING_PROGRAMME.md", "CHATGPT_PROJECT_INSTRUCTIONS.md"):
            source_path = ROOT / rel
            if not source_path.is_file():
                raise ControlError(f"methodology source is missing required installation file {rel}")
            shutil.copy2(source_path, pcm_home / rel)

        brief_identity = _prepare_accepted_brief(brief_source, target)
        project_authority = [
            ".pcm/project/PROJECT_OBJECTIVE.md", ".pcm/project/REQUIREMENTS.md",
            ".pcm/project/EXEC_PLAN.md",
        ]
        native_authority_paths = [item["path"] for item in native_authority]
        authority_files = native_authority_paths + project_authority + [
            ".pcm/GUARDRAILS.md", ".pcm/AGENTS.md", ".pcm/CODING_PROGRAMME.md",
            ".pcm/CHATGPT_PROJECT_INSTRUCTIONS.md", ".pcm/control/delegation.json",
            ".pcm/control/instantiation.json",
        ]
        context_universal = [".pcm/GUARDRAILS.md", ".pcm/AGENTS.md"]
        context_universal.extend(rel for rel in ("GUARDRAILS.md", "AGENTS.md") if rel in native_authority_paths)
        target_cfg = {
            "schema_version": 1,
            "template_mode": True,
            "instantiation_required": True,
            "test_first_policy": "required",
            "project_name": "{{PROJECT_NAME}}",
            "authority_files": authority_files,
            "project_authority_files": project_authority,
            "project_objective_path": ".pcm/project/PROJECT_OBJECTIVE.md",
            "requirements_path": ".pcm/project/REQUIREMENTS.md",
            "execution_plan_path": ".pcm/project/EXEC_PLAN.md",
            "generated_state_paths": [".pcm/control/lcr.json"],
            "acceptance_branch": branch,
            "context_max_bytes": source_cfg["context_max_bytes"],
            "context_universal_files": context_universal,
            "runtime_budget_minutes": source_cfg["runtime_budget_minutes"],
            "durability_flush_margin_minutes": source_cfg["durability_flush_margin_minutes"],
        }
        write_json(pcm_home / "control" / "project.json", target_cfg)
        write_json(pcm_home / "control" / "claims.json", {"schema_version": 1, "claims": []})
        write_json(
            pcm_home / "control" / "delegation.json",
            {"schema_version": 1, "leaf_actor_class": {"PCM-I01": "AUTONOMOUS"}},
        )
        template_tasks = {
            "schema_version": 1,
            "tasks": [{
                "id": "PCM-I01",
                "title": "Project authority instantiation draft",
                "requirements": ["REQ-001"],
                "depends_on": [],
                "write_paths": [
                    ".pcm/project/PROJECT_OBJECTIVE.md", ".pcm/project/REQUIREMENTS.md",
                    ".pcm/project/EXEC_PLAN.md",
                    ".pcm/control/tasks.json", ".pcm/control/delegation.json",
                ],
                "status": "pending",
                "acceptance": ["{{PROJECT_INSTANTIATION_ACCEPTANCE}}"],
                "verification": {"leaf_close": [], "promotion": []},
                "work_type": "non_code",
            }],
        }
        write_json(pcm_home / "control" / "tasks.json", template_tasks)
        instantiation = {
            "schema_version": 1,
            "status": "draft",
            "methodology": methodology,
            "target_source": {
                "commit": target_source_head,
                "tree": target_source_tree,
                "branch": branch,
            },
            "accepted_brief": brief_identity,
            "native_authority": native_authority,
            "approval": None,
        }
        write_json(pcm_home / "control" / "instantiation.json", instantiation)

        initial_lcr = {
            "schema_version": 1,
            "generated_at": external_git(target, "show", "-s", "--format=%cI", target_source_head),
            "active_leaf": {"id": "PCM-I01", "label": "Project authority instantiation draft", "status": "pending"},
            "authority_hashes": {},
            "repo_fingerprint": "",
            "task_contract_hash": sha256_file(pcm_home / "control" / "tasks.json"),
            "claims_hash": sha256_file(pcm_home / "control" / "claims.json"),
            "checkpoint": {
                "source_head": target_source_head,
                "source_tree": target_source_tree,
                "branch": branch,
                "working_state_digest": sha256_bytes(b""),
            },
            "accepted_base": {"branch": branch, "head": target_source_head, "tree": target_source_tree},
            "ready_tasks": ["PCM-I01"],
            "unresolved_claims": [],
            "blockers": [],
            "last_receipt": None,
            "acceptance_tags": {},
            "receipt_hashes": {},
            "applicable_context": {
                "authority_files": context_universal,
                "requirements": ["REQ-001"],
                "plan_leaf": "PCM-I01",
                "ancestors": [],
                "dependencies": [],
            },
            "next_transition": {"actor_class": "AUTONOMOUS", "next_leaf": "PCM-I01"},
            "migration_provenance": None,
        }
        write_json(pcm_home / "control" / "lcr.json", initial_lcr)

        external_git(target, "add", "--", ".pcm")
        commit = external_git_result(
            target, "-c", "user.name=PCM Bootstrap", "-c", "user.email=pcm@local.invalid",
            "commit", "-m", "chore: instantiate PCM control substrate",
        )
        if commit.returncode != 0:
            raise ControlError(f"PCM instantiation commit failed: {commit.stderr.strip()}")
        install_head = external_git(target, "rev-parse", "HEAD")
        if not external_clean_worktree(target):
            raise ControlError("instantiation did not leave target repository clean")
        target_check = subprocess.run(
            [sys.executable, str(pcm_home / "projectctl.py"), "check"],
            cwd=target, text=True, capture_output=True, check=False,
        )
        if target_check.returncode != 0:
            raise ControlError(f"instantiated target failed check: {target_check.stdout.strip()} {target_check.stderr.strip()}")
        print("INSTANTIATE: PASS")
        print(f"METHODOLOGY_COMMIT: {methodology['commit']}")
        print(f"METHODOLOGY_TREE: {methodology['tree']}")
        print(f"TARGET_SOURCE_COMMIT: {target_source_head}")
        print(f"TARGET_SOURCE_TREE: {target_source_tree}")
        print(f"ACCEPTED_BRIEF_SHA256: {brief_identity['sha256']}")
        print(f"INSTALLATION_COMMIT: {install_head}")
        print(f"TEMPLATE_CHECKPOINT: {install_head}")
        print("NEXT: draft project authority, commit it, then run .pcm/projectctl.py finalize-instantiation under PROGRAMME_OWNER")
        return 0
    except (ControlError, OSError) as exc:
        print(f"INSTANTIATE: FAIL\nERROR: {exc}")
        return 1


def _finalize_checkpoint_args() -> argparse.Namespace:
    return argparse.Namespace(
        bootstrap_lcr=False,
        admit_branch_change=False,
        admit_authority_change=True,
        admit_contract_change=True,
        admit_acceptance_change=True,
        admit_receipts=False,
        admit_claims_change=True,
        admit_independent_review_result=False,
        admit_programme_owner_decision=False,
        admit_work=False,
        admit_control_change=True,
        admit_delegation_change=True,
        actor_class="PROGRAMME_OWNER",
    )


def command_finalize_instantiation(args: argparse.Namespace) -> int:
    try:
        if args.actor_class != "PROGRAMME_OWNER":
            raise ControlError("finalize-instantiation requires actor class PROGRAMME_OWNER")
        note = args.note.strip()
        if not note:
            raise ControlError("finalize-instantiation requires a non-empty programme-owner note")
        if PCM_HOME == ROOT:
            raise ControlError("finalize-instantiation is available only inside an installed consuming project")
        if not clean_worktree():
            raise ControlError("finalize-instantiation requires all draft authority changes to be committed first")
        cfg, tasks, _hashes, _tags, _receipts = structural_core()
        if not cfg.get("instantiation_required", False) or not cfg.get("template_mode", False):
            raise ControlError("project is not awaiting consuming-project instantiation approval")
        if cfg.get("test_first_policy") != "required":
            raise ControlError("consuming-project finalization requires test_first_policy=required")
        record = load_json(INSTANTIATION_JSON)
        if record.get("status") != "draft":
            raise ControlError("instantiation record is not in draft state")
        unresolved: list[str] = []
        for path in governance_paths(cfg):
            match = PLACEHOLDER_RE.search(read_text(path))
            if match:
                unresolved.append(f"{path.relative_to(ROOT)}:{match.group(0)}")
        if unresolved:
            raise ControlError(f"instantiation authority still contains unresolved placeholder {unresolved[0]}")
        if any(task["id"] == "PCM-I01" for task in tasks):
            raise ControlError("replace the PCM-I01 template task with the admitted project task graph before finalization")

        cfg["template_mode"] = False
        PROJECT_JSON.write_text(json.dumps(cfg, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        record["status"] = "approved"
        record["approval"] = {
            "actor_class": "PROGRAMME_OWNER",
            "note": note,
            "approved_at": datetime.now(timezone.utc).isoformat(),
        }
        INSTANTIATION_JSON.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        # Validate the completed authority envelope, then coalesce its generated
        # LCR projection into the same approval commit rather than creating a
        # second generated-state-only checkpoint commit.
        structural_core()
        run_git("add", "--", PROJECT_REL, INSTANTIATION_REL)
        if command_checkpoint(_finalize_checkpoint_args()) != 0:
            raise ControlError("programme-owner instantiation admission checkpoint failed")
        commit = git_result(
            "-c", "user.name=PCM Programme Owner", "-c", "user.email=pcm@local.invalid",
            "commit", "-m", "governance: approve PCM project instantiation",
        )
        if commit.returncode != 0:
            raise ControlError(f"instantiation approval commit failed: {commit.stderr.strip()}")
        approval_commit = run_git("rev-parse", "HEAD")
        structural_validation()
        if not clean_worktree():
            raise ControlError("finalize-instantiation did not leave a clean working tree")
        print("FINALIZE_INSTANTIATION: PASS")
        print(f"APPROVAL_COMMIT: {approval_commit}")
        print(f"CHECKPOINT_COMMIT: {approval_commit}")
        print(f"READY: {','.join(ready_tasks(load_tasks())) or '<none>'}")
        return 0
    except (ControlError, OSError) as exc:
        print(f"FINALIZE_INSTANTIATION: FAIL\nERROR: {exc}")
        return 1


def command_check(_: argparse.Namespace) -> int:
    try:
        cfg, tasks, hashes = structural_validation()
        print("CHECK: PASS")
        print(f"authority_files={len(hashes)}")
        print(f"tasks={len(tasks)}")
        print(f"ready={','.join(ready_tasks(tasks)) or '<none>'}")
        print(f"task_contract_hash={task_contract_hash()}")
        print(f"repo_fingerprint={repo_fingerprint(cfg)}")
        print("mode=template (placeholders permitted)" if cfg.get("template_mode") else "mode=project")
        return 0
    except ControlError as exc:
        print(f"CHECK: FAIL\nERROR: {exc}")
        return 1


def command_ready(_: argparse.Namespace) -> int:
    try:
        cfg, tasks, _hashes = structural_validation()
        require_project_mode(cfg, "ready")
        values = ready_tasks(tasks)
        print("\n".join(values) if values else "<none>")
        return 0
    except ControlError as exc:
        print(f"READY: FAIL\nERROR: {exc}")
        return 1


def command_migrate_lcr(_: argparse.Namespace) -> int:
    try:
        if not clean_worktree():
            raise ControlError("LCR migration requires a clean working tree")
        cfg, _tasks, _hashes = structural_validation()
        if state_mode(cfg) != "handoff":
            raise ControlError("migrate-lcr requires a valid legacy handoff configuration")
        if LCR_JSON.exists():
            raise ControlError("control/lcr.json already exists")
        handoff = load_json(HANDOFF_JSON)
        head, _tree, _branch = git_identity()
        cfg["generated_state_paths"] = [LCR_REL]
        cfg["lcr_migration"] = {
            "legacy_state_commit": head,
            "legacy_handoff_sha256": sha256_file(HANDOFF_JSON),
            "legacy_source_head": handoff["source_head"],
            "legacy_source_tree": handoff["source_tree"],
        }
        PROJECT_JSON.write_text(json.dumps(cfg, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        HANDOFF_JSON.unlink()
        print("MIGRATE-LCR: PREPARED")
        print(f"legacy_state_commit={head}")
        print("next=commit migration, then run checkpoint --bootstrap-lcr")
        return 0
    except ControlError as exc:
        print(f"MIGRATE-LCR: FAIL\nERROR: {exc}")
        return 1


def command_checkpoint(args: argparse.Namespace) -> int:
    try:
        cfg_preview = config()
        mode = state_mode(cfg_preview)
        staged = staged_paths()
        unstaged = unstaged_or_untracked_paths()
        coalesced_lcr = mode == "lcr" and bool(staged)
        cfg, tasks, hashes, tags, receipts = structural_core(
            allow_pending_acceptance=coalesced_lcr and TASKS_REL in staged,
        )
        state_path = generated_state_file(cfg)
        if coalesced_lcr:
            if generated_state_rel(cfg) in staged or generated_state_rel(cfg) in unstaged:
                raise ControlError("coalesced checkpoint requires the generated LCR to be unchanged before admission")
            if unstaged:
                raise ControlError(
                    "coalesced checkpoint requires all intended non-LCR changes to be staged; "
                    f"unstaged/untracked: {', '.join(unstaged)}"
                )
        elif not clean_worktree():
            raise ControlError(
                "checkpoint requires either a clean working tree (legacy post-commit admission) or, in LCR mode, "
                "fully staged intended changes with no unstaged/untracked files"
            )
        bootstrap_lcr = mode == "lcr" and not state_path.exists()
        if bootstrap_lcr and not args.bootstrap_lcr:
            raise ControlError("control/lcr.json is missing; explicit --bootstrap-lcr required after migration")
        if args.bootstrap_lcr and not bootstrap_lcr:
            raise ControlError("--bootstrap-lcr is allowed only when LCR mode is configured and control/lcr.json is absent")
        if mode == "lcr":
            verify_lcr_migration_provenance(cfg)
        state = {} if bootstrap_lcr else load_json(state_path)
        if state:
            if mode == "handoff":
                validate_handoff_schema(state)
            else:
                validate_lcr_schema(state, allow_legacy_context_shape=True)
        head, _tree, branch = git_identity()
        old_branch = state_branch(state, cfg) if state else None
        if old_branch and old_branch != branch and not args.admit_branch_change:
            raise ControlError(f"branch changed from {old_branch} to {branch}; explicit --admit-branch-change required")
        if state:
            validate_checkpoint_history(cfg, tasks, state, head, args)
            if coalesced_lcr:
                validate_admitted_paths(cfg, tasks, state, staged, args, context="staged transition")
            validate_admitted_task_semantics(state, cfg, tasks, args.actor_class)

        if mode == "handoff":
            old_hashes = state.get("authority_hashes") if isinstance(state.get("authority_hashes"), dict) else {}
            old_contract = state.get("task_contract_hash")
            old_claims = state.get("claims_hash")
            old_tags = state.get("acceptance_tags") if isinstance(state.get("acceptance_tags"), dict) else {}
            old_receipts = state.get("receipt_hashes") if isinstance(state.get("receipt_hashes"), dict) else {}
            old_base = None
        else:
            old_hashes = state.get("authority_hashes") if isinstance(state.get("authority_hashes"), dict) else {}
            old_contract = state.get("task_contract_hash")
            old_claims = state.get("claims_hash")
            old_tags = state.get("acceptance_tags") if isinstance(state.get("acceptance_tags"), dict) else {}
            old_receipts = state.get("receipt_hashes") if isinstance(state.get("receipt_hashes"), dict) else {}
            old_base = state.get("accepted_base") if isinstance(state.get("accepted_base"), dict) else None

        old_delegation = old_hashes.get(DELEGATION_REL) if old_hashes else None
        new_delegation = hashes.get(DELEGATION_REL)
        if old_hashes and old_delegation != new_delegation:
            if not args.admit_delegation_change:
                raise ControlError("delegation policy changed; --admit-delegation-change required")
            bounded_refinement = bool(state and bounded_refinement_delegation_transition(
                (latest_generated_state_commit(cfg, head) if mode == "lcr" else state_source_head(state, cfg)) or head,
                tasks,
                load_delegation(tasks, cfg),
            ))
            if args.actor_class != "PROGRAMME_OWNER" and not bounded_refinement:
                raise ControlError(
                    "delegation policy change requires actor class PROGRAMME_OWNER unless it only adds "
                    "same-actor bounded refinement tasks"
                )
        if old_hashes and old_hashes != hashes and not args.admit_authority_change and not args.admit_contract_change:
            raise ControlError("authority hashes changed; explicit admission required")
        if old_contract and old_contract != task_contract_hash() and not args.admit_contract_change:
            raise ControlError("task contract changed; --admit-contract-change required")
        current_claims = claims_hash()
        if old_claims and old_claims != current_claims and not args.admit_claims_change:
            raise ControlError("claims state changed; --admit-claims-change required")
        changed_existing_tags = any(tags.get(tag) != target for tag, target in old_tags.items())
        if changed_existing_tags and not args.admit_acceptance_change:
            raise ControlError("acceptance tag targets changed; --admit-acceptance-change required")
        for rel, digest in old_receipts.items():
            if receipts.get(rel) != digest:
                raise ControlError(f"verification receipt is append-only and changed or disappeared: {rel}")
        if set(receipts) - set(old_receipts) and not args.admit_receipts:
            raise ControlError("new verification receipts require --admit-receipts")
        if mode == "lcr" and old_base and old_base != accepted_base_record(cfg):
            state_commit = latest_generated_state_commit(cfg, head)
            tolerated_coalesced_advance = (
                branch == cfg["acceptance_branch"]
                and state_commit == head
                and old_base.get("branch") == cfg["acceptance_branch"]
                and isinstance(old_base.get("head"), str)
                and state_source_head(state, cfg) is not None
                and is_ancestor(old_base["head"], state_source_head(state, cfg))
                and generated_only_history(old_base["head"], state_source_head(state, cfg), LCR_REL)
            )
            if not tolerated_coalesced_advance and not args.admit_acceptance_change:
                raise ControlError("accepted base changed; --admit-acceptance-change required")

        source_head = head if coalesced_lcr else derived_checkpoint_source_head(head, generated_state_rel(cfg))
        if mode == "handoff":
            updated = build_expected_handoff(cfg, tasks, hashes, tags, receipts, source_head)
            active = updated["active_task"]
        else:
            updated = build_expected_lcr(
                cfg, tasks, hashes, tags, receipts, source_head,
                working_state_digest_override=(clean_working_state_digest() if coalesced_lcr else None),
            )
            active = updated["active_leaf"]["id"] if updated["active_leaf"] else None
        state_path.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if coalesced_lcr:
            run_git("add", "--", generated_state_rel(cfg))
        print("CHECKPOINT: PASS")
        if coalesced_lcr:
            print("commit_mode=coalesced (commit staged transition and generated LCR together)")
        print(f"active_leaf={active or '<none>'}")
        print(f"repo_fingerprint={updated['repo_fingerprint']}")
        return 0
    except ControlError as exc:
        print(f"CHECKPOINT: FAIL\nERROR: {exc}")
        return 1


def extract_requirement_sections(required_ids: list[str]) -> str:
    cfg = config()
    return _requirement_sections_from_text(read_text(ROOT / cfg["requirements_path"]), required_ids)


def render_universal_authority(cfg: dict[str, Any]) -> str:
    parts: list[str] = []
    for rel in cfg["context_universal_files"]:
        parts.extend([f"### {rel}", read_text(ROOT / rel).strip()])
    return "\n\n".join(parts) if parts else "(none)"


def render_authority_sections(refs: list[str], cfg: dict[str, Any]) -> str:
    parts: list[str] = []
    cache: dict[str, dict[str, str]] = {}
    for ref in refs:
        rel, section_id = parse_context_ref(ref, cfg)
        if rel not in cache:
            cache[rel] = parse_authority_sections(rel)
        section = cache[rel].get(section_id)
        if section is None:
            raise ControlError(f"missing referenced authority section {rel}#{section_id}")
        parts.extend([f"### {ref}", section])
    return "\n\n".join(parts) if parts else "(none)"


def render_plan_leaves(task_ids: list[str], plan_blocks: dict[str, str]) -> str:
    if not task_ids:
        return "(none)"
    return "\n\n".join(plan_blocks[task_id] for task_id in task_ids)


def render_dependency_leaves(dependency_ids: list[str], plan_blocks: dict[str, str]) -> str:
    return render_plan_leaves(dependency_ids, plan_blocks)


def render_unresolved_claims() -> str:
    claims = [claim for claim in load_claims() if claim["status"] != "VERIFIED"]
    if not claims:
        return "(none)"
    parts: list[str] = []
    for claim in claims:
        evidence = ", ".join(claim["evidence"]) if claim["evidence"] else "(none)"
        parts.extend([
            f"### {claim['id']} — {claim['status']}",
            claim["statement"],
            f"Evidence: {evidence}",
        ])
    return "\n\n".join(parts)


def semantic_record_bytes(record: dict[str, Any]) -> tuple[bytes, str]:
    admitted = record["admitted_task_id"]
    if admitted is None:
        path = ROOT / record["path"]
        if path.is_symlink() or not path.is_file():
            raise ControlError(f"semantic context source is unavailable: {record['path']}")
        data = path.read_bytes()
        source = "current-worktree"
    else:
        tag = f"accepted/{admitted}"
        commit = run_git("rev-parse", f"refs/tags/{tag}^{{commit}}")
        data = git_file_bytes(commit, record["path"])
        source = f"{tag}@{commit}"
    observed = sha256_bytes(data)
    if observed != record["sha256"]:
        raise ControlError(
            f"semantic context source hash drift for {record['id']}: "
            f"expected {record['sha256']} observed {observed}"
        )
    return data, source


def render_semantic_record(record: dict[str, Any]) -> str:
    data, source = semantic_record_bytes(record)
    try:
        content = data.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        content = base64.b64encode(data).decode("ascii")
        encoding = "base64"
    return "\n".join([
        f"### {record['id']}",
        f"PATH: {record['path']}",
        f"SOURCE: {source}",
        f"SHA256: {record['sha256']}",
        f"ENCODING: {encoding}",
        "CONTENT:",
        content,
    ])


def render_semantic_routes(task: dict[str, Any]) -> str:
    routes = task.get("semantic_routes")
    if routes is None:
        return "(legacy dependency-context task)"
    if not routes:
        return "(none)"
    parts: list[str] = []
    for route in routes:
        parts.extend([
            f"## Route {route['id']}",
            f"MODE: {route['route_mode']}",
            f"OWNER: {route['owner_record']['id']} ({route['owner_record']['path']})",
        ])
        if route["conditional_triggers"]:
            parts.append("TRIGGERS:")
            for trigger in route["conditional_triggers"]:
                state = "TRIGGERED" if trigger["triggered"] else "SUPPRESSED"
                parts.append(f"- {trigger['id']}: {state} — {trigger['reason']}")
        if route["exclusions"]:
            parts.append("EXCLUSIONS:")
            for exclusion in route["exclusions"]:
                record = exclusion["record"]
                parts.append(f"- {record['id']} ({record['path']}): {exclusion['reason']}")

        selected: list[dict[str, Any]] = []
        if route["route_mode"] == "CHANGE_MEANING":
            selected.append(route["owner_record"])
            selected.extend(route["complete_records"])
            selected.extend(route["bounded_records"])
        else:
            selected.extend(route["bounded_records"])

        # Triggered dependencies are required semantic input. Validation guarantees
        # they are already represented in the active record set, but include them
        # defensively and deduplicate by durable source identity.
        selected.extend(
            trigger["record"] for trigger in route["conditional_triggers"] if trigger["triggered"]
        )
        seen: set[tuple[str, str, str | None]] = set()
        rendered: list[str] = []
        for record in selected:
            key = _route_record_key(record)
            if key in seen:
                continue
            seen.add(key)
            rendered.append(render_semantic_record(record))
        parts.append("ROUTE MATERIAL:")
        parts.append("\n\n".join(rendered) if rendered else "(none)")
    return "\n\n".join(parts)



def render_refinement(task: dict[str, Any]) -> str:
    refinement = task.get("refinement")
    if refinement is None:
        return "(none)"
    prior = refinement["prior_repair_task_ids"]
    recurrence = "INDEPENDENT_REVIEW_REQUIRED" if prior else "FIRST_OCCURRENCE"
    return "\n".join([
        f"ENVELOPE_TASK: {refinement['envelope_task_id']}",
        f"MECHANISM_ID: {refinement['mechanism_id']}",
        "FRESH_REVIEW_REQUIRED: true",
        f"RECURRENCE_CLASSIFICATION: {recurrence}",
        f"PRIOR_REPAIR_TASKS: {', '.join(prior) if prior else '(none)'}",
    ])


def packet_fallback_status(
    *, kind: str, task_id: str, required_bytes: int, max_bytes: int, next_action: str
) -> str:
    return "\n".join([
        f"{kind}: FALLBACK_REQUIRED",
        f"TASK: {task_id}",
        f"OMITTED_PACKET: {kind.lower()}:{task_id}",
        f"REQUIRED_BYTES: {required_bytes}",
        f"BUDGET_BYTES: {max_bytes}",
        f"REQUIRED_NEXT_ACTION: {next_action}",
        "PARTIAL_PACKET_VALID: false",
    ]) + "\n"


def command_context(_: argparse.Namespace) -> int:
    try:
        cfg, tasks, hashes = structural_validation()
        require_project_mode(cfg, "context")
        active = derived_active_task(tasks)
        if not active:
            raise ControlError("no uniquely derived active task; commit exactly one in_progress task or reduce the ready frontier to one task")
        by_id = {task["id"]: task for task in tasks}; task = by_id[active]
        actor_class = load_delegation(tasks, cfg)[active]
        if actor_class == "INDEPENDENT_REVIEW":
            raise ControlError(f"leaf {active} requires actor class INDEPENDENT_REVIEW; fresh independent reviewer context required")
        if actor_class == "PROGRAMME_OWNER":
            raise ControlError(f"leaf {active} requires actor class PROGRAMME_OWNER; autonomous worker must stop")
        global_block, plan_blocks = parse_plan()
        scope = bounded_context_scope(cfg, tasks, active)
        req_text = extract_requirement_sections(scope["requirements"])
        universal_text = render_universal_authority(cfg)
        section_refs = [ref for ref in scope["authority_files"] if "#" in ref]
        section_text = render_authority_sections(section_refs, cfg)
        claim_text = render_unresolved_claims()
        blockers = blocked_claim_ids()
        head, tree, branch = git_identity()
        if actor_class == "AUTONOMOUS" and branch == cfg["acceptance_branch"]:
            raise ControlError(
                f"leaf {active} delegated AUTONOMOUS may not obtain executable context on acceptance branch {branch}; "
                "switch to a non-acceptance work branch and admit the branch change first"
            )

        common = [
            "# VERIFIED CURRENT-WORK PROJECTION", "", "Generated context. Not governing authority.",
            f"SOURCE_HEAD: {head}", f"SOURCE_TREE: {tree}", f"BRANCH: {branch}",
            f"REPO_FINGERPRINT: {repo_fingerprint(cfg)}", f"EXEC_PLAN_SHA256: {hashes[cfg['execution_plan_path']]}",
            f"TASK_CONTRACT_SHA256: {task_contract_hash()}", f"ACTIVE_TASK: {active}", f"ACTOR_CLASS: {actor_class}", "",
            "## Universal authority files", universal_text, "",
            "## Applicable authority sections", section_text, "",
            "## Relevant requirements", req_text, "", "## Global execution constraints", global_block, "",
        ]
        if "semantic_routes" in task:
            packet_parts = common + [
                "## Required semantic route material", render_semantic_routes(task), "",
                "## Refinement envelope", render_refinement(task), "",
                f"## Active plan leaf — {active}", plan_blocks[active],
            ]
        else:
            ancestor_text = render_plan_leaves(scope["ancestors"], plan_blocks)
            dependency_text = render_dependency_leaves(scope["dependencies"], plan_blocks)
            packet_parts = common + [
                "## Required execution ancestors", ancestor_text, "",
                "## Required dependency leaves", dependency_text, "",
                f"## Active plan leaf — {active}", plan_blocks[active],
            ]
        packet_parts += [
            "", "## Current claims and blockers", claim_text,
            f"BLOCKERS: {', '.join(blockers) if blockers else '(none)'}",
            "", "## Actor transition", f"NEXT_LEAF: {active}", f"ACTOR_CLASS: {actor_class}",
        ]
        packet = "\n".join(packet_parts) + "\n"
        required_bytes = len(packet.encode("utf-8"))
        if required_bytes > cfg["context_max_bytes"]:
            print(packet_fallback_status(
                kind="CONTEXT", task_id=active, required_bytes=required_bytes,
                max_bytes=cfg["context_max_bytes"],
                next_action=(
                    "use a full-material handoff or programme-owner-approved larger context budget; "
                    "do not continue from a partial projection"
                ),
            ), end="")
            return 1
        print(packet, end=""); return 0
    except ControlError as exc:
        print(f"CONTEXT: FAIL\nERROR: {exc}"); return 1


def session_state_path() -> Path:
    raw = run_git("rev-parse", "--path-format=absolute", "--git-path", "projectctl/session.json")
    if not raw:
        raise ControlError("could not resolve Git metadata session-state path")
    return Path(raw)


def command_session_start(_: argparse.Namespace) -> int:
    try:
        cfg, _tasks, _hashes = structural_validation()
        require_project_mode(cfg, "session-start")
        head, _tree, branch = git_identity()
        now = datetime.now(timezone.utc)
        state = {
            "schema_version": 1,
            "started_at": now.isoformat(),
            "branch": branch,
            "source_head": head,
            "actor_instance_id": secrets.token_hex(16),
        }
        path = session_state_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("SESSION_START: PASS")
        print(f"STARTED_AT: {state['started_at']}")
        print(f"RUNTIME_BUDGET_MINUTES: {cfg['runtime_budget_minutes']}")
        print(f"DURABILITY_FLUSH_MARGIN_MINUTES: {cfg['durability_flush_margin_minutes']}")
        print(f"ACTOR_INSTANCE_ID: {state['actor_instance_id']}")
        return 0
    except ControlError as exc:
        print(f"SESSION_START: FAIL\nERROR: {exc}")
        return 1


def command_session_status(_: argparse.Namespace) -> int:
    try:
        cfg, _tasks, _hashes = structural_validation()
        require_project_mode(cfg, "session-status")
        path = session_state_path()
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ControlError("session state is missing; run session-start first") from exc
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ControlError("session state is unreadable or invalid") from exc
        if not isinstance(state, dict) or state.get("schema_version") != 1:
            raise ControlError("session state has unsupported schema")
        started_at = state.get("started_at")
        if not isinstance(started_at, str) or not started_at:
            raise ControlError("session state has no valid started_at timestamp")
        try:
            started = datetime.fromisoformat(started_at)
        except ValueError as exc:
            raise ControlError("session state started_at is not a valid ISO-8601 timestamp") from exc
        if started.tzinfo is None or started.utcoffset() is None:
            raise ControlError("session state started_at must be timezone-aware")
        elapsed_seconds = (datetime.now(timezone.utc) - started.astimezone(timezone.utc)).total_seconds()
        if elapsed_seconds < -1:
            raise ControlError("session state started_at is in the future")
        elapsed_minutes = max(0.0, elapsed_seconds / 60.0)
        flush_at = cfg["runtime_budget_minutes"] - cfg["durability_flush_margin_minutes"]
        recommended = elapsed_minutes >= flush_at
        status = "FLUSH_WINDOW" if recommended else "RUNNING"
        if elapsed_minutes >= cfg["runtime_budget_minutes"]:
            status = "BUDGET_EXCEEDED"
        print(f"SESSION_STATUS: {status}")
        print(f"STARTED_AT: {started.astimezone(timezone.utc).isoformat()}")
        print(f"ELAPSED_MINUTES: {elapsed_minutes:.2f}")
        print(f"RUNTIME_BUDGET_MINUTES: {cfg['runtime_budget_minutes']}")
        print(f"DURABILITY_FLUSH_MARGIN_MINUTES: {cfg['durability_flush_margin_minutes']}")
        print(f"FLUSH_RECOMMENDED: {'yes' if recommended else 'no'}")
        return 0
    except ControlError as exc:
        print(f"SESSION_STATUS: FAIL\nERROR: {exc}")
        return 1


def current_actor_instance_id() -> str:
    path = session_state_path()
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ControlError("session state is missing; run session-start first") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ControlError("session state is unreadable or invalid; run session-start again") from exc
    actor = state.get("actor_instance_id") if isinstance(state, dict) else None
    if not isinstance(actor, str) or not re.fullmatch(r"[0-9a-f]{32}", actor):
        raise ControlError("session has no valid actor instance id; run session-start again")
    head, _tree, branch = git_identity()
    if state.get("source_head") != head or state.get("branch") != branch:
        raise ControlError("session actor instance is stale for current Git identity; run session-start again")
    return actor


def external_json_output_path(raw: str | None, label: str) -> Path:
    if not raw:
        raise ControlError(f"{label} requires --output")
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    else:
        candidate = candidate.resolve()
    if path_is_within(candidate, ROOT.resolve()):
        raise ControlError(f"{label} output must be outside the repository working tree")
    if candidate.exists():
        raise ControlError(f"{label} output already exists: {candidate}")
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


def canonical_object_hash(value: dict[str, Any], hash_field: str) -> str:
    payload = dict(value)
    payload.pop(hash_field, None)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256_bytes(encoded)


def programme_owner_artifact_record(rel: str) -> dict[str, Any]:
    safe_rel_path(rel, "programme-owner candidate artifact")
    path = ROOT / rel
    if path.is_symlink() or not path.is_file():
        raise ControlError(f"programme-owner candidate artifact must be a regular file: {rel}")
    tracked = git_result("ls-files", "--error-unmatch", "--", rel)
    if tracked.returncode != 0:
        raise ControlError(f"programme-owner candidate artifact is not tracked by Git: {rel}")
    data = path.read_bytes()
    return {"path": rel, "sha256": sha256_bytes(data), "size_bytes": len(data)}


def programme_owner_unresolved_items() -> list[dict[str, Any]]:
    items = []
    for claim in sorted(load_claims(), key=lambda value: value["id"]):
        if claim["status"] not in {"UNKNOWN", "BLOCKED"}:
            continue
        items.append({
            "id": claim["id"],
            "statement": claim["statement"],
            "status": claim["status"],
            "evidence": claim["evidence"],
        })
    return items


def programme_owner_declared_next(tasks: list[dict[str, Any]], gate_id: str) -> list[dict[str, str]]:
    return [
        {"id": task["id"], "title": task["title"]}
        for task in tasks
        if gate_id in task["depends_on"]
    ]


def validate_programme_owner_packet_shape(packet: dict[str, Any]) -> None:
    required = {
        "schema_version", "kind", "generated_at", "gate", "actor_class",
        "prepared_by_actor_instance_id", "source_identity", "candidate_artifacts",
        "material_decisions", "unresolved_items", "freedoms", "prohibitions",
        "requested_decision", "declared_next", "packet_sha256",
    }
    if not isinstance(packet, dict) or set(packet) != required:
        raise ControlError("programme-owner packet has invalid shape")
    if packet.get("schema_version") != 1 or packet.get("kind") != "programme_owner_review_packet":
        raise ControlError("programme-owner packet has unsupported schema or kind")
    if packet.get("actor_class") != "PROGRAMME_OWNER":
        raise ControlError("programme-owner packet actor class is invalid")
    if packet.get("packet_sha256") != canonical_object_hash(packet, "packet_sha256"):
        raise ControlError("programme-owner packet hash mismatch")


def load_programme_owner_packet(path: Path) -> dict[str, Any]:
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ControlError(f"programme-owner packet is missing: {path}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ControlError(f"programme-owner packet is unreadable or invalid JSON: {path}") from exc
    validate_programme_owner_packet_shape(packet)
    return packet


def validate_programme_owner_packet_against_repo(
    packet: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    cfg, tasks, hashes = structural_validation()
    require_project_mode(cfg, "programme-owner review")
    if not clean_worktree():
        raise ControlError("programme-owner packet validation requires a clean working tree")
    active = derived_active_task(tasks)
    if not active:
        raise ControlError("programme-owner packet validation requires a uniquely derived active task")
    by_id = {task["id"]: task for task in tasks}
    task = by_id[active]
    delegation = load_delegation(tasks, cfg)
    if delegation[active] != "PROGRAMME_OWNER":
        raise ControlError(f"active leaf {active} is not a PROGRAMME_OWNER leaf")
    review = task.get("programme_owner_review")
    if review is None:
        raise ControlError(f"active leaf {active} has no programme_owner_review contract")
    if packet.get("gate") != {"id": task["id"], "title": task["title"]}:
        raise ControlError("programme-owner packet gate identity does not match current contract")
    actor = packet.get("prepared_by_actor_instance_id")
    if not isinstance(actor, str) or not re.fullmatch(r"[0-9a-f]{32}", actor):
        raise ControlError("programme-owner packet preparer actor instance id is invalid")
    identity = packet.get("source_identity")
    required_identity = {
        "head", "tree", "branch", "repo_fingerprint", "task_contract_sha256", "authority_hashes"
    }
    if not isinstance(identity, dict) or set(identity) != required_identity:
        raise ControlError("programme-owner packet source identity has invalid shape")
    head, tree, branch = git_identity()
    expected_identity = {
        "head": head,
        "tree": tree,
        "branch": branch,
        "repo_fingerprint": repo_fingerprint(cfg),
        "task_contract_sha256": task_contract_hash(),
        "authority_hashes": hashes,
    }
    if identity != expected_identity:
        raise ControlError("programme-owner packet source identity does not match current Git and authority hashes")
    expected_candidates = [
        programme_owner_artifact_record(rel) for rel in review["candidate_paths"]
    ]
    if packet.get("candidate_artifacts") != expected_candidates:
        raise ControlError("programme-owner packet candidate artifacts do not match current contract")
    if packet.get("material_decisions") != review["material_decisions"]:
        raise ControlError("programme-owner packet material decisions do not match current contract")
    if packet.get("freedoms") != review["freedoms"]:
        raise ControlError("programme-owner packet freedoms do not match current contract")
    if packet.get("prohibitions") != review["prohibitions"]:
        raise ControlError("programme-owner packet prohibitions do not match current contract")
    if packet.get("requested_decision") != review["requested_decision"]:
        raise ControlError("programme-owner packet requested decision does not match current contract")
    if packet.get("unresolved_items") != programme_owner_unresolved_items():
        raise ControlError("programme-owner packet unresolved items do not match current claims")
    if packet.get("declared_next") != programme_owner_declared_next(tasks, active):
        raise ControlError("programme-owner packet declared next leaves do not match current task graph")
    return task, review


def git_file_bytes(commit: str, rel: str) -> bytes:
    safe_rel_path(rel, "historical Git path")
    result = subprocess.run(
        ["git", "show", f"{commit}:{rel}"], cwd=ROOT, capture_output=True, check=False
    )
    if result.returncode != 0:
        raise ControlError(f"historical Git source is missing {rel} at {commit[:12]}")
    return result.stdout


def load_programme_owner_decisions(
    tasks: list[dict[str, Any]], delegation: dict[str, str]
) -> dict[str, list[dict[str, Any]]]:
    decisions: dict[str, list[dict[str, Any]]] = {}
    if not PROGRAMME_OWNER_DECISIONS_DIR.exists():
        return decisions
    by_id = {task["id"]: task for task in tasks}
    current_head = run_git("rev-parse", "HEAD")
    for path in sorted(PROGRAMME_OWNER_DECISIONS_DIR.glob("*/*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ControlError(f"invalid programme-owner decision record {path.relative_to(ROOT)}") from exc
        required = {
            "schema_version", "kind", "recorded_at", "gate_id", "packet", "decision",
            "note", "recorded_by_actor_instance_id", "decision_sha256",
        }
        if not isinstance(record, dict) or set(record) != required:
            raise ControlError(f"programme-owner decision record has invalid shape: {path.relative_to(ROOT)}")
        if record.get("schema_version") != 1 or record.get("kind") != "programme_owner_decision":
            raise ControlError(f"programme-owner decision record has unsupported schema: {path.relative_to(ROOT)}")
        if record.get("decision") not in {"approve", "reject"}:
            raise ControlError(f"programme-owner decision has invalid decision: {path.relative_to(ROOT)}")
        if not isinstance(record.get("note"), str) or not record["note"].strip():
            raise ControlError(f"programme-owner decision note must be non-empty: {path.relative_to(ROOT)}")
        actor = record.get("recorded_by_actor_instance_id")
        if not isinstance(actor, str) or not re.fullmatch(r"[0-9a-f]{32}", actor):
            raise ControlError(f"programme-owner decision actor instance is invalid: {path.relative_to(ROOT)}")
        if record.get("decision_sha256") != canonical_object_hash(record, "decision_sha256"):
            raise ControlError(f"programme-owner decision hash mismatch: {path.relative_to(ROOT)}")
        packet = record.get("packet")
        validate_programme_owner_packet_shape(packet)
        gate = packet["gate"]
        gate_id = record.get("gate_id")
        if gate_id != gate.get("id") or gate_id not in by_id:
            raise ControlError(f"programme-owner decision gate identity is invalid: {path.relative_to(ROOT)}")
        if path.parent.name != gate_id or path.stem != packet["packet_sha256"]:
            raise ControlError(f"programme-owner decision path does not match its packet identity: {path.relative_to(ROOT)}")
        task = by_id[gate_id]
        if delegation.get(gate_id) != "PROGRAMME_OWNER":
            raise ControlError(f"programme-owner decision references non-PROGRAMME_OWNER leaf {gate_id}")
        review = task.get("programme_owner_review")
        if review is None:
            raise ControlError(f"programme-owner decision references leaf without programme_owner_review: {gate_id}")
        if gate != {"id": task["id"], "title": task["title"]}:
            raise ControlError(f"programme-owner decision gate label differs from current contract: {gate_id}")
        if [item.get("path") for item in packet["candidate_artifacts"]] != review["candidate_paths"]:
            raise ControlError(f"programme-owner decision candidate paths differ from current contract: {gate_id}")
        for field in ("material_decisions", "freedoms", "prohibitions", "requested_decision"):
            if packet.get(field) != review[field]:
                raise ControlError(f"programme-owner decision {field} differs from current contract: {gate_id}")
        if packet.get("declared_next") != programme_owner_declared_next(tasks, gate_id):
            raise ControlError(
                f"programme-owner decision declared next leaves differ from current task graph: {gate_id}"
            )
        identity = packet["source_identity"]
        source_head = identity.get("head") if isinstance(identity, dict) else None
        if not git_commit_exists(source_head):
            raise ControlError(f"programme-owner decision source head is missing: {gate_id}")
        if identity.get("tree") != commit_tree(source_head):
            raise ControlError(f"programme-owner decision source tree mismatch: {gate_id}")
        if not is_ancestor(source_head, current_head):
            raise ControlError(f"programme-owner decision source head is not in current history: {gate_id}")
        source_tasks = git_file_bytes(source_head, TASKS_REL)
        if identity.get("task_contract_sha256") != sha256_bytes(source_tasks):
            raise ControlError(f"programme-owner decision task contract hash mismatch: {gate_id}")
        authority = identity.get("authority_hashes")
        if not isinstance(authority, dict):
            raise ControlError(f"programme-owner decision authority hashes are invalid: {gate_id}")
        for rel, digest in authority.items():
            if sha256_bytes(git_file_bytes(source_head, rel)) != digest:
                raise ControlError(f"programme-owner decision authority hash mismatch for {rel}: {gate_id}")
        for artifact in packet["candidate_artifacts"]:
            if not isinstance(artifact, dict) or set(artifact) != {"path", "sha256", "size_bytes"}:
                raise ControlError(f"programme-owner decision candidate artifact shape is invalid: {gate_id}")
            data = git_file_bytes(source_head, artifact["path"])
            if artifact["sha256"] != sha256_bytes(data) or artifact["size_bytes"] != len(data):
                raise ControlError(f"programme-owner decision candidate artifact hash mismatch: {artifact['path']}")
        decisions.setdefault(gate_id, []).append(record)
    return decisions


def validate_programme_owner_acceptance(
    tasks: list[dict[str, Any]], delegation: dict[str, str], decisions: dict[str, list[dict[str, Any]]]
) -> None:
    for task in tasks:
        if task["status"] != "accepted" or delegation[task["id"]] != "PROGRAMME_OWNER":
            continue
        approved = any(record["decision"] == "approve" for record in decisions.get(task["id"], []))
        if not approved:
            raise ControlError(
                f"accepted PROGRAMME_OWNER leaf {task['id']} requires an approved programme-owner decision"
            )


def load_independent_review_results(
    tasks: list[dict[str, Any]], delegation: dict[str, str]
) -> dict[str, list[dict[str, Any]]]:
    results: dict[str, list[dict[str, Any]]] = {}
    if not INDEPENDENT_REVIEW_RESULTS_DIR.exists():
        return results
    by_id = {task["id"]: task for task in tasks}
    current_head = run_git("rev-parse", "HEAD")
    for path in sorted(INDEPENDENT_REVIEW_RESULTS_DIR.glob("*/*.json")):
        if path.is_symlink():
            raise ControlError(f"independent-review result must not be a symlink: {path.relative_to(ROOT)}")
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ControlError(f"invalid independent-review result record {path.relative_to(ROOT)}") from exc
        required = {
            "schema_version", "kind", "generated_at", "task_id", "packet_sha256", "packet",
            "reviewer_actor_instance_id", "verdict", "finding", "route", "source_identity",
            "result_sha256",
        }
        if not isinstance(record, dict) or set(record) != required:
            raise ControlError(f"independent-review result record has invalid shape: {path.relative_to(ROOT)}")
        if record.get("schema_version") != 1 or record.get("kind") != "independent_review_result":
            raise ControlError(f"independent-review result record has unsupported schema: {path.relative_to(ROOT)}")
        if record.get("verdict") not in {"pass", "repair"}:
            raise ControlError(f"independent-review result has invalid verdict: {path.relative_to(ROOT)}")
        if not isinstance(record.get("finding"), str) or not record["finding"].strip():
            raise ControlError(f"independent-review result finding must be non-empty: {path.relative_to(ROOT)}")
        reviewer = record.get("reviewer_actor_instance_id")
        if not isinstance(reviewer, str) or not re.fullmatch(r"[0-9a-f]{32}", reviewer):
            raise ControlError(f"independent-review result reviewer actor is invalid: {path.relative_to(ROOT)}")
        if record.get("result_sha256") != canonical_object_hash(record, "result_sha256"):
            raise ControlError(f"independent-review result hash mismatch: {path.relative_to(ROOT)}")
        packet = record.get("packet")
        validate_review_packet_shape(packet)
        task_id = record.get("task_id")
        if task_id != packet["task"].get("id") or task_id not in by_id:
            raise ControlError(f"independent-review result task identity is invalid: {path.relative_to(ROOT)}")
        if path.parent.name != task_id or path.stem != packet["packet_sha256"]:
            raise ControlError(f"independent-review result path does not match packet identity: {path.relative_to(ROOT)}")
        if record.get("packet_sha256") != packet["packet_sha256"]:
            raise ControlError(f"independent-review result packet hash does not match embedded packet: {task_id}")
        if record.get("source_identity") != packet["source_identity"]:
            raise ControlError(f"independent-review result source identity differs from embedded packet: {task_id}")
        if reviewer == packet["author_actor_instance_id"]:
            raise ControlError(f"independent-review result was produced by the author actor instance: {task_id}")
        if delegation.get(task_id) != "INDEPENDENT_REVIEW":
            raise ControlError(f"independent-review result references non-INDEPENDENT_REVIEW leaf {task_id}")
        task = by_id[task_id]
        review = task.get("independent_review")
        if review is None:
            raise ControlError(f"independent-review result references leaf without independent_review: {task_id}")
        expected_task = {
            "id": task["id"],
            "title": task["title"],
            "repair_task_id": review["repair_task_id"],
        }
        if packet.get("task") != expected_task or packet.get("actor_class") != "INDEPENDENT_REVIEW":
            raise ControlError(f"independent-review result packet differs from current review contract: {task_id}")
        expected_paths = {
            "sources": review["source_paths"],
            "candidates": review["candidate_paths"],
            "evidence": review["evidence_paths"],
        }
        material = packet.get("review_material")
        if not isinstance(material, dict) or set(material) != set(expected_paths):
            raise ControlError(f"independent-review result packet material has invalid shape: {task_id}")
        for role, paths in expected_paths.items():
            records = material.get(role)
            if not isinstance(records, list) or [r.get("path") if isinstance(r, dict) else None for r in records] != paths:
                raise ControlError(f"independent-review result {role} differ from current review contract: {task_id}")
        if record["verdict"] == "pass":
            if record.get("route") != {"kind": "PASS"}:
                raise ControlError(f"independent-review PASS result has invalid route: {task_id}")
        elif record.get("route") != {"kind": "REPAIR", "task_id": review["repair_task_id"]}:
            raise ControlError(f"independent-review REPAIR result has invalid route: {task_id}")
        identity = packet["source_identity"]
        source_head = identity.get("head") if isinstance(identity, dict) else None
        if not git_commit_exists(source_head):
            raise ControlError(f"independent-review result source head is missing: {task_id}")
        if identity.get("tree") != commit_tree(source_head):
            raise ControlError(f"independent-review result source tree mismatch: {task_id}")
        if not is_ancestor(source_head, current_head):
            raise ControlError(f"independent-review result source head is not in current history: {task_id}")
        if identity.get("task_contract_sha256") != sha256_bytes(git_file_bytes(source_head, TASKS_REL)):
            raise ControlError(f"independent-review result task contract hash mismatch: {task_id}")
        authority = identity.get("authority_hashes")
        if not isinstance(authority, dict):
            raise ControlError(f"independent-review result authority hashes are invalid: {task_id}")
        for rel, digest in authority.items():
            if sha256_bytes(git_file_bytes(source_head, rel)) != digest:
                raise ControlError(f"independent-review result authority hash mismatch for {rel}: {task_id}")
        for role, records in material.items():
            for item in records:
                data = review_record_bytes(item)
                if git_file_bytes(source_head, item["path"]) != data:
                    raise ControlError(
                        f"independent-review result {role[:-1] if role.endswith('s') else role} bytes "
                        f"do not match reviewed source commit: {item['path']}"
                    )
        stored = dict(record)
        stored["_repository_path"] = path.relative_to(ROOT).as_posix()
        results.setdefault(task_id, []).append(stored)
    return results


def validate_independent_review_acceptance(
    tasks: list[dict[str, Any]],
    delegation: dict[str, str],
    results: dict[str, list[dict[str, Any]]],
    acceptance_targets: dict[str, str],
) -> None:
    for task in tasks:
        task_id = task["id"]
        if task["status"] != "accepted" or delegation[task_id] != "INDEPENDENT_REVIEW":
            continue
        passes = [record for record in results.get(task_id, []) if record["verdict"] == "pass"]
        if not passes:
            raise ControlError(
                f"accepted INDEPENDENT_REVIEW leaf {task_id} requires a recorded independent-review PASS"
            )
        target = acceptance_targets.get(task_id)
        if not target:
            raise ControlError(f"accepted INDEPENDENT_REVIEW leaf {task_id} has no acceptance tag target")
        stale_reasons: list[str] = []
        for record in passes:
            packet = record["packet"]
            rel = record["_repository_path"]
            try:
                if git_file_bytes(target, rel) != (ROOT / rel).read_bytes():
                    raise ControlError("PASS result record is not bound into the acceptance tag")
                source_head = packet["source_identity"]["head"]
                if not is_ancestor(source_head, target):
                    raise ControlError("reviewed source commit is not an ancestor of the acceptance tag")
                reviewed_tasks = {
                    item.get("id"): item
                    for item in historical_tasks_at_commit(source_head)
                    if isinstance(item.get("id"), str)
                }
                accepted_tasks = {
                    item.get("id"): item
                    for item in historical_tasks_at_commit(target)
                    if isinstance(item.get("id"), str)
                }
                reviewed_task = reviewed_tasks.get(task_id)
                accepted_task = accepted_tasks.get(task_id)
                if reviewed_task is None or accepted_task is None:
                    raise ControlError("reviewed task is missing from source or acceptance target")
                if task_semantic_contract(reviewed_task) != task_semantic_contract(accepted_task):
                    raise ControlError("reviewed task semantic contract changed after PASS")
                for authority_rel, digest in packet["source_identity"]["authority_hashes"].items():
                    if sha256_bytes(git_file_bytes(target, authority_rel)) != digest:
                        raise ControlError(f"authority bytes changed after PASS: {authority_rel}")
                for role, material in packet["review_material"].items():
                    for item in material:
                        expected = review_record_bytes(item)
                        if git_file_bytes(target, item["path"]) != expected:
                            label = role[:-1] if role.endswith("s") else role
                            raise ControlError(f"{label} bytes changed after PASS: {item['path']}")
            except (ControlError, OSError) as exc:
                stale_reasons.append(str(exc))
                continue
            break
        else:
            detail = stale_reasons[0] if stale_reasons else "no valid PASS remained"
            raise ControlError(f"independent-review PASS for {task_id} is stale: {detail}")


def review_file_record(rel: str) -> dict[str, Any]:
    safe_rel_path(rel, "independent review material")
    path = ROOT / rel
    if path.is_symlink() or not path.is_file():
        raise ControlError(f"independent review material must be a regular file: {rel}")
    tracked = git_result("ls-files", "--error-unmatch", "--", rel)
    if tracked.returncode != 0:
        raise ControlError(f"independent review material is not tracked by Git: {rel}")
    data = path.read_bytes()
    try:
        content = data.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        content = base64.b64encode(data).decode("ascii")
        encoding = "base64"
    return {
        "path": rel,
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
        "encoding": encoding,
        "content": content,
    }


def review_record_bytes(record: dict[str, Any]) -> bytes:
    required = {"path", "sha256", "size_bytes", "encoding", "content"}
    if not isinstance(record, dict) or set(record) != required:
        raise ControlError("review packet material record has invalid shape")
    rel = safe_rel_path(record["path"], "review packet material path")
    encoding = record["encoding"]
    content = record["content"]
    if not isinstance(content, str):
        raise ControlError(f"review packet material content is invalid: {rel}")
    if encoding == "utf-8":
        data = content.encode("utf-8")
    elif encoding == "base64":
        try:
            data = base64.b64decode(content.encode("ascii"), validate=True)
        except Exception as exc:
            raise ControlError(f"review packet material base64 is invalid: {rel}") from exc
    else:
        raise ControlError(f"review packet material encoding is invalid: {rel}")
    if record["size_bytes"] != len(data) or record["sha256"] != sha256_bytes(data):
        raise ControlError(f"review packet material hash mismatch: {rel}")
    return data


def validate_review_packet_shape(packet: dict[str, Any]) -> None:
    required = {
        "schema_version", "kind", "generated_at", "task", "actor_class",
        "author_actor_instance_id", "source_identity", "review_material", "packet_sha256",
    }
    if not isinstance(packet, dict) or set(packet) != required:
        raise ControlError("review packet has invalid shape")
    if packet.get("schema_version") != 1 or packet.get("kind") != "independent_review_packet":
        raise ControlError("review packet has unsupported schema or kind")
    expected_hash = canonical_object_hash(packet, "packet_sha256")
    if packet.get("packet_sha256") != expected_hash:
        raise ControlError("review packet hash mismatch")


def load_review_packet(path: Path) -> dict[str, Any]:
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ControlError(f"review packet is missing: {path}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ControlError(f"review packet is unreadable or invalid JSON: {path}") from exc
    validate_review_packet_shape(packet)
    return packet


def validate_review_packet_against_repo(packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    cfg, tasks, hashes = structural_validation()
    require_project_mode(cfg, "independent review")
    if not clean_worktree():
        raise ControlError("review packet validation requires a clean working tree")
    active = derived_active_task(tasks)
    if not active:
        raise ControlError("review packet validation requires a uniquely derived active task")
    by_id = {task["id"]: task for task in tasks}
    task = by_id[active]
    delegation = load_delegation(tasks, cfg)
    if delegation[active] != "INDEPENDENT_REVIEW":
        raise ControlError(f"active leaf {active} is not an INDEPENDENT_REVIEW leaf")
    review = task.get("independent_review")
    if review is None:
        raise ControlError(f"active leaf {active} has no independent_review contract")
    task_packet = packet.get("task")
    if task_packet != {
        "id": task["id"],
        "title": task["title"],
        "repair_task_id": review["repair_task_id"],
    }:
        raise ControlError("review packet task identity does not match current contract")
    if packet.get("actor_class") != "INDEPENDENT_REVIEW":
        raise ControlError("review packet actor class is invalid")
    actor = packet.get("author_actor_instance_id")
    if not isinstance(actor, str) or not re.fullmatch(r"[0-9a-f]{32}", actor):
        raise ControlError("review packet author actor instance id is invalid")
    identity = packet.get("source_identity")
    required_identity = {
        "head", "tree", "branch", "repo_fingerprint", "task_contract_sha256", "authority_hashes"
    }
    if not isinstance(identity, dict) or set(identity) != required_identity:
        raise ControlError("review packet source identity has invalid shape")
    head, tree, branch = git_identity()
    expected_identity = {
        "head": head,
        "tree": tree,
        "branch": branch,
        "repo_fingerprint": repo_fingerprint(cfg),
        "task_contract_sha256": task_contract_hash(),
        "authority_hashes": hashes,
    }
    if identity != expected_identity:
        raise ControlError("review packet source identity does not match current Git and authority hashes")
    material = packet.get("review_material")
    if not isinstance(material, dict) or set(material) != {"sources", "candidates", "evidence"}:
        raise ControlError("review packet material has invalid shape")
    expected_paths = {
        "sources": review["source_paths"],
        "candidates": review["candidate_paths"],
        "evidence": review["evidence_paths"],
    }
    for role, paths in expected_paths.items():
        records = material.get(role)
        if not isinstance(records, list) or [r.get("path") if isinstance(r, dict) else None for r in records] != paths:
            raise ControlError(f"review packet {role} do not match authorised review scope")
        for record in records:
            data = review_record_bytes(record)
            current = ROOT / record["path"]
            if current.is_symlink() or not current.is_file() or current.read_bytes() != data:
                raise ControlError(f"review packet material does not match current repository: {record['path']}")
    return task, review


def command_review_packet(args: argparse.Namespace) -> int:
    path: Path | None = None
    try:
        cfg, tasks, hashes = structural_validation()
        require_project_mode(cfg, "review-packet")
        if not clean_worktree():
            raise ControlError("review-packet requires a clean working tree")
        active = derived_active_task(tasks)
        if not active:
            raise ControlError("review-packet requires a uniquely derived active task")
        by_id = {task["id"]: task for task in tasks}
        task = by_id[active]
        delegation = load_delegation(tasks, cfg)
        if delegation[active] != "INDEPENDENT_REVIEW":
            raise ControlError(f"leaf {active} is not an INDEPENDENT_REVIEW leaf")
        review = task.get("independent_review")
        if review is None:
            raise ControlError(f"leaf {active} has no independent_review contract")
        actor = current_actor_instance_id()
        head, tree, branch = git_identity()
        packet: dict[str, Any] = {
            "schema_version": 1,
            "kind": "independent_review_packet",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task": {
                "id": task["id"],
                "title": task["title"],
                "repair_task_id": review["repair_task_id"],
            },
            "actor_class": "INDEPENDENT_REVIEW",
            "author_actor_instance_id": actor,
            "source_identity": {
                "head": head,
                "tree": tree,
                "branch": branch,
                "repo_fingerprint": repo_fingerprint(cfg),
                "task_contract_sha256": task_contract_hash(),
                "authority_hashes": hashes,
            },
            "review_material": {
                "sources": [review_file_record(rel) for rel in review["source_paths"]],
                "candidates": [review_file_record(rel) for rel in review["candidate_paths"]],
                "evidence": [review_file_record(rel) for rel in review["evidence_paths"]],
            },
            "packet_sha256": "",
        }
        packet["packet_sha256"] = canonical_object_hash(packet, "packet_sha256")
        path = external_json_output_path(args.output, "review-packet")
        payload = json.dumps(packet, indent=2, sort_keys=True) + "\n"
        required_bytes = len(payload.encode("utf-8"))
        if required_bytes > cfg["context_max_bytes"]:
            print(packet_fallback_status(
                kind="REVIEW_PACKET", task_id=active, required_bytes=required_bytes,
                max_bytes=cfg["context_max_bytes"],
                next_action=(
                    "use a full-material review handoff or programme-owner-approved larger context budget; "
                    "do not review from partial material"
                ),
            ), end="")
            return 1
        path.write_text(payload, encoding="utf-8")
        print("REVIEW_PACKET: PASS")
        print(f"TASK: {active}")
        print(f"PACKET_PATH: {path}")
        print(f"PACKET_SHA256: {packet['packet_sha256']}")
        return 0
    except (ControlError, OSError) as exc:
        if path is not None and path.exists():
            path.unlink(missing_ok=True)
        print(f"REVIEW_PACKET: FAIL\nERROR: {exc}")
        return 1


def command_review_validate(args: argparse.Namespace) -> int:
    try:
        packet = load_review_packet(Path(args.packet).expanduser().resolve())
        task, _review = validate_review_packet_against_repo(packet)
        print("REVIEW_PACKET_VALIDATE: PASS")
        print(f"TASK: {task['id']}")
        print(f"PACKET_SHA256: {packet['packet_sha256']}")
        return 0
    except (ControlError, OSError) as exc:
        print(f"REVIEW_PACKET_VALIDATE: FAIL\nERROR: {exc}")
        return 1


def command_review_result(args: argparse.Namespace) -> int:
    path: Path | None = None
    durable_path: Path | None = None
    try:
        finding = args.finding.strip()
        if not finding:
            raise ControlError("review-result finding must be non-empty")
        packet = load_review_packet(Path(args.packet).expanduser().resolve())
        task, review = validate_review_packet_against_repo(packet)
        reviewer = current_actor_instance_id()
        if reviewer == packet["author_actor_instance_id"]:
            raise ControlError("independent review requires a fresh reviewer actor instance")
        route = {"kind": "PASS"} if args.verdict == "pass" else {
            "kind": "REPAIR", "task_id": review["repair_task_id"]
        }
        result: dict[str, Any] = {
            "schema_version": 1,
            "kind": "independent_review_result",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task_id": task["id"],
            "packet_sha256": packet["packet_sha256"],
            "packet": packet,
            "reviewer_actor_instance_id": reviewer,
            "verdict": args.verdict,
            "finding": finding,
            "route": route,
            "source_identity": packet["source_identity"],
            "result_sha256": "",
        }
        result["result_sha256"] = canonical_object_hash(result, "result_sha256")
        path = external_json_output_path(args.output, "review-result")
        durable_path = INDEPENDENT_REVIEW_RESULTS_DIR / task["id"] / f"{packet['packet_sha256']}.json"
        if durable_path.exists():
            raise ControlError(f"independent-review result already exists for packet {packet['packet_sha256']}")
        payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
        durable_path.parent.mkdir(parents=True, exist_ok=True)
        durable_path.write_text(payload, encoding="utf-8")
        path.write_text(payload, encoding="utf-8")
        print("REVIEW_RESULT: PASS")
        print(f"TASK: {task['id']}")
        print(f"VERDICT: {args.verdict}")
        if route["kind"] == "PASS":
            print("ROUTE: PASS")
        else:
            print(f"ROUTE: REPAIR:{route['task_id']}")
        print(f"RESULT_PATH: {path}")
        print(f"RESULT_SHA256: {result['result_sha256']}")
        return 0
    except (ControlError, OSError) as exc:
        if path is not None and path.exists():
            path.unlink(missing_ok=True)
        if durable_path is not None and durable_path.exists():
            durable_path.unlink(missing_ok=True)
        print(f"REVIEW_RESULT: FAIL\nERROR: {exc}")
        return 1


def command_programme_owner_packet(args: argparse.Namespace) -> int:
    path: Path | None = None
    try:
        cfg, tasks, hashes = structural_validation()
        require_project_mode(cfg, "programme-owner-packet")
        if not clean_worktree():
            raise ControlError("programme-owner-packet requires a clean working tree")
        active = derived_active_task(tasks)
        if not active:
            raise ControlError("programme-owner-packet requires a uniquely derived active task")
        by_id = {task["id"]: task for task in tasks}
        task = by_id[active]
        delegation = load_delegation(tasks, cfg)
        if delegation[active] != "PROGRAMME_OWNER":
            raise ControlError(f"leaf {active} is not a PROGRAMME_OWNER leaf")
        review = task.get("programme_owner_review")
        if review is None:
            raise ControlError(f"leaf {active} has no programme_owner_review contract")
        actor = current_actor_instance_id()
        head, tree, branch = git_identity()
        packet: dict[str, Any] = {
            "schema_version": 1,
            "kind": "programme_owner_review_packet",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "gate": {"id": task["id"], "title": task["title"]},
            "actor_class": "PROGRAMME_OWNER",
            "prepared_by_actor_instance_id": actor,
            "source_identity": {
                "head": head,
                "tree": tree,
                "branch": branch,
                "repo_fingerprint": repo_fingerprint(cfg),
                "task_contract_sha256": task_contract_hash(),
                "authority_hashes": hashes,
            },
            "candidate_artifacts": [
                programme_owner_artifact_record(rel) for rel in review["candidate_paths"]
            ],
            "material_decisions": list(review["material_decisions"]),
            "unresolved_items": programme_owner_unresolved_items(),
            "freedoms": list(review["freedoms"]),
            "prohibitions": list(review["prohibitions"]),
            "requested_decision": review["requested_decision"],
            "declared_next": programme_owner_declared_next(tasks, active),
            "packet_sha256": "",
        }
        packet["packet_sha256"] = canonical_object_hash(packet, "packet_sha256")
        path = external_json_output_path(args.output, "programme-owner-packet")
        path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("PROGRAMME_OWNER_PACKET: PASS")
        print(f"GATE: {active}")
        print(f"PACKET_PATH: {path}")
        print(f"PACKET_SHA256: {packet['packet_sha256']}")
        return 0
    except (ControlError, OSError) as exc:
        if path is not None and path.exists():
            path.unlink(missing_ok=True)
        print(f"PROGRAMME_OWNER_PACKET: FAIL\nERROR: {exc}")
        return 1


def command_programme_owner_decision(args: argparse.Namespace) -> int:
    path: Path | None = None
    try:
        note = args.note.strip()
        if not note:
            raise ControlError("programme-owner-decision note must be non-empty")
        packet = load_programme_owner_packet(Path(args.packet).expanduser().resolve())
        task, _review = validate_programme_owner_packet_against_repo(packet)
        actor = current_actor_instance_id()
        record: dict[str, Any] = {
            "schema_version": 1,
            "kind": "programme_owner_decision",
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "gate_id": task["id"],
            "packet": packet,
            "decision": args.decision,
            "note": note,
            "recorded_by_actor_instance_id": actor,
            "decision_sha256": "",
        }
        record["decision_sha256"] = canonical_object_hash(record, "decision_sha256")
        path = PROGRAMME_OWNER_DECISIONS_DIR / task["id"] / f"{packet['packet_sha256']}.json"
        if path.exists():
            raise ControlError(f"programme-owner decision already exists for packet {packet['packet_sha256']}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("PROGRAMME_OWNER_DECISION: PASS")
        print(f"GATE: {task['id']}")
        print(f"DECISION: {args.decision}")
        print(f"DECISION_PATH: {path.relative_to(ROOT)}")
        print(f"DECISION_SHA256: {record['decision_sha256']}")
        return 0
    except (ControlError, OSError) as exc:
        if path is not None and path.exists():
            path.unlink(missing_ok=True)
        print(f"PROGRAMME_OWNER_DECISION: FAIL\nERROR: {exc}")
        return 1


def path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def bundle_output_path(raw: str | None, branch: str, head: str) -> Path:
    if raw:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        else:
            candidate = candidate.resolve()
    else:
        safe_branch = re.sub(r"[^A-Za-z0-9._-]+", "-", branch).strip("-") or "detached"
        candidate = (ROOT.parent / f"{ROOT.name}-{safe_branch}-{head[:12]}.bundle").resolve()
    if path_is_within(candidate, ROOT.resolve()):
        raise ControlError("bundle output must be outside the repository working tree")
    if candidate.exists():
        raise ControlError(f"bundle output already exists: {candidate}")
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


def create_verified_bundle(path: Path, cfg: dict[str, Any], branch: str, head: str) -> str:
    acceptance_ref = resolve_acceptance_ref(cfg)
    acceptance_target = run_git("rev-parse", acceptance_ref)
    canonical_acceptance_ref = f"refs/heads/{cfg['acceptance_branch']}"
    synthesized_acceptance_ref = False
    if acceptance_ref != canonical_acceptance_ref:
        run_git("update-ref", canonical_acceptance_ref, acceptance_target)
        synthesized_acceptance_ref = True

    try:
        local_refs = run_git("for-each-ref", "--format=%(refname)", "refs/heads", "refs/tags").splitlines()
        refs = ["HEAD", *local_refs]
        deduped: list[str] = []
        seen: set[str] = set()
        for ref in refs:
            if ref and ref not in seen:
                seen.add(ref)
                deduped.append(ref)
        created = git_result("bundle", "create", str(path), *deduped)
        if created.returncode != 0:
            path.unlink(missing_ok=True)
            raise ControlError(f"git bundle create failed: {created.stderr.strip()}")
        verified = git_result("bundle", "verify", str(path))
        if verified.returncode != 0:
            path.unlink(missing_ok=True)
            raise ControlError(f"git bundle verify failed: {(verified.stderr or verified.stdout).strip()}")
        listed = git_result("bundle", "list-heads", str(path))
        if listed.returncode != 0:
            path.unlink(missing_ok=True)
            raise ControlError(f"git bundle list-heads failed: {listed.stderr.strip()}")
        listed_refs: dict[str, str] = {}
        for line in listed.stdout.splitlines():
            try:
                target, ref = line.split(maxsplit=1)
            except ValueError:
                continue
            listed_refs[ref] = target
        branch_ref = f"refs/heads/{branch}"
        if listed_refs.get("HEAD") != head:
            path.unlink(missing_ok=True)
            raise ControlError("finished bundle HEAD does not match repository HEAD")
        if listed_refs.get(branch_ref) != head:
            path.unlink(missing_ok=True)
            raise ControlError(f"finished bundle does not bind current branch {branch} to HEAD")
        if listed_refs.get(canonical_acceptance_ref) != acceptance_target:
            path.unlink(missing_ok=True)
            raise ControlError("finished bundle is missing the configured acceptance ref")
        if any(ref.startswith("refs/remotes/") for ref in listed_refs):
            path.unlink(missing_ok=True)
            raise ControlError("finished bundle unexpectedly contains remote-tracking refs")
        if any(ref.startswith("refs/worktrees/") for ref in listed_refs):
            path.unlink(missing_ok=True)
            raise ControlError("finished bundle unexpectedly contains linked-worktree private refs")
        return sha256_file(path)
    finally:
        if synthesized_acceptance_ref:
            removed = git_result("update-ref", "-d", canonical_acceptance_ref, acceptance_target)
            if removed.returncode != 0:
                path.unlink(missing_ok=True)
                raise ControlError("failed to remove temporary local acceptance ref after bundle export")


def command_flush(args: argparse.Namespace) -> int:
    path: Path | None = None
    try:
        if not clean_worktree():
            raise ControlError("flush requires a clean working tree; commit intended work first")
        cfg = config()
        require_project_mode(cfg, "flush")
        if state_mode(cfg) != "lcr":
            raise ControlError("flush requires LCR mode")
        structural_validation()
        head, tree, branch = git_identity()
        path = bundle_output_path(args.output, branch, head)
        digest = create_verified_bundle(path, cfg, branch, head)
        print("FLUSH: PASS")
        print("FLUSH_CHECKPOINT_COMMIT: none")
        print(f"BUNDLE_PATH: {path}")
        print(f"BUNDLE_SHA256: {digest}")
        print(f"BUNDLE_HEAD: {head}")
        print(f"BUNDLE_TREE: {tree}")
        print(f"BRANCH: {branch}")
        return 0
    except (ControlError, OSError) as exc:
        if path is not None and path.exists():
            path.unlink(missing_ok=True)
        print(f"FLUSH: FAIL\nERROR: {exc}")
        return 1


def command_verify_gate(args: argparse.Namespace) -> int:
    try:
        cfg, tasks, hashes = structural_validation()
        require_project_mode(cfg, "verify-gate")
        if not clean_worktree():
            raise ControlError("verify-gate requires a clean working tree and admitted prior receipts")
        active = derived_active_task(tasks)
        if not active:
            raise ControlError("verify-gate requires a uniquely derived active task")
        by_id = {task["id"]: task for task in tasks}
        task = by_id[active]
        gate_key = VERIFICATION_GATES[args.gate]
        checks = task["verification"][gate_key]
        executed: list[str] = []
        reused: list[str] = []
        created: list[str] = []

        for check in checks:
            input_fingerprint = verification_input_fingerprint(check["inputs"])
            governing_fingerprint = verification_governing_fingerprint(task, args.gate, check)
            evidence_key = verification_evidence_key(
                task, args.gate, check, input_fingerprint, governing_fingerprint
            )
            reusable = reusable_verification_receipt(evidence_key, verification_expected_exit_codes(check))
            if reusable is not None:
                reused.append(check["id"])
                continue

            before_head, before_tree, branch = git_identity()
            before_fp = repo_fingerprint(cfg)
            before_state = working_state_digest(cfg)
            before_auth = hashes
            result = subprocess.run(
                check["command"], cwd=ROOT, text=True, capture_output=True, check=False
            )
            mutated = False
            try:
                after_head, after_tree, after_branch = git_identity()
                after_fp = repo_fingerprint(cfg)
                after_state = working_state_digest(cfg)
                after_auth = authority_hashes(cfg)
                mutated = (
                    before_head, before_tree, branch, before_fp, before_state, before_auth
                ) != (
                    after_head, after_tree, after_branch, after_fp, after_state, after_auth
                )
            except ControlError:
                mutated = True

            allowed_exit_codes = verification_expected_exit_codes(check)
            if result.returncode not in allowed_exit_codes and not mutated:
                prior_failure = reusable_failed_verification_receipt(evidence_key, result, mutated)
                if prior_failure is not None:
                    detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
                    raise ControlError(
                        f"verification check {check['id']} returned {result.returncode}; expected one of "
                        f"{allowed_exit_codes}; identical failure already recorded in "
                        f"{prior_failure.relative_to(ROOT)}: {detail}"
                    )

            receipt_path = write_required_verification_receipt(
                task, args.gate, check,
                input_fingerprint, governing_fingerprint, evidence_key,
                result, mutated,
                before_head, before_tree, branch,
                before_fp, before_state, before_auth,
            )
            executed.append(check["id"])
            created.append(receipt_path.relative_to(ROOT).as_posix())
            if mutated:
                raise ControlError(
                    f"verification check {check['id']} mutated repository state; receipt={created[-1]}"
                )
            if result.returncode not in allowed_exit_codes:
                detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
                raise ControlError(
                    f"verification check {check['id']} returned {result.returncode}; expected one of {allowed_exit_codes}: {detail}"
                )

        print("VERIFY_GATE: PASS")
        print(f"GATE: {args.gate}")
        print(f"TASK: {active}")
        print(f"EXECUTED: {','.join(executed) if executed else '<none>'}")
        print(f"REUSED: {','.join(reused) if reused else '<none>'}")
        print(f"RECEIPTS_CREATED: {len(created)}")
        return 0
    except ControlError as exc:
        print(f"VERIFY_GATE: FAIL\nERROR: {exc}")
        return 1


def command_verify(args: argparse.Namespace) -> int:
    try:
        cfg, _tasks, hashes = structural_validation()
        require_project_mode(cfg, "verify")
        command = list(args.command)
        if command and command[0] == "--": command = command[1:]
        if not command: raise ControlError("verify requires a command after --")
        before_head, before_tree, branch = git_identity()
        before_fp = repo_fingerprint(cfg); before_state = working_state_digest(cfg); before_auth = hashes
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        mutated = False
        try:
            after_head, after_tree, after_branch = git_identity()
            after_fp = repo_fingerprint(cfg); after_state = working_state_digest(cfg); after_auth = authority_hashes(cfg)
            mutated = (before_head, before_tree, branch, before_fp, before_state, before_auth) != (after_head, after_tree, after_branch, after_fp, after_state, after_auth)
        except ControlError:
            mutated = True
        now = datetime.now(timezone.utc)
        stem = now.strftime("%Y%m%dT%H%M%S%fZ") + "-" + sha256_bytes(args.claim.encode("utf-8"))[:10]
        RECEIPTS_DIR.mkdir(parents=True, exist_ok=True); receipt_path = RECEIPTS_DIR / f"{stem}.json"
        if receipt_path.exists(): raise ControlError("verification receipt path collision")
        receipt = {
            "schema_version": 1, "generated_at": now.isoformat(), "claim": args.claim,
            "command": command, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
            "stdout_sha256": sha256_bytes(result.stdout.encode("utf-8")), "stderr_sha256": sha256_bytes(result.stderr.encode("utf-8")),
            "source_head": before_head, "source_tree": before_tree, "branch": branch,
            "repo_fingerprint": before_fp, "working_state_digest": before_state, "authority_hashes": before_auth,
            "repository_mutated": mutated,
            "claim_boundary": "This receipt establishes only that the recorded command produced the recorded exit/output against the recorded repository state.",
        }
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"RECEIPT: {receipt_path.relative_to(ROOT)}"); print(f"EXIT_CODE: {result.returncode}")
        if mutated:
            print("REPOSITORY_MUTATED: yes"); print("VERIFY: FAIL"); print("ERROR: verification command mutated repository state"); return 2
        if result.stdout: print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
        if result.stderr: print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
        return result.returncode
    except ControlError as exc:
        print(f"VERIFY: FAIL\nERROR: {exc}"); return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest="subcommand", required=True)
    p = sub.add_parser("check"); p.set_defaults(func=command_check)
    p = sub.add_parser("instantiate")
    p.add_argument("--target-repo", required=True)
    p.add_argument("--accepted-brief", required=True)
    p.set_defaults(func=command_instantiate)
    p = sub.add_parser("finalize-instantiation")
    p.add_argument("--actor-class", choices=sorted(ACTOR_CLASSES), required=True)
    p.add_argument("--note", required=True)
    p.set_defaults(func=command_finalize_instantiation)
    p = sub.add_parser("ready"); p.set_defaults(func=command_ready)
    p = sub.add_parser("context"); p.set_defaults(func=command_context)
    p = sub.add_parser("migrate-lcr"); p.set_defaults(func=command_migrate_lcr)
    p = sub.add_parser("checkpoint")
    p.add_argument("--bootstrap-lcr", action="store_true")
    p.add_argument("--admit-branch-change", action="store_true")
    p.add_argument("--admit-authority-change", action="store_true")
    p.add_argument("--admit-contract-change", action="store_true")
    p.add_argument("--admit-acceptance-change", action="store_true")
    p.add_argument("--admit-receipts", action="store_true")
    p.add_argument("--admit-claims-change", action="store_true")
    p.add_argument("--admit-independent-review-result", action="store_true")
    p.add_argument("--admit-programme-owner-decision", action="store_true")
    p.add_argument("--admit-work", action="store_true")
    p.add_argument("--admit-control-change", action="store_true")
    p.add_argument("--admit-delegation-change", action="store_true")
    p.add_argument("--actor-class", choices=sorted(ACTOR_CLASSES), default="AUTONOMOUS")
    p.set_defaults(func=command_checkpoint)
    p = sub.add_parser("session-start"); p.set_defaults(func=command_session_start)
    p = sub.add_parser("session-status"); p.set_defaults(func=command_session_status)
    p = sub.add_parser("flush"); p.add_argument("--output"); p.set_defaults(func=command_flush)
    p = sub.add_parser("review-packet"); p.add_argument("--output", required=True); p.set_defaults(func=command_review_packet)
    p = sub.add_parser("review-validate"); p.add_argument("--packet", required=True); p.set_defaults(func=command_review_validate)
    p = sub.add_parser("review-result")
    p.add_argument("--packet", required=True)
    p.add_argument("--verdict", choices=["pass", "repair"], required=True)
    p.add_argument("--finding", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=command_review_result)
    p = sub.add_parser("programme-owner-packet")
    p.add_argument("--output", required=True)
    p.set_defaults(func=command_programme_owner_packet)
    p = sub.add_parser("programme-owner-decision")
    p.add_argument("--packet", required=True)
    p.add_argument("--decision", choices=["approve", "reject"], required=True)
    p.add_argument("--note", required=True)
    p.set_defaults(func=command_programme_owner_decision)
    p = sub.add_parser("verify-gate"); p.add_argument("gate", choices=sorted(VERIFICATION_GATES)); p.set_defaults(func=command_verify_gate)
    p = sub.add_parser("verify"); p.add_argument("--claim", required=True); p.add_argument("command", nargs=argparse.REMAINDER); p.set_defaults(func=command_verify)
    return parser


def main() -> int:
    args = build_parser().parse_args(); return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
