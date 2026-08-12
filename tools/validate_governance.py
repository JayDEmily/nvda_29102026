from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
import runtime_identity  # noqa: E402


class GovernanceError(RuntimeError):
    pass


ACCEPTED_DISPOSITIONS = {"ACCEPTED", "GATE0_PASS"}
KNOWN_ROLES = {
    "project_manager",
    "integration_auditor",
    "semantic_worker",
    "semantic_reviewer",
    "normative_writer",
    "test_author",
    "implementation_worker",
}
PROOF_CLASSES = {"MECHANICAL", "SEMANTIC", "BOTH"}


class ValidatedAdmission:
    __slots__ = ("admission", "candidate_commit", "candidate_parent", "changed_paths")

    def __init__(
        self,
        *,
        admission: dict[str, Any],
        candidate_commit: str,
        candidate_parent: str,
        changed_paths: tuple[str, ...],
    ) -> None:
        self.admission = admission
        self.candidate_commit = candidate_commit
        self.candidate_parent = candidate_parent
        self.changed_paths = changed_paths


def canonical_sha(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _require(record: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - record.keys())
    if missing:
        raise GovernanceError(f"{label} missing required fields: {', '.join(missing)}")


def _candidate_binding(record: dict[str, Any], label: str) -> tuple[str | None, str | None]:
    commit = record.get("candidate_commit")
    digest = record.get("candidate_sha256")
    if not commit and not digest:
        raise GovernanceError(f"{label} has no candidate commit or content hash")
    return commit, digest


def _is_accepted(record: dict[str, Any]) -> bool:
    return record.get("disposition") in ACCEPTED_DISPOSITIONS


def _git_blob(repo_root: Path, commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=repo_root)
    except (subprocess.CalledProcessError, OSError) as exc:
        raise GovernanceError(f"Git candidate does not contain required path: {path}") from exc


def _source_authority_hashes(repo_root: Path, commit: str) -> dict[str, str]:
    text = _git_blob(repo_root, commit, "authority/AUTHORITY_MANIFEST.md").decode()
    result: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3:
            continue
        path_cell, _, hash_cell = cells
        if not (path_cell.startswith("`") and path_cell.endswith("`")):
            continue
        if not (hash_cell.startswith("`") and hash_cell.endswith("`")):
            continue
        path = path_cell[1:-1]
        digest = hash_cell[1:-1]
        if len(digest) == 64:
            result[path] = digest
    if not result:
        raise GovernanceError("source authority manifest has no parseable authority entries")
    return result


def accepted_semantic_index_entries(
    index: dict[str, Any],
    *,
    admissions: dict[str, dict[str, Any]] | None = None,
    repo_root: Path | None = None,
) -> dict[str, dict[str, Any]]:
    if index.get("status") != "ACCEPTED" or not index.get("admission_id"):
        raise GovernanceError("semantic index is not accepted")
    if admissions is None or repo_root is None:
        raise GovernanceError("accepted semantic index requires admission and repository binding")
    admission = admissions.get(index["admission_id"])
    if not admission or not _is_accepted(admission):
        raise GovernanceError("semantic index admission is absent or not accepted")
    if admission.get("record_type") != "SEMANTIC_RESULT":
        raise GovernanceError("semantic index admission has wrong record type")
    if admission.get("proposition_id") != "RAW_SIGNAL_SEMANTIC_INDEX_V1":
        raise GovernanceError("semantic index admission has wrong proposition")
    if admission.get("artifact_path") != "docs/governance/SEMANTIC_INDEX.json":
        raise GovernanceError("semantic index admission has wrong artifact path")
    candidate_commit = admission.get("candidate_commit")
    if not isinstance(candidate_commit, str) or not candidate_commit:
        raise GovernanceError("semantic index admission has no candidate commit")
    try:
        candidate_index = json.loads(
            _git_blob(repo_root, candidate_commit, "docs/governance/SEMANTIC_INDEX.json")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GovernanceError("candidate semantic index JSON is invalid") from exc
    expected_index_sha = canonical_sha(candidate_index)
    if admission.get("artifact_sha256") != expected_index_sha:
        raise GovernanceError("semantic index admission index hash mismatch")
    if canonical_sha(index) != expected_index_sha:
        raise GovernanceError("semantic index bytes do not match admitted candidate index")

    source_authorities = _source_authority_hashes(repo_root, candidate_commit)
    entries = index.get("entries")
    if not isinstance(entries, list):
        raise GovernanceError("semantic index entries are malformed")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        entry_id = entry.get("entry_id")
        if not entry_id or entry_id in result:
            raise GovernanceError("semantic index has missing or duplicate entry ID")
        refs = entry.get("authority_refs")
        if not refs:
            raise GovernanceError(f"semantic index entry {entry_id} has no source authority")
        for ref in refs:
            path = ref.get("path")
            digest = ref.get("sha256")
            admitted_digest = source_authorities.get(path)
            if not admitted_digest or admitted_digest != digest:
                raise GovernanceError(
                    f"semantic index source authority is not admitted or hash-bound: {path}"
                )
            actual = hashlib.sha256(_git_blob(repo_root, candidate_commit, path)).hexdigest()
            if actual != digest:
                raise GovernanceError(f"semantic index source authority bytes mismatch: {path}")
        result[entry_id] = entry
    for entry_id, entry in result.items():
        for dependency in entry.get("dependencies", []):
            if dependency not in result:
                raise GovernanceError(
                    f"semantic index entry {entry_id} has unknown dependency {dependency}"
                )
    return result


def validate_work_order(
    work_order: dict[str, Any],
    admissions: dict[str, dict[str, Any]],
    *,
    accepted_base_commit: str,
) -> None:
    _require(
        work_order,
        {
            "work_order_id",
            "work_order_admission_id",
            "gate",
            "stage",
            "proposition_id",
            "authority_ref",
            "authority_status",
            "accepted_base_commit",
            "commissioned_role",
            "allowed_mutations",
            "proof_class",
            "falsifier",
            "pass_means",
            "pass_does_not_mean",
            "dependencies",
            "stop_conditions",
        },
        "work order",
    )
    if work_order["authority_status"] != "GOVERNED":
        raise GovernanceError("executable work order authority_status must be GOVERNED")
    if work_order["accepted_base_commit"] != accepted_base_commit:
        raise GovernanceError("work order accepted base does not match admitted Git base")
    if work_order["commissioned_role"] not in KNOWN_ROLES:
        raise GovernanceError("work order commissioned role is unknown")
    if work_order["proof_class"] not in PROOF_CLASSES:
        raise GovernanceError("work order proof class is invalid")
    if not work_order["stop_conditions"]:
        raise GovernanceError("work order requires an explicit stop condition")
    if work_order["pass_means"] == work_order["pass_does_not_mean"]:
        raise GovernanceError("work order PASS boundary is not discriminating")

    authority_ref = work_order["authority_ref"]
    authority_id = authority_ref.get("admission_id")
    authority = admissions.get(authority_id)
    if not authority or not _is_accepted(authority):
        raise GovernanceError("work order does not reference an accepted authority admission")
    if canonical_sha(authority) != authority_ref.get("sha256"):
        raise GovernanceError("work order authority hash does not bind the admitted record")
    if authority.get("proposition_id") != work_order["proposition_id"]:
        raise GovernanceError("work order proposition is not the admitted authority proposition")

    delegation_id = work_order["work_order_admission_id"]
    delegation = admissions.get(delegation_id)
    if not delegation or not _is_accepted(delegation):
        raise GovernanceError("work order has no accepted delegation")
    if delegation.get("record_type") != "WORK_ORDER_DELEGATION":
        raise GovernanceError("work order delegation has wrong record type")
    if delegation.get("work_order_id") != work_order["work_order_id"]:
        raise GovernanceError("work order delegation ID does not match work order")
    if delegation.get("work_order_sha256") != canonical_sha(work_order):
        raise GovernanceError("work order delegation work order hash mismatch")
    if delegation.get("proposition_id") != work_order["proposition_id"]:
        raise GovernanceError("work order delegation proposition mismatch")
    if delegation.get("authority_ref") != work_order["authority_ref"]:
        raise GovernanceError("work order delegation authority mismatch")
    if delegation.get("accepted_base_commit") != work_order["accepted_base_commit"]:
        raise GovernanceError("work order delegation base mismatch")
    if delegation.get("commissioned_role") != work_order["commissioned_role"]:
        raise GovernanceError("work order delegation role mismatch")
    if delegation.get("allowed_mutations") != work_order["allowed_mutations"]:
        raise GovernanceError("work order delegation mutation scope mismatch")
    if delegation.get("proof_class") != work_order["proof_class"]:
        raise GovernanceError("work order delegation proof scope mismatch")

    for dependency_id in work_order["dependencies"]:
        dependency = admissions.get(dependency_id)
        if not dependency or not _is_accepted(dependency):
            raise GovernanceError(f"work order dependency is not admitted: {dependency_id}")


def validate_attempt(work_order: dict[str, Any], attempt: dict[str, Any]) -> None:
    _require(
        attempt,
        {
            "attempt_id",
            "work_order_id",
            "actor_id",
            "actor_role",
            "actor_thread_id",
            "actor_runtime_ref",
            "accepted_base_commit",
            "candidate_commit",
            "candidate_sha256",
            "actual_changed_paths",
            "proof_results",
        },
        "attempt",
    )
    if attempt["work_order_id"] != work_order["work_order_id"]:
        raise GovernanceError("attempt work order mismatch")
    if attempt["actor_role"] != work_order["commissioned_role"]:
        raise GovernanceError("attempt actor role does not match commissioned role")
    if attempt["accepted_base_commit"] != work_order["accepted_base_commit"]:
        raise GovernanceError("attempt accepted base mismatch")
    _candidate_binding(attempt, "attempt")
    unexpected = set(attempt["actual_changed_paths"]) - set(work_order["allowed_mutations"])
    if unexpected:
        raise GovernanceError(f"attempt changed paths outside authority: {sorted(unexpected)}")


def validate_git_candidate_binding(
    work_order: dict[str, Any],
    attempt: dict[str, Any],
    *,
    candidate_commit: str,
    candidate_parent: str,
    changed_paths: list[str],
) -> None:
    """Bind an attempt declaration to mechanically derived Git candidate facts."""
    declared_commit = attempt.get("candidate_commit")
    if not declared_commit or declared_commit != candidate_commit:
        raise GovernanceError("candidate commit does not match attempt declaration")
    if candidate_parent != work_order.get("accepted_base_commit"):
        raise GovernanceError("candidate parent does not match accepted Git base")

    declared_paths = attempt.get("actual_changed_paths")
    if not isinstance(declared_paths, list):
        raise GovernanceError("attempt changed paths declaration is malformed")
    if set(changed_paths) != set(declared_paths):
        raise GovernanceError("Git changed paths do not match attempt changed paths")

    unexpected = set(changed_paths) - set(work_order.get("allowed_mutations", []))
    if unexpected:
        raise GovernanceError(
            f"Git changed paths exceed work-order authority: {sorted(unexpected)}"
        )


def git_candidate_facts(repo_root: Path, candidate_commit: str) -> tuple[str, list[str]]:
    try:
        subprocess.run(
            ["git", "cat-file", "-e", f"{candidate_commit}^{{commit}}"],
            cwd=repo_root,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        parents_line = subprocess.check_output(
            ["git", "rev-list", "--parents", "-n", "1", candidate_commit],
            cwd=repo_root,
            text=True,
        ).strip().split()
        if len(parents_line) != 2:
            raise GovernanceError("candidate commit must have exactly one parent")
        parent = parents_line[1]
        changed = subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", candidate_commit],
            cwd=repo_root,
            text=True,
        ).splitlines()
    except (subprocess.CalledProcessError, OSError) as exc:
        raise GovernanceError("candidate commit is not present in the repository") from exc
    return parent, sorted(path for path in changed if path)


def validate_attempt_runtime_identity(
    attempt: dict[str, Any], receipts: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    try:
        return runtime_identity.validate_runtime_ref(
            attempt["actor_runtime_ref"],
            receipts=receipts,
            expected_agent_id=attempt["actor_id"],
            expected_role=attempt["actor_role"],
            expected_thread_identity=attempt["actor_thread_id"],
        )
    except runtime_identity.RuntimeIdentityError as exc:
        raise GovernanceError(f"attempt runtime identity is not authenticated: {exc}") from exc


def validate_review_runtime_identity(
    review: dict[str, Any], receipts: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    try:
        return runtime_identity.validate_runtime_ref(
            review["reviewer_runtime_ref"],
            receipts=receipts,
            expected_agent_id=review["reviewer_id"],
            expected_role="semantic_reviewer",
            expected_thread_identity=review["reviewer_thread_id"],
        )
    except runtime_identity.RuntimeIdentityError as exc:
        raise GovernanceError(f"review runtime identity is not authenticated: {exc}") from exc


def validate_review(
    work_order: dict[str, Any], attempt: dict[str, Any], review: dict[str, Any]
) -> None:
    _require(
        review,
        {
            "review_id",
            "work_order_id",
            "attempt_id",
            "reviewer_id",
            "reviewer_thread_id",
            "reviewer_runtime_ref",
            "candidate_commit",
            "candidate_sha256",
            "authority_ref",
            "authority_re_read",
            "legitimacy",
            "proof_quality",
            "falsification_evidence",
            "limitations",
        },
        "review",
    )
    if review["work_order_id"] != work_order["work_order_id"]:
        raise GovernanceError("review work order mismatch")
    if review["attempt_id"] != attempt["attempt_id"]:
        raise GovernanceError("review attempt mismatch")
    if review["reviewer_id"] == attempt["actor_id"]:
        raise GovernanceError("reviewer identity is not independent from worker")
    if review["reviewer_thread_id"] == attempt["actor_thread_id"]:
        raise GovernanceError("reviewer thread is not independent from worker")
    if review["authority_re_read"] is not True:
        raise GovernanceError("review does not record independent authority re-read")
    if review["authority_ref"] != work_order["authority_ref"]:
        raise GovernanceError("review authority reference does not match work order")
    if _candidate_binding(review, "review") != _candidate_binding(attempt, "attempt"):
        raise GovernanceError("review candidate binding does not match attempt candidate")
    if not review["falsification_evidence"]:
        raise GovernanceError("review contains no falsification evidence")


def validate_admission(
    work_order: dict[str, Any],
    attempt: dict[str, Any],
    review: dict[str, Any],
    admission: dict[str, Any],
) -> None:
    validate_attempt(work_order, attempt)
    validate_review(work_order, attempt, review)
    _require(
        admission,
        {
            "admission_id",
            "record_type",
            "disposition",
            "proposition_id",
            "authority_ref",
            "work_order_id",
            "attempt_id",
            "review_id",
            "accepted_base_commit",
            "candidate_commit",
            "candidate_sha256",
            "admitted_at_utc",
        },
        "admission",
    )
    if admission["record_type"] != "SEMANTIC_RESULT":
        raise GovernanceError("semantic transaction has wrong admission record type")
    if admission["work_order_id"] != work_order["work_order_id"]:
        raise GovernanceError("admission work order mismatch")
    if admission["attempt_id"] != attempt["attempt_id"]:
        raise GovernanceError("admission attempt mismatch")
    if admission["review_id"] != review["review_id"]:
        raise GovernanceError("admission review mismatch")
    if admission["proposition_id"] != work_order["proposition_id"]:
        raise GovernanceError("admission proposition mismatch")
    if admission["authority_ref"] != work_order["authority_ref"]:
        raise GovernanceError("admission authority mismatch")
    if admission["accepted_base_commit"] != work_order["accepted_base_commit"]:
        raise GovernanceError("admission accepted base mismatch")
    if _candidate_binding(admission, "admission") != _candidate_binding(attempt, "attempt"):
        raise GovernanceError("admission candidate binding does not match attempt candidate")
    if admission["disposition"] == "ACCEPTED":
        if review["legitimacy"] != "AUTHORISED":
            raise GovernanceError("admission cannot overcome review legitimacy rejection")
        if review["proof_quality"] != "PROVEN":
            raise GovernanceError("admission cannot overcome unproven proof quality")


def validate_admission_transaction(
    repo_root: Path,
    work_order: dict[str, Any],
    attempt: dict[str, Any],
    review: dict[str, Any],
    admission: dict[str, Any],
    *,
    admissions: dict[str, dict[str, Any]],
    accepted_base_commit: str,
) -> ValidatedAdmission:
    """Validate the only state-advancing semantic admission path.

    Git facts are derived here rather than accepted from caller declarations.
    """
    validate_work_order(work_order, admissions, accepted_base_commit=accepted_base_commit)
    validate_attempt(work_order, attempt)
    try:
        runtime_receipts = runtime_identity.load_runtime_receipts(repo_root)
    except runtime_identity.RuntimeIdentityError as exc:
        raise GovernanceError(f"runtime identity receipt store is invalid: {exc}") from exc
    worker_receipt = validate_attempt_runtime_identity(attempt, runtime_receipts)
    candidate_commit = attempt.get("candidate_commit")
    if not isinstance(candidate_commit, str) or not candidate_commit:
        raise GovernanceError("semantic Git admission requires a candidate commit")
    candidate_parent, changed_paths = git_candidate_facts(repo_root, candidate_commit)
    validate_git_candidate_binding(
        work_order,
        attempt,
        candidate_commit=candidate_commit,
        candidate_parent=candidate_parent,
        changed_paths=changed_paths,
    )
    validate_review(work_order, attempt, review)
    reviewer_receipt = validate_review_runtime_identity(review, runtime_receipts)
    if worker_receipt["agent_id"] == reviewer_receipt["agent_id"]:
        raise GovernanceError("worker and reviewer runtime identities are not independent")
    if worker_receipt["agent_transcript_path"] == reviewer_receipt["agent_transcript_path"]:
        raise GovernanceError("worker and reviewer runtime thread identities are not independent")
    validate_admission(work_order, attempt, review, admission)
    return ValidatedAdmission(
        admission=dict(admission),
        candidate_commit=candidate_commit,
        candidate_parent=candidate_parent,
        changed_paths=tuple(changed_paths),
    )


def advance_state_after_admission(
    state: dict[str, Any], validated: ValidatedAdmission
) -> dict[str, Any]:
    if not isinstance(validated, ValidatedAdmission):
        raise GovernanceError("state advancement requires a validated transaction")
    admission = validated.admission
    if not _is_accepted(admission):
        raise GovernanceError("rejected record cannot advance admitted state")
    if admission.get("candidate_commit") != validated.candidate_commit:
        raise GovernanceError("validated transaction candidate changed before state advance")
    updated = dict(state)
    updated["latest_admission_id"] = admission["admission_id"]
    if admission.get("record_type") == "SEMANTIC_RESULT":
        updated["candidate_control_commit"] = validated.candidate_commit
    updated["current_work_order"] = None
    updated["current_attempt"] = None
    updated["first_blocker"] = None
    return updated


def validate_admitted_state_binding(
    state: dict[str, Any],
    *,
    current_git_parent: str,
    admissions: dict[str, dict[str, Any]],
) -> None:
    latest_id = state.get("latest_admission_id")
    if not latest_id:
        raise GovernanceError("ADMITTED_STATE has no latest admission ID")
    latest = admissions.get(latest_id)
    if not latest or not _is_accepted(latest):
        raise GovernanceError("ADMITTED_STATE latest admission is absent or not accepted")
    admitted_candidate = state.get("candidate_control_commit")
    if admitted_candidate != current_git_parent:
        raise GovernanceError(
            "ADMITTED_STATE admitted candidate disagrees with Git admission-control parent"
        )
    if state.get("operational_status") == "GATE0_PASS":
        if latest.get("disposition") != "GATE0_PASS":
            raise GovernanceError("GATE0_PASS state does not bind a Gate 0 admission")
        if latest.get("proven_commit") != admitted_candidate:
            raise GovernanceError(
                "Gate 0 admission proven commit disagrees with admitted candidate"
            )
        if state.get("gate0_proven_commit") != admitted_candidate:
            raise GovernanceError(
                "ADMITTED_STATE Gate 0 proven commit disagrees with admitted candidate"
            )
    elif latest.get("record_type") == "SEMANTIC_RESULT":
        if latest.get("candidate_commit") != admitted_candidate:
            raise GovernanceError("semantic admission candidate disagrees with admitted candidate")


def _repo_root() -> Path:
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    return Path(out.strip()).resolve()


def validate_repository_static(root: Path) -> None:
    for rel in [
        "schemas/semantic_index.schema.json",
        "schemas/work_order.schema.json",
        "schemas/attempt_record.schema.json",
        "schemas/review.schema.json",
        "schemas/admission_record.schema.json",
        "schemas/admitted_state.schema.json",
        "docs/governance/SEMANTIC_INDEX.json",
        "docs/governance/ADMITTED_STATE.json",
    ]:
        data = json.loads((root / rel).read_text())
        if not isinstance(data, dict):
            raise GovernanceError(f"governance JSON is not an object: {rel}")
    index = json.loads((root / "docs/governance/SEMANTIC_INDEX.json").read_text())
    if index.get("status") == "PENDING":
        if index.get("admission_id") is not None or index.get("entries") != []:
            raise GovernanceError("pending semantic index must be empty and unadmitted")
    elif index.get("status") == "ACCEPTED":
        admissions: dict[str, dict[str, Any]] = {}
        for path in sorted((root / "docs/governance/admissions").glob("*.json")):
            record = json.loads(path.read_text())
            admission_id = record.get("admission_id")
            if admission_id:
                admissions[admission_id] = record
        accepted_semantic_index_entries(index, admissions=admissions, repo_root=root)
    else:
        raise GovernanceError("semantic index has invalid status")

    state = json.loads((root / "docs/governance/ADMITTED_STATE.json").read_text())
    if state.get("operational_status") == "CANDIDATE_FOR_INDEPENDENT_AUDIT":
        if state.get("current_work_order") is not None or state.get("current_attempt") is not None:
            raise GovernanceError("construction candidate cannot claim active admitted work")
        if state.get("latest_admission_id") is not None:
            raise GovernanceError("construction candidate cannot claim a latest admission")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static", action="store_true", required=True)
    args = parser.parse_args(argv)
    del args
    try:
        validate_repository_static(_repo_root())
        print("PASS: Gate 1+ governance substrate validation")
        return 0
    except (GovernanceError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
